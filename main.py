name: WeChat to EPUB

on:
  push:
    paths:
      - 'input.txt'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Chrome and ChromeDriver
        run: |
          sudo apt-get update
          sudo apt-get install -y wget unzip xvfb libxi6 libgconf-2-4
          wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
          sudo apt install -y ./google-chrome-stable_current_amd64.deb
          wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
          unzip chromedriver_linux64.zip
          sudo mv chromedriver /usr/local/bin/
          sudo chmod +x /usr/local/bin/chromedriver

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install selenium

      - name: Run main.py with headless chrome
        run: xvfb-run python main.py

      - name: Upload EPUB artifact
        uses: actions/upload-artifact@v4
        with:
          name: wechat-epub
          path: output.epub


