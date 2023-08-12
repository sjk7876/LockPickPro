"""
This file runs the GUI for the program, relying on bruteforce.py for the work

@Author Spencer Kurtz
"""

import bruteforce

from tkinter import *

"""
TODO
metal pipe falling sound
nyan cat loading bar ?

min size
max size

GENERATE EXE
"""

frame = ""

def main():
    global frame

    gui = Tk()
    gui.title("Lock Pick Pro")
    gui.geometry("400x300")

    frame = startPage(gui)
    frame.pack()

    gui.mainloop()


def startPage(gui):
    print("start")

    frame = Frame(gui)

    #DEE6F2
    #EBF0F7

    # Create header
    headerLabel = Label(frame, text="Choose Method", font=("Courier", 14))

    # Create labels for inputs
    hashLabel = Label(frame, text="Hash:")
    orLabel = Label(frame, text="or")
    passLabel = Label(frame, text="Password:")
    algoLabel = Label(frame, text="Algorithm:")

    # Create input fields
    hashEntry = Entry(frame, bg='#DEE6F2')
    passEntry = Entry(frame, bg='#DEE6F2')
    algoEntry = Entry(frame, bg='#DEE6F2')

    # Create continue button
    startPageCont = Button(frame, text="continue")

    # Organize widgets using grid layout
    headerLabel.grid(row=0, column=1, padx=10, pady=5, sticky=E)
    hashLabel.grid(row=1, column=0, padx=10, pady=5, sticky=E)
    orLabel.grid(row=2, column=0, padx=10, pady=5, sticky=E)
    passLabel.grid(row=3, column=0, padx=10, pady=5, sticky=E)
    algoLabel.grid(row=4, column=0, padx=10, pady=5, sticky=E)
    hashEntry.grid(row=1, column=1, padx=10, pady=5)
    passEntry.grid(row=3, column=1, padx=10, pady=5)
    algoEntry.grid(row=4, column=1, padx=10, pady=5)
    startPageCont.grid(row=5,column=1, padx=10, pady=5)

    return frame


    


if (__name__ == "__main__"):
    main()

"""
def on_button_click():
    input1_value = entry1.get()
    input2_value = entry2.get()
    input3_value = entry3.get()
    
    entry1.destroy()
    entry2.destroy()
    entry3.destroy()
    label1.destroy()
    label2.destroy()
    label3.destroy()
    button.destroy()
    
    result_label.config(text=f"Input 1: {input1_value}\nInput 2: {input2_value}\nInput 3: {input3_value}")
    
    radio_var = tk.StringVar(root, "Option 1")
    
    def on_radio_change():
        selected_option = radio_var.get()
        selected_label.config(text=f"Selected Option: {selected_option}")
    
    radio1 = tk.Radiobutton(root, text="Option 1", variable=radio_var, value="Option 1", command=on_radio_change)
    radio2 = tk.Radiobutton(root, text="Option 2", variable=radio_var, value="Option 2", command=on_radio_change)
    
    input_new = tk.Entry(root)
    submit_new = tk.Button(root, text="Submit", command=lambda: print(f"Entered Value: {input_new.get()}"))
    selected_label = tk.Label(root, text="Selected Option: ")
    
    radio1.grid(row=0, column=0, padx=10, pady=5)
    radio2.grid(row=1, column=0, padx=10, pady=5)
    input_new.grid(row=2, column=0, padx=10, pady=5)
    submit_new.grid(row=3, column=0, padx=10, pady=10)
    selected_label.grid(row=4, column=0, padx=10, pady=5)

# Create the main window
root = tk.Tk()
root.title("Input Program")

# Create labels for inputs
label1 = tk.Label(root, text="Input 1:")
label2 = tk.Label(root, text="Input 2:")
label3 = tk.Label(root, text="Input 3:")

# Create input fields
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
entry3 = tk.Entry(root)

# Create a button
button = tk.Button(root, text="Submit", command=on_button_click)

# Create a label to display results
result_label = tk.Label(root, text="Results will appear here.")

# Organize widgets using grid layout
label1.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
label2.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
label3.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
entry1.grid(row=0, column=1, padx=10, pady=5)
entry2.grid(row=1, column=1, padx=10, pady=5)
entry3.grid(row=2, column=1, padx=10, pady=5)
button.grid(row=3, columnspan=2, padx=10, pady=10)
result_label.grid(row=4, columnspan=2, padx=10, pady=5)

# Start the Tkinter event loop
root.mainloop()
"""