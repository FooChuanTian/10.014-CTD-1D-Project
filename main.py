import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import platform

if platform.system() != "Windows":
    messagebox.showerror("OS Error",\
        "This program requires a Windows Operating System to run!")
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
        self.btn_dict[MorseWin] = {"button":tk.Button(self, text="Morse",\
                                command=lambda: self.showWindow(MorseWin))}
        self.btn_dict[MorseWin].update({"status":tk.Label(self, \
                                        text="Not solved yet...")})
        self.btn_dict[MorseWin].update({"row":1, "column":0, "complete":0})

        # Challenge 2: Cipher Properties
        self.btn_dict[CipherWin] = {"button":tk.Button(self, text="Cipher",\
                                command=lambda: self.showWindow(CipherWin))}
        self.btn_dict[CipherWin].update({"status":tk.Label(self,\
                                        text="Not solved yet...")})
        self.btn_dict[CipherWin].update({"row":1, "column":1, "complete":0})

        # Challenge 3: Binary Properties
        self.btn_dict[BinaryWin] = {"button":tk.Button(self, text="Binary", \
                                command=lambda: self.showWindow(BinaryWin))}
        self.btn_dict[BinaryWin].update({"status":tk.Label(self,\
                                        text="Not solved yet...")})
        self.btn_dict[BinaryWin].update({"row":1, "column":2,\
                                        "complete":0})

        # Final flag input
        self.final_btn = tk.Button(self, text="Submit final string",\
                                state=tk.DISABLED,\
                                command=lambda: \
                                    self.showWindow(FinalChallenge))

        # Place window elements
        print(self.btn_dict)
        for entry in self.btn_dict:
            current_entry = self.btn_dict[entry]
            current_entry["button"].grid(row=current_entry["row"],\
                                        column=current_entry["column"])
            current_entry["status"].grid(row=current_entry["row"]+1,\
                                        column=current_entry["column"])
        self.final_btn.grid(row=3, column=0, columnspan=len(self.btn_dict))
    
    def showWindow(self, cont):
        """opens a new window when challenge buttons are clicked on"""
        self.new = cont(self)
    
    def setStatus(self, cont, flag):
        """sets a challenge as complete by:
        -setting "complete" flag in self.btn_dict to 1
        -displaying challenge flag in main page
        """
        self.btn_dict[cont]["status"].configure(text="Flag: {}"\
                                            .format(str(flag)))
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
                                    command=lambda: morse_challenge.\
                                        morse_audio(morse_challenge.\
                                                    str_to_morse(self.flag)))
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
        if text_input.lower() == self.flag.lower():
            ttk.Label(self, text="Good job!").grid(row=message_display_row,\
                                                    column=0)
            self.parent.setStatus(MorseWin, self.flag)
        else:
            ttk.Label(self, text="Wrong!").grid(row=message_display_row, \
                                                column=0)


class CipherWin(tk.Toplevel):
    """"Creates the GUI window for Challenge 2: Cipher"""
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.flag = "Look"
        label = tk.Label(self, text="Next Page")
        self.title("hello_cipher")
        label.grid(row=0,column=0)
        self.parent.setStatus(CipherWin, self.flag)


