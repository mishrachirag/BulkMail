
appIconPath = "Design/mail.ico"
appTitle = "Bulk Mail"
appApperanceMode = "dark"  # Themes: blue (default), dark-blue, green
appDefaultColorTheme = "dark-blue"# Modes: system (default), light, dark

def windowDesign(window,height,width):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    window.resizable(width = False,height=False)

def windowDesignFrame(window,height,width):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    window.minsize(width,height)
    window.maxsize(width,height)


def designLabel(widget,data):
    widget.configure(text=data,font=("Courier", 15),height=1,width=8)

def designLabelBold(widget,data):
    widget.configure(text=data,font=("Courier", 15,"bold"),height=1,width=8)

#textVariable
def designLabelDynamic(widget,data):
    widget.configure(textvariable=data,font=("Courier", 16,"bold"),height=1,width=8)

def designButton(widget,data):
    widget.configure(text=data,width=120,height=32,corner_radius=8)
