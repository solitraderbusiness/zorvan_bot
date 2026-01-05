"""
Verification script to check if all required files exist.
Run this after pulling from git to verify your setup.
"""
import os
import sys

def check_file(filepath):
    """Check if a file exists."""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {filepath}")
    return exists

def main():
    print("Checking backend files...\n")

    all_exist = True

    # Core files
    files_to_check = [
        # Main files
        "app/__init__.py",
        "app/config.py",
        "app/database.py",
        "app/main.py",

        # Models
        "app/models/__init__.py",
        "app/models/user.py",
        "app/models/class_.py",
        "app/models/file.py",

        # Schemas
        "app/schemas/__init__.py",
        "app/schemas/user.py",
        "app/schemas/class_.py",
        "app/schemas/file.py",
        "app/schemas/chat.py",

        # API
        "app/api/__init__.py",
        "app/api/auth.py",
        "app/api/users.py",
        "app/api/classes.py",
        "app/api/files.py",
        "app/api/chat.py",

        # Services
        "app/services/__init__.py",
        "app/services/transcription_service.py",
        "app/services/pdf_service.py",
        "app/services/rag_service.py",

        # Utils
        "app/utils/__init__.py",
        "app/utils/security.py",
        "app/utils/dependencies.py",

        # Config
        ".env.example",
        "requirements.txt",
    ]

    for filepath in files_to_check:
        if not check_file(filepath):
            all_exist = False

    print("\n" + "="*50)
    if all_exist:
        print("✓ All files exist! You're ready to run the backend.")
        print("\nNext steps:")
        print("1. Create virtual environment: python -m venv venv")
        print("2. Activate it: venv\\Scripts\\activate")
        print("3. Install packages: pip install -r requirements.txt")
        print("4. Copy .env.example to .env")
        print("5. Run: uvicorn app.main:app --reload")
    else:
        print("✗ Some files are missing!")
        print("\nTry running: git pull origin claude/class-audio-organizer-oSoNu")
        print("If that doesn't work, you may need to re-clone the repository.")
        sys.exit(1)

if __name__ == "__main__":
    main()
