"""
GUI Tool to handle PDFs.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import pdfmerge
from tkinter import ttk
import pdffromlinks
import pdfcompile

main = tk.Tk()
main.title("Wyz's PDF Utility")
main.iconbitmap('favicon.ico')
# main.geometry("300x300")

main.rowconfigure(0, weight=1)
main.columnconfigure(0, weight=1)

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
                             '''Choose a folder where your nW PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
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

def two_merge(output_folder, output_file, input_file1, input_file2):
    """GUI version of merge_many_pdfs."""
    # Check for required input:
    
    
    if output_folder.get() == "":
        messagebox.showerror("Error: No Output Folder specified",
                             '''Choose a folder where your nW PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
        return

    if output_file.get() == "":
        messagebox.showerror("Error: No Output File specified", "Type a filename for your merged pdf.")
        return
    if input_file1.get() == "":
        messagebox.showerror("Error: Input File 1 not specified", "Choose a PDF to merge.")
        return

    if input_file2.get() == "":
        messagebox.showerror("Error: Input File 2 not specified", "Choose a PDF to merge.")
        return

    try:
        two_merge_button.configure(state=tk.DISABLED)
        destination, errors = pdfmerge.merge_two_pdfs(input_file1.get(), input_file2.get(), output_folder.get(), output_file.get())
        
    except FileNotFoundError:
        messagebox.showerror("Error: File Not Found",
                             f'''Are there backslashes in any address? If so, use the Input button instead of copy pasting a file address directly.''')
    except FileExistsError:
        messagebox.showerror("Error: File Already Exists",
                             f"File already exists. Change the output file name to something else.")
    except OSError:
        messagebox.showerror("Error: OSError", f"OSError: One or both of the PDF input files might be corrupted.")
    else:
        if not errors:
            messagebox.showinfo("Complete", f"Output file to {destination}.")
        elif errors:
            # error_string = len(errors) * "{:error}\n".format(*errors)

            messagebox.showinfo("Complete",
                                f"Output file to {destination}.\n\nYou encountered the following errors:\n\n{errors}")
    finally:
        two_merge_button.configure(state=tk.NORMAL)


def sequence_merge(output_folder, output_file, input_files):
    """GUI version of merge_many_pdfs."""
    # Check for required input:
    
    
    if output_folder.get() == "":
        messagebox.showerror("Error: No Output Folder specified",
                             '''Choose a folder where your nW PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
        return

    if output_file.get() == "":
        messagebox.showerror("Error: No Output File specified", "Type a filename for your merged pdf.")
        return
    if input_files.get() == "":
        messagebox.showerror("Error: No Input Files specified", "Choose PDFs to merge.")
        return

    try:
        sequence_merge_button.configure(state=tk.DISABLED)
        input_files_list = main.tk.splitlist(input_files.get())
        print(input_files_list)
        destination, errors = pdfmerge.merge_many_pdfs(output_folder.get(), output_file.get(), *input_files_list)
    
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

def reorder_one(output_folder, output_file, input_file, page_no):
    """GUI version of merge_many_pdfs."""
    # Check for required input:
    
    
    if output_folder.get() == "":
        messagebox.showerror("Error: No Output Folder specified",
                             '''Choose a folder where your nW PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
        return

    if output_file.get() == "":
        messagebox.showerror("Error: No Output File specified", "Type a filename for your rearranged PDF.")
        return
    if input_file.get() == "":
        messagebox.showerror("Error: No Input Files specified", "Choose a PDF to rearrange.")
        return

    if page_no.get() == "":
        messagebox.showerror("Error: No Page/Page Range specified", "Choose pages to be kept or reordered. Separate the pages and page ranges with commas. For example, '1,2,4,5-10,3,4'. Writing a range backwards like '10-8' will give you the pages in reverse (10, 9, 8).")
        return

    try:
        reorder_button.configure(state=tk.DISABLED)
        input_file = input_file.get()
        page_list = pdfcompile.make_list_of_pages_from_string(page_no.get())
        
        destination = pdfcompile.rearrange_pdf(input_file, page_list, output_folder.get(), output_file.get())
    
    except FileNotFoundError:
        messagebox.showerror("Error: File Not Found",
                             f'''Are there backslashes in any address? If so, use the Input button instead of copy pasting a file address directly.''')
    
    except FileExistsError:
        messagebox.showerror("Error: File Already Exists",
                             f"File already exists. Change the output file name to something else.")
    except TypeError as e:
        messagebox.showerror("Error: TypeError", str(e))
    except IndexError as e:
        messagebox.showerror("Error: Index Error", "The document does not have the pages you specified. Check the page ranges you have typed.")
    else:
        messagebox.showinfo("Complete", f"Output pages {page_list} of input file {input_file} to {destination}.")
        
    finally:
        reorder_button.configure(state=tk.NORMAL)

# Create an overarching notebook. This will contain nested tabs.
nb = ttk.Notebook(main)
nb.grid(row=0, column=0, columnspan=50, sticky='NESW')
nb.rowconfigure(0, weight=1)
nb.columnconfigure(0, weight=1)


# NB TAB 1: Merging Tab ############################################
merge_frame = ttk.Frame(nb)
nb.add(merge_frame, text='Merge', sticky='EW')

# Nested Notebook within Merging Tab for all merging functions
merge_tab = ttk.Notebook(merge_frame)
merge_tab.grid(row=0, column=0, columnspan=50, sticky='NESW')
merge_tab.rowconfigure(0, weight=1)
merge_tab.columnconfigure(0, weight=1)


# MERGE_TAB 1: Merge 2 PDFs in Sequence #####################################
# "two" added to the end of variables here to represent 2 PDFs.

# TODO: Right now, without workarounds, this is not very useful. It can also only merge files within the same folder. 
two_merge_tab = ttk.Frame(merge_tab)
merge_tab.add(two_merge_tab, text='Merge 2 PDFs', sticky='EW')
# Output folder
output_folder_label_two = ttk.Label(two_merge_tab, text="Choose Output Folder:")
output_folder_label_two.grid(row=0, column=0, sticky='EW')
output_folder_two = ttk.Entry(two_merge_tab)
output_folder_two.grid(row=1, column=0, sticky='EW')

# Output Button
output_button_two = ttk.Button(two_merge_tab, text="Output", command=lambda: choose_folder_button(output_folder_two))
output_button_two.grid(row=1, column=1, sticky='EW')

# Output File
output_file_label_two = ttk.Label(two_merge_tab, text="Type Output File Name:")
output_file_label_two.grid(row=2, column=0, sticky='EW')
output_file_two = ttk.Entry(two_merge_tab)
output_file_two.grid(row=3, column=0, sticky='EW')

# Input file 1
input_file1_label_two = ttk.Label(two_merge_tab, text="Choose Input File 1:")
input_file1_label_two.grid(row=4, column=0, sticky='EW')
input_file1_two = ttk.Entry(two_merge_tab)
input_file1_two.grid(row=5, column=0, sticky='EW')

# Input Button 1
input_file1_button_two = ttk.Button(two_merge_tab, text="Input 1", command=lambda: choose_file_button(input_file1_two))
input_file1_button_two.grid(row=5, column=1, sticky='EW')

# Input file 2
input_file2_label_two = ttk.Label(two_merge_tab, text="Choose Input File 2:")
input_file2_label_two.grid(row=6, column=0, sticky='EW')
input_file2_two = ttk.Entry(two_merge_tab)
input_file2_two.grid(row=7, column=0, sticky='EW')

# Input Button 2
input_file2_button_two = ttk.Button(two_merge_tab, text="Input 2", command=lambda: choose_file_button(input_file2_two))
input_file2_button_two.grid(row=7, column=1, sticky='EW')

# Merge two in sequence
two_merge_button = ttk.Button(two_merge_tab, text="Merge 2 Input Files", command=lambda: two_merge(output_folder_two, output_file_two, input_file1_two, input_file2_two))
two_merge_button.grid(row=8, column=0, padx=(0,10), pady=10, sticky='EW')

# MERGE_TAB 2: Merge All PDFs in Folder #####################################
# "f" added to the end of variables here to represent folder.
folder_merge_tab = ttk.Frame(merge_tab)
merge_tab.add(folder_merge_tab, text='Merge PDFs in Folder')

# Output folder
output_folder_label_f = ttk.Label(folder_merge_tab, text="Choose Output Folder:")
output_folder_label_f.grid(row=0, column=0, sticky='EW')
output_folder_f = ttk.Entry(folder_merge_tab)
output_folder_f.grid(row=1, column=0, sticky='EW')

# Output Button
output_button_f = ttk.Button(folder_merge_tab, text="Output", command=lambda: choose_folder_button(output_folder_f))
output_button_f.grid(row=1, column=1, sticky='EW')

# Output File
output_file_label_f = ttk.Label(folder_merge_tab, text="Type Output File Name:")
output_file_label_f.grid(row=2, column=0, sticky='EW')
output_file_f = ttk.Entry(folder_merge_tab)
output_file_f.grid(row=3, column=0, sticky='EW')

# Input folder
input_folder_label_f = ttk.Label(folder_merge_tab, text="Choose Input Folder:")
input_folder_label_f.grid(row=4, column=0, sticky='EW')
input_folder_f = ttk.Entry(folder_merge_tab)
input_folder_f.grid(row=5, column=0, sticky='EW')

# Input Button
input_button_f = ttk.Button(folder_merge_tab, text="Input", command=lambda: choose_folder_button(input_folder_f))
input_button_f.grid(row=5, column=1, sticky='EW')

# Merge all in folder
folder_merge_button = ttk.Button(folder_merge_tab, text="Merge Input Folder",
                                      command=lambda: folder_merge(output_folder_f, output_file_f, input_folder_f))
folder_merge_button.grid(row=6, column=0, padx=(0,10), pady=10, sticky='EW')

# MERGE_TAB 3: Merge All PDFs in Sequence #####################################
# "s" added to the end of variables here to represent sequence.

# TODO: Right now, without workarounds, this is not very useful. It can also only merge files within the same folder. 
seq_merge_tab = ttk.Frame(merge_tab)
merge_tab.add(seq_merge_tab, text='Merge Many PDFs')

# Output folder
output_folder_label_s = ttk.Label(seq_merge_tab, text="Choose Output Folder:")
output_folder_label_s.grid(row=0, column=0, sticky='EW')
output_folder_s = ttk.Entry(seq_merge_tab)
output_folder_s.grid(row=1, column=0, sticky='EW')

# Output Button
output_button_s = ttk.Button(seq_merge_tab, text="Output", command=lambda: choose_folder_button(output_folder_s))
output_button_s.grid(row=1, column=1, sticky='EW')

# Output File
output_file_label_s = ttk.Label(seq_merge_tab, text="Type Output File Name:")
output_file_label_s.grid(row=2, column=0, sticky='EW')
output_file_s = ttk.Entry(seq_merge_tab)
output_file_s.grid(row=3, column=0, sticky='EW')

# Input files
input_files_label_s = ttk.Label(seq_merge_tab, text="Choose Input File(s):")
input_files_label_s.grid(row=4, column=0, sticky='EW')
input_files_s = ttk.Entry(seq_merge_tab)
input_files_s.grid(row=5, column=0, sticky='EW')

# Input Button
input_button_s = ttk.Button(seq_merge_tab, text="Input", command=lambda: choose_files_button(input_files_s))
input_button_s.grid(row=5, column=1, sticky='EW')

# Merge all in sequence
sequence_merge_button = ttk.Button(seq_merge_tab, text="Merge Input Files", command=lambda: sequence_merge(output_folder_s, output_file_s, input_files_s))
sequence_merge_button.grid(row=6, column=0, padx=(0,10), pady=10, sticky='EW')


# NB TAB 2: Rearranging Tab ############################################
rearrange_frame = ttk.Frame(nb)
nb.add(rearrange_frame, text='Rearrange', sticky='NESW')

# Nested Notebook within Merging Tab for all rearranging functions
rearrange_tab = ttk.Notebook(rearrange_frame)
rearrange_tab.grid(row=0, column=0, columnspan=50, sticky='NESW')
rearrange_tab.rowconfigure(0, weight=1)
rearrange_tab.columnconfigure(0, weight=1)

# REARRANGE_TAB 1: Re-order 1 PDF by Page Number #####################################
# "ro" added to the end of variables here to represent "reorder".

reorder_one_tab = ttk.Frame(rearrange_tab)
rearrange_tab.add(reorder_one_tab, text='Re-Order PDF', sticky='EW')
# Output folder
output_folder_label_ro = ttk.Label(reorder_one_tab, text="Choose Output Folder:")
output_folder_label_ro.grid(row=0, column=0, sticky='EW')
output_folder_ro = ttk.Entry(reorder_one_tab)
output_folder_ro.grid(row=1, column=0, sticky='EW')

# Output Button
output_button_ro = ttk.Button(reorder_one_tab, text="Output", command=lambda: choose_folder_button(output_folder_ro))
output_button_ro.grid(row=1, column=1, sticky='EW')

# Output File
output_file_label_ro = ttk.Label(reorder_one_tab, text="Type Output File Name:")
output_file_label_ro.grid(row=2, column=0, sticky='EW')
output_file_ro = ttk.Entry(reorder_one_tab)
output_file_ro.grid(row=3, column=0, sticky='EW')

# Input file
input_file_label_ro = ttk.Label(reorder_one_tab, text="Choose Input File:")
input_file_label_ro.grid(row=4, column=0, sticky='EW')
input_file_ro = ttk.Entry(reorder_one_tab)
input_file_ro.grid(row=5, column=0, sticky='EW')

# Input Button
input_file_button_ro = ttk.Button(reorder_one_tab, text="Input", command=lambda: choose_file_button(input_file_ro))
input_file_button_ro.grid(row=5, column=1, sticky='EW')

# Page Numbers
page_nos_label_ro = ttk.Label(reorder_one_tab, text="Choose Pages")
page_nos_label_ro.grid(row=6, column=0, sticky='EW')
page_nos_ro = ttk.Entry(reorder_one_tab)
page_nos_ro.grid(row=7, column=0, sticky='EW')


# Reorder one PDF
reorder_button = ttk.Button(reorder_one_tab, text="Reorder PDF", command=lambda: reorder_one(output_folder_ro, output_file_ro, input_file_ro, page_nos_ro))
reorder_button.grid(row=8, column=0, padx=(0,10), pady=10, sticky='EW')




# MAIN LOOP

tk.mainloop()
