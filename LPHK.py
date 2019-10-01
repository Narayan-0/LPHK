#! /usr/bin/python3

import sys, os

try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("[LPHK] Error loading launchpad.py")

import lp_events, scripts, kb, files, sound, window

PATH = sys.path[0]

lp = launchpad.Launchpad()

def init():
    args = sys.argv.copy()
    options = []
    
    while len(args) > 1:  # args[0] = script name
        arg = args.pop();
        
        if (arg == "--debug") or (arg == "-d"):
            options.append("debug");
            print("[LPHK] Debugging mode active! Will not shut down on window close.")
            print("[LPHK] Run shutdown() to manually close the program correctly.")
            
        elif arg == "--autoconnect":
            options.append("autoconnect");
            
        elif arg.startswith("--layout="):
            options.append("loadlayout");
            options.insert(0, arg[9:])

        else:
            print("[LPHK] Invalid argument: " + arg + ". Ignoring...")

    files.init(PATH)
    sound.init(PATH)
    
    return options

def shutdown():
    if lp_events.timer != None:
        lp_events.timer.cancel()
    scripts.to_run = []
    for x in range(9):
        for y in range(9):
            if scripts.threads[x][y] != None:
                scripts.threads[x][y].kill.set()
    if window.lp_connected:
        scripts.unbind_all()
        lp_events.timer.cancel()
        lp.Close()
        window.lp_connected = False
    if window.restart:
        os.execv(sys.executable, ["\"" + sys.executable + "\""] + sys.argv)
    sys.exit("[LPHK] Shutting down...")

def main():
    options = init()
    window.init(lp, launchpad, options)
    if not "debug" in options:
        shutdown()

main()
