import requests
import time
from macro import run_macro
import psutil
import os
import threading
from PIL import Image
import pystray
import ctypes  # for hiding console window on Windows
import configparser
import json
import sys
import tkinter
from tkinter import filedialog, messagebox
import webbrowser

VERSION = '0.1.1'
stop_event = threading.Event()

def exit_app(icon, item):
    stop_event.set()
    icon.stop()

# disable self-signed cert warnings
requests.packages.urllib3.disable_warnings()

# handler to open GitHub repo
def open_repo(icon, item):
    webbrowser.open('https://github.com/DaBomber60/LeagueChatHider')

def load_base_path():
    # config file path in script directory
    cfg_file = os.path.join(os.path.dirname(__file__), 'settings.ini')
    cp = configparser.ConfigParser()
    # try loaded path
    if os.path.exists(cfg_file):
        cp.read(cfg_file)
        path = cp.get('Paths', 'league_dir', fallback='')
        if os.path.isdir(path) and os.path.isfile(os.path.join(path,'Config','game.cfg')) and os.path.isfile(os.path.join(path,'Config','PersistedSettings.json')):
            return path
    # default path
    default = r"C:\Riot Games\League of Legends"
    if os.path.isdir(default):
        return default
    # prompt user
    tkinter.Tk().withdraw()
    while True:
        selected = filedialog.askdirectory(title="Select League of Legends Installation Directory")
        if not selected:
            retry = messagebox.askretrycancel("Error", "Directory selection required")
            if not retry:
                sys.exit("Directory selection cancelled by user")
            continue
        if os.path.isfile(os.path.join(selected,'Config','game.cfg')) and os.path.isfile(os.path.join(selected,'Config','PersistedSettings.json')):
            cp['Paths'] = {'league_dir': selected}
            with open(cfg_file, 'w') as f:
                cp.write(f)
            return selected
        messagebox.showerror("Invalid Directory", "Selected directory does not contain required config files")

# determine league installation directory
LEAGUE_DIR = load_base_path()

API_URL = "https://127.0.0.1:2999/liveclientdata/gamestats"

state = None  # current state accessible for tray menu
state_labels = {
    'waiting_for_client': 'Waiting for client',
    'wait_for_loading_screen': 'Waiting for loading screen',
    'wait_for_game_start': 'Waiting for game start',
    'monitor_game_running': 'Game running'
}

icon = None

def set_state(new):
    global state, icon
    state = new
    if icon:
        icon.menu = build_menu()
        icon.update_menu()

def build_menu():
    """Create the system tray menu with current state label."""
    return pystray.Menu(
        pystray.MenuItem(lambda item: state_labels.get(state, ''), None, enabled=False),
        pystray.MenuItem(f"Version: {VERSION}", None, enabled=False),
        pystray.MenuItem('League Chat Hider on GitHub', open_repo),
        pystray.MenuItem('Exit', exit_app)
    )

def get_json():
    try:
        r = requests.get(API_URL, timeout=5, verify=False)
        return r.status_code, r.json()
    except Exception:
        return None, None

def is_client_running():
    return any(proc.info['name']== 'LeagueClientUx.exe' for proc in psutil.process_iter(['name']))

def update_configs():
    """Ensure NativeOffsetY and NativeOffsetX are set in both game.cfg and PersistedSettings.json."""
    # Paths to config files
    base = os.path.join(LEAGUE_DIR, 'Config')
    ini_path = os.path.join(base, 'game.cfg')
    json_path = os.path.join(base, 'PersistedSettings.json')
    # Update game.cfg
    cp = configparser.ConfigParser()
    cp.read(ini_path)
    changed = False
    if cp['Chat'].get('NativeOffsetY') != '1':
        cp['Chat']['NativeOffsetY'] = '1'
        changed = True
    if cp['Chat'].get('NativeOffsetX') != '0':
        cp['Chat']['NativeOffsetX'] = '0'
        changed = True
    if changed:
        with open(ini_path, 'w') as f:
            cp.write(f)
    # Update PersistedSettings.json
    with open(json_path, 'r') as f:
        data = json.load(f)
    for file in data.get('files', []):
        if file.get('name') == 'Game.cfg':
            for section in file.get('sections', []):
                if section.get('name') == 'Chat':
                    for setting in section.get('settings', []):
                        if setting.get('name') == 'NativeOffsetY':
                            setting['value'] = '1'
                        if setting.get('name') == 'NativeOffsetX':
                            setting['value'] = '0'
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    global state
    while not stop_event.is_set():
        # wait for client
        set_state('waiting_for_client')
        while not is_client_running():
            time.sleep(5)

        # wait for loading screen to finish
        set_state('wait_for_loading_screen')
        update_configs()
        while is_client_running():
            status, data = get_json()
            if status == 404 and data.get('errorCode') == 'RESOURCE_NOT_FOUND':
                break
            time.sleep(1)
        else:
            continue

        # wait for game start
        set_state('wait_for_game_start')
        # fetch window dimensions and chat scale
        cfg = configparser.ConfigParser()
        cfg.read(os.path.join(LEAGUE_DIR, 'Config', 'game.cfg'))
        window_w = int(cfg['General'].get('Width', 0))
        window_h = int(cfg['General'].get('Height', 0))
        chat_scale = int(cfg['HUD'].get('ChatScale', 0))
        while is_client_running():
            status, data = get_json()
            if status == 200 and 'gameTime' in data and data.get('gameTime', 0) > 1:
                run_macro(window_w, window_h, chat_scale)
                break
            time.sleep(0.1)
        else:
            continue

        # monitor game until it ends or client closes
        set_state('monitor_game_running')
        while is_client_running():
            status, data = get_json()
            if status != 200:
                break
            time.sleep(30)

if __name__ == "__main__":
    # hide console window on Windows
    if os.name == 'nt':
        hWnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hWnd:
            ctypes.windll.user32.ShowWindow(hWnd, 0)

    # update configs before starting
    update_configs()

    # start main loop in background thread
    thread = threading.Thread(target=main)
    thread.start()

    # load tray icon
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    image = Image.open(icon_path)
    # initial tray icon and dynamic menu
    icon = pystray.Icon('LeagueChatHider', image, 'LeagueChatHider', build_menu())
    icon.run()
    # wait for background thread to exit cleanly
    thread.join()