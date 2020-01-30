import tkinter as tk
from tkinter import filedialog, messagebox
import pdfmerge
from tkinter import ttk

main = tk.Tk()
main.title("Wyz's PDF Merger")
main.iconbitmap('favicon.ico')
main.geometry("300x300")


def choose_folder_button(entry):
    """Opens file dialog and fills out output_folder or input_folder entry."""
    folder = filedialog.askdirectory(initialdir="/", title="Select folder")
    if folder != "":
        entry.delete(0, tk.END)
        entry.insert(0, folder)

def choose_file_button(entry):
    """Opens file dialog and fills out input_file entry."""
    folder = filedialog.askopenfilename(initialdir="/", title="Select files", filetypes=[("PDF file", "*.pdf")])
    if folder != "":
        entry.delete(0, tk.END)
        entry.insert(0, folder)

def choose_files_button(entry):
    """Opens file dialog and fills out multiple file names."""
    folder = filedialog.askopenfilenames(initialdir="/", title="Select file", filetypes=[("PDF file", "*.pdf")])
    if folder != "":
        entry.delete(0, tk.END)
        entry.insert(0, folder)

def folder_merge(output_folder, output_file, input_folder):
    """GUI version of merge_pdfs_from_folder."""
    # Check for required input:
    if output_folder.get() == "":
        messagebox.showerror("Error: No Output Folder specified",
                             '''Choose a folder where your new PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
        return

    if output_file.get() == "":
        messagebox.showerror("Error: No Output File specified", "Type a filename for your merged pdf.")
        return
    if input_folder.get() == "":
        messagebox.showerror("Error: No Input Folder specified", "Choose a folder where all your PDFs are located.")
        return

    try:
        folder_merge_button.configure(state=tk.NORMAL)
        destination, errors = pdfmerge.merge_pdfs_from_folder(input_folder.get(), output_folder.get(), output_file.get())
    except FileNotFoundError:
        messagebox.showerror("Error: File Not Found",
                             f'''File {input_folder.get()} does not exist. Are there backslashes in the address? If so, use the Input or Output button instead of copy pasting a file address directly.''')
        return
    except FileExistsError:
        messagebox.showerror("Error: File Already Exists",
                             f"File already exists. Change the output file name to something else.")
        return
    else:
        if not errors:
            messagebox.showinfo("Complete", f"Output file to {destination}.")
        elif errors:
            # error_string = len(errors) * "{:error}\n".format(*errors)

            messagebox.showinfo("Complete",
                                f"Output file to {destination}.\n\nYou encountered the following errors:\n\n{errors}")
    finally:
        folder_merge_button.configure(state=tk.NORMAL)

def sequence_merge(output_folder, output_file, input_files):
    """GUI version of merge_many_pdfs."""
    # Check for required input:
    
    
    if output_folder.get() == "":
        messagebox.showerror("Error: No Output Folder specified",
                             '''Choose a folder where your new PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
        return

    if output_file.get() == "":
        messagebox.showerror("Error: No Output File specified", "Type a filename for your merged pdf.")
        return
    if input_files.get() == "":
        messagebox.showerror("Error: No Input Files specified", "Choose PDfs to merge.")
        return

    try:
        input_files_list = main.tk.splitlist(input_files.get())
        print(input_files_list)
        destination, errors = pdfmerge.merge_many_pdfs(output_folder.get(), output_file.get(), *input_files_list)
        sequence_merge_button.configure(state=tk.DISABLED)
    except FileNotFoundError:
        messagebox.showerror("Error: File Not Found",
                             f'''Are there backslashes in any address? If so, use the Input button instead of copy pasting a file address directly.''')
    except FileExistsError:
        messagebox.showerror("Error: File Already Exists",
                             f"File already exists. Change the output file name to something else.")
    else:
        if not errors:
            messagebox.showinfo("Complete", f"Output file to {destination}.")
        elif errors:
            # error_string = len(errors) * "{:error}\n".format(*errors)

            messagebox.showinfo("Complete",
                                f"Output file to {destination}.\n\nYou encountered the following errors:\n\n{errors}")
    finally:
        sequence_merge_button.configure(state=tk.NORMAL)

    

# Create a notebook
nb = ttk.Notebook(main)
nb.grid(row=0, column=0, columnspan=50, sticky='NESW')
nb.rowconfigure(0, weight=1)
nb.columnconfigure(0, weight=1)

# TAB 1: Merge All PDFs in Folder #####################################
# "f" added to the end of variables here to represent folder.
folder_merge_tab = ttk.Frame(nb)
nb.add(folder_merge_tab, text='Merge PDFs in Folder')

# Output folder
output_folder_label_f = ttk.Label(folder_merge_tab, text="Choose Output Folder:")
output_folder_label_f.grid(row=0, column=0)
output_folder_f = ttk.Entry(folder_merge_tab)
output_folder_f.grid(row=1, column=0)

# Output Button
output_button_f = ttk.Button(folder_merge_tab, text="Output", command=lambda: choose_folder_button(output_folder_f))
output_button_f.grid(row=1, column=1)

# Output File
output_file_label_f = ttk.Label(folder_merge_tab, text="Type Output File Name:")
output_file_label_f.grid(row=2, column=0)
output_file_f = ttk.Entry(folder_merge_tab)
output_file_f.grid(row=3, column=0)

# Input folder
input_folder_label_f = ttk.Label(folder_merge_tab, text="Choose Input Folder:")
input_folder_label_f.grid(row=4, column=0)
input_folder_f = ttk.Entry(folder_merge_tab)
input_folder_f.grid(row=5, column=0)

# Input Button
input_button_f = ttk.Button(folder_merge_tab, text="Input", command=lambda: choose_folder_button(input_folder_f))
input_button_f.grid(row=5, column=1)

# Merge all in folder
folder_merge_button = ttk.Button(folder_merge_tab, text="Merge from Input Folder",
                                      command=lambda: folder_merge(output_folder_f, output_file_f, input_folder_f))
folder_merge_button.grid(row=6, column=0, padx=(10, 0), pady=10)

# TAB 2: Merge All PDFs in Sequence #####################################
# "s" added to the end of variables here to represent sequence.
seq_merge_tab = ttk.Frame(nb)
nb.add(seq_merge_tab, text='Merge PDFs in Sequence')

# Output folder
output_folder_label_s = ttk.Label(seq_merge_tab, text="Choose Output Folder:")
output_folder_label_s.grid(row=0, column=0)
output_folder_s = ttk.Entry(seq_merge_tab)
output_folder_s.grid(row=1, column=0)

# Output Button
output_button_s = ttk.Button(seq_merge_tab, text="Output", command=lambda: choose_folder_button(output_folder_s))
output_button_s.grid(row=1, column=1)

# Output File
output_file_label_s = ttk.Label(seq_merge_tab, text="Type Output File Name:")
output_file_label_s.grid(row=2, column=0)
output_file_s = ttk.Entry(seq_merge_tab)
output_file_s.grid(row=3, column=0)

# Input files
input_files_label_s = ttk.Label(seq_merge_tab, text="Choose Input File(s):")
input_files_label_s.grid(row=4, column=0)
input_files_s = ttk.Entry(seq_merge_tab)
input_files_s.grid(row=5, column=0)

# Input Button
input_button_s = ttk.Button(seq_merge_tab, text="Input", command=lambda: choose_files_button(input_files_s))
input_button_s.grid(row=5, column=1)

# Merge all in sequence
sequence_merge_button = ttk.Button(seq_merge_tab, text="Merge from Input Files", command=lambda: sequence_merge(output_folder_s, output_file_s, input_files_s))
sequence_merge_button.grid(row=6, column=0, padx=(10, 0), pady=10)





# MAIN LOOP

tk.mainloop()
