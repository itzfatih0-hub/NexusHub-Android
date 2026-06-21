#!/usr/bin/env python3
# ============================================================
# PYTHON SETUP — NEXUS EXECUTOR (ANDROID/TERMUX VERSION)
# AUTHOR: PROFESOR_FATIH + NEXUS 1.0
# ============================================================

import os
import sys
import subprocess
import platform
import time

# ============================================================
# KONFIGURASI
# ============================================================

VERSION = "1.0.0"
AUTHOR = "PROFESOR_FATIH + NEXUS 1.0"
REQUIRED_PACKAGES = [
    "requests",
    "pillow"
]

# ============================================================
# COLORS (TERMUX SUPPORT)
# ============================================================

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_color(text, color=Colors.WHITE):
    print(f"{color}{text}{Colors.RESET}")

def clear():
    os.system('clear')

# ============================================================
# BANNER
# ============================================================

def banner():
    clear()
    print_color("""
    ╔═══════════════════════════════════════════════╗
    ║    PYTHON SETUP — NEXUS EXECUTOR             ║
    ║    PLATFORM: ANDROID (TERMUX)                ║
    ║    AUTHOR: PROFESOR_FATIH + NEXUS 1.0        ║
    ║    VERSION: 1.0.0 — OVERPOWER 2026           ║
    ╚═══════════════════════════════════════════════╝
    """, Colors.GREEN)
    print_color(f"📱 Platform: Android (Termux)", Colors.CYAN)
    print_color(f"📌 Version: {VERSION}", Colors.CYAN)
    print("="*50)
    print()

# ============================================================
# CHECK FUNCTIONS
# ============================================================

