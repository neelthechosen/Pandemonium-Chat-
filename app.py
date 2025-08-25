from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet
import random
import time
from threading import Thread, Lock

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chaos-secret!'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

# Global variables
users = {}
current_chaos_event = None
chaos_lock = Lock()
message_count = 0

# Chaos events definitions
chaos_events = [
    {
        'name': 'Scramble',
        'description': 'Random letters in messages are shuffled!',
        'apply': lambda msg: ''.join([c if random.random() > 0.3 else random.choice('abcdefghijklmnopqrstuvwxyz') for c in msg])
    },
    {
        'name': 'Emoji Flood',
        'description': 'All words replaced by random emojis!',
        'apply': lambda msg: ' '.join([random.choice(['😀', '😎', '🤖', '👾', '🐸', '🦄', '🍕', '🚀', '🎉', '💥']) for _ in msg.split()])
    },
    {
        'name': 'Rule Drop',
        'description': 'From now on, every message must start with 🐸',
        'apply': lambda msg: '🐸 ' + msg
    },
    {
        'name': 'Reverse Mode',
        'description': 'Messages display backwards!',
        'apply': lambda msg: msg[::-1]
    },
    {
        'name': 'UPPERCASE MADNESS',
        'description': 'ALL MESSAGES WILL BE IN UPPERCASE!',
        'apply': lambda msg: msg.upper()
    },
    {
        'name': 's p a c e d  o u t',
        'description': 'M e s s a g e s  g e t  e x t r a  s p a c e s',
        'apply': lambda msg: ' '.join([c for c in msg])
    }
]

def chaos_event_worker():
    """Background thread that triggers chaos events periodically"""
    global current_chaos_event
    while True:
        time.sleep(random.randint(30, 60))  # Wait 30-60 seconds
        
        with chaos_lock:
            # Select a random chaos event
            current_chaos_event = random.choice(chaos_events)
            
            # Send event notification to all clients
            socketio.emit('chaos_event', {
                'name': current_chaos_event['name'],
                'description': current_chaos_event['description']
            }, broadcast=True)
            
            # For bot intrusion event (special case)
            if current_chaos_event['name'] == 'Bot Intrusion':
                for _ in range(random.randint(2, 5)):
                    time.sleep(2)
                    alerts = [
                        "⚠️ Reality collapsing in 10s",
                        "🚨 SYSTEM BREACH DETECTED",
                        "🔮 The prophecy is unfolding...",
                        "🌪️ Chaos levels critical",
                        "👁️ They are watching us",
                        "💀 ERROR: Existence failing"
                    ]
                    socketio.emit('message', {
                        'username': 'SYSTEM-BOT',
                        'message': random.choice(alerts),
                        'timestamp': time.strftime('%H:%M:%S')
                    }, broadcast=True)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    users[request.sid] = f'User{random.randint(1000, 9999)}'
    emit('user_joined', {'username': users[request.sid], 'users_count': len(users)}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        username = users.pop(request.sid)
        emit('user_left', {'username': username, 'users_count': len(users)}, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    global message_count
    message = data['message']
    
    # Apply chaos event if active
    with chaos_lock:
        if current_chaos_event:
            message = current_chaos_event['apply'](message)
    
    # Increment message counter and occasionally trigger special events
    message_count += 1
    if message_count % 20 == 0:
        socketio.emit('message', {
            'username': 'CHAOS-BOT',
            'message': 'The chaos is growing... 🌋',
            'timestamp': time.strftime('%H:%M:%S')
        }, broadcast=True)
    
    # Broadcast the message to all clients
    emit('message', {
        'username': users[request.sid],
        'message': message,
        'timestamp': time.strftime('%H:%M:%S')
    }, broadcast=True)

if __name__ == '__main__':
    # Start the chaos event thread
    event_thread = Thread(target=chaos_event_worker)
    event_thread.daemon = True
    event_thread.start()
    
    socketio.run(app, debug=True, host='0.0.0.0')
