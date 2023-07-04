import time, pyautogui, keyboard, random
import tkinter as tk

window = tk.Tk()
window.bind_all("<1>", lambda event:event.widget.focus_set())
xpos: int = 0
ypos: int = 0
hotkey: str = '0'
hotkeyCode = 0

running: bool = False

randomTimeOffset: bool = False
randomPositionOffset: bool = False

pyautogui.FAILSAFE = False #allows the autoclicker to click at (0,0)

window.title('AutoClicker')

def clickedStart(): #start the autoclicker from the start button
    global running
    running = True
    startAutoclicker(True)

def startAutoclicker(shouldStart): #start the autoclicker if shouldStart
    if shouldStart == False:
        return
    
    global running
    hideWidgets() #hide widgets so the autoclicker does not click its own buttons by mistake
    time.sleep(2)

    intervalInt = None
    xOffset, yOffset, timeOffset = 0, 0, 0

    try:
        intervalInt = float(txtClickDelay.get())
    except:
        intervalInt = 0

    try:
        xCoordinate = int(txtClickXPosition.get())
        yCoordinate = int(txtClickYPosition.get())
    except:
        xCoordinate, yCoordinate = 0, 0
    pyautogui.click(xCoordinate, yCoordinate)
    start = time.time()

    while True:
        if keyboard.is_pressed(hotkey):
            break
        if time.time() <= (start + intervalInt):
            continue
        if(randomPositionOffset):
            xOffset, yOffset = random.randrange(-5,5), random.randrange(-5,5)
        if(randomTimeOffset):
            timeOffset = random.uniform(-1,1)
        pyautogui.click(xCoordinate + xOffset, yCoordinate + yOffset)
        start = time.time() + timeOffset

    showWidgets()

def setHotkey(): #update the global hotkey value and code, diplay and bind the new hotkey
    global hotkey
    global hotkeyCode
    keyboard.remove_hotkey(hotkeyCode) # hotkeyCode identifies the previously bound hotkey and is returned by keyboard.add_hotkey()

    hotkey = keyboard.read_key()
    updateButtonText(btnStart, f'Start ({hotkey})')
    hotkeyCode = keyboard.add_hotkey(hotkey, hotkeyPress)

def hotkeyPress(): #start/stop the autoclicker depending on the state of "running"
    global running
    running = not running
    startAutoclicker(running)

hotkeyCode = keyboard.add_hotkey('0', hotkeyPress)

def clickedSetMousePosition(): #prepare to record next click position, set window to fullscreen and opaque and hide all widgets
    window.attributes('-fullscreen', True)
    window.attributes('-alpha', 0.3)
    hideWidgets()

    window.bind('<Button-1>', getMousePosition)
    
def clickedRandomDelay(): #flip the state of the set random delay button
    global randomTimeOffset
    randomTimeOffset = (not randomTimeOffset)
    if(btnRandomDelay.cget('relief') == tk.RAISED):
        btnRandomDelay.configure(bg='white', fg='black', relief=tk.SUNKEN)
    else:
        btnRandomDelay.configure(bg='green', fg='lightgreen', relief=tk.RAISED)

def clickedRandomPosition(): #flip the state of the set random position button
    global randomPositionOffset
    randomPositionOffset = (not randomPositionOffset)
    if(btnRandomPosition.cget('relief') == tk.RAISED):
        btnRandomPosition.configure(bg='white', fg='black', relief=tk.SUNKEN)
    else:
        btnRandomPosition.configure(bg='green', fg='lightgreen', relief=tk.RAISED)

def getMousePosition(event): #set the x and y position for the autoclicker, and regenerate all the widgets
    xpos, ypos = pyautogui.position()
    clearEntry(txtClickXPosition)
    clearEntry(txtClickYPosition)
    txtClickXPosition.insert(tk.END, xpos)
    txtClickYPosition.insert(tk.END, ypos)

    window.unbind('<Button-1>')

    window.attributes('-fullscreen', False)
    window.attributes('-alpha', 1)
    showWidgets()

def clearEntry(entry: tk.Entry): #clear an Entry text box
    entry.delete(0, tk.END)

def hideWidgets(): #hide all widgets
    for l in list:
        l.grid_remove()

def showWidgets(): #show all widgets
    for l in list:
        l.grid()

def updateButtonText(entry: tk.Button, newText):
    entry.configure(text=newText)

#Tkinter window setup
lblInterval = tk.Label(window, text='Click interval')
lblInterval.grid(column=1, row=0, padx=(50,10))

lblPosition = tk.Label(window, text='Mouse position')
lblPosition.grid(column=3, row=0, padx=(10,50))

txtClickDelay = tk.Entry(window, width=10)
txtClickDelay.grid(column=1, row=1, padx=(50,10))
txtClickDelay.insert(tk.END, '0')

txtClickXPosition = tk.Entry(window, width=4)
txtClickXPosition.grid(column=3, row=1, padx=(10,110))
txtClickXPosition.insert(tk.END, xpos)

txtClickYPosition = tk.Entry(window, width=4)
txtClickYPosition.grid(column=3, row=1, padx=(10,10))
txtClickYPosition.insert(tk.END, ypos)

btnSetMousePosition = tk.Button(window, text='Set position', command=clickedSetMousePosition, bg='green', fg='lightgreen')
btnSetMousePosition.grid(column=3, row=2, padx=(10,50), pady=(10,10))

btnStart = tk.Button(window, text='Start (0)', command=clickedStart, bg='green', fg='lightgreen')
btnStart.grid(column=1, row=2, padx=(50,10), pady=(10,10))   

btnRandomDelay = tk.Button(window, text='Random time offset', command=clickedRandomDelay, bg='green', fg='lightgreen', relief=tk.RAISED)
btnRandomDelay.grid(column=1, row=3, padx=(50,10), pady=(10,15))

btnRandomPosition = tk.Button(window, text='Random position offset', command=clickedRandomPosition, bg='green', fg='lightgreen', relief=tk.RAISED)
btnRandomPosition.grid(column=3, row=3, padx=(10,50), pady=(10,15))

btnSetHotkey = tk.Button(window, text='Set hotkey', command=setHotkey, bg='green', fg='lightgreen')
btnSetHotkey.grid(column=2, row=2, padx=(10,10))

list = window.grid_slaves()

window.mainloop()
