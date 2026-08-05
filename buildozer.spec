name: Build Android APK

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/uses/python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install buildozer cython==0.29.36

      - name: Cache Buildozer global directory
        uses: actions/cache@v4
        with:
          path: ~/.buildozer
          key: buildozer-runner-${{ runner.os }}-py3.11.6-${{ hashFiles('**/buildozer.spec') }}
          restore-keys: |
            buildozer-runner-${{ runner.os }}-py3.11.6-

      - name: Clean stale Buildozer and p4a caches
        run: |
          rm -rf .buildozer
          rm -rf ~/.buildozer/android/platform/python-for-android/.build
          rm -rf ~/.buildozer/android/platform/python-for-android/dist/hostpython3* || true

      - name: Build APK with Buildozer
        uses: ArtemSydoryk/buildozer-action@v1
        with:
          command: buildozer -v android debug

      - name: Upload APK artifact
        uses: actions/upload-artifact@v4
        with:
          name: package
          path: bin/*.apk
