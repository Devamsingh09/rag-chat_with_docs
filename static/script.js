document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const chatForm = document.getElementById('chatForm');
    const fileInput = document.getElementById('fileInput');
    const queryInput = document.getElementById('queryInput');
    const uploadStatus = document.getElementById('uploadStatus');
    const chatMessages = document.getElementById('chatMessages');

    // Handle file upload
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const files = fileInput.files;
        if (files.length === 0) {
            showUploadStatus('Please select files to upload.', 'error');
            return;
        }

        const formData = new FormData();
        for (let file of files) {
            formData.append('files', file);
        }

        try {
            console.log('Sending upload request to:', '/upload');
            console.log('FormData contents:', Array.from(formData.entries()));

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            console.log('Response status:', response.status);
            console.log('Response headers:', Object.fromEntries(response.headers.entries()));

            const result = await response.json();
            console.log('Response result:', result);

            if (response.ok) {
                showUploadStatus(result.message, 'success');
            } else {
                showUploadStatus(result.error || 'Upload failed.', 'error');
            }
        } catch (error) {
            console.error('Fetch error:', error);
            showUploadStatus('Network error occurred.', 'error');
        }
    });

    // Handle chat
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const query = queryInput.value.trim();
        if (!query) return;

        // Add user message to chat
        addMessage(query, 'user');
        queryInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'query': query
                })
            });

            const result = await response.json();

            if (response.ok) {
                addMessage(result.response, 'bot');
            } else {
                addMessage(result.error || 'An error occurred.', 'bot');
            }
        } catch (error) {
            addMessage('Network error occurred.', 'bot');
        }
    });

    function showUploadStatus(message, type) {
        uploadStatus.textContent = message;
        uploadStatus.className = type;
        uploadStatus.style.display = 'block';

        setTimeout(() => {
            uploadStatus.style.display = 'none';
        }, 5000);
    }

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
