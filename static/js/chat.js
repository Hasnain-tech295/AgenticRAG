// Chat interface JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.querySelector('.chat-form');
    const chatInput = document.querySelector('.chat-input');
    const chatMessages = document.getElementById('chat-messages');

    // Auto-focus on input when page loads
    chatInput.focus();

    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        // Add loading state
        const sendButton = document.querySelector('.send-button');
        const originalHTML = sendButton.innerHTML;
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        sendButton.disabled = true;

        // Scroll to bottom after form submission
        setTimeout(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 100);
    });

    // Auto-resize textarea (if we change to textarea later)
    function autoResizeTextarea() {
        chatInput.style.height = 'auto';
        chatInput.style.height = chatInput.scrollHeight + 'px';
    }

    // Enter key to submit
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // Smooth scroll to bottom when new messages appear
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Scroll to bottom on page load if there are messages
    if (chatMessages.children.length > 0) {
        scrollToBottom();
    }

    // Add some visual feedback for successful message send
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('sent')) {
        // Could add a success animation here
        console.log('Message sent successfully');
    }

    // Typing indicator (could be enhanced later with WebSocket)
    let typingTimer;
    chatInput.addEventListener('input', function() {
        clearTimeout(typingTimer);
        // Could show typing indicator here
    });
});