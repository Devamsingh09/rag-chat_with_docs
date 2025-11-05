# Real-Time RAG Chat Application

A FastAPI-based RAG (Retrieval-Augmented Generation) chat application that allows users to upload documents and chat with them using AI.

## Features

- Upload multiple documents (PDF, TXT, DOCX)
- Real-time chat with uploaded documents
- Vector search using ChromaDB and HuggingFace embeddings
- Google Generative AI for response generation

## Quick Start

### Prerequisites
- Python 3.8+
- Google AI API key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation & Setup

1. **Clone or download the project:**
   ```bash
   git clone https://github.com/Devamsingh09/rag-chat_with_docs.git

   cd real_time_rag
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```

5. **Run the application:**
   ```bash
   python -m uvicorn app:app --reload --host 0.0.0.0 --port 57826
   ```

6. **Open in browser:**
   Navigate to: http://localhost:57826

## How to Use

### Step 1: Upload Documents
- Click "Choose Files" to select documents (PDF, TXT, DOCX supported)
- Click "Upload Files" to process them
- Wait for the success message

### Step 2: Chat with Documents
- Type your question in the chat input
- Press Enter or click "Send"
- The AI will respond based on the uploaded documents

### Step 3: Continue Chatting
- Ask follow-up questions
- Upload more documents as needed
- Each upload processes new documents and updates the knowledge base

## Project Structure

```
real_time_rag/
├── app.py                 # Main FastAPI application
├── main.py               # Alternative entry point
├── requirements.txt      # Python dependencies
├── render.yaml          # Render deployment config
├── .env.example         # Environment variables template
├── README.md            # This file
├── static/              # Frontend files
│   ├── index.html       # Main HTML page
│   ├── script.js        # Frontend JavaScript
│   └── styles.css       # CSS styles
├── src/                 # Backend source code
│   ├── chat_handler.py  # Chat processing logic
│   ├── embeddings.py    # Vector embeddings creation
│   ├── loaders.py       # Document loading utilities
│   ├── rag_chain.py     # RAG chain setup
│   └── text_splitter.py # Document chunking
├── data/                # Data directory
│   └── text_files/      # Sample text files
├── chroma_db/           # Vector database (auto-generated)
└── notebook/            # Jupyter notebooks
```

## API Endpoints

- `GET /`: Serve the main HTML page
- `POST /upload`: Upload documents for processing
  - Accepts: `files` (FormData with multiple files)
  - Returns: JSON with success/error message
- `POST /chat`: Send chat messages
  - Accepts: `query` (form data)
  - Returns: JSON with AI response

## Deployment to Render

### Prerequisites
- GitHub account
- Render account
- Google AI API key

### Steps

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** real-time-rag
     - **Runtime:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Add environment variables:
     - `GOOGLE_API_KEY`: Your Google AI API key
     - `USER_AGENT`: RealTimeRAG/1.0

3. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment completion
   - Access your app at the provided Render URL

## Environment Variables

- `GOOGLE_API_KEY`: **Required** - Your Google Generative AI API key
- `USER_AGENT`: Optional - User agent string (defaults to "MyFastAPIApp/1.0")

## Troubleshooting

### Common Issues

1. **"Network error occurred" on upload:**
   - Check that the server is running on the correct port
   - Verify CORS settings in app.py
   - Check browser console for detailed error messages

2. **"No documents uploaded yet" error:**
   - Upload documents first before chatting
   - Check that files were processed successfully

3. **Import errors:**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Activate virtual environment before running

4. **API key errors:**
   - Verify GOOGLE_API_KEY is set correctly in .env file
   - Check API key validity on Google AI Studio

### Debug Mode
Run with debug logging:
```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 57826 --log-level debug
```

## Notes

- Render's free tier has limitations on persistent storage, so uploaded documents and vector stores are temporary
- For production use, consider using persistent storage solutions like AWS S3 or database storage
- The app processes documents in memory, so very large documents may cause memory issues
