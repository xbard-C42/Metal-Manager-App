# Copper Manager App

A portable Python application for managing copper (and optionally silver/gold) holdings, featuring:

- PIN-protected access stored securely on a SIM card or local config
- Live price fetching via Metals API
- Inventory database with SQLite
- Clean Tkinter GUI
- Portable WinPython and PyInstaller packaging for USB deployment

![Metal-Manager-App Banner](https://github.com/xbard-C42/Metal-Manager-App/blob/main/Copper%20Manager%20App.jpg)

## Features
1. **Secure Authentication**: PIN hashed with PBKDF2, stored on SIM or local `config.json`.
2. **Live Pricing**: Fetch real-time copper prices (XCU/USD).
3. **Inventory Management**: Track bars by weight, purity, location (on-person, vehicle, cache).
4. **Portable Deployment**: Runs from WinPython USB or PyInstaller-frozen single executable.
5. **Extensible**: Easily add silver/gold symbol support in `api.py` and UI.

## Quickstart
1. **Install WinPython** on your USB drive.
2. **Clone** this repo into `USB_ROOT\\CopperManager`.
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
