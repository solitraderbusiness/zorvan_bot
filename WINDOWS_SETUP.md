# Windows 11 Setup Guide - Zorvan Bot

Complete step-by-step guide for Windows 11 users.

## Prerequisites

### Install Required Software

1. **Python 3.11+**: https://www.python.org/downloads/
   - ⚠️ Check "Add Python to PATH" during installation!

2. **Node.js 18+**: https://nodejs.org/
   - Download the LTS version

3. **Git**: https://git-scm.com/download/win
   - Use default settings

4. **ffmpeg**: https://www.gyan.dev/ffmpeg/builds/
   - Download "ffmpeg-release-essentials.zip"
   - Extract to `C:\ffmpeg`
   - Add `C:\ffmpeg\bin` to PATH (see instructions below)

### Adding ffmpeg to PATH

1. Press `Windows` key, type "environment"
2. Click "Edit the system environment variables"
3. Click "Environment Variables"
4. Under "System variables", find "Path", click "Edit"
5. Click "New", add: `C:\ffmpeg\bin`
6. Click OK on all windows
7. Restart Command Prompt to apply changes

---

## Step 1: Clone the Repository

1. **Choose a location** for your project (e.g., `C:\Users\YourName\Projects`)

2. **Open Command Prompt**:
   - Press `Windows + R`
   - Type `cmd`
   - Press Enter

3. **Navigate to your projects folder**:
   ```cmd
   cd C:\Users\YourName\Projects
   ```

4. **Clone the repository**:
   ```cmd
   git clone https://github.com/solitraderbusiness/zorvan_bot.git
   ```

5. **Navigate into the project**:
   ```cmd
   cd zorvan_bot
   ```

---

## Step 2: Backend Setup

### Option A: Automated Setup (Recommended)

1. **Navigate to backend folder**:
   ```cmd
   cd backend
   ```

2. **Run the setup script**:
   ```cmd
   setup.bat
   ```

3. **Follow the prompts**, then:
   ```cmd
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Option B: Manual Setup

1. **Open File Explorer**, go to `zorvan_bot\backend`
2. **Click in the address bar**, type `cmd`, press Enter
3. **Run these commands**:

```cmd
python verify_files.py
python -m venv venv
venv\Scripts\activate
copy .env.example .env
pip install --timeout=1000 -r requirements.txt
```

### Run the Backend

```cmd
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
Creating admin user: vfx.soli@gmail.com
Admin user created successfully
```

**Keep this window open!**

---

## Step 3: Frontend Setup

### Open a NEW Command Prompt

1. Press `Windows + R`, type `cmd`, press Enter

2. **Navigate to frontend**:
   ```cmd
   cd C:\Users\YourName\Projects\zorvan_bot\frontend
   ```

3. **Install packages**:
   ```cmd
   npm install
   ```

4. **Run frontend**:
   ```cmd
   npm run dev
   ```

You should see:
```
➜  Local:   http://localhost:5173/
```

**Keep this window open too!**

---

## Step 4: Access the Application

1. **Open your browser**
2. **Go to**: http://localhost:5173
3. **Login**:
   - Email: `vfx.soli@gmail.com`
   - Password: `Ali011111`

---

## Common Issues

### "Python not recognized"
- Reinstall Python with "Add to PATH" checked
- Restart computer

### "npm not recognized"
- Reinstall Node.js
- Restart computer

### "ffmpeg not recognized"
- Verify PATH is set correctly
- Restart Command Prompt

### "ModuleNotFoundError: No module named 'app.models'"
- Make sure you're in the `backend` folder
- Run `python verify_files.py` to check all files exist
- If files are missing, run `git pull` again

### Timeout during pip install
```cmd
pip install --timeout=1000 -r requirements.txt
```

Or install in batches:
```cmd
pip install fastapi uvicorn python-multipart sqlalchemy
pip install python-jose passlib python-dotenv pydantic
pip install -r requirements.txt
```

### Port already in use
- Close other applications
- Or use different ports:
  - Backend: `uvicorn app.main:app --reload --port 8001`
  - Frontend: `npm run dev -- --port 5174`

---

## Daily Usage

Every time you want to use the app:

### Terminal 1 - Backend
```cmd
cd path\to\zorvan_bot\backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend
```cmd
cd path\to\zorvan_bot\frontend
npm run dev
```

### Browser
http://localhost:5173

---

## Verification Checklist

Run this to verify everything is set up:

```cmd
cd backend
python verify_files.py
```

All checks should show ✓

---

## Getting Help

- Check the error message carefully
- Make sure you're in the correct directory
- Try restarting Command Prompt
- Restart your computer if issues persist

Contact: vfx.soli@gmail.com
