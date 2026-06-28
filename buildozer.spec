[app]

# ============================================================
# IDENTITAS APLIKASI
# ============================================================

title = Nexus Executor
package.name = nexusexecutor
package.domain = com.nexus

# ============================================================
# VERSI
# ============================================================

version = 1.0.0

# ============================================================
# SOURCE CODE
# ============================================================

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,json

# Exclude file yang gak perlu
source.exclude_exts = spec,pyc,pyo
source.exclude_dirs = tests, __pycache__, venv, bin, logs, scripts
source.exclude_patterns = *.spec,*.log,*.pyc

# ============================================================
# REQUIREMENTS (YANG DIPERLUIN)
# ============================================================

requirements = python3,kivy,requests

# ============================================================
# ORIENTASI & TAMPILAN
# ============================================================

orientation = portrait
fullscreen = 0

# ============================================================
# ICON & SPLASH
# ============================================================

# Ganti dengan icon lo sendiri
# icon.filename = %(source.dir)s/assets/icon.png
# presplash.filename = %(source.dir)s/assets/splash.png

# ============================================================
# ANDROID SPECIFIC
# ============================================================

# API Level
android.api = 31
android.minapi = 21
android.ndk_api = 21

# Architektur (support semua)
android.archs = arm64-v8a, armeabi-v7a

# Permission
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Others
android.allow_backup = True
android.wakelock = False

# ============================================================
# KIVY & PYTHON FOR ANDROID
# ============================================================

osx.kivy_version = 2.2.0
p4a.bootstrap = sdl2

# ============================================================
# BUILD SETTINGS
# ============================================================

[buildozer]
log_level = 2
warn_on_root = 1

# Output folder
bin_dir = ./bin
build_dir = ./.buildozer