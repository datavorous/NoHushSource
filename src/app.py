from flask import Flask, render_template, request, redirect, session, url_for
import json
import requests
import os
from datetime import datetime
import secrets
import string

app = Flask(__name__)
app.secret_key = 'thefuckamidoing'
SITE_KEY = "HAKUNA"
SECRET_KEY = "MATATA"

def verify_turnstile_token():
    turnstile_token = request.form.get('cf-turnstile-response')
    site_key = 'HAKUNA'
    secret_key = 'MATATA'
    response = requests.post(
        'https://challenges.cloudflare.com/turnstile/v0/siteverify',
        json={
            'secret': secret_key,
            'response': turnstile_token,
            'sitekey': site_key,
            'remoteip': request.remote_addr
        }
    )
    return response.json().get('success', False)

def genstr(length):
    alphabet = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(alphabet) for _ in range(length))
    return random_string

def load_posts():
    if os.path.exists('posts.json'):
        with open('posts.json', 'r') as f:
            data = json.load(f)
            return data.get('topics', [])
    else:
        return []

@app.route('/new_post/<topic_name>', methods=['POST'])
def new_post(topic_name):
    if not verify_turnstile_token():
        return "Turnstile token verification failed", 403

    message = request.form['message']
    if len(message) < 20 or len(message) > 1000:
        return "Message length should be between 20 and 500 characters."

    user_id = session.get('user_id')
    if not user_id:
        user_id = generate_user_id()
        session['user_id'] = user_id

    message_id = genstr(6)

    post = {
        'user_id': user_id,
        'message': message,
        'date': datetime.now().strftime("%d/%m/%y %H:%M:%S"),
        'message_id': message_id
    }

    save_post(topic_name, post)

    return redirect(url_for('topic', topic_name=topic_name))

def save_post(topic_name, post):
    data = {'topics': load_posts()}
    topic = next((t for t in data['topics'] if t['name'] == topic_name), None)
    if topic is None:
        topic = {'name': topic_name, 'posts': []}
        data['topics'].append(topic)

    existing_post = next((p for p in topic['posts'] if p['message_id'] == post['message_id']), None)
    if existing_post:
        existing_post.update(post)
    else:
        post['message_id'] = generate_message_id()
        topic['posts'].append(post)

    topic['posts'].sort(key=lambda x: datetime.strptime(x['date'], "%d/%m/%y %H:%M:%S"), reverse=True)

    with open('posts.json', 'w') as f:
        json.dump(data, f)

def generate_message_id():
    return str(genstr(6))

@app.route('/')
def index():
    topics = load_posts()
    return render_template('index.html', topics=topics)

@app.route('/topic/<topic_name>')
def topic(topic_name):
    topics = load_posts()
    topic = next((t for t in topics if t['name'] == topic_name), None)
    if topic is None:
        return "Topic not found"
    posts = topic.get('posts', [])
    posts.sort(key=lambda x: datetime.strptime(x['date'], "%d/%m/%y %H:%M:%S"), reverse=True)
    message_id = generate_message_id()
    return render_template('home.html', posts=posts, message_id=message_id, topic_name=topic_name)

@app.route('/post/<message_id>', methods=['GET', 'POST'])
def post(message_id):
    if not verify_turnstile_token():
        return "fuck off, u not human"
    posts = load_posts()
    for topic in posts:
        for post in topic.get('posts', []):
            if str(post.get('message_id')) == (message_id):
                if request.method == 'POST':
                    comment = request.form['comment']
                    user_id = session.get('user_id')
                    if not user_id:
                        user_id = generate_user_id()
                        session['user_id'] = user_id
                    post.setdefault('comments', []).append({
                        'user_id': user_id,
                        'comment': comment
                    })
                    save_post(topic['name'], post)
                return render_template('message.html', post=post)
    return "Message not found"

@app.route('/message/<message_id>', methods=['GET'])
def display_message(message_id):
    posts = load_posts()
    for topic in posts:
        for post in topic.get('posts', []):
            if post.get('message_id') == message_id:
                return render_template('message.html', post=post)
    return "Message not found"

@app.route('/legal')
def legal_page():
    return render_template('legal.html')

@app.route('/donate')
def donate_page():
    return render_template('donate.html')

def generate_user_id():
    return str(genstr(6))

if __name__ == '__main__':
    app.run(debug=True)