def check_python():
    """Check if Python is installed"""
    try:
        result = subprocess.run(
            ["python", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            print_color(f"[✓] Python found: {version}", Colors.GREEN)
            return True
        return False
    except:
        return False

def check_pip():
    """Check if pip is installed"""
    try:
        result = subprocess.run(
            ["python", "-m", "pip", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_color("[✓] Pip found!", Colors.GREEN)
            return True
        return False
    except:
        return False

def check_package(package):
    """Check if package is installed"""
    try:
        result = subprocess.run(
            ["python", "-c", f"import {package}"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False

# ============================================================
# INSTALL FUNCTIONS (TERMUX SPECIFIC)
# ============================================================

def install_python_termux():
    """Install Python via Termux pkg"""
    print_color("\n[✓] Installing Python via pkg...", Colors.BLUE)
    try:
        subprocess.run(["pkg", "update", "-y"], check=True)
        subprocess.run(["pkg", "install", "python", "-y"], check=True)
        print_color("[✓] Python installed successfully!", Colors.GREEN)
        return True
    except Exception as e:
        print_color(f"[✗] Failed to install Python: {e}", Colors.RED)
        return False

def install_pip_termux():
    """Install pip in Termux"""
    print_color("\n[✓] Installing pip...", Colors.BLUE)
    try:
        subprocess.run(["python", "-m", "ensurepip", "--upgrade"], check=True)
        print_color("[✓] Pip installed successfully!", Colors.GREEN)
        return True
    except Exception as e:
        print_color(f"[✗] Failed to install pip: {e}", Colors.RED)
        return False

def install_packages_termux():
    """Install required packages in Termux"""
    print_color("\n[✓] Installing Python packages...", Colors.BLUE)
    
    installed = []
    failed = []
    
    for package in REQUIRED_PACKAGES:
        print_color(f"  - Installing {package}...", Colors.CYAN, end=" ")
        if check_package(package):
            print_color("✅ Already installed", Colors.GREEN)
            installed.append(package)
        else:
            try:
                subprocess.run(
                    ["pip", "install", package],
                    check=True,
                    capture_output=True
                )
                print_color("✅ Installed!", Colors.GREEN)
                installed.append(package)
            except Exception as e:
                print_color(f"❌ Failed!", Colors.RED)
                failed.append(package)
    
    return installed, failed

# ============================================================
# CREATE FOLDERS
# ============================================================

def create_folders():
    """Create necessary folders"""
    print_color("\n[✓] Creating folders...", Colors.BLUE)
    
    folders = [
        os.path.expanduser("~/nexus_executor"),
        os.path.expanduser("~/nexus_executor/scripts"),
        os.path.expanduser("~/nexus_executor/logs")
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print_color(f"  - Created: {folder}", Colors.CYAN)
    
    print_color("[✓] Folders created!", Colors.GREEN)

# ============================================================
# CREATE REQUIREMENTS.TXT
# ============================================================

def create_requirements():
    """Create requirements.txt for Android"""
    print_color("\n[✓] Creating requirements.txt...", Colors.BLUE)
    
    req_path = os.path.expanduser("~/nexus_executor/requirements.txt")
    with open(req_path, 'w') as f:
        for package in REQUIRED_PACKAGES:
            f.write(f"{package}\n")
    
    print_color(f"[✓] Created: {req_path}", Colors.GREEN)

# ============================================================
# CREATE LAUNCHER SCRIPT
# ============================================================

def create_launcher():
    """Create launcher script for easy access"""
    print_color("\n[✓] Creating launcher...", Colors.BLUE)
    
    launcher_path = os.path.expanduser("~/nexus_executor/run.sh")
    with open(launcher_path, 'w') as f:
        f.write("""#!/bin/bash
# NEXUS EXECUTOR — ANDROID LAUNCHER
# AUTHOR: PROFESOR_FATIH + NEXUS 1.0

cd ~/nexus_executor
python nexus_executor.py
""")
    
    os.chmod(launcher_path, 0o755)
    print_color(f"[✓] Created: {launcher_path}", Colors.GREEN)

# ============================================================
# SHOW SUMMARY
# ============================================================

def show_summary(installed, failed):
    """Show installation summary"""
    print_color("\n" + "="*50, Colors.CYAN)
    print_color("📊 INSTALLATION SUMMARY", Colors.GREEN)
    print_color("="*50, Colors.CYAN)
    
    print_color(f"\n✅ Installed packages: {len(installed)}", Colors.GREEN)
    for pkg in installed:
        print_color(f"  - {pkg}", Colors.WHITE)
    
    if failed:
        print_color(f"\n❌ Failed packages: {len(failed)}", Colors.RED)
        for pkg in failed:
            print_color(f"  - {pkg}", Colors.RED)
        print_color("\n⚠️ Try installing manually:", Colors.YELLOW)
        for pkg in failed:
            print_color(f"  pip install {pkg}", Colors.CYAN)
    
    print_color("\n📁 Folders created:", Colors.GREEN)
    print_color("  ~/nexus_executor/", Colors.WHITE)
    print_color("  ~/nexus_executor/scripts/", Colors.WHITE)
    print_color("  ~/nexus_executor/logs/", Colors.WHITE)
    
    print_color("\n🚀 NEXT STEPS:", Colors.GREEN)
    print_color("  1. Copy nexus_executor.py to ~/nexus_executor/", Colors.CYAN)
    print_color("  2. Run: cd ~/nexus_executor && python nexus_executor.py", Colors.CYAN)
    print_color("  3. Or run: bash ~/nexus_executor/run.sh", Colors.CYAN)

# ============================================================
# MAIN
# ============================================================

def main():
    banner()
    time.sleep(1)
    
    print_color("[1/5] CHECKING PYTHON...", Colors.BLUE)
    if not check_python():
        if not install_python_termux():
            print_color("[✗] Python setup failed!", Colors.RED)
            input("\nPress ENTER to exit...")
            sys.exit(1)
    else:
        print_color("[✓] Python is ready!", Colors.GREEN)
    
    print_color("\n[2/5] CHECKING PIP...", Colors.BLUE)
    if not check_pip():
        if not install_pip_termux():
            print_color("[✗] Pip setup failed!", Colors.RED)
            input("\nPress ENTER to exit...")
            sys.exit(1)
    else:
        print_color("[✓] Pip is ready!", Colors.GREEN)
    
    print_color("\n[3/5] INSTALLING PACKAGES...", Colors.BLUE)
    installed, failed = install_packages_termux()
    
    print_color("\n[4/5] CREATING FOLDERS...", Colors.BLUE)
    create_folders()
    
    print_color("\n[5/5] CREATING REQUIREMENTS.TXT & LAUNCHER...", Colors.BLUE)
    create_requirements()
    create_launcher()
    
    show_summary(installed, failed)
    
    print_color("\n" + "="*50, Colors.CYAN)
    print_color("✅ ANDROID SETUP COMPLETE!", Colors.GREEN)
    print_color("="*50, Colors.CYAN)
    
    input("\nPress ENTER to exit...")

if __name__ == "__main__":
    main()
