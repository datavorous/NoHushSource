from flask import Flask, render_template, request, redirect, session, url_for
import json
import requests
import os

from datetime import datetime
#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = 'thefuckamidoingwithmylife'
SITE_KEY = "0x4AAAAAAAYa8jTSBMieaZz7"
SECRET_KEY = "0x4AAAAAAAYa8ssTtuFiGDxM-6fB-NGYi3M"

# Verify Turnstile token function
def verify_turnstile_token():
    # Get the Turnstile token from the form data
    turnstile_token = request.form.get('cf-turnstile-response')

    # Validate the Turnstile token
    site_key = '0x4AAAAAAAXkS-fuHI8ozcYp'  # Your Turnstile site key
    secret_key = '0x4AAAAAAAXkSxgpHIHpzNl9iLTcooaC8_w'  # Your Turnstile secret key

    response = requests.post(
        'https://challenges.cloudflare.com/turnstile/v0/siteverify',
        json={
            'secret': secret_key,
            'response': turnstile_token,
            'sitekey': site_key,
            'remoteip': request.remote_addr
        }
    )

    # Return True if token is valid, False otherwise
    return response.json().get('success', False)


import secrets
import string

def genstr(length):
    alphabet = string.ascii_letters + string.digits  # Define the alphabet for the random string
    random_string = ''.join(secrets.choice(alphabet) for _ in range(length))  # Generate the random string
    return random_string

#limiter = Limiter(app,key_func=get_remote_address,default_limits=["1 per minute"])
# limiter is problematic

# Load posts from database
def load_posts():
    if os.path.exists('posts.json'):
        with open('posts.json', 'r') as f:
            data = json.load(f)
            return data.get('topics', [])
    else:
        return []

  # Import uuid4 function to generate unique message IDs

@app.route('/new_post/<topic_name>', methods=['POST'])
#@limiter.limit("1 per minute")
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

    # Generate a unique message_id
    message_id = genstr(6)

    # Create the new post with the message_id
    post = {
        'user_id': user_id,
        'message': message,
        'date': datetime.now().strftime("%d/%m/%y %H:%M:%S"),
        'message_id': message_id  # Assign the generated message_id
    }

    # Save the new post
    save_post(topic_name, post)

    return redirect(url_for('topic', topic_name=topic_name))


# Save post to database
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

    with open('posts.json', 'w') as f:
        json.dump(data, f)

# Generate a message ID
def generate_message_id():
    return str(genstr(6))# Adjust as needed for your requirements

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
    posts.sort(key=lambda x: x['date'], reverse=True)
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
                        'comment': comment,
                        'date': datetime.now().strftime("%d/%m/%y %H:%M:%S")
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
