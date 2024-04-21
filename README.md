# NoHushSource
Anon does microblogging   
Generated with claude: 

Certainly! Here's a comprehensive guide to help your team members understand the project source.

**Introduction**

This project is a Flask web application that allows users to post messages anonymously. The application uses JSON files to store the posts and implements basic security measures like Cloudflare's Turnstile CAPTCHA and message length validation. The project also includes some JavaScript functionality to enhance the user experience.

**File Structure**

1. `app.py`: This is the main Python file that contains the Flask application logic.
2. `home.html`: This is the HTML template for the home page, which displays the message feed and the posting form.
3. `message.html`: This is the HTML template for displaying a single message.
4. `index.css`: This file contains the CSS styles for the application.

**app.py**

1. **Imports**: The file imports necessary modules and libraries, including Flask, json, random, os, requests, and datetime.
2. **Flask App Initialization**: The Flask app is initialized, and a secret key is set for session management.
3. **Database Functions**:
   - `load_posts()`: This function loads the posts from the `posts.json` file or returns an empty list if the file doesn't exist.
   - `save_post(post)`: This function saves a new post to the `posts.json` file by appending it to the existing list of posts.
   - `generate_message_id()`: This function generates a random message ID for each new post.
4. **Routes**:
   - `@app.route('/')`: This route handles the home page request. It loads the posts, sorts them by date in descending order, generates a new message ID, and renders the `home.html` template with the posts and the new message ID.
   - `@app.route('/post', methods=['POST'])`: This route handles the form submission for creating a new post. It validates the Turnstile CAPTCHA token, checks the message length, generates a user ID if none exists in the session, creates a new post dictionary with the user ID, message, and date, and saves the post using `save_post(post)`. Finally, it redirects the user to the home page.
   - `@app.route('/message/<int:message_id>')`: This route displays a single message based on the provided `message_id`. It loads the posts, finds the matching post, and renders the `message.html` template with the post data.
5. **Helper Function**: `generate_user_id()`: This function generates a random user ID between 1000 and 99999.

**home.html**

This file contains the HTML structure for the home page. It includes:

1. Google Analytics tracking code.
2. A header with the application title and links.
3. A container div containing:
   - A form for posting a new message, including a textarea, a hidden message ID field, a hidden user ID field, a Cloudflare Turnstile CAPTCHA div, and a submit button.
   - A div to display the feed of posts, with each post showing the user ID, message, date, and a "Copy Link" button.
4. JavaScript code for:
   - Storing and retrieving the user ID in localStorage.
   - Copying the link to a specific message when the "Copy Link" button is clicked.
   - Automatically adjusting the height of the textarea based on its content.
   - Preventing the right-click context menu and certain keyboard shortcuts that may open developer tools.

**message.html**

This file contains the HTML structure for displaying a single message. It includes:

1. Google Analytics tracking code.
2. A div containing the user ID, message ID, message text, and date.
3. CSS styles for the message display.

**index.css**

This file contains the CSS styles for the entire application, including:

1. General styles for the body, links, boxes, posts, user IDs, dates, and messages.
2. Styles for the "Copy Link" button.
3. Styles for the textarea, button, and header.
4. Styles for the Turnstile CAPTCHA container and input fields.
5. Media queries for responsive design on smaller screens.
6. Styles for the small text links in the header.

**Usage**

To run the application locally, follow these steps:

1. Install the required dependencies (Flask and requests).
2. Run the `app.py` file using `python app.py` or `flask run`.
3. Access the application in your web browser at `http://localhost:5000`.

**Deployment**

The application is currently deployed on PythonAnywhere. To access the live version, visit `http://nohush.pythonanywhere.com`.

**Security Considerations**

While the application implements basic security measures like message length validation and Cloudflare's Turnstile CAPTCHA, it's important to note that it does not implement comprehensive security measures for storing and displaying user-generated content. Additional measures, such as input sanitization, content filtering, and secure storage, should be implemented before deploying the application to a production environment.

**Contributions and Collaboration**

If you wish to contribute to the project or collaborate with your team members, you can follow standard Git workflow practices, such as creating branches, making changes, and submitting pull requests. Ensure that your team members have access to the project repository and coordinate your efforts to avoid conflicts.
