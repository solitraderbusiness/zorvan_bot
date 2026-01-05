# Zorvan Bot - Setup Guide

Complete guide to set up and run the Class Audio Organizer application.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download Node.js](https://nodejs.org/)
- **ffmpeg** - Required for audio processing

### Installing ffmpeg

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

## Step 1: Backend Setup

### 1.1 Navigate to backend directory
```bash
cd backend
```

### 1.2 Create a Python virtual environment
```bash
python -m venv venv
```

### 1.3 Activate the virtual environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 1.4 Install Python dependencies
```bash
pip install -r requirements.txt
```

This will install:
- FastAPI - Web framework
- SQLAlchemy - Database ORM
- Whisper - Audio transcription
- LangChain - RAG framework
- ChromaDB - Vector database
- And other dependencies

**Note:** Installing Whisper and PyTorch may take several minutes.

### 1.5 Configure environment variables

The `.env` file is already created with default settings. You can modify it if needed:

```bash
nano .env  # or use any text editor
```

**Important settings:**
- `OPENAI_API_KEY` - (Optional) Add your OpenAI API key for better RAG responses
  - Get one at: https://platform.openai.com/api-keys
  - Without this, the app will use local models (slower but free)
- `ADMIN_EMAIL` and `ADMIN_PASSWORD` - Default admin credentials
- `WHISPER_MODEL` - Options: tiny, base, small, medium, large
  - `base` is recommended for balance between speed and accuracy

### 1.6 Run the backend server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will:
1. Create the SQLite database automatically
2. Create the admin user (vfx.soli@gmail.com / Ali011111)
3. Start the API server on http://localhost:8000

You can view the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Keep this terminal open** and proceed to frontend setup in a new terminal.

## Step 2: Frontend Setup

### 2.1 Open a new terminal and navigate to frontend directory
```bash
cd frontend
```

### 2.2 Install Node.js dependencies
```bash
npm install
```

This will install:
- React 18
- TypeScript
- Tailwind CSS
- React Router
- Axios
- Zustand (state management)

### 2.3 Run the frontend development server
```bash
npm run dev
```

The frontend will start on http://localhost:5173

## Step 3: Access the Application

1. Open your browser and go to: **http://localhost:5173**

2. Login with the default admin credentials:
   - **Email:** vfx.soli@gmail.com
   - **Password:** Ali011111

3. You should now see the dashboard!

## Step 4: Using the Application

### Creating Classes (Admin Only)

1. Click **"Create Class"** on the dashboard
2. Enter a name (e.g., "Advanced Mathematics")
3. Optionally add a description
4. Click **"Create"**

### Adding Users (Admin Only)

1. Click **"Admin Panel"** in the navigation
2. Click **"Add User"**
3. Enter email and password
4. Choose if the user should be an admin
5. Click **"Create"**

### Uploading Files

1. Click on a class from the dashboard
2. Click **"Upload File (Audio/PDF)"**
3. Select your audio file or PDF
4. Wait for the upload and processing
   - Audio files will be automatically transcribed using Whisper
   - PDFs will have text extracted
   - All content will be added to the RAG system

**Supported audio formats:**
- MP3, WAV, M4A, OGG, FLAC, AAC, WMA

**Note:** Large audio files (>25MB, >40min) are fully supported!

### Asking Questions

1. After uploading files, type your question in the chat box
2. The AI will search through all uploaded materials
3. You'll get an answer with source citations

**Example questions:**
- "What topics were covered in yesterday's lecture?"
- "Explain the concept of neural networks from the class"
- "What are the key formulas mentioned?"

### Changing Password

1. Click **"Profile"** in the navigation
2. Enter your current password
3. Enter and confirm your new password
4. Click **"Change Password"**

## Troubleshooting

### Backend Issues

**Error: "No module named 'app'"**
- Make sure you're in the `backend` directory
- Make sure the virtual environment is activated

**Error: "ffmpeg not found"**
- Install ffmpeg (see Prerequisites section)
- Make sure it's in your PATH

**Slow transcription:**
- Use a smaller Whisper model (tiny or base)
- Larger models (medium, large) are more accurate but slower

### Frontend Issues

**Error: "Cannot connect to API"**
- Make sure the backend is running on port 8000
- Check the `.env` file in frontend directory
- Verify `VITE_API_URL=http://localhost:8000/api`

**Blank page or errors:**
- Check the browser console for errors (F12)
- Make sure all npm packages installed correctly
- Try `npm install` again

### Database Issues

**Want to reset the database?**
```bash
cd backend
rm zorvan_bot.db
# Restart the backend - it will create a fresh database
```

## Production Deployment

For production deployment:

1. **Backend:**
   - Change `SECRET_KEY` in `.env` to a secure random value
   - Use PostgreSQL instead of SQLite
   - Use a production WSGI server (e.g., Gunicorn with Uvicorn workers)
   - Set `DEBUG=False`

2. **Frontend:**
   - Build the production bundle: `npm run build`
   - Serve with nginx or similar
   - Update `VITE_API_URL` to your production API URL

3. **Security:**
   - Use HTTPS for both frontend and backend
   - Configure proper CORS origins
   - Use strong passwords for all users
   - Regularly update dependencies

## Getting Help

For issues or questions:
- Check the API documentation: http://localhost:8000/docs
- Review the error logs in the terminal
- Contact: vfx.soli@gmail.com

## Features Overview

- **Multi-Class Support** - Organize materials by course/topic
- **Audio Transcription** - Automatic transcription using Whisper
- **PDF Support** - Extract and search PDF content
- **AI Q&A** - Ask questions using RAG technology
- **User Management** - Email-based access control
- **Admin Panel** - Manage users and classes
- **No File Limits** - Upload large audio files without restrictions
- **Secure Authentication** - JWT-based authentication
- **Password Management** - Users can change their passwords

Enjoy using Zorvan Bot!