class BinaryWin(tk.Toplevel):
    """Creates the GUI window for Challenge 3: Binary"""
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.flag = "You"
        self.title("Binary Challenge")

        s = ttk.Style()
        s.configure('colour.TFrame', background ="red")
        s.configure('colour_1.TFrame', background ="blue")

        #Create Frames
        self.frame_1 = ttk.Frame(self)
        self.frame_2 = ttk.Frame(self)
        self.frame_3 = ttk.Frame(self)
        self.frame_4 = ttk.Frame(self)

        #Place frames in window
        self.frame_1.grid(row=0, columnspan=2,padx=10, pady = 10)
        self.frame_2.grid(row=1, columnspan=2,padx= 10,pady =10)
        self.frame_3.grid(rowspan=3, column=0)
        self.frame_4.grid(row=2, column=1)


        #Create window elements
        self.desc = ttk.Label(self.frame_1,\
                    text="Convert The Following Binary Code:")
        self.desc.configure(font=('Comic Sans', 20))

        self.display_button = ttk.Button(self.frame_2, width=200,\
                        text="Click here to display binary code",\
                        command=lambda:[self.display_button.grid_forget(),self.display_binary_code()])

        self.ascii_table_Desc = tk.Label(self.frame_3, text='Ascii Table')
        self.photo_path = 'resources/binary_table.png'
        self.photo = tk.PhotoImage(file=self.photo_path)
        self.ascii_Table = tk.Label(self.frame_3,image=self.photo)
        

        self.textbox_Desc = tk.Label(self.frame_4, text='Enter your answer here:')
        self.textbox = tk.Text(self.frame_4)
       
        self.submit_btn = ttk.Button(self.frame_4, text="Submit",\
                        command=lambda: self.compare_input())

        # Place window elements in frames
        self.desc.grid(column = 0,columnspan=3, row= 0)
        self.display_button.grid(column =0, columnspan=3, row = 1)
        self.ascii_table_Desc.pack(side='top')
        self.ascii_Table.pack()
        self.textbox_Desc.grid(row=0)
        self.textbox.grid(row=1)
        self.submit_btn.grid(row=2)
        

    def display_binary_code(self):
        self.label_1 = ttk.Label(self,text="01011001 01101111 01110101")
        self.label_1.configure(anchor='center',font=('Comic Sans',20))
        self.label_1.grid(row =1,columnspan=2,padx=10,pady=10,sticky="EW")
        

    def compare_input(self):
        """Compares input in textbox with the correct input
        Displays whether the input was correct or not in the window itself
        """
        # Get string input from textbox
        text_input = self.textbox.get(1.0, "end-1c")
        # To make sure only the first letter of word input is uppercase to account for "You" being spelled in different case
        cleaned_text = (text_input.lower()).capitalize()

        # Comparing user-input and correct strings and 
        # displaying whether or not they match
        if cleaned_text == self.flag:
            ttk.Label(self.frame_4, text="Good job!").grid(row=3)
            

            self.parent.setStatus(BinaryWin, self.flag)
        else:
            ttk.Label(self.frame_4, text="Wrong!").grid(row=3)


class FinalChallenge(tk.Toplevel):
    """Creates the GUI window to input all flags in order"""

    def __init__(self, parent):
        # Setting program parameters
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("One last thing...")
        self.flag = "Look Behind You"

        # Creating window elements
        self.desc = tk.Label(self, text="Congratulations on completing all \
                            challenges! However, one final puzzle awaits...\
                            \nRearrange the flags in the right order")
        self.desc.grid(row=0, column=0, columnspan=3)

        self.btn_dict = {}
        self.switch_ls = []
        self.current_order = []
        self.cls_ls = list(self.parent.btn_dict.keys())

        k=0
        for key in self.parent.btn_dict:
            current_entry = self.parent.btn_dict[key]
            current_flag = current_entry["status"].cget("text").replace("Flag: ", "")
            self.btn_dict[key] = tk.Button(self, text=current_flag)
            self.btn_dict[key].grid(row=1, column=k)
            k += 1
        
        self.btn_dict[MorseWin].configure(command=lambda: self.switch_btn(MorseWin))
        self.btn_dict[BinaryWin].configure(command=lambda: self.switch_btn(BinaryWin))
        self.btn_dict[CipherWin].configure(command=lambda: self.switch_btn(CipherWin))

        self.submit_button = tk.Button(self, text="Submit", command=self.verify)
        self.submit_button.grid(row=2, column=0, columnspan=3)
    
    def switch_btn(self, btn_key):
        """switches the 2 buttons present in self.switch_ls
        only switches if there are 2 buttons present in self.switch_ls
        clears self.switch_ls after switching
        """
        self.switch_ls.append(self.btn_dict[btn_key])
        if len(self.switch_ls) == 2:
            coord_1 = self.switch_ls[0].grid_info()
            coord_2 = self.switch_ls[1].grid_info()
            self.switch_ls[0].grid(row=coord_2["row"],\
                                column=coord_2["column"])
            self.switch_ls[1].grid(row=coord_1["row"],\
                                column=coord_1["column"])
            self.switch_ls = []

    def verify(self):
        """verifies that buttons are in right order"""
        in_order_dict = {}
        for key in self.btn_dict:
            in_order_dict.update({self.btn_dict[key].grid_info()["column"]:\
                                    self.btn_dict[key].cget("text")})
        
        compare_string_ls = []
        for i in range(len(in_order_dict)):
            compare_string_ls.append(in_order_dict[i])
        
        message_display_row = self.submit_button.grid_info()["row"] + 1
        
        if " ".join(compare_string_ls) == self.flag:
            ttk.Label(self, text="Good job!").grid(row=message_display_row,\
                    column=0, columnspan=len(self.btn_dict))
        else:
            ttk.Label(self, text="Wrong!").grid(row=message_display_row,\
                    column=0, columnspan=len(self.btn_dict))
        

def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()