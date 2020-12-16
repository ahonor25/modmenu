import keyboard, threading, gd, pymem, overlay, pywintypes, time, pygame
from win32gui import GetForegroundWindow, GetWindow, GetWindowRect, GetWindowText
from win32api import EnumDisplayMonitors

hotkey = "shift+tab"
process_name = "GeometryDash.exe"

class Player:
    def __init__(self, address, mem: pymem.Pymem):
        self.address = address
        self.mem = mem
        self.vent = False
        self.update()

    def update(self):
        self.vent = self.get_vent()

    def get_vent(self):
        return self.mem.read_uint(self.address + 0x31)

def write_username(text, address):
    pm.write_string(address, text)
    
def read_username(address):
    return pm.read_string(address)

addresses = [
    ("input", "Username", 0x05A502F8, (read_username, write_username)),
]

pm = pymem.Pymem("Geometry Dash.exe")
client = pymem.process.module_from_name(pm.process_handle, "GameAssembly.dll").lpBaseOfDll

# TODO: less cpu usage like wtf

overlay.init()
open = False

hacks = []
inputs = []

for intype, name, address, onoff in addresses:
    on, off = onoff
    print(on(address))
    if intype == "input":
        input = overlay.InputBox(overlay.gray, overlay.gray, 200, 200, 75, 30, 22, on(address), off, address)
        hacks.append(input)
        inputs.append(input)
    elif intype == "toggle":
        check = overlay.Checkbox(overlay.gray, overlay.blue, 200, 200, 10, 10, False)
        hacks.append(check)

def open_overlay():
    global open
    if open:
        open = False
        return
    open = True

def fullscreen():
    fs = False
    mons = EnumDisplayMonitors()
    hwnd = GetForegroundWindow()
    try:
        rect = GetWindowRect(hwnd)
    except pywintypes.error:
        return False
    for mon in mons:
        if rect == mon[2]:
            fs = True
            break
    if not fs:
        child = GetWindow(hwnd, 5)
        while child > 0:
            childRect = GetWindowRect(child)
            for mon in mons:
                if childRect == mon[2]:
                    fs = True
                    break
            if fs:
                break
            child = GetWindow(child, 2)
    return fs

keyboard.add_hotkey(hotkey, open_overlay, suppress=True)

while True:
    events = pygame.event.get()
    if open:
        overlay.startLoop()
        for t in hacks:
            t.draw()
            for e in pygame.event.get():
                handled = t.handle_event(e)
                if handled:
                    text, off, address = handled
                    off(text, address)
                t.update()
        overlay.endLoop()
        continue
    overlay.startLoop()
    overlay.endLoop()