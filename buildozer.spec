[app]

# (str) Title of your application
title = Meetup Tracker

# (str) Package name
package.name = meetuptracker

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the base dir)
source.include_exts = py,png,jpg,kv,atlas,db

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3==3.11.6,hostpython3==3.11.6,kivy,kivymd,plyer,pillow,pyjnius,sqlite3,reportlab

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 24

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >= 23)
android.allow_backup = True

# (bool) Enable AndroidX support. Enable when packaging KivyMD or any other project depending on AndroidX.
android.enable_androidx = True


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = ignore, 1 = warn, 2 = error)
warn_on_root = 1
