# Lock Tool
# github.com/alexkmnsky

# Designed for Python 3.7.2
# **Requires Tkinter for the interface
# The only bypass for this tool is to logout via CTRL+ALT+DEL

import tkinter as tk
import tkinter.ttk as ttk
import threading
import ctypes
import time

STOPPED = False

def antiSwitch(parent):
    while(not STOPPED):
        # Release alt key
        ctypes.windll.user32.keybd_event(0x12, 0, 2, 0)
        # Release super/windows key
        ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)
        time.sleep(0.01)

class LimitedEntry(tk.Entry):

    def __init__(self, parent, limit, *args, **kwargs):

        self.limit = limit
        validate = (parent.register(self.validate), "%i")
        super().__init__(parent, *args, **kwargs, validate = "key", validatecommand = validate)

    def validate(self, i):
        if int(i) < self.limit:
            return True
        else:
            self.bell()
            return False

class App(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        parent.title("Lock Tool Configuration")
        super().__init__(parent, *args, **kwargs)
        self.pack()

        self.notebook = ttk.Notebook(self, width = 300, height = 100)

        self.options = ttk.Frame(self.notebook)
        
        self.password = tk.StringVar(self.options)
        ttk.Label(self.options, text = "Password:").pack(padx = 10, side = "left")
        ttk.Entry(self.options, textvariable = self.password).pack(side = "left")

        self.log = ttk.Frame(self.notebook)

        self.notebook.add(self.options, text = "Options")
        self.notebook.add(self.log, text = "Log")
        self.notebook.pack(fill = "y", padx = 10, pady = 5)

        self.startButton = ttk.Button(text = "Run", command = self.run)
        self.startButton.pack(side = "right", padx = 10, pady = (5, 15))

        parent.protocol("WM_DELETE_WINDOW", self.quit)

    def run(self):
        parent = tk.Toplevel()
        self.screen = Screen(parent, self.password.get())
        parent.mainloop()

    def quit(self):
        global STOPPED
        STOPPED = True
        quit()

class Screen(tk.Frame):

    def __init__(self, parent, password, *args, **kwargs):
        self.parent = parent
        parent.title("MAIN LOCK WINDOW")
        parent.config(bg = "black")
        parent.attributes("-fullscreen", True)
        super().__init__(parent, *args, **kwargs)

        self.config(bg = "")
        self.pack(expand = True)

        self.login = tk.Frame(self, width = 300, height = 100, relief = "raised", borderwidth = 3)
        self.login.pack(anchor = "center")
        self.login.pack_propagate(0)

        self.iconData = tk.PhotoImage(file = "keys.png")
        self.icon = tk.Label(self.login, image = self.iconData)
        self.icon.pack(side = "left", padx = 20)

        self.password = tk.StringVar(self)
        self.input = LimitedEntry(
            self.login,
            limit = 20,
            font = ("Arial", 16, ""),
            show = "•",
            textvariable = self.password
        )
        self.input.pack(side = "right", padx = 20)

        self.thread = threading.Thread(target = lambda: antiSwitch(self.parent))
        self.thread.start()

        parent.wm_attributes("-topmost", "true")
        parent.bind("<FocusOut>", lambda event: self.parent.focus_force())
        parent.bind("<Return>", lambda event: self.validate(password))
        parent.protocol("WM_DELETE_WINDOW", self.parent.focus_force)

    def validate(self, correctpass):
        if(self.password.get() == correctpass):
            global STOPPED
            STOPPED = True
            quit()

root = tk.Tk()
app = App(root)
if(not STOPPED):
    root.mainloop()


