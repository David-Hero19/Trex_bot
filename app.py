
import threading
import time
import queue
import sys

from flask import Flask, render_template, jsonify, Response, stream_with_context

app = Flask(__name__)

# Shared state
bot_state = {
    "running": False,
    "jumps": 0,
    "status": "idle",   
}
log_queue = queue.Queue()
bot_thread = None


def log(msg):
    print(msg)
    log_queue.put(msg)



def run_bot(region):
    global bot_state
    try:
        import pyautogui
        import numpy as np
        from PIL import ImageGrab

        SCAN_OFFSET_X  = 150
        SCAN_TOP       = 10
        SCAN_BOTTOM    = 2
        DARK_THRESHOLD = 180
        JUMP_COOLDOWN  = 0.5
        SAMPLE_RATE    = 120

        left, top, right, bottom = region
        width  = right - left
        height = bottom - top

        # Find dino x
        dino_x = left + int(width * 0.08)

        # Find ground y
        search_top = top + int(height * 0.6)
        screenshot = ImageGrab.grab(bbox=(left, search_top, right, bottom))
        arr = __import__("numpy").array(screenshot)
        darkness = (arr.mean(axis=2) < DARK_THRESHOLD).mean(axis=1)
        candidates = __import__("numpy").where(darkness > 0.3)[0]
        ground_y = (search_top + int(candidates[0])) if len(candidates) else top + int(height * 0.80)

        scan_x      = dino_x + SCAN_OFFSET_X
        scan_height = (ground_y - top) - SCAN_BOTTOM

        log(f"SCAN:x={scan_x} ground_y={ground_y} height={scan_height}px")

        # Click game area and start
        cx = (left + right) // 2
        cy = (top + bottom) // 2
        pyautogui.click(cx, cy)
        time.sleep(0.3)
        pyautogui.press("space")
        log("STARTED")

        interval       = 1.0 / SAMPLE_RATE
        last_jump_time = 0.0
        jumps          = 0

        while bot_state["running"]:
            now           = time.time()
            cooldown_over = (now - last_jump_time) > JUMP_COOLDOWN

            if cooldown_over:
                scan_top_y    = ground_y - scan_height
                scan_bottom_y = ground_y - SCAN_BOTTOM
                if scan_top_y < scan_bottom_y:
                    col = ImageGrab.grab(bbox=(scan_x - 2, scan_top_y, scan_x + 2, scan_bottom_y))
                    col_arr = __import__("numpy").array(col)
                    dark = (
                        (col_arr[:, :, 0] < DARK_THRESHOLD) &
                        (col_arr[:, :, 1] < DARK_THRESHOLD) &
                        (col_arr[:, :, 2] < DARK_THRESHOLD)
                    )
                    if dark.any():
                        pyautogui.press("space")
                        last_jump_time = time.time()
                        jumps += 1
                        bot_state["jumps"] = jumps
                        log(f"JUMP:{jumps}")

            time.sleep(interval)

    except Exception as e:
        log(f"ERROR:{e}")
    finally:
        bot_state["running"] = False
        bot_state["status"]  = "stopped"
        log("STOPPED")


# Routes 

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    from flask import request
    global bot_thread, bot_state

    if bot_state["running"]:
        return jsonify({"ok": False, "msg": "Bot already running"})

    data   = request.get_json()
    region = (
        int(data["left"]),
        int(data["top"]),
        int(data["right"]),
        int(data["bottom"]),
    )

    bot_state["running"] = True
    bot_state["jumps"]   = 0
    bot_state["status"]  = "running"

    bot_thread = threading.Thread(target=run_bot, args=(region,), daemon=True)
    bot_thread.start()

    return jsonify({"ok": True})


@app.route("/stop", methods=["POST"])
def stop():
    global bot_state
    bot_state["running"] = False
    bot_state["status"]  = "stopped"
    log("STOP_REQUESTED")
    return jsonify({"ok": True})


@app.route("/status")
def status():
    return jsonify(bot_state)


@app.route("/logs")
def logs():
    """Server-Sent Events stream of log messages."""
    def generate():
        while True:
            try:
                msg = log_queue.get(timeout=1)
                yield f"data: {msg}\n\n"
            except queue.Empty:
                yield ": heartbeat\n\n"
    return Response(stream_with_context(generate()), mimetype="text/event-stream")


if __name__ == "__main__":
    print("🦕  T-Rex Bot server starting …")
    print("    Open http://localhost:5000 in your browser")
    app.run(debug=False, threaded=True)
