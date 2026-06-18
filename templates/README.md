# 🦕 T-Rex Bot — Web Control Panel

A Flask web app that lets you control the T-Rex dino auto-player from your browser.

## Setup

1. Install dependencies:
   ```
   pip install flask pyautogui pillow numpy
   ```

2. Run the server:
   ```
   python app.py
   ```

3. Open your browser at:
   ```
   http://localhost:5000
   ```

## How to use

1. Open the game at https://elgoog.im/t-rex/ in another browser window
2. Get the canvas coordinates:
   - Press **F12** in Chrome to open DevTools
   - Click the **Console** tab
   - Paste this and press Enter:
     ```js
     document.querySelector('canvas').getBoundingClientRect()
     ```
   - Note the `left`, `top`, `right`, `bottom` values
3. Enter those values in the control panel
4. Click **▶ Start Bot**
5. Switch to the game window — the bot will start playing automatically!

## Project structure

```
trex_project/
├── app.py              ← Flask backend + bot logic
├── templates/
│   └── index.html      ← Control panel frontend
└── README.md
```
