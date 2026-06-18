# Trex Bot

A Python bot that automatically plays the Chrome T-Rex game by scanning 
pixels on the screen in real time. Built a Flask web dashboard to control 
and monitor the bot from the browser.

## What it does
- Watches the screen 120 times per second
- Detects incoming obstacles by checking pixel brightness
- Automatically presses Space to jump
- Web control panel shows live jump count and logs

## What I used
- Python
- Flask
- PyAutoGUI
- Pillow (PIL)
- HTML & CSS & JavaScript

## How to run it
1. Install dependencies:
   pip install flask pyautogui pillow numpy

2. Run the server:
   python app.py

3. Open your browser at http://localhost:5000

4. Open https://elgoog.im/t-rex/ in another window

5. Enter the canvas coordinates and click Start Bot
