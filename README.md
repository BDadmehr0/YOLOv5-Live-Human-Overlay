
# 🧠 YOLOv5 Live Human Overlay

🎯 This project creates a transparent overlay on your screen that detects humans in real-time using YOLOv5 and draws bounding boxes and aim-lines on them.

<p align="center">
  <img src="https://img.shields.io/badge/YOLOv5-Powered-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Python-3.8%2B-yellow?style=flat-square" />
  <img src="https://img.shields.io/badge/Windows-Supported-lightgrey?style=flat-square" />
</p>

## 📷 Features

- Real-time human detection using YOLOv5.
- Transparent fullscreen overlay drawn with `tkinter`.
- Click-through window so you can interact with the desktop/apps below.
- Draws bounding boxes and aim-lines to detected humans.
- GPU support (if available).

## 🚀 Requirements

Make sure you have Python 3.8+ and install the following dependencies:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install pyautogui mss numpy opencv-python pillow
pip install pywin32
````

## 💻 How to Run

```bash
python main.py
```

> On first run, it will download the pretrained YOLOv5 model (`yolov5s`) from Ultralytics Hub.

## 🧠 How It Works

1. Uses `mss` to capture the screen in real-time.
2. Runs inference on the captured frames using YOLOv5.
3. Detects humans (`person` class only).
4. Calculates their position and draws:

   * Red bounding box (torso estimate).
   * Green circle (center).
   * Blue line from your mouse to the target.
5. The `tkinter` window is set to be **transparent and click-through**.


## ⚠️ Notes

* **Windows only** (due to `pywin32` and `ctypes` for click-through).
* Designed for 1600x900 resolution by default. Adjust `SCREEN_WIDTH/HEIGHT` if needed.
* Performance depends on GPU availability.

## 📸 Screenshot

![Screenshot 1](https://github.com/BDadmehr0/YOLOv5-Live-Human-Overlay/blob/main/src/Screenshot%20(3).png "Screenshot 1")

![Screenshot 2](https://github.com/BDadmehr0/YOLOv5-Live-Human-Overlay/blob/main/src/Screenshot%20(7).png "Screenshot 2")

## 📄 License

[MIT License](LICENSE)

## ✨ Credits

* [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5)
* Python libraries: `tkinter`, `torch`, `pyautogui`, `mss`, `opencv`, `pywin32`
