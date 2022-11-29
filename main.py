import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import platform
import string

if platform.system() != "Windows":
    messagebox.showerror("OS Error", "This program requires a Windows Operating System to run!")
    exit(1)

import binary_challenge
import morse_challenge
import cipher_challenge


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Setting main window parameters
        self.__height = "700"
        self.__width = "700"

        self.title("Capture-The-Flag")
        self.geometry(self.__width + "x" + self.__height)
        self.resizable(True, True)

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
    
        self.frames = {}

        self.frame = MainWindow(container, self)

        self.frames[MainWindow] = self.frame

        self.show_frame(MainWindow)


    def show_frame(self, cont):
        """shows a frame in self.frames"""
        frame = self.frames[cont]
        frame.tkraise()


class MainWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.__numRow = 2
        self.__numCol  = 3
        self.grid(row=0, column=0)
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=0)

        # Initialise dict of challenge button properties
        # The dictionary has the following structure:
        # {btn_class:{btn_object, label_object, row, column}}
        self.btn_dict = {}

        # Challenge 1: Morse Properties
        self.btn_dict[MorseWin] = {"button":tk.Button(self, text="Morse", command=lambda: self.showWindow(MorseWin))}
        self.btn_dict[MorseWin].update({"status":tk.Label(self, text="Not solved yet...")})
        self.btn_dict[MorseWin].update({"row":1, "column":0, "complete":0})

        # Challenge 2: Cipher Properties
        self.btn_dict[CipherWin] = {"button":tk.Button(self, text="Cipher", command=lambda: self.showWindow(CipherWin))}
        self.btn_dict[CipherWin].update({"status":tk.Label(self, text="Not solved yet...")})
        self.btn_dict[CipherWin].update({"row":1, "column":1, "complete":0})

        # Challenge 3: Binary Properties
        self.btn_dict[BinaryWin] = {"button":tk.Button(self, text="Binary", command=lambda: self.showWindow(BinaryWin))}
        self.btn_dict[BinaryWin].update({"status":tk.Label(self, text="Not solved yet...")})
        self.btn_dict[BinaryWin].update({"row":1, "column":2, "complete":0})

        # Final flag input
        self.final_btn = tk.Button(self, text="Submit final string", state=tk.DISABLED)

        # Place window elements
        print(self.btn_dict)
        for entry in self.btn_dict:
            current_entry = self.btn_dict[entry]
            current_entry["button"].grid(row=current_entry["row"], column=current_entry["column"])
            current_entry["status"].grid(row=current_entry["row"]+1, column=current_entry["column"])
        self.final_btn.grid(row=3, column=0)
    
    def showWindow(self, cont):
        """opens a new window when challenge buttons are clicked on"""
        self.new = cont(self)
    
    def setStatus(self, cont, flag):
        """sets a challenge as complete by:
        -setting "complete" flag in self.btn_dict to 1
        -displaying challenge flag in main page
        """
        self.btn_dict[cont]["status"].configure(text="Flag: {}".format(str(flag)))
        self.btn_dict[cont]["complete"] = 1
        if self.checkAllComplete() == True:
            self.final_btn.configure(state=tk.NORMAL)
    
    def checkAllComplete(self):
        """checks if all challenges are complete"""
        for key in self.btn_dict:
            if self.btn_dict[key]["complete"] == 0:
                return False
        return True


class MorseWin(tk.Toplevel):

    def __init__(self, parent):
        """Creates the GUI window for Challenge 1: Morse"""
        tk.Toplevel.__init__(self, parent)
        # Set flag string to convert to morse code
        self.parent = parent
        self.flag = "Behind"
        self.title("Morse Challenge")

        # Create window elements
        self.desc = ttk.Label(self,\
                                text="Decode the following morse code:")
        self.play_button = ttk.Button(self, width=100,\
                                    text="Click here for morse code",\
                                    command=lambda: morse_challenge.morse_audio(morse_challenge.str_to_morse(self.flag)))
        self.submit_btn = ttk.Button(self, text="Submit",\
                                    command=lambda: self.compare_input())
        self.textbox = tk.Text(self)

        # Place window elements
        self.desc.grid(row=0, column=0)
        self.play_button.grid(row=1, column=0)
        self.textbox.grid(row=2, column=0)
        self.submit_btn.grid(row=3, column=0)
    

    def compare_input(self):
        """Compares input in textbox with the correct input
        Displays whether the input was correct or not in the window itself
        """
        # Get string input from textbox
        text_input = self.textbox.get(1.0, "end-1c")

        # Comparing user-input and correct strings and 
        # displaying whether or not they match
        message_display_row = self.submit_btn.grid_info()["row"]+1
        if text_input == self.flag:
            ttk.Label(self, text="Good job!").grid(row=message_display_row, column=0)
            self.parent.setStatus(MorseWin, self.flag)
        else:
            ttk.Label(self, text="Wrong!").grid(row=message_display_row, column=0)


class CipherWin(tk.Toplevel):
    """"Creates the GUI window for Challenge 2: Cipher"""
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.flag_cipher = "Look"

        # Create window elements
        self.cipher_desc = ttk.Label(self,\
                                text="Decode the following cipher code:")
        #self.play_btn_img = PhotoImage(file="resources/play_button_2.png")
        self.cipher_playButton = ttk.Button(self, width=100,\
                                        text="Click here for cipher code",\
                                    command=lambda: cipher_challenge.caesar(cipher_challenge.plain_text,8,[string.ascii_lowercase,string.ascii_uppercase,string.punctuation]))
        self.submit_btn_cipher = ttk.Button(self, text="Submit",\
                                    command=lambda: self.compare_input())
        self.textbox_cipher = tk.Text(self)

        # Place window elements
        self.cipher_desc.grid(row=0, column=0)
        self.cipher_playButton.grid(row=1, column=0)
        self.textbox_cipher.grid(row=2, column=0)
        self.submit_btn_cipher.grid(row=3, column=0)

    def compare_input(self):
        """Compares input in textbox with the correct input
        Displays whether the input was correct or not in the window itself
        """
        # Get string input from textbox
        text_input = self.textbox_cipher.get(1.0, "end-1c")

        # Comparing user-input and correct strings and 
        # displaying whether or not they match
        message_display_row = self.submit_btn_cipher.grid_info()["row"]+1
        if text_input == self.flag_cipher:
            ttk.Label(self, text="Good job!").grid(row=message_display_row, column=0)
            self.parent.setStatus(CipherWin, self.flag_cipher)
        else:
            ttk.Label(self, text="Wrong!").grid(row=message_display_row, column=0)


class BinaryWin(tk.Toplevel):
    """Creates the GUI window for Challenge 3: Binary"""
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.flag = "You"
        label = tk.Label(self, text="Next Page")
        self.title("hello_bin")
        label.grid(row=0,column=0)
        self.parent.setStatus(BinaryWin, self.flag)


class FinalChallenge(tk.Toplevel):
    """Creates the GUI window to input all flags in order"""
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.flag = "Look Behind You"
        label = tk.Label(self, text="Next Page")
        self.title("hello_final")
        label.grid(row=0,column=0)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()