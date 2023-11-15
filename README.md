# ChatRoom - CS50W Capstone Project

## Description and Design Choices

ChatRoom is a real-time chat application developed to fulfill the requirements of my final capstone project for CS50W. This application allows registered users to engage in one-on-one conversations, view profiles, and update their personal information. The application is built using Django for the backend and HTML, CSS, and JavaScript for the frontend.

## Key Features

- One-on-one chat functionality
- User profile management
- Real-time messaging
- User authentication and registration
- Message preview and history

## Installation

To run this application, you will need Python 3 and Django installed. Once you have these prerequisites, follow these steps:

1. Clone the repository: `git clone <repository_url>`
2. Navigate to the project directory
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run the development server: `python3 manage.py runserver`

## Usage

1. Register a new user account by clicking on the registration link and follow the steps on the page.
2. Once registered, log in with your account credentials.
3. You should see the main page with chat previews on the left, and if you have selected a specific chat preview, its message history will appear on the right. 
   Note that if you only have 1 user in your app, there will not be any chat previews or message history to be displayed.
4. On the top of the main page, you will see a navigation bar with 4 different words:
    - ChatRoom: this is the name of the app (clicking on this while on other pages will bring you back to the main page)
    - Username: this is your username, and clicking on it directs you to your own profile page where you can edit your profile details
    - Members: this is the Members page where you can see all registered users within the app and start a chat with any user
    - Log Out: clicking on this logs you out of the app and redirects you to the login page

## Files

### Static

- `chatroom/default.png`: the default profile picture displayed if a user did not upload any profile picture
- `static/chatroom/Styles.css`: CSS for webpage styling

### Templates

#### chatroom

- `templates/chatroom/landing.html`: landing page for new/logged-out users
- `templates/chatroom/layout.html`: layout HTML template for all the chatroom HTML templates
- `templates/chatroom/login.html`: login page
- `templates/chatroom/register.html`: registration page

#### chatapp

- `templates/chatapp/base.html`: the main chat app page containing the JavaScript logic and send message form
- `templates/chatapp/chat_history.html`: the chat_history section extending from `base.html`
- `templates/chatapp/chat_preview.html`: the chat_preview section extending from `base.html`, rendering the details in each chat preview
- `templates/chatapp/edit_profile.html`: the Edit Profile page for users to manage their profile
- `templates/chatapp/members.html`: the Members page listing all users (except yourself) in the app
- `templates/chatapp/profile.html`: the profile page layout and logic

## Distinctiveness and Complexity

### Value Proposition

Making a chat app in itself is distinct from the other 5 projects, none of which were chat/messaging related.

### Real-Time Messaging (sort of)

Unlike the previous projects, ChatRoom supports real-time messaging between users, enabling (almost) instant communication. I managed this by using a combination of event listeners in JavaScript as well as simulated clicking of the chat previews (which had the event listeners for clicks to fetch the updated state). In my case, I had set the update interval to 5 seconds (which can be adjusted lower) to simulate real-time messaging. I have considered diving deeper into the use of Django Channels/Signals and using WebSockets but decided against it as I was already more than halfway through the project when I learned about these tools (a learning point for me as I am now aware of such tools/techniques when it comes to developing projects that require some kind of a notification system that is initiated by the server instead of the client).

### User Profile Management

Users can customize their profiles, including uploading profile pictures, updating email addresses, and adding personal bios, providing a personalized experience.

### Member Start Chat Functionality

The backend logic for start chat was more complicated than I thought it would be as it required conditionals to check if a user already had an existing chat with the other user. It also involved a greater detail in constructing the models in Django to ensure that Chat and Message data are logically connected in a way that the APIs and queries would work fine.

### Dynamic Chat Previews and Interactive UI

The functionality of the `base.html` template builds upon the lessons learned from Mail and Network, where I learned how to make single-page apps and utilize APIs. ChatRoom brings this to a further level by offering the dynamic chat preview functionality, displaying the last sent message and the corresponding timestamp as it is updated. The frontend design employs a combination of HTML, CSS, and JavaScript to create an engaging and user-friendly interface, improving overall usability.
