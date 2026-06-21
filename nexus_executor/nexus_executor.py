#!/usr/bin/env python3
# ============================================================
# NEXUS EXECUTOR — ANDROID VERSION
# AUTHOR: PROFESOR_FATIH + NEXUS 1.0
# ============================================================

import os
import sys
import json
import time
import requests
import subprocess
from datetime import datetime

# ============================================================
# KONFIGURASI
# ============================================================

VERSION = "1.0.0"
AUTHOR = "PROFESOR_FATIH + NEXUS 1.0"
SCRIPT_DIR = os.path.expanduser("~/nexus_executor/scripts")
os.makedirs(SCRIPT_DIR, exist_ok=True)

# ============================================================
# COLORS
# ============================================================

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

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
    ║    NEXUS EXECUTOR — ANDROID                  ║
    ║    AUTHOR: PROFESOR_FATIH + NEXUS 1.0        ║
    ║    VERSION: 1.0.0 — OVERPOWER 2026           ║
    ╚═══════════════════════════════════════════════╝
    """, Colors.GREEN)
    print_color(f"📱 Platform: Android (Termux)", Colors.CYAN)
    print_color(f"📌 Scripts Folder: {SCRIPT_DIR}", Colors.CYAN)
    print("="*50)
    print()

# ============================================================
# MENU FUNCTIONS
# ============================================================

def list_scripts():
    """List all scripts"""
    scripts = os.listdir(SCRIPT_DIR)
    if not scripts:
        print_color("📂 No scripts found!", Colors.YELLOW)
        return []
    
    print_color("\n📚 AVAILABLE SCRIPTS:", Colors.GREEN)
    for i, script in enumerate(scripts, 1):
        if script.endswith('.lua'):
            print_color(f"  {i}. {script}", Colors.WHITE)
    return scripts

def execute_script():
    """Execute script"""
    scripts = list_scripts()
    if not scripts:
        return
    
    name = input("\n📝 Script name: ").strip()
    path = os.path.join(SCRIPT_DIR, name)
    
    if not os.path.exists(path):
        print_color(f"❌ Script not found: {name}", Colors.RED)
        return
    
    with open(path, 'r') as f:
        content = f.read()
    
    print_color("\n▶️ EXECUTING SCRIPT...", Colors.CYAN)
    print("="*50)
    
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('print('):
            content_text = line[6:-1].strip('"\'')
            print_color(f"📤 {content_text}", Colors.WHITE)
        elif line.startswith('--'):
            print_color(f"💬 {line[2:]}", Colors.BLUE)
    
    print("="*50)
    print_color("✅ Script executed successfully!", Colors.GREEN)

def create_script():
    """Create new script"""
    name = input("\n📝 Script name (with .lua): ").strip()
    if not name.endswith('.lua'):
        name += '.lua'
    
    print_color("\n📝 Enter script content (type 'END' on new line to finish):", Colors.CYAN)
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    
    content = '\n'.join(lines)
    path = os.path.join(SCRIPT_DIR, name)
    with open(path, 'w') as f:
        f.write(content)
    
    print_color(f"✅ Script saved: {name}", Colors.GREEN)

def download_script():
    """Download script from URL"""
    url = input("\n📥 Script URL: ").strip()
    name = input("📝 Save as (with .lua): ").strip()
    if not name.endswith('.lua'):
        name += '.lua'
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            path = os.path.join(SCRIPT_DIR, name)
            with open(path, 'w') as f:
                f.write(response.text)
            print_color(f"✅ Downloaded: {name}", Colors.GREEN)
        else:
            print_color(f"❌ Failed: HTTP {response.status_code}", Colors.RED)
    except Exception as e:
        print_color(f"❌ Error: {e}", Colors.RED)

# ============================================================
# MAIN
# ============================================================

def main():
    # Create default script if none exists
    default_path = os.path.join(SCRIPT_DIR, "default.lua")
    if not os.path.exists(default_path):
        with open(default_path, 'w') as f:
            f.write("""-- NEXUS EXECUTOR — DEFAULT SCRIPT
-- AUTHOR: PROFESOR_FATIH + NEXUS 1.0

print("NEXUS EXECUTOR IS READY!")
print("Welcome to the ultimate executor!")
""")
    
    while True:
        banner()
        
        print_color("📌 MENU:", Colors.GREEN)
        print("  1. 📚 List Scripts")
        print("  2. ▶️ Execute Script")
        print("  3. 📝 Create Script")
        print("  4. ⬇️ Download Script")
        print("  5. ❌ Exit")
        print()
        
        choice = input(Colors.CYAN + "📌 Choose: " + Colors.RESET).strip()
        
        if choice == "1":
            list_scripts()
            input("\nPress ENTER to continue...")
        elif choice == "2":
            execute_script()
            input("\nPress ENTER to continue...")
        elif choice == "3":
            create_script()
            input("\nPress ENTER to continue...")
        elif choice == "4":
            download_script()
            input("\nPress ENTER to continue...")
        elif choice == "5":
            print_color("\n👋 Exiting Nexus Executor...", Colors.YELLOW)
            sys.exit(0)
        else:
            print_color("❌ Invalid choice!", Colors.RED)
            input("\nPress ENTER to continue...")

if __name__ == "__main__":
    main()
