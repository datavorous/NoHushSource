from flask import Flask, render_template, request, redirect, session
import json
import random
import os
import requests
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load posts from database
def load_posts():
    if os.path.exists('posts.json'):
        with open('posts.json', 'r') as f:
            posts = json.load(f)
    else:
        posts = []
    return posts

# Save post to database
def save_post(post):
    posts = load_posts()
    post['message_id'] = generate_message_id()  # Assign a message ID
    posts.append(post)
    with open('posts.json', 'w') as f:
        json.dump(posts, f)

# Generate a message ID
def generate_message_id():
    return random.randint(10000, 999999)  # Adjust as needed for your requirements

@app.route('/')
def index():
    posts = load_posts()
    posts.sort(key=lambda x: x['date'], reverse=True)
    message_id = generate_message_id()  # Generate a message ID
    return render_template('home.html', posts=posts, message_id=message_id)

@app.route('/post', methods=['POST'])
def post():
    message = request.form['message']
    turnstile_token = request.form.get('cf-turnstile-response')  # Get the Turnstile token

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

    if response.json().get('success', False):  # Check if Turnstile validation is successful
        if len(message) >= 18 and len(message) <= 500:  # Message length validation
            user_id = session.get('user_id')
            if not user_id:
                user_id = generate_user_id()
                session['user_id'] = user_id
            post = {'user_id': user_id, 'message': message, 'date': datetime.now().strftime("%d/%m/%y %H:%M:%S")}
            save_post(post)
    return redirect('/')

@app.route('/message/<int:message_id>')  # Route to display a single message based on its ID
def display_message(message_id):
    posts = load_posts()
    for post in posts:
        if post.get('message_id') == message_id:
            return render_template('message.html', post=post)
    return "Message not found"

def generate_user_id():
    return random.randint(1000, 99999)

if __name__ == '__main__':
    app.run(debug=True)
