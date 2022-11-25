import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import platform

if platform.system() != "Windows":
    messagebox.showerror("OS Error", "This program requires a Windows Operating System to run!")
    exit(1)

import binary_challenge
import morse_challenge
import cipher_challenge


class MainWindow:
    def __init__(self, master):
        self.master = master

        # Setting main window parameters
        self.__height = "700"
        self.__width = "700"
        self.__numRow = 2
        self.__numCol  = 3

        self.master.title("Capture-The-Flag")
        self.master.geometry(self.__width + "x" + self.__height)
        self.master.resizable(True, True)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.frame = ttk.Frame(self.master)
        self.frame.grid(row=0, column=0)
        self.frame.rowconfigure(self.__numRow, weight=1)
        self.frame.columnconfigure(self.__numCol, weight=1)

        # Initialise list of challenge button properties
        # Each entry in list is a dictionary with keys 
        # {"name", "row", "column", "function"}
        self.btnls = []

        # Challenge 1: Morse Properties
        self.btnls.append({"name":"Morse", "row":1, "column":0,\
                           "func":self.morse_win})

        # Challenge 2: Cipher Properties
        self.btnls.append({"name":"Substitution Cipher", "row":1, "column":1,\
                           "func":cipher_challenge.test})

        # Challenge 3: Binary Properties
        self.btnls.append({"name":"Binary", "row":1, "column":2,\
                           "func":binary_challenge.test})

        # Create buttons and add them to dictionaries in btnls
        for entry in self.btnls:
            entry.update({"btn":ttk.Button(self.frame, text=entry["name"],\
                        command=entry["func"])})
            entry.update({"label":ttk.Label(self.frame,\
                        text="Not solved yet...")})

            entry["btn"].grid(row=entry["row"], column=entry["column"],\
                            sticky="news", padx=1, pady=1)
            entry["label"].grid(row=entry["row"] + 1, column=entry["column"],\
                            sticky="news", padx=1, pady=1)
    
    
    def morse_win(self):
        """Creates the GUI window for Challenge 1: Morse"""

        # Set flag string to convert to morse code
        self.flag_morse = "Behind"

        # Create window elements
        self.morse_top = tk.Toplevel(self.frame)
        self.morse_desc = ttk.Label(self.morse_top,\
                                text="Decode the following morse code:")
        #self.play_btn_img = PhotoImage(file="resources/play_button_2.png")
        self.morse_playButton = ttk.Button(self.morse_top, width=100,\
                                        text="Click here for morse code",\
                                    command=lambda: morse_challenge.morse_audio(morse_challenge.str_to_morse(self.flag_morse)))
        self.submit_btn_morse = ttk.Button(self.morse_top, text="Submit",\
                                    command=lambda: self.compare_input(self.flag_morse, self.textbox_morse, 0, self.morse_top, self.submit_btn_morse))
        self.textbox_morse = tk.Text(self.morse_top)

        # Place window elements
        self.morse_desc.grid(row=0, column=0)
        self.morse_playButton.grid(row=1, column=0)
        self.textbox_morse.grid(row=2, column=0)
        self.submit_btn_morse.grid(row=3, column=0)
    
    
    def test_win(self):
        self.test_top = tk.Toplevel(self.frame)
        self.sampleQuestion = ttk.Label(self.test_top, text="Type 'Hello World!' to solve this test question!")
        self.submit_btn_test = ttk.Button(self.test_top, text="click here!",\
                                      command=lambda: self.compare_input("Hello World!", self.textbox_test, None, self.test_top, self.submit_btn_test))
        self.textbox_test = tk.Text(self.test_top)

        self.sampleQuestion.grid(row=0, column=0)
        self.textbox_test.grid(row=1, column=0)
        self.submit_btn_test.grid(row=2, column=0)
    
    def new_window(self, win_type):
        self.newWindow = tk.Toplevel(self.master)
        self.app = win_type(self.newWindow)
    
    
    def compare_input(self, correct_in, textbox, index, top, submit_btn):
        """Compares input in textbox with the correct input
        Displays whether the input was correct or not in the window itself
        """
        # Get string input from textbox
        text_input = textbox.get(1.0, "end-1c")

        # Comparing user-input and correct strings and 
        # displaying whether or not they match
        message_display_row = submit_btn.grid_info()["row"]+1
        if text_input == correct_in:
            ttk.Label(top, text="Good job!").grid(row=message_display_row, column=0)
            self.solved_flag(index, correct_in)
        else:
            ttk.Label(top, text="Nope!").grid(row=message_display_row, column=0)

    
    def solved_flag(self, btn, flag):
        """If a challenge is solved, show flag in main window"""
        self.btnls[btn]["label"] = ttk.Label(self.frame, text="Flag: {}".format(flag))
        self.btnls[btn]["label"].grid(row=self.btnls[btn]["row"] + 1,\
                                    column=self.btnls[btn]["column"], sticky="news", padx=1, pady=1)


class morse_app:
    def __init__(self, master):

        self.master = master
        self.frame = tk.Frame(self.master)

        # Setting main window parameters
        self.__height = "700"
        self.__width = "700"
        self.__numRow = 2
        self.__numCol  = 3

        self.frame = ttk.Frame(self.master)
        self.frame.rowconfigure(self.__numRow, weight=1)
        self.frame.columnconfigure(self.__numCol, weight=1)

        self.flag_morse = "Behind"

        # Create window elements
        self.morse_desc = ttk.Label(self.frame,\
                                text="Decode the following morse code:")
        #self.play_btn_img = PhotoImage(file="resources/play_button_2.png")
        self.morse_playButton = ttk.Button(self.frame, width=100,\
                                        text="Click here for morse code",\
                                    command=lambda: morse_challenge.morse_audio(morse_challenge.str_to_morse(self.flag_morse)))
        self.submit_btn_morse = ttk.Button(self.frame, text="Submit",\
                                    command=lambda: self.compare_input(self.flag_morse, self.textbox_morse, 0, self, self.submit_btn_morse))
        self.textbox_morse = tk.Text(self.frame)

        # Place window elements
        self.morse_desc.grid(row=0, column=0)
        self.morse_playButton.grid(row=1, column=0)
        self.textbox_morse.grid(row=2, column=0)
        self.submit_btn_morse.grid(row=3, column=0)
        self.frame.grid(row=0, column=0)
    

    def compare_input(self, correct_in, textbox, index, top, submit_btn):
        """Compares input in textbox with the correct input
        Displays whether the input was correct or not in the window itself
        """
        # Get string input from textbox
        text_input = textbox.get(1.0, "end-1c")

        # Comparing user-input and correct strings and 
        # displaying whether or not they match
        message_display_row = submit_btn.grid_info()["row"]+1
        if text_input == correct_in:
            ttk.Label(top, text="Good job!").grid(row=message_display_row, column=0)
            self.master.solved_flag(index, correct_in)
        else:
            ttk.Label(top, text="Nope!").grid(row=message_display_row, column=0)


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()