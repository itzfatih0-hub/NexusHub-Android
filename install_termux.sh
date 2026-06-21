#!/bin/bash
# ============================================================
# NEXUS EXECUTOR — ANDROID INSTALLER (TERMUX)
# AUTHOR: PROFESOR_FATIH + NEXUS 1.0
# ============================================================

echo "╔═══════════════════════════════════════════════╗"
echo "║    NEXUS EXECUTOR — ANDROID INSTALLER        ║"
echo "║    AUTHOR: PROFESOR_FATIH + NEXUS 1.0        ║"
echo "╚═══════════════════════════════════════════════╝"

# Update packages
echo "[✓] Updating packages..."
pkg update -y && pkg upgrade -y

# Install Python
echo "[✓] Installing Python..."
pkg install python -y

# Install dependencies
echo "[✓] Installing Python dependencies..."
pip install requests

# Copy files
echo "[✓] Copying Nexus Executor files..."
cp -r ../nexus_executor ~/

echo ""
echo "✅ ANDROID INSTALLATION COMPLETE!"
echo "✅ Nexus Executor installed to ~/nexus_executor/"
echo "✅ Run with: cd ~/nexus_executor && python nexus_executor.py"