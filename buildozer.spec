[app]

# (str) Title of your application
title = Meetup Tracker

# (str) Package name
package.name = meetuptracker

# (str) Package domain (needed for android/ios packaging) - reverse-DNS
# style, doesn't need to be a real domain for a personal sideloaded app
package.domain = org.personal

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.3.1,kivymd==1.2.0,plyer,pillow,pyjnius

# (str) Presplash / icon can be added later; skipped for this personal build

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# CAMERA: needed for the "Take Photo" receipt button.
# We deliberately do NOT request WRITE_EXTERNAL_STORAGE / READ_EXTERNAL_STORAGE
# - the app stores its database and receipts in app-private storage,
# which needs no storage permission on any Android version.
android.permissions = CAMERA

# (int) Target Android API, minimum API and NDK API
# minapi bumped from 23 to 24: Python's build needs the preadv/pwritev
# functions, which Android's NDK only exposes starting at API 24.
android.api = 33
android.minapi = 24

# (list) The Android archs to build for
android.archs = arm64-v8a

# (bool) Automatically accept the Android SDK license agreements.
# Without this, the very first build stops and waits for you to type
# "y" to accept a license - this avoids that interactive prompt.
android.accept_sdk_license = True

# (str) Log level (2 = debug output, useful the first few times you build)
[buildozer]
log_level = 2
warn_on_root = 1
