#!/usr/bin/env python3
"""
ChickOrder Backend Run Script
Cross-platform Python script to start the FastAPI server
"""

import os
import sys
import subprocess
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_colored(message, color=Colors.NC):
    """Print colored message"""
    print(f"{color}{message}{Colors.NC}")


def check_and_create_venv():
    """Check if virtual environment exists, create if not"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print_colored("Virtual environment not found. Creating one...", Colors.YELLOW)
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_colored("✓ Virtual environment created", Colors.GREEN)
    return venv_path


def get_python_executable():
    """Get the Python executable (use venv if available)"""
    venv_python = Path("venv/bin/python") if os.name != 'nt' else Path("venv/Scripts/python.exe")
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def check_env_file():
    """Check if .env file exists, create from .env.example if not"""
    env_path = Path(".env")
    if not env_path.exists():
        print_colored("⚠️  .env file not found!", Colors.YELLOW)
        env_example = Path(".env.example")
        if env_example.exists():
            print_colored("Copying .env.example to .env...", Colors.YELLOW)
            env_path.write_text(env_example.read_text())
            print_colored("⚠️  Please update .env with your configuration before running!", Colors.RED)
        else:
            print_colored("❌ .env.example not found!", Colors.RED)
            sys.exit(1)


def install_dependencies(python_exe):
    """Install/update dependencies"""
    print_colored("Checking dependencies...", Colors.GREEN)
    try:
        subprocess.run(
            [python_exe, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
            check=True
        )
        print_colored("✓ Dependencies installed", Colors.GREEN)
    except subprocess.CalledProcessError:
        print_colored("❌ Failed to install dependencies", Colors.RED)
        sys.exit(1)


def check_database(python_exe):
    """Check if database is initialized"""
    print_colored("Checking database...", Colors.GREEN)
    try:
        result = subprocess.run(
            [python_exe, "-c", 
             "from database import SessionLocal; from models import User; "
             "db = SessionLocal(); admin = db.query(User).filter(User.is_admin == True).first(); "
             "db.close(); exit(0 if admin else 1)"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print_colored("Database not initialized. Running init_db.py...", Colors.YELLOW)
            subprocess.run([python_exe, "init_db.py"], check=True)
            print_colored("✓ Database initialized", Colors.GREEN)
    except subprocess.CalledProcessError as e:
        print_colored(f"⚠️  Database check failed: {e}", Colors.YELLOW)
        print_colored("Continuing anyway...", Colors.YELLOW)
    except Exception as e:
        print_colored(f"⚠️  Could not check database: {e}", Colors.YELLOW)
        print_colored("Continuing anyway...", Colors.YELLOW)


def run_server(python_exe):
    """Run the FastAPI server"""
    print_colored("🚀 Starting FastAPI server...", Colors.GREEN)
    print_colored("API will be available at: http://localhost:8000", Colors.BLUE)
    print_colored("API docs will be available at: http://localhost:8000/docs", Colors.BLUE)
    print_colored("Press Ctrl+C to stop the server", Colors.GREEN)
    print("")
    
    try:
        subprocess.run(
            [python_exe, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            check=True
        )
    except KeyboardInterrupt:
        print_colored("\n\n👋 Server stopped", Colors.YELLOW)
    except subprocess.CalledProcessError as e:
        print_colored(f"\n❌ Server failed to start: {e}", Colors.RED)
        sys.exit(1)


def main():
    """Main function"""
    print_colored("🐔 Starting ChickOrder Backend...", Colors.GREEN)
    print("")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Setup steps
    check_and_create_venv()
    python_exe = get_python_executable()
    check_env_file()
    install_dependencies(python_exe)
    check_database(python_exe)
    
    # Run server
    print("")
    run_server(python_exe)


if __name__ == "__main__":
    main()

