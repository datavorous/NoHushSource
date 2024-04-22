# Documentation

## Overview

A text-based forum web application built using Python Flask for the backend, HTML/CSS for the frontend, and vanilla JavaScript for client-side interactions. It allows users to post messages, comment on posts, and browse topics. The application incorporates features like session management, Turnstile integration for spam prevention, and dynamic content generation.

## Folder Structure

```
imageboard/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── topic.html
│   └── post.html
├── data/
│   └── posts.json
├── app.py
└── requirements.txt
```

- **static/**: Contains static files such as CSS and JavaScript.
- **templates/**: Contains HTML templates for rendering pages.
- **data/**: Stores JSON data for posts.
- **app.py**: Main Flask application file.
- **requirements.txt**: Lists required Python packages.

## Components

### Backend (app.py)

- **Flask Routes**: Defines routes for handling HTTP requests.
  - `/`: Renders the home page.
  - `/topic/<topic_name>`: Renders a topic page and handles message posting.
  - `/post/<message_id>`: Renders a post page and handles comment posting.
- **Session Management**: Manages user sessions and generates unique user IDs.
- **JSON Data Handling**: Loads and saves post data from/to `posts.json`.
- **Turnstile Integration**: Integrates Turnstile for spam prevention.

### Frontend (templates/*.html, static/css/style.css, static/js/script.js)

- **HTML Templates**: Define the structure of web pages using Jinja2 templating.
  - `base.html`: Base template with header, navigation, and footer.
  - `home.html`: Homepage template with a welcome message.
  - `topic.html`: Template for displaying topics and posting messages.
  - `post.html`: Template for displaying posts and comments.
- **CSS Styling**: Defines styles for various elements to create a visually appealing UI.
- **JavaScript**: Implements Turnstile validation for form submissions.

## Usage

1. **Setup Environment**: Install Python and Flask.
2. **Install Dependencies**: Install required Python packages using `pip install -r requirements.txt`.
3. **Run the Application**: Execute `python app.py` to start the Flask server.
4. **Access the Application**: Open a web browser and navigate to `http://localhost:5000` to access the Imageboard Forum.
5. **Interact with the Forum**: Browse topics, post messages, and comment on posts.

## External Dependencies

- **Flask**: Web framework for Python.
- **Cloudflare Turnstile**: CAPTCHA-like system for spam prevention.

---

This documentation provides an overview of the Imageboard Forum application, its structure, functionality, and usage instructions. It serves as a guide for understanding and using the codebase effectively.
