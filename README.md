# Chaos Chat App

A real-time multi-user chat application with random chaos events that shuffle, distort, or replace messages every 30-90 seconds.

## Features

- Multiple users can join the same chatroom
- Real-time message broadcasting
- Random chaos events that:
  - Shuffle all messages
  - Distort some messages by replacing characters
  - Replace messages with funny alternatives
- Simple and responsive UI

## Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python app.py`
6. Open your browser to `http://localhost:10000`

## Deployment to Render

### Prerequisites
- GitHub account
- Render account

### Steps

1. Fork this repository to your GitHub account
2. Go to [Render.com](https://render.com) and sign up/login
3. Click "New +" and select "Web Service"
4. Connect your GitHub account if not already connected
5. Select the forked repository
6. Fill in the details:
   - Name: `chaos-chat` (or your preferred name)
   - Environment: `Python 3`
   - Region: Choose the closest to your users
   - Branch: `main` (or your preferred branch)
   - Root Directory: Leave blank
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -k eventlet -w 1 app:app`
   - Plan: `Free`
7. Click "Create Web Service"
8. Render will automatically deploy your application

### Alternative Deployment with render.yaml

If you have the `render.yaml` file in your repository:

1. Go to your Render Dashboard
2. Click "New +" and select "Blueprint"
3. Connect your GitHub repository
4. Render will detect the `render.yaml` file and configure the service automatically

## Technologies Used

- Backend: Flask, Flask-SocketIO
- Frontend: HTML, CSS, JavaScript
- Real-time communication: WebSockets
- Async server: Eventlet
- Deployment: Gunicorn, Render.com

## How It Works

1. Users join by entering a username
2. Messages are broadcast to all connected users in real-time
3. A background thread triggers chaos events every 30-90 seconds:
   - Shuffle: Randomly reorders all messages
   - Distort: Replaces characters in some messages with random characters
   - Replace: Changes some messages to funny alternatives
4. System messages notify users of chaos events and user join/leave events

## Notes

- The free tier of Render may spin down your service after periods of inactivity
- For production use, consider using a proper database instead of in-memory storage
- The chaos events are purely for entertainment and may make serious conversations difficult
