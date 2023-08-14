"""
This file runs the GUI for the program, relying on bruteforce.py for the work

@Author Spencer Kurtz
"""

import bruteforce

import tkinter
from tkinter import StringVar, messagebox, ttk, E, W, BooleanVar, Frame, PhotoImage
from tkinter import messagebox

from threading import Thread

from playsound import playsound


# Global to hold current hash, file location, and mangle flag
masterHash = ""
masterFile = ""
masterMangle = False


def main():
    global frame

    gui = App()

    gui.mainloop()


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Lock Pick Pro")
        self.geometry("500x300")
        self.minsize(200, 200)
        self.maxsize(900, 900)

        photo = PhotoImage(file = 'amogus.png')
        self.wm_iconphoto(False, photo)

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

            self.after(0, lambda: computeFrame.foundPasswordUpdate(algo, found_pass))

        thread = Thread(target=task)
        thread.start()


class startFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        global masterHash

        self.mAlgo = StringVar(self, "")

        # Create header
        self.headerLabel = ttk.Label(self, text="Choose Method", font=("Courier", 14))  

        # Create hash section
        hashContainer = Frame(self)

        self.hashLabel = ttk.Label(hashContainer, text="Hash:")
        self.hashEntry = ttk.Entry(hashContainer)

        self.hashLabel.grid(row=0, column=0, padx=10, sticky=W)
        self.hashEntry.grid(row=0, column=1, padx=30, sticky=E)

        # Create password section
        passwordContainer = Frame(self)

        self.passLabel = ttk.Label(passwordContainer, text="Password:")
        self.passEntry = ttk.Entry(passwordContainer)

        self.passLabel.grid(row=0, column=0, padx=10, sticky=W)
        self.passEntry.grid(row=0, column=1, padx=10, sticky=W)

        # Create or
        self.orLabel = ttk.Label(self, text="or")      

        # Create algo section
        algoContainer = Frame(self)

        self.algoLabel = ttk.Label(algoContainer, text="Algorithm:")

        self.MD5Radio = ttk.Radiobutton(algoContainer, text="MD5", value="md5", variable=self.mAlgo)
        self.SHA1Radio = ttk.Radiobutton(algoContainer, text="SHA1", value="sha1", variable=self.mAlgo)
        self.SHA256Radio = ttk.Radiobutton(algoContainer, text="SHA256", value="sha256", variable=self.mAlgo)

        self.algoLabel.grid(row=0, column=0, padx=10, sticky=W)
        self.MD5Radio.grid(row=0, column=1, padx=10, sticky=W)
        self.SHA1Radio.grid(row=0, column=2, padx=10, sticky=W)
        self.SHA256Radio.grid(row=0, column=3, padx=10, sticky=W)

        # Create continue button
        self.startPageCont = ttk.Button(self, text="continue", command=lambda: self.startPageContClick(controller))

        # Organize widgets using grid layout
        self.headerLabel.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        hashContainer.grid(row=1, column=0, padx=30, pady=5, sticky=W)
        self.orLabel.grid(row=2, column=0, padx=40, pady=5, sticky=W)
        passwordContainer.grid(row=3, column=0, padx=30, pady=5, sticky=W)
        algoContainer.grid(row=4, column=0, padx=30, pady=5, sticky=W)
        self.startPageCont.grid(row=5,column=0, padx=10, pady=15)
    

    def startPageContClick(self, controller):
        global masterHash

        # Validate inputs
        if self.hashEntry.get() != "":
            masterHash = self.hashEntry.get()

        elif self.passEntry.get() != "" and self.mAlgo.get() != "":
            masterHash = bruteforce.hashPasswordWithAlgo(self.passEntry.get(), self.mAlgo.get())
        
        else:
            messagebox.showwarning("Warning", "Please either fill in the hash or fill in the password and select an algorithm.")
            return
        
        controller.show_frame("optionsFrame")


class optionsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.mangle = BooleanVar(self, True)
        self.file = StringVar(self, "wordlists/fasttrack.txt")

        # Create header
        self.headerLabel = ttk.Label(self, text="Cracking Options", font=("Courier", 14))

        # Create mangle radio buttons
        mangleContainer = Frame(self)
        mangeLabel = ttk.Label(mangleContainer, text="Mangle:")
        yesRadio = ttk.Radiobutton(mangleContainer, text="Yes", value=True, variable=self.mangle)
        noRadio = ttk.Radiobutton(mangleContainer, text="No", value=False, variable=self.mangle)

        mangeLabel.grid(row=0, column=0)
        yesRadio.grid(row=1, column=0)
        noRadio.grid(row=2, column=0)

        # Create wordlist radio buttons
        i = 0
        wordListContainer = Frame(self)

        wordListLabel = ttk.Label(wordListContainer, text="Choose a word list:")
        wordListLabel.grid(row=i, column=0, sticky=W)

        files = bruteforce.getWordLists()
        for i in range(len(files)):
            radio = ttk.Radiobutton(wordListContainer, text=files[i], value="wordlists/"+files[i], variable=self.file)
            radio.grid(row=i+1, column=0, sticky=W)
        
        self.customFileEntry = ttk.Entry(wordListContainer)
        self.customFileEntry.grid(row=i+2, column=1, sticky=W)

        customFileRadio = ttk.Radiobutton(wordListContainer, text="Custom (full path):", value="custom", variable=self.file)
        customFileRadio.grid(row=i+2, column=0, sticky=W)

        # Create continue button
        self.optionsPageCont = ttk.Button(self, text="start", command=lambda: self.optionsPageContClick(controller))

        # Organize widgets using grid layout
        self.headerLabel.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        wordListContainer.grid(row=1, column=0, padx=40, pady=5)
        mangleContainer.grid(row=1, column=1, padx=0, pady=5)
        self.optionsPageCont.grid(row=2, column=0, padx=50, pady=15, sticky=W)


    def optionsPageContClick(self, controller):
        global masterFile, masterMangle
        print(self.file.get())
        print(self.customFileEntry.get)

        # TODO test this validation
        try:
            if self.file.get() == "custom":
                if self.customFileEntry.endswith(".txt"):
                    self.file = self.customFileEntry.get()
                    print("e",self.file.get())
                else:
                    messagebox.showwarning("Warning", "Must be a txt file")
                    return
            
            with open(self.file.get(), "r") as f:
                x = f.read()

            masterFile = self.file.get()
            masterMangle = self.mangle.get()
            self.file = ""
            
        except Exception as e:
            messagebox.showwarning("Warning", "Error reading file")
            return

        controller.show_frame("computeFrame")
        

class computeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        global masterHash, masterFile, masterMangle

        super().__init__(parent)

        # TODO create progress bar

        # Create header
        self.headerLabel = ttk.Label(self, text="Cracking Progress", font=("Courier", 14))

        # Create labels for inputs
        self.progressLabel = ttk.Label(self, text="Number Checked:")
        self.foundLabel = ttk.Label(self, text="Found Password:")
        self.algoLabel = ttk.Label(self, text="Algorithm Used:")

        # Create labels for output
        self.progressOutLabel = ttk.Label(self, text="")
        self.foundOutLabel = ttk.Label(self, text="")
        self.algoOutLabel = ttk.Label(self, text="")

        # Create continue button
        self.computePageCont = ttk.Button(self, text="restart", command=lambda: controller.show_frame("startFrame"))

        # Organize widgets using grid layout
        self.headerLabel.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        self.progressLabel.grid(row=1, column=0, padx=30, pady=5, sticky=W)
        self.progressOutLabel.grid(row=1, column=1, padx=30, pady=5, sticky=W)
        self.foundLabel.grid(row=2, column=0, padx=30, pady=5, sticky=W)
        self.foundOutLabel.grid(row=2, column=1, padx=30, pady=5, sticky=W)
        self.algoLabel.grid(row=3, column=0, padx=30, pady=5, sticky=W)
        self.algoOutLabel.grid(row=3, column=1, padx=30, pady=5, sticky=W)
        self.computePageCont.grid(row=4, column=0, padx=10, pady=15)
    

    def foundPasswordUpdate(self, algo, foundPass):
        self.algoOutLabel.config(text=algo)
        if foundPass is not None:
            self.foundOutLabel.config(text=foundPass)
        else: 
            self.foundOutLabel.config(text="No match found")
        
        playsound('sounds/metal_pipe.mp3')
    
    
    def reset(self):
        self.algoOutLabel.config(text="")
        self.foundOutLabel.config(text="")


if (__name__ == "__main__"):
    main()

# TODO validate custom file works
    # TODO fix custom file checking
# TODO get more files
# TODO num counted progress bar
# C:\Users\spenc\Downloads\help.txt
