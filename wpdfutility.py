"""
GUI Tool to handle PDFs.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import pdfmerge
from tkinter import ttk
import pdffromlinks
import pdfcompile
import webbrowser
import re
from GUI_layout import show, Options, Coordinates as XY, LabelsEntriesButtons
# import LEB 

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
                             '''Choose a folder where your new PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
        return

    if output_file.get() == "":
        messagebox.showerror("Error: No Output File specified", "Type a filename for your merged pdf.")
        return
    if input_folder.get() == "":
        messagebox.showerror("Error: No Input Folder specified", "Choose a folder where all your PDFs are located.")
        return

    try:
        folder_merge_button.configure(state=tk.DISABLED)
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
                             '''Choose a folder where your new PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
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
                             '''Choose a folder where your new PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
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

def reorder_one(output_folder, output_file, input_file, page_nos):
    """GUI version of rearrange_pdf."""
    # Check for required input:
    
    
    if output_folder.get() == "":
        messagebox.showerror("Error: No Output Folder specified",
                             '''Choose a folder where your new PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
        return

    if output_file.get() == "":
        messagebox.showerror("Error: No Output File specified", "Type a filename for your rearranged PDF.")
        return
    if input_file.get() == "":
        messagebox.showerror("Error: No Input Files specified", "Choose a PDF to rearrange.")
        return

    if page_nos.get() == "":
        messagebox.showerror("Error: No Page/Page Range specified", "Choose pages to be kept or reordered. Separate the pages and page ranges with commas. For example, '1,2,4,5-10,3,4'. Writing a range backwards like '10-8' will give you the pages in reverse (10, 9, 8).")
        return

    try:
        reorder_button.configure(state=tk.DISABLED)
        input_file = input_file.get()
        page_list = pdfcompile.make_list_of_pages_from_string(page_nos.get())
        
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

def remove_one(output_folder, output_file, input_file, page_nos):
    """GUI version of remove_pages_from_pdfs."""
    # Check for required input:
    
    
    if output_folder.get() == "":
        messagebox.showerror("Error: No Output Folder specified",
                             '''Choose a folder where your new PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
        return

    if output_file.get() == "":
        messagebox.showerror("Error: No Output File specified", "Type a filename for your PDF with removed pages.")
        return
    if input_file.get() == "":
        messagebox.showerror("Error: No Input Files specified", "Choose a PDF to remove pages from.")
        return

    if page_nos.get() == "":
        messagebox.showerror("Error: No Page/Page Range specified", "Choose pages to be removed. Separate the pages and page ranges with commas. For example, '1,2,4,5-10,3,4'. Writing a range backwards like '10-8' will give you the pages in reverse (10, 9, 8).")
        return

    try:
        reorder_button.configure(state=tk.DISABLED)
        input_file = input_file.get()
        page_list = pdfcompile.make_list_of_pages_from_string(page_nos.get())
        
        destination, pages_removed = pdfcompile.remove_pages_from_pdf(input_file, page_list, output_folder.get(), output_file.get())
    
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
    except ValueError as e:
        messagebox.showerror("Error: Value Error", str(e))
    else:
        messagebox.showinfo("Complete", f"Removed pages {pages_removed} of input file {input_file}, and output file to {destination}.")
        
    finally:
        remove_button.configure(state=tk.NORMAL)

def dl_all(output_folder, output_file, start_html_page, root_html_page, max_depth, regex_filter):
    """GUI version of download_all_pdf."""
    unexpected_errors = []
    
    if output_folder.get() == "":
        messagebox.showerror("Error: No Output Folder specified",
                             '''Choose a folder where your new PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
        return

    if output_file.get() == "":
        messagebox.showerror("Error: No Output File specified", "Type a filename for your PDF with all the PDFs. Note that the PDF will be split if there are too many links. You can merge this later with the Merge functions. Note that bookmarks will be gone if you do this.")
        return
    if start_html_page.get() == "":
        messagebox.showerror("Error: No URL specified", "Choose a URL to start downloading PDFs from recursively.")
        return

    if root_html_page.get() == "":
        messagebox.showerror("Error: No Root URL specified", "Type in a base URL to handle cases where links in the HTML are relative. For example, if your starting site is yourexample.com/firstpage.html, the Root URL is yourexample.com.")
        return

    if max_depth.get() == "":
        messagebox.showerror("Error: No Max Depth specified", "Choose how far the script should check. It is not recommended that you set this number too high as the time taken increases exponentially, and you may not actually get that many unique links in the end. For more targeted results, make sure to change the regex filter.")
        return
    
    try:
        max_depth_int = pdffromlinks.check_integer(max_depth.get())
    except ValueError as e:
        messagebox.showerror("Error: ValueError", str(e))
        return
    
    try:
        pdffromlinks.check_and_set_recursion_depth(max_depth_int)
    except OverflowError as e:
        messagebox.showerror("Error: OverflowError", str(e))
    
    
    try: 
        dl_all_button.config(state=tk.DISABLED)
        pdffromlinks.download_all_pdf(start_html_page.get(), root_html_page.get(), output_file.get(), output_folder.get(), regex_filter.get(), max_depth_int)

    except FileNotFoundError as e:
        if "[WinError 206]" in str(e):
            messagebox.showerror("Error: File Not Found", str(e))
        else:
            messagebox.showerror("Error: File Not Found",
                             f'''File {input_folder.get()} does not exist. Are there backslashes in the address? If so, use the Input or Output button instead of copy pasting a file address directly.''')
        return
    except FileExistsError:
        messagebox.showerror("Error: File Already Exists",
                             f"File already exists. Change the output file name to something else.")
        return
    except Exception as e:
        print(e)
        unexpected_errors.append(str(e))

    else:
        if unexpected_errors:
            if output_folder.get()[-1] == "/":
                messagebox.showinfo("Complete", f"Output file to {output_folder.get()}{output_file.get()}. Unexpected Errors Encountered: \n\n{unexpected_errors}")
            else:
                messagebox.showinfo("Complete", f"Output file to {output_folder.get()}/{output_file.get()}. Unexpected Errors Encountered: \n\n{unexpected_errors}")
        else:
            if output_folder.get()[-1] == "/":
                messagebox.showinfo("Complete", f"Output file to {output_folder.get()}{output_file.get()}.")
            else:
                messagebox.showinfo("Complete", f"Output file to {output_folder.get()}/{output_file.get()}.")
        
    finally:
        dl_all_button.configure(state=tk.NORMAL)

def dl_one(output_folder, output_file, start_html_page):
    """GUI version of download_as_pdf for single URL."""
    unexpected_errors = []
    if output_folder.get() == "":
        messagebox.showerror("Error: No Output Folder specified",
                             '''Choose a folder where your new PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
        return

    if output_file.get() == "":
        messagebox.showerror("Error: No Output File specified", "Type a filename for your PDF.")
        return
    if start_html_page.get() == "":
        messagebox.showerror("Error: No URL specified", "Choose a URL to start downloading a PDF from.")
        return

    try: 
        dl_one_button.config(state=tk.DISABLED)
        pdffromlinks.download_as_pdf(start_html_page.get(), output_file.get(), output_folder.get())

    except FileNotFoundError as e:
        if "[WinError 206]" in str(e):
            messagebox.showerror("Error: File Not Found", str(e))
        else:
            messagebox.showerror("Error: File Not Found",
                             f'''File {input_folder.get()} does not exist. Are there backslashes in the address? If so, use the Input or Output button instead of copy pasting a file address directly.''')
        return
    except FileExistsError:
        messagebox.showerror("Error: File Already Exists",
                             f"File already exists. Change the output file name to something else.")
        return
    except Exception as e:
        print(e)
        unexpected_errors.append(str(e))

    else:
        if unexpected_errors:
            if output_folder.get()[-1] == "/":
                messagebox.showinfo("Complete", f"Output file to {output_folder.get()}{output_file.get()}. Unexpected Errors Encountered: \n\n{unexpected_errors}")
            else:
                messagebox.showinfo("Complete", f"Output file to {output_folder.get()}/{output_file.get()}. Unexpected Errors Encountered: \n\n{unexpected_errors}")
        else:
            if output_folder.get()[-1] == "/":
                messagebox.showinfo("Complete", f"Output file to {output_folder.get()}{output_file.get()}.")
            else:
                messagebox.showinfo("Complete", f"Output file to {output_folder.get()}/{output_file.get()}.")
        
    finally:
        dl_one_button.configure(state=tk.NORMAL)

def dl_list(output_folder, output_file, html_page_list):
    """GUI version of download_as_pdf for list of URLs."""
    
    unexpected_errors = []
    if output_folder.get() == "":
        messagebox.showerror("Error: No Output Folder specified",
                             '''Choose a folder where your new PDF will be located. Try not to copy paste directly into this box if you are using Windows, as the backslashes may lead to issues. Use the 'Output' box instead.''')
        return

    if output_file.get() == "":
        messagebox.showerror("Error: No Output File specified", "Type a filename for your PDF.")
        return
    if html_page_list.get() == "":
        messagebox.showerror("Error: No URLs specified", "Choose a list of URLs to start downloading PDFs from. You can also copy paste the list of URLs you got in the LINK.txt file while trying to download multiple PDFs from one link. It does not matter if there are other characters around the quotation marks.")
        return
    print(html_page_list.get())
    html_pages = re.findall(r'[\'\"](.*?)[\'\"]', html_page_list.get())
    print(html_pages)
    if not html_pages:
        messagebox.showerror("Error: No URLs specified", "Separate your URLs between single quotes. You can also copy paste the list of URLs you got in the LINK.txt file while trying to download multiple PDFs from one link. It does not matter if there are other characters around the single quote marks.")
        return


    try: 
        dl_list_button.config(state=tk.DISABLED)
        pdffromlinks.download_as_pdf(html_pages, output_file.get(), output_folder.get())

    except FileNotFoundError as e:
        messagebox.showerror("Error: File Not Found",
                            f'''File {input_folder.get()} does not exist. Are there backslashes in the address? If so, use the Input or Output button instead of copy pasting a file address directly.''')
        return
    except FileExistsError:
        messagebox.showerror("Error: File Already Exists",
                             f"File already exists. Change the output file name to something else.")
        return
    except Exception as e:
        print(e)
        unexpected_errors.append(str(e))

    else:
        if unexpected_errors:
            if output_folder.get()[-1] == "/":
                messagebox.showinfo("Complete", f"Output file to {output_folder.get()}{output_file.get()}. Unexpected Errors Encountered: \n\n{unexpected_errors}")
            else:
                messagebox.showinfo("Complete", f"Output file to {output_folder.get()}/{output_file.get()}. Unexpected Errors Encountered: \n\n{unexpected_errors}")
        else:
            if output_folder.get()[-1] == "/":
                messagebox.showinfo("Complete", f"Output file to {output_folder.get()}{output_file.get()}.")
            else:
                messagebox.showinfo("Complete", f"Output file to {output_folder.get()}/{output_file.get()}.")
        
    finally:
        dl_list_button.configure(state=tk.NORMAL)
## 1 Feb 2019: Redo UI. Have Output Folders and Output Files on top. The rest of the Input appears depending on the option chosen in a dropdown menu.

# Layout is contained in GUI_layout.py, from the Coordinates class, which uses named tuples x and y to represent row and column respectively. The Coordinates class is imported as XY for easier editing.

        

# Output folder
output_folder_label = ttk.Label(main, text="Choose Output Folder:")
output_folder_label.grid(row=XY.output_folder_label.x, column=XY.output_folder_label.y, sticky='NESW')
output_folder = ttk.Entry(main)
output_folder.grid(row=XY.output_folder.x, column=XY.output_folder.y, sticky='NESW')

# Output Button
output_button = ttk.Button(main, text="Output", command=lambda: choose_folder_button(output_folder))
output_button.grid(row=XY.output_button.x, column=XY.output_button.y, sticky='NESW')

# Output File
output_file_label = ttk.Label(main, text="Type Output File Name:")
output_file_label.grid(row=XY.output_file_label.x, column=XY.output_file_label.y, sticky='NESW')
output_file = ttk.Entry(main)
output_file.grid(row=XY.output_file.x, column=XY.output_file.y, sticky='NESW')


options = list(Options.option_dict.keys())
chosen_option = tk.StringVar()
chosen_option.set(options[1])

LEB = LabelsEntriesButtons(main)

def show_gui(choice):
    """Show relevant options only"""
    chosen_option.set(choice)
    show(main, chosen_option.get(), LEB)

show_gui(chosen_option.get())

dropdown = ttk.OptionMenu(main, chosen_option, options[1], *options, command=show_gui)

dropdown.grid(row=XY.dropdown.x,column=XY.dropdown.y, sticky='NESW')

#TODO Make text in dropdown left-aligned or justified

#TODO Hide these until dropdown chosen

## INPUTS BELOW OUTPUTFILES
# # Input folder
# input_folder_label = ttk.Label(main, text="Choose Input Folder:")
# input_folder_label.grid(row=XY.input_folder_label.x, column=XY.input_folder_label.y, sticky='NESW')
# input_folder = ttk.Entry(main)
# input_folder.grid(row=XY.input_folder.x, column=XY.input_folder.y, sticky='NESW')

# # Input Folder Button
# input_folder_button = ttk.Button(main, text="Input", command=lambda: choose_folder_button(input_folder))
# input_folder_button.grid(row=XY.input_folder_button.x, column=XY.input_folder_button.y, sticky='NESW')


# Input File
input_file_label = ttk.Label(main, text="Choose Input File:")
input_file_label.grid(row=XY.input_file_label.x, column=XY.input_file_label.y, sticky='NESW')
input_file = ttk.Entry(main)
input_file.grid(row=XY.input_file.x, column=XY.input_file.y, sticky='NESW')

# Input File Button
input_file_button = ttk.Button(main, text="Input", command=lambda: choose_file_button(input_file))

input_file_button.grid(row=XY.input_file_button.x, column=XY.input_file_button.y, sticky='NESW')


# Page Numbers
page_nos_label = ttk.Label(main, text="Pages/Ranges:")
page_nos_label.grid(row=XY.page_nos_label.x, column=XY.page_nos_label.y, sticky='NESW')
page_nos = ttk.Entry(main)
page_nos.grid(row=XY.page_nos.x, column=XY.page_nos.y, sticky='NESW')

# TODO Implement input multiple files in a user-friendly way









# Create an overarching notebook. This will contain nested tabs.
nb = ttk.Notebook(main)
nb.grid(row= 333, column=0, columnspan=50, sticky='NESW')
nb.rowconfigure(0, weight=1)
nb.columnconfigure(0, weight=1)


# NB TAB 1: Merging Tab ############################################
merge_frame = ttk.Frame(nb)
nb.add(merge_frame, text='Merge', sticky='NESW')

# Nested Notebook within Merging Tab for all merging functions
merge_tab = ttk.Notebook(merge_frame)
merge_tab.grid(row=0, column=0, columnspan=50, sticky='NESW')
merge_tab.rowconfigure(0, weight=1)
merge_tab.columnconfigure(0, weight=1)

# MERGE_TAB 1: Merge All PDFs in Folder #####################################
# "f" added to the end of variables here to represent folder.
folder_merge_tab = ttk.Frame(merge_tab)
merge_tab.add(folder_merge_tab, text='Merge PDFs in Folder', sticky='NESW')

# Output folder
output_folder_label_f = ttk.Label(folder_merge_tab, text="Choose Output Folder:")
output_folder_label_f.grid(row=0, column=0, sticky='NESW')
output_folder_f = ttk.Entry(folder_merge_tab)
output_folder_f.grid(row=1, column=0, sticky='NESW')

# Output Button
output_button_f = ttk.Button(folder_merge_tab, text="Output", command=lambda: choose_folder_button(output_folder_f))
output_button_f.grid(row=1, column=1, sticky='NESW')

# Output File
output_file_label_f = ttk.Label(folder_merge_tab, text="Type Output File Name:")
output_file_label_f.grid(row=2, column=0, sticky='NESW')
output_file_f = ttk.Entry(folder_merge_tab)
output_file_f.grid(row=3, column=0, sticky='NESW')

# Input folder
input_folder_label_f = ttk.Label(folder_merge_tab, text="Choose Input Folder:")
input_folder_label_f.grid(row=4, column=0, sticky='NESW')
input_folder_f = ttk.Entry(folder_merge_tab)
input_folder_f.grid(row=5, column=0, sticky='NESW')

# Input Button
input_button_f = ttk.Button(folder_merge_tab, text="Input", command=lambda: choose_folder_button(input_folder_f))
input_button_f.grid(row=5, column=1, sticky='NESW')

# Merge all in folder
folder_merge_button = ttk.Button(folder_merge_tab, text="Merge Input Folder",
                                      command=lambda: folder_merge(output_folder_f, output_file_f, input_folder_f))
folder_merge_button.grid(row=6, column=0, padx=(0,10), pady=10, sticky='NESW')

# MERGE_TAB 2: Merge 2 PDFs in Sequence #####################################
# "two" added to the end of variables here to represent 2 PDFs.

two_merge_tab = ttk.Frame(merge_tab)
merge_tab.add(two_merge_tab, text='Merge 2 PDFs', sticky='NESW')
# Output folder
output_folder_label_two = ttk.Label(two_merge_tab, text="Choose Output Folder:")
output_folder_label_two.grid(row=0, column=0, sticky='NESW')
output_folder_two = ttk.Entry(two_merge_tab)
output_folder_two.grid(row=1, column=0, sticky='NESW')

# Output Button
output_button_two = ttk.Button(two_merge_tab, text="Output", command=lambda: choose_folder_button(output_folder_two))
output_button_two.grid(row=1, column=1, sticky='NESW')

# Output File
output_file_label_two = ttk.Label(two_merge_tab, text="Type Output File Name:")
output_file_label_two.grid(row=2, column=0, sticky='NESW')
output_file_two = ttk.Entry(two_merge_tab)
output_file_two.grid(row=3, column=0, sticky='NESW')

# Input file 1
input_file1_label_two = ttk.Label(two_merge_tab, text="Choose Input File 1:")
input_file1_label_two.grid(row=4, column=0, sticky='NESW')
input_file1_two = ttk.Entry(two_merge_tab)
input_file1_two.grid(row=5, column=0, sticky='NESW')

# Input Button 1
input_file1_button_two = ttk.Button(two_merge_tab, text="Input 1", command=lambda: choose_file_button(input_file1_two))
input_file1_button_two.grid(row=5, column=1, sticky='NESW')

# Input file 2
input_file2_label_two = ttk.Label(two_merge_tab, text="Choose Input File 2:")
input_file2_label_two.grid(row=6, column=0, sticky='NESW')
input_file2_two = ttk.Entry(two_merge_tab)
input_file2_two.grid(row=7, column=0, sticky='NESW')

# Input Button 2
input_file2_button_two = ttk.Button(two_merge_tab, text="Input 2", command=lambda: choose_file_button(input_file2_two))
input_file2_button_two.grid(row=7, column=1, sticky='NESW')

# Merge two in sequence
two_merge_button = ttk.Button(two_merge_tab, text="Merge 2 Input Files", command=lambda: two_merge(output_folder_two, output_file_two, input_file1_two, input_file2_two))
two_merge_button.grid(row=8, column=0, padx=(0,10), pady=10, sticky='NESW')

# MERGE_TAB 3: Merge All PDFs in Sequence #####################################
# "s" added to the end of variables here to represent sequence.

# TODO: Right now, without workarounds, this is not very useful. It can also only merge files within the same folder. 
seq_merge_tab = ttk.Frame(merge_tab)
merge_tab.add(seq_merge_tab, text='Merge Many PDFs')

# Output folder
output_folder_label_s = ttk.Label(seq_merge_tab, text="Choose Output Folder:")
output_folder_label_s.grid(row=0, column=0, sticky='NESW')
output_folder_s = ttk.Entry(seq_merge_tab)
output_folder_s.grid(row=1, column=0, sticky='NESW')

# Output Button
output_button_s = ttk.Button(seq_merge_tab, text="Output", command=lambda: choose_folder_button(output_folder_s))
output_button_s.grid(row=1, column=1, sticky='NESW')

# Output File
output_file_label_s = ttk.Label(seq_merge_tab, text="Type Output File Name:")
output_file_label_s.grid(row=2, column=0, sticky='NESW')
output_file_s = ttk.Entry(seq_merge_tab)
output_file_s.grid(row=3, column=0, sticky='NESW')

# Input files
input_files_label_s = ttk.Label(seq_merge_tab, text="Choose Input File(s):")
input_files_label_s.grid(row=4, column=0, sticky='NESW')
input_files_s = ttk.Entry(seq_merge_tab)
input_files_s.grid(row=5, column=0, sticky='NESW')

# Input Button
input_button_s = ttk.Button(seq_merge_tab, text="Input", command=lambda: choose_files_button(input_files_s))
input_button_s.grid(row=5, column=1, sticky='NESW')

# Merge all in sequence
sequence_merge_button = ttk.Button(seq_merge_tab, text="Merge Input Files", command=lambda: sequence_merge(output_folder_s, output_file_s, input_files_s))
sequence_merge_button.grid(row=6, column=0, padx=(0,10), pady=10, sticky='NESW')


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
rearrange_tab.add(reorder_one_tab, text='Re-Order PDF', sticky='NESW')
# Output folder
output_folder_label_ro = ttk.Label(reorder_one_tab, text="Choose Output Folder:")
output_folder_label_ro.grid(row=0, column=0, sticky='NESW')
output_folder_ro = ttk.Entry(reorder_one_tab)
output_folder_ro.grid(row=1, column=0, sticky='NESW')

# Output Button
output_button_ro = ttk.Button(reorder_one_tab, text="Output", command=lambda: choose_folder_button(output_folder_ro))
output_button_ro.grid(row=1, column=1, sticky='NESW')

# Output File
output_file_label_ro = ttk.Label(reorder_one_tab, text="Type Output File Name:")
output_file_label_ro.grid(row=2, column=0, sticky='NESW')
output_file_ro = ttk.Entry(reorder_one_tab)
output_file_ro.grid(row=3, column=0, sticky='NESW')

# Input file
input_file_label_ro = ttk.Label(reorder_one_tab, text="Choose Input File:")
input_file_label_ro.grid(row=4, column=0, sticky='NESW')
input_file_ro = ttk.Entry(reorder_one_tab)
input_file_ro.grid(row=5, column=0, sticky='NESW')

# Input Button
input_file_button_ro = ttk.Button(reorder_one_tab, text="Input", command=lambda: choose_file_button(input_file_ro))
input_file_button_ro.grid(row=5, column=1, sticky='NESW')

# Page Numbers
page_nos_label_ro = ttk.Label(reorder_one_tab, text="Arrange Pages/Ranges:")
page_nos_label_ro.grid(row=6, column=0, sticky='NESW')
page_nos_ro = ttk.Entry(reorder_one_tab)
page_nos_ro.grid(row=7, column=0, sticky='NESW')


# Reorder one PDF
reorder_button = ttk.Button(reorder_one_tab, text="Reorder PDF", command=lambda: reorder_one(output_folder_ro, output_file_ro, input_file_ro, page_nos_ro))
reorder_button.grid(row=8, column=0, padx=(0,10), pady=10, sticky='NESW')

# REARRANGE_TAB 2: Remove pages from 1 PDF by Page Number #####################################
# "rm" added to the end of variables here to represent "remove".

remove_tab = ttk.Frame(rearrange_tab)
rearrange_tab.add(remove_tab, text='Remove Pages', sticky='NESW')
# Output folder
output_folder_label_rm = ttk.Label(remove_tab, text="Choose Output Folder:")
output_folder_label_rm.grid(row=0, column=0, sticky='NESW')
output_folder_rm = ttk.Entry(remove_tab)
output_folder_rm.grid(row=1, column=0, sticky='NESW')

# Output Button
output_button_rm = ttk.Button(remove_tab, text="Output", command=lambda: choose_folder_button(output_folder_rm))
output_button_rm.grid(row=1, column=1, sticky='NESW')

# Output File
output_file_label_rm = ttk.Label(remove_tab, text="Type Output File Name:")
output_file_label_rm.grid(row=2, column=0, sticky='NESW')
output_file_rm = ttk.Entry(remove_tab)
output_file_rm.grid(row=3, column=0, sticky='NESW')

# Input file
input_file_label_rm = ttk.Label(remove_tab, text="Choose Input File:")
input_file_label_rm.grid(row=4, column=0, sticky='NESW')
input_file_rm = ttk.Entry(remove_tab)
input_file_rm.grid(row=5, column=0, sticky='NESW')

# Input Button
input_file_button_rm = ttk.Button(remove_tab, text="Input", command=lambda: choose_file_button(input_file_rm))
input_file_button_rm.grid(row=5, column=1, sticky='NESW')

# Page Numbers
page_nos_label_rm = ttk.Label(remove_tab, text="Remove Pages/Ranges:")
page_nos_label_rm.grid(row=6, column=0, sticky='NESW')
page_nos_rm = ttk.Entry(remove_tab)
page_nos_rm.grid(row=7, column=0, sticky='NESW')


# Remove pages from one PDF
remove_button = ttk.Button(remove_tab, text="Remove Pages", command=lambda: remove_one(output_folder_rm, output_file_rm, input_file_rm, page_nos_rm))
remove_button.grid(row=8, column=0, padx=(0,10), pady=10, sticky='NESW')

# NB TAB 3: Links to PDF Tab ############################################
link_frame = ttk.Frame(nb)
nb.add(link_frame, text='Links to PDF', sticky='NESW')

# Nested Notebook within Merging Tab for all rearranging functions
link_tab = ttk.Notebook(link_frame)
link_tab.grid(row=0, column=0, columnspan=50, sticky='NESW')
link_tab.rowconfigure(0, weight=1)
link_tab.columnconfigure(0, weight=1)

# LINK_TAB 1: Download All Links Within Links to a set recursion depth#####################################
# "da" added to the end of variables here to represent "download_all".
dl_all_tab = ttk.Frame(link_tab)
link_tab.add(dl_all_tab, text='PDFs from 1 Link', sticky='NESW')

# Output folder
output_folder_label_da = ttk.Label(dl_all_tab, text="Choose Output Folder:")
output_folder_label_da.grid(row=0, column=0, sticky='NESW')
output_folder_da = ttk.Entry(dl_all_tab)
output_folder_da.grid(row=1, column=0, sticky='NESW')

# Output Button
output_button_da = ttk.Button(dl_all_tab, text="Output", command=lambda: choose_folder_button(output_folder_da))
output_button_da.grid(row=1, column=1, sticky='NESW')

# Output File
output_file_label_da = ttk.Label(dl_all_tab, text="Type Output File Name:")
output_file_label_da.grid(row=2, column=0, sticky='NESW')
output_file_da = ttk.Entry(dl_all_tab)
output_file_da.grid(row=3, column=0, sticky='NESW')

# Start HTML Page
start_html_page_label_da = ttk.Label(dl_all_tab, text="Input the 1st HTML Page:")
start_html_page_label_da.grid(row=4, column=0, sticky='NESW')
start_html_page_da = ttk.Entry(dl_all_tab)
start_html_page_da.grid(row=5, column=0, sticky='NESW')

# Root HTML Page
root_html_label_da = ttk.Label(dl_all_tab, text="Input the Root HTML Page:")
root_html_label_da.grid(row=6, column=0, sticky='NESW')
root_html_da = ttk.Entry(dl_all_tab)
root_html_da.grid(row=7, column=0, sticky='NESW')


# Recursion Depth
max_depth_label_da = ttk.Label(dl_all_tab, text="Max Recursion Depth (Int)")
max_depth_label_da.grid(row=8, column=0, sticky='NESW')
max_depth_da = ttk.Entry(dl_all_tab)
max_depth_da.grid(row=9, column=0, sticky='NESW')

# Regex Filter
regex_filter_label_da = ttk.Label(dl_all_tab, text="Regex Filter")
regex_filter_label_da.grid(row=10, column=0, sticky='NESW')
regex_filter_da = ttk.Entry(dl_all_tab)
regex_filter_da.grid(row=11, column=0, sticky='NESW')

regex_filter_da.insert(0, r"(?!.*feed\.xml)(?!\#)")

# Regex Guide Button

regex_guide_url = "https://docs.python.org/3.8/library/re.html"
# See also https://www.rexegg.com/regex-quickstart.html

regex_guide_button_da = ttk.Button(dl_all_tab, text="Regex Guide", command=lambda: webbrowser.open(regex_guide_url))
regex_guide_button_da.grid(row=11, column=1, sticky='NESW')

# Compile PDFs from link within links
dl_all_button = ttk.Button(dl_all_tab, text="Multiple PDFs from Link", command=lambda: dl_all(output_folder_da, output_file_da, start_html_page_da, root_html_da, max_depth_da, regex_filter_da))
dl_all_button.grid(row=12, column=0, padx=(0,10), pady=10, sticky='NESW')


# LINK_TAB 2: Download One PDF from a given link or list of links #####################################
# "do" added to the end of variables here to represent "download_one".
dl_one_tab = ttk.Frame(link_tab)
link_tab.add(dl_one_tab, text='PDF from Link', sticky='NESW')

# Output folder
output_folder_label_do = ttk.Label(dl_one_tab, text="Choose Output Folder:")
output_folder_label_do.grid(row=0, column=0, sticky='NESW')
output_folder_do = ttk.Entry(dl_one_tab)
output_folder_do.grid(row=1, column=0, sticky='NESW')

# Output Button
output_button_do = ttk.Button(dl_one_tab, text="Output", command=lambda: choose_folder_button(output_folder_do))
output_button_do.grid(row=1, column=1, sticky='NESW')

# Output File
output_file_label_do = ttk.Label(dl_one_tab, text="Type Output File Name:")
output_file_label_do.grid(row=2, column=0, sticky='NESW')
output_file_do = ttk.Entry(dl_one_tab)
output_file_do.grid(row=3, column=0, sticky='NESW')

# Start HTML Page
start_html_page_label_do = ttk.Label(dl_one_tab, text="Input the HTML Page:")
start_html_page_label_do.grid(row=4, column=0, sticky='NESW')
start_html_page_do = ttk.Entry(dl_one_tab)
start_html_page_do.grid(row=5, column=0, sticky='NESW')

# Compile PDFs from link within links
dl_one_button = ttk.Button(dl_one_tab, text="1 PDF from Link", command=lambda: dl_one(output_folder_do, output_file_do, start_html_page_do))
dl_one_button.grid(row=12, column=0, padx=(0,10), pady=10, sticky='NESW')

# LINK_TAB 3: Download One PDF from each in a list and merge them###################################
# "dil" added to the end of variables here to represent "download in list".
dl_list_tab = ttk.Frame(link_tab)
link_tab.add(dl_list_tab, text='PDF from List', sticky='NESW')

# Output folder
output_folder_label_dil = ttk.Label(dl_list_tab, text="Choose Output Folder:")
output_folder_label_dil.grid(row=0, column=0, sticky='NESW')
output_folder_dil = ttk.Entry(dl_list_tab)
output_folder_dil.grid(row=1, column=0, sticky='NESW')

# Output Button
output_button_dil = ttk.Button(dl_list_tab, text="Output", command=lambda: choose_folder_button(output_folder_dil))
output_button_dil.grid(row=1, column=1, sticky='NESW')

# Output File
output_file_label_dil = ttk.Label(dl_list_tab, text="Type Output File Name:")
output_file_label_dil.grid(row=2, column=0, sticky='NESW')
output_file_dil = ttk.Entry(dl_list_tab)
output_file_dil.grid(row=3, column=0, sticky='NESW')

# HTML Page List
html_page_list_label_dil = ttk.Label(dl_list_tab, text="Input Multiple Links w/ ''")
html_page_list_label_dil.grid(row=4, column=0, sticky='NESW')
html_page_list_dil = ttk.Entry(dl_list_tab)
html_page_list_dil.grid(row=5, column=0, sticky='NESW')

# Compile PDFs from link within links
dl_list_button = ttk.Button(dl_list_tab, text="PDFs from List", command=lambda: dl_list(output_folder_dil, output_file_dil, html_page_list_dil))
dl_list_button.grid(row=12, column=0, padx=(0,10), pady=10, sticky='NESW')

# MAIN LOOP

tk.mainloop()
