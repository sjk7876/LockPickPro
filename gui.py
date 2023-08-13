"""
This file runs the GUI for the program, relying on bruteforce.py for the work

@Author Spencer Kurtz
"""

import bruteforce

import tkinter
from tkinter import StringVar, messagebox, ttk, E, BooleanVar, Frame
from tkinter import messagebox

from threading import Thread

from playsound import playsound

"""
TODO
metal pipe falling sound
nyan cat loading bar ?

GENERATE EXE
"""


# Global to hold current hash, file location, and mangle flag
masterHash = ""
masterFile = ""
masterMangle = False

# metalPipeSound = AudioSegment.from_mp3("E:\Coding\PenTestingTool\sounds\metal_pipe.mp3")


def main():
    global frame

    gui = App()

    gui.mainloop()


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Lock Pick Pro")
        self.geometry("400x300")
        self.minsize(200, 200)
        self.maxsize(900, 900)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (startFrame, optionsFrame, computeFrame):
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame            

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("startFrame")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

        if frame_name == "computeFrame":
            self.processComputeTask(frame)
    
    def processComputeTask(self, computeFrame):
        def task():
            computeFrame.reset()
            algo = bruteforce.determineHashAlgo(masterHash)
            found_pass = bruteforce.startCrackWithCPU(masterHash, algo, masterFile, masterMangle)

            self.after(0, lambda: computeFrame.update_ui(algo, found_pass))

        thread = Thread(target=task)
        thread.start()


class startFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        global masterHash

        self.mAlgo = StringVar(self, "")

        # Create header
        self.headerLabel = ttk.Label(self, text="Choose Method", font=("Courier", 14))

        # Create labels for inputs
        self.hashLabel = ttk.Label(self, text="Hash:")
        self.orLabel = ttk.Label(self, text="or")
        self.passLabel = ttk.Label(self, text="Password:")
        self.algoLabel = ttk.Label(self, text="Algorithm:")

        # Create input fields
        self.hashEntry = ttk.Entry(self)
        self.passEntry = ttk.Entry(self)

        # Create radio buttons
        self.MD5Radio = ttk.Radiobutton(self, text="MD5", value="md5", variable=self.mAlgo)
        self.SHA1Radio = ttk.Radiobutton(self, text="SHA1", value="sha1", variable=self.mAlgo)
        self.SHA256Radio = ttk.Radiobutton(self, text="SHA256", value="sha256", variable=self.mAlgo)

        # Create continue button
        self.startPageCont = ttk.Button(self, text="continue", command=lambda: self.startPageContClick(controller))

        # Organize widgets using grid layout
        self.headerLabel.grid(row=0, column=1, padx=10, pady=5, sticky=E)
        self.hashLabel.grid(row=1, column=0, padx=10, pady=5, sticky=E)
        self.orLabel.grid(row=2, column=0, padx=10, pady=5, sticky=E)
        self.passLabel.grid(row=3, column=0, padx=10, pady=5, sticky=E)
        self.algoLabel.grid(row=4, column=0, padx=10, pady=5, sticky=E)
        self.hashEntry.grid(row=1, column=1, padx=10, pady=5)
        self.passEntry.grid(row=3, column=1, padx=10, pady=5)
        self.MD5Radio.grid(row=4, column=1, padx=10, pady=5, sticky=E)
        self.SHA1Radio.grid(row=4, column=2, padx=10, pady=5, sticky=E)
        self.SHA256Radio.grid(row=4, column=3, padx=10, pady=5, sticky=E)
        self.startPageCont.grid(row=5,column=1, padx=10, pady=5)

        # self.pack()
    

    def startPageContClick(self, controller):
        global masterHash

        # Validate inputs
        if self.hashEntry.get() != "":
            masterHash = self.hashEntry.get()
            # store and go to next page

        elif self.passEntry.get() != "" and self.mAlgo != "":
            masterHash = bruteforce.hashPasswordWithAlgo(self.passEntry.get(), self.mAlgo.get())
        
        else:
            messagebox.showwarning("Warning", "Please either fill in the hash or fill in the password and select an algorithm.")
            return
        
        print(masterHash)
        controller.show_frame("optionsFrame")


class optionsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.mangle = BooleanVar(self)
        self.file = StringVar(self, "")

        # Create header
        self.headerLabel = ttk.Label(self, text="Cracking Options", font=("Courier", 14))

        # Create labels for inputs
        self.mangeLabel = ttk.Label(self, text="Mangle:")
        self.wordListLabel = ttk.Label(self, text="WordList:")

        # Create entry for inputs
        self.customFileEntry = ttk.Entry(self)

        # Create radio buttons
        self.yesRadio = ttk.Radiobutton(self, text="Yes", value=True, variable=self.mangle)
        self.noRadio = ttk.Radiobutton(self, text="No", value=False, variable=self.mangle)

        # TODO Change to for loop with bruteforce call to print list of files
        self.fasttrackRadio = ttk.Radiobutton(self, text="fasttrack.txt", value="wordlists/fasttrack.txt", variable=self.file)
        self.customFileRadio = ttk.Radiobutton(self, text="Custom (full path):", value=self.customFileEntry.get(), variable=self.file)

        # Create continue button
        self.optionsPageCont = ttk.Button(self, text="start", command=lambda: self.optionsPageContClick(controller))

        # Organize widgets using grid layout
        self.headerLabel.grid(row=0, column=1, padx=10, pady=5, sticky=E)
        self.mangeLabel.grid(row=1, column=0, padx=10, pady=5, sticky=E)
        self.yesRadio.grid(row=1, column=1, padx=10, pady=5, sticky=E)
        self.noRadio.grid(row=1, column=2, padx=10, pady=5, sticky=E)
        self.wordListLabel.grid(row=2, column=0, padx=10, pady=5, sticky=E)
        self.fasttrackRadio.grid(row=3, column=0, padx=10, pady=5, sticky=E)
        self.customFileRadio.grid(row=4, column=0, padx=10, pady=5, sticky=E)
        self.customFileEntry.grid(row=4, column=1, pady=5, sticky=E)
        self.optionsPageCont.grid(row=5, column=1, padx=10, pady=5, sticky=E)

        # self.pack()
    
    
    def optionsPageContClick(self, controller):
        global masterFile, masterMangle

        # TODO test this validation
        try:
            with open(self.file.get(), "r") as f:
                x = f.read()
            masterFile = self.file.get()
            masterMangle = self.mangle.get()
        except Exception as e:
            print("Error reading file")
            messagebox.showwarning("Warning", "No such file")
            return

        controller.show_frame("computeFrame")
        

class computeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        global masterHash, masterFile, masterMangle

        super().__init__(parent)

        # TODO create progress bar

        # Create labels for inputs
        self.progressLabel = ttk.Label(self, text="Progress")
        self.foundLabel = ttk.Label(self, text="Found Password:")
        self.algoLabel = ttk.Label(self, text="Algorithm Used:")

        # algo = bruteforce.determineHashAlgo(masterHash)

        # foundPass = bruteforce.startCrackWithCPU(masterHash, algo, masterFile, masterMangle)

        # Create labels for output
        self.foundOutLabel = ttk.Label(self, text="")

        self.algoOutLabel = ttk.Label(self, text="")

        # Create continue button
        self.computePageCont = ttk.Button(self, text="restart", command=lambda: controller.show_frame("startFrame"))

        # Organize widgets using grid layout
        self.progressLabel.grid(row=0, column=1, padx=10, pady=5, sticky=E)
        self.foundLabel.grid(row=1, column=0, padx=10, pady=5, sticky=E)
        self.foundOutLabel.grid(row=1, column=1, padx=10, pady=5, sticky=E)
        self.algoLabel.grid(row=2, column=0, padx=10, pady=5, sticky=E)
        self.algoOutLabel.grid(row=2, column=1, padx=10, pady=5, sticky=E)
        self.computePageCont.grid(row=3, column=1, padx=10, pady=5, sticky=E)
    

    def update_ui(self, algo, foundPass):
        # metalPipeSound = AudioSegment.from_mp3("sounds\metal_pipe.mp3")
        # play(metalPipeSound)
        playsound('sounds\metal_pipe.mp3')

        self.algoOutLabel.config(text=algo)
        if foundPass is not None:
            self.foundOutLabel.config(text=foundPass)
        else: 
            self.foundOutLabel.config(text="No match found")
    
    
    def reset(self):
        self.algoOutLabel.config(text="")
        self.foundOutLabel.config(text="")


if (__name__ == "__main__"):
    main()

# TODO
# fix computeFrame, have to wait for bruteforce to finish first