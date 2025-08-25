import os
import random
import time
import threading
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chaos-secret-key-2024'
# Use threading instead of eventlet
socketio = SocketIO(app, async_mode='threading')

# Store messages and users
messages = []
users = {}

# Chaos event types
CHAOS_EVENTS = [
    'shuffle',
    'distort',
    'replace'
]

FUNNY_REPLACEMENTS = [
    "I'm a teapot, short and stout!",
    "The server is feeling chaotic today!",
    "Oops, my bad! I dropped your message.",
    "A wild chaos event appeared!",
    "This message was too boring, so I spiced it up!",
    "The hamsters powering the server need more coffee!",
    "I'd tell you a joke about UDP, but you might not get it.",
    "Your message was intercepted by chaos gnomes!",
    "The message you're looking for is in another chat.",
    "404: Message not found (but actually chaos event)"
]

def chaos_worker():
    """Background thread that triggers chaos events periodically"""
    while True:
        # Wait for a random time between 30-90 seconds
        time.sleep(random.randint(30, 90))
        
        # Skip if no messages
        if not messages:
            continue
            
        # Select a random chaos event
        event_type = random.choice(CHAOS_EVENTS)
        
        with app.app_context():
            if event_type == 'shuffle':
                # Shuffle all messages
                random.shuffle(messages)
                message = "🌀 Chaos Event: All messages have been shuffled!"
                
            elif event_type == 'distort':
                # Distort some random messages
                num_to_distort = max(1, len(messages) // 3)
                indices_to_distort = random.sample(range(len(messages)), num_to_distort)
                
                for idx in indices_to_distort:
                    original_msg = messages[idx]['text']
                    # Replace some characters with random ones
                    if len(original_msg) > 3:
                        distortion_count = max(1, len(original_msg) // 4)
                        msg_list = list(original_msg)
                        for _ in range(distortion_count):
                            pos = random.randint(0, len(msg_list) - 1)
                            msg_list[pos] = chr(random.randint(33, 126))
                        messages[idx]['text'] = ''.join(msg_list)
                
                message = "🤪 Chaos Event: Some messages have been distorted!"
                
            elif event_type == 'replace':
                # Replace some random messages with funny text
                num_to_replace = max(1, len(messages) // 4)
                indices_to_replace = random.sample(range(len(messages)), num_to_replace)
                
                for idx in indices_to_replace:
                    messages[idx]['text'] = random.choice(FUNNY_REPLACEMENTS)
                
                message = "🎭 Chaos Event: Some messages have been replaced!"
            
            # Add chaos event as a system message
            messages.append({
                'username': 'System',
                'text': message,
                'timestamp': time.strftime('%H:%M:%S'),
                'system': True
            })
            
            # Broadcast updated messages to all clients
            socketio.emit('message_history', messages)

# Start the chaos thread
chaos_thread = threading.Thread(target=chaos_worker, daemon=True)
chaos_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('message_history', messages)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        username = users[request.sid]
        del users[request.sid]
        # Broadcast user left message
        messages.append({
            'username': 'System',
            'text': f'{username} left the chat',
            'timestamp': time.strftime('%H:%M:%S'),
            'system': True
        })
        emit('user_count', len(users), broadcast=True)
        emit('message', {
            'username': 'System',
            'text': f'{username} left the chat',
            'timestamp': time.strftime('%H:%M:%S'),
            'system': True
        }, broadcast=True)

@socketio.on('join')
def handle_join(data):
    username = data['username']
    users[request.sid] = username
    # Broadcast user joined message
    messages.append({
        'username': 'System',
        'text': f'{username} joined the chat',
        'timestamp': time.strftime('%H:%M:%S'),
        'system': True
    })
    emit('user_count', len(users), broadcast=True)
    emit('message', {
        'username': 'System',
        'text': f'{username} joined the chat',
        'timestamp': time.strftime('%H:%M:%S'),
        'system': True
    }, broadcast=True)

@socketio.on('send_message')
def handle_send_message(data):
    username = users.get(request.sid, 'Anonymous')
    message_data = {
        'username': username,
        'text': data['text'],
        'timestamp': time.strftime('%H:%M:%S'),
        'system': False
    }
    messages.append(message_data)
    emit('message', message_data, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    # Use the Flask development server instead of socketio.run
    app.run(host="0.0.0.0", port=port, debug=True)
