import tkinter as tk
from tkinter  import filedialog, messagebox
import pdfmerge
from tkinter import ttk


main = tk.Tk()
main.title("Wyz's PDF Merger")
main.iconbitmap('favicon.ico')
main.geometry("300x200")

def choose_folder_button(button, entry):
    '''Opens file dialog and fills out output_folder entry.'''
    folder = filedialog.askdirectory(initialdir = "/", title = "Select output folder")
    entry.delete(0, tk.END)
    entry.insert(0, folder)

def folder_merge():
    '''GUI version of merge in pdf.'''
    
    # try:
    # Prevent use of button while merge takes place.
    # mergefromfolderbutton.configure(state=tk.DISABLED)

    destination, errors = pdfmerge.merge_pdfs_from_folder(input_folder.get(), output_folder.get(), outputfilename.get())
    if not errors:
        messagebox.showinfo("Complete", f"Output file to {destination}.")
    elif errors:
        # error_string = len(errors) * "{:error}\n".format(*errors)
        
        messagebox.showinfo("Complete", f"Output file to {destination}.\n\nYou encountered the following errors:\n\n{errors}")
    # except:
    #     messagebox.showwarning("Error", "Encountered an error.")
    #     raise
    
    # finally:
    #     # Enable button again
    mergefromfolderbutton.configure(state=tk.NORMAL)



# Output folder
output_folder_label = ttk.Label(text="Choose Output Folder:")
output_folder_label.grid(row=0, column=0)
output_folder = ttk.Entry()
output_folder.grid(row=1, column=0)

# Output Button
output_button = ttk.Button(text="Output", command=lambda:choose_folder_button(output_button, output_folder))
output_button.grid(row=1, column=1)

# Output File
output_file_label = ttk.Label(text="Type Output File Name:")
output_file_label.grid(row=2, column=0)
outputfilename = ttk.Entry()
outputfilename.grid(row=3, column=0)


# Input folder
input_folder_label = ttk.Label(text="Choose Input Folder:")
input_folder_label.grid(row=4, column=0)
input_folder = ttk.Entry()
input_folder.grid(row=5, column=0)

# Input Button
input_button = ttk.Button(text="Input", command=lambda:choose_folder_button(input_button, input_folder))
input_button.grid(row=5, column=1)

# Merge all in folder
mergefromfolderbutton = ttk.Button(text="Merge from Input Folder", command=folder_merge)
mergefromfolderbutton.grid(row=6, column=0)





button = tk.Button()

tk.mainloop()