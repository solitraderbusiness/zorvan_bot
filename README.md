# Zorvan Bot - Class Audio Organizer

A comprehensive AI-powered class audio organizer that allows students to upload class recordings and PDFs, and ask questions using RAG (Retrieval-Augmented Generation).

## Features

- 🎓 **Multiple Classes**: Create and manage different university topics
- 🎤 **Audio Transcription**: Automatic transcription of class recordings using Whisper
- 📄 **PDF Support**: Upload and process PDF documents
- 💬 **AI Chat**: Ask questions and get answers from your class materials
- 👥 **User Management**: Email-based access control with admin panel
- 🔒 **Secure Authentication**: JWT-based authentication with password management
- 📁 **Large File Support**: No limitations on audio file size or duration

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Audio Transcription**: OpenAI Whisper
- **PDF Processing**: PyPDF2
- **RAG System**: LangChain + ChromaDB + Sentence Transformers
- **LLM**: OpenAI GPT (configurable)

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Routing**: React Router

## Project Structure

```
zorvan_bot/
├── backend/           # FastAPI backend
│   ├── app/          # Application code
│   ├── uploads/      # Uploaded files
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/         # Source code
│   └── package.json
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- ffmpeg (for audio processing)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Edit `.env` and add your configuration (OpenAI API key, etc.)

6. Run the backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Run the frontend:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Default Admin Account

- **Email**: vfx.soli@gmail.com
- **Password**: Ali011111

## Usage

1. **Login**: Use the default admin credentials or credentials provided by an admin
2. **Create Classes**: Navigate to the admin panel to create new classes
3. **Add Users**: Admins can add users with email and password
4. **Upload Files**: Upload audio recordings and PDFs to classes
5. **Ask Questions**: Use the chat interface to ask questions about your class materials

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Running Tests
```bash
cd backend
pytest
```

### Database Migrations
The application uses SQLAlchemy with automatic table creation on startup.

## Deployment

### Using Docker (Coming Soon)
```bash
docker-compose up -d
```

### Manual Deployment
1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables for production
3. Use a production WSGI server (uvicorn with gunicorn)
4. Build the frontend: `npm run build`
5. Serve the frontend with nginx or similar

## Contributing

This is a private educational project. Contact the administrator for access.

## License

Private - All Rights Reserved

## Support

For issues or questions, contact: vfx.soli@gmail.com
