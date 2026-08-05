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

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3==3.11.6,hostpython3==3.11.6,kivy,kivymd,plyer,pillow,pyjnius,sqlite3,reportlab

# (str) Custom source folders for requirements
# Sets custom source for any requirement with recipes
# requirements.source.kivy = ../kivy

# (str) Presplash animation image
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = Name:service_script.py:ndarray

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the predefined names:
# red, blue, green, white, black, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey.
#android.presplash_color = white

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 24

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 23b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip python-for-android compilation
#p4a.source_dir =

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port argument to p4a (for development)
#p4a.port =


#
# Python for android (p4a) specific
#

# (list) p4a command line arguments
#p4a.hook =

# (bool) enable Android logcat filtering
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of linking
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >= 23)
android.allow_backup = True

# (str) XML file for custom backup rules (see official Android documentation)
#android.backup_rules =

# (str) If you need to insert extra code in AndroidManifest.xml
#android.manifest.extra_xml =

# (str) Custom Java code to add to the main activity
#android.add_src =

# (list) Java classes to add to the manifest
#android.add_activites =

# (list) Android custom Gradle dependencies
#android.gradle_dependencies =

# (bool) Enable AndroidX support. Enable when packaging KivyMD or any other project depending on AndroidX.
android.enable_androidx = True

# (list) Packaging options
#p4a.packaging_options =

# (list) Java files to add to the project (list of file names)
#android.add_java_files =

# (list) User targets to build
#android.add_build_targets =

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (list of absolute paths)
#android.add_libs_external =

# (list) Android shared libraries to add (.so files)
#android.add_libs_relative =

# (list) Android AAR libraries to add (.aar files)
#android.add_aars =

# (list) Java classes to add to the application class
#android.add_app_classes =


#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# See https://github.com/kivy/kivy-ios for more information

# (str) Name of the project to generate
#ios.project_name = sample

# (str) App bundle identifier
#ios.bundle_id = org.kivy.sample

# (str) App display name
#ios.display_name = My App

# (str) Development team ID
#ios.development_team = ABCDE12345

#
# Desktop Specific
#

# (str) Icon of the application
#desktop.icon =

# (str) Title of the application
#desktop.title = Meetup Tracker


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = ignore, 1 = warn, 2 = error)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output storage, absolute or relative to spec file
# bin_dir = ./bin
