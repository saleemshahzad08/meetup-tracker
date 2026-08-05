[app]
# (str) Title of your application
title = Meetup Tracker
# (str) Package name
package.name = meetuptracker
# (str) Package domain (needed for android/ios packaging)
package.domain = org.personal
# (str) Source code where the main.py lives
source.dir = .
# (list) Source files to include (Crucial: Added 'db' so your database packages)
source.include_exts = py,png,jpg,jpeg,kv,atlas,db
# (str) Application versioning
version = 0.1
# (list) Application requirements
# Relaxed versions to prevent 502/timeout resolution loops, added sqlite3.
# reportlab added for the PDF export feature.
requirements = python3,kivy,kivymd,plyer,pillow,pyjnius,sqlite3,reportlab
# (str) Supported orientation
orientation = portrait
# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0
# (list) Permissions
android.permissions = CAMERA
# (int) Target Android API and minimum API
# Set to 34 (Android 14) for maximum stability with modern Buildozer engines
android.api = 34
android.minapi = 24
# (list) The Android archs to build for
android.archs = arm64-v8a
# (bool) Automatically accept the Android SDK license agreements.
android.accept_sdk_license = True

[buildozer]
# (str) Log level (2 = debug output)
log_level = 2
# (int) Display warning if buildozer is run as root
warn_on_root = 1
