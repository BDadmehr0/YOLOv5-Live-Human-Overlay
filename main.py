import tkinter as tk
from ctypes import windll
import pyautogui
import mss
import numpy as np
import cv2
import threading
import time
import torch
import warnings
import win32con
import win32gui

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

warnings.filterwarnings("ignore", category=FutureWarning)

class Overlay(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-topmost', True)
        self.overrideredirect(True)
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+0+0")
        self.wm_attributes("-transparentcolor", "white")

        self.canvas = tk.Canvas(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="white", highlightthickness=0)
        self.canvas.pack()

        self.mouse_pos = (0, 0)
        self.robot_positions = []

        self.after(10, self.make_window_clickthrough)
        self.update_loop()

    def make_window_clickthrough(self):
        hwnd = windll.user32.GetParent(self.winfo_id())
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        ex_style |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOOLWINDOW
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)

    def update_mouse_pos(self):
        self.mouse_pos = pyautogui.position()

    def update_robot_positions(self, positions):
        self.robot_positions = positions

    def update_loop(self):
        self.canvas.delete("all")
        self.update_mouse_pos()

        x, y = self.mouse_pos

        for (rx, ry) in self.robot_positions:
            self.canvas.create_rectangle(rx-30, ry-70, rx+30, ry+70, outline='red', width=2)
            self.canvas.create_oval(rx-15, ry-15, rx+15, ry+15, outline='green', width=1)

            self.canvas.create_line(x, y, rx, ry, fill='blue', width=1)

        self.after(30, self.update_loop)


def screen_capture_and_detect(overlay):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.to(device)

    target_classes = ['person']

    monitor = {"top": 0, "left": 0, "width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}
    with mss.mss() as sct:
        while True:
            screenshot = np.array(sct.grab(monitor))
            img_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

            results = model(img_bgr)
            detections = results.pandas().xyxy[0]

            detected_positions = []

            for _, row in detections.iterrows():
                cls = row['name']
                if cls not in target_classes:
                    continue

                x1, y1, x2, y2 = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])
                center_x = (x1 + x2) // 2
                center_y = int((y1 + y2) // 2 - (y2 - y1) * 0.25)
                detected_positions.append((center_x, center_y))

            overlay.update_robot_positions(detected_positions)
            time.sleep(0.03)


if __name__ == "__main__":
    overlay = Overlay()
    t = threading.Thread(target=screen_capture_and_detect, args=(overlay,), daemon=True)
    t.start()
    overlay.mainloop()
