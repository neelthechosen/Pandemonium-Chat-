document.addEventListener('DOMContentLoaded', function() {
    const socket = io();
    const messagesContainer = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const usersCount = document.getElementById('users-count');
    const chaosAlert = document.getElementById('chaos-alert');
    const chaosContent = document.getElementById('chaos-content');
    
    // Connect to server
    socket.on('connect', function() {
        addSystemMessage('Connected to the chatroom');
    });
    
    // Handle user joined event
    socket.on('user_joined', function(data) {
        usersCount.textContent = data.users_count;
        addSystemMessage(`${data.username} joined the chat`);
    });
    
    // Handle user left event
    socket.on('user_left', function(data) {
        usersCount.textContent = data.users_count;
        addSystemMessage(`${data.username} left the chat`);
    });
    
    // Handle incoming messages
    socket.on('message', function(data) {
        addMessage(data.username, data.message, data.timestamp, false);
    });
    
    // Handle chaos events
    socket.on('chaos_event', function(data) {
        chaosContent.innerHTML = `<h3>CHAOS EVENT: ${data.name}</h3><p>${data.description}</p>`;
        chaosAlert.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            chaosAlert.style.display = 'none';
        }, 5000);
        
        addSystemMessage(`CHAOS EVENT: ${data.name} - ${data.description}`);
    });
    
    // Send message on button click
    sendButton.addEventListener('click', sendMessage);
    
    // Send message on Enter key
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            socket.emit('send_message', { message: message });
            addMessage('You', message, new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}), true);
            messageInput.value = '';
        }
    }
    
    function addMessage(username, message, timestamp, isOwn) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(isOwn ? 'user-message' : 'other-message');
        
        messageElement.innerHTML = `
            <div class="message-header">
                <span class="username">${username}</span>
                <span class="timestamp">${timestamp}</span>
            </div>
            <div class="message-content">${message}</div>
        `;
        
        messagesContainer.appendChild(messageElement);
        scrollToBottom();
    }
    
    function addSystemMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'system-message');
        messageElement.textContent = message;
        
        messagesContainer.appendChild(messageElement);
        scrollToBottom();
    }
    
    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Initial focus on input
    messageInput.focus();
});
