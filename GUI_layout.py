"""Contains the layout of the app in a class."""

from collections import namedtuple
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
# from LabelsEntriesButtons import LabelsEntriesButtons as LEB

class Coordinates:
    """Class containing coordinates of each layout item. As these are relative, they will show up in the relatively correct position no matter what. This class is to enable easier editing."""
    XY = namedtuple('XY', 'x y')
    output_folder_label = XY(0, 0)
    output_folder = XY(1, 0)
    output_button =  XY(1, 1)
    output_file_label =  XY(2,0)
    output_file = XY(3,0)
    dropdown = XY(4,0)
    input_folder_label = XY(5,0)
    input_folder = XY(6,0)
    input_folder_button = XY(6,1)
    input_file_label = XY(7,0)
    input_file = XY(8,0)
    input_file_button = XY(8,1)
    input_file1_label = XY(9,0)
    input_file1 = XY(10,0)
    input_file1_button = XY(10,1)
    input_file2_label = XY(11,0)
    input_file2 = XY(12,0)
    input_file2_button = XY(12,1)
    page_nos_label = XY(13,0)
    page_nos = XY(14,0)

    # Final Buttons
    # Place these at the very end
    final_button= XY(200, 0)
    

class LabelsEntriesButtons:
    """Class containing all Labels and Entries to be shown and hidden as necessary."""
    

    def __init__(self,main):
        self.main = main
        # Input Folder
        self.input_folder_label = ttk.Label(main, text="Choose Input Folder:")
        self.input_folder = ttk.Entry(main)
        self.input_folder_button = ttk.Button(main, text="Input", command=lambda: choose_folder_button(main, self.input_folder))

        # Input 2 Files
        self.input_file1_label = ttk.Label(main, text="Choose Input File 1:")
        self.input_file1 = ttk.Entry(main)
        self.input_file1_button = ttk.Button(main, text="Input 1", command=lambda: choose_file_button(self.input_file1))
        self.input_file2_label = ttk.Label(main, text="Choose Input File 2:")
        self.input_file2 = ttk.Entry(main)
        self.input_file2_button = ttk.Button(main, text="Input 2", command=lambda: choose_file_button(self.input_file2))


        # BUTTONS

        # Merge All in Folder
        self.folder_merge_button = ttk.Button(main, text="Merge Input Folder",
                                      command=lambda: folder_merge(output_folder_f, output_file_f, input_folder_f))

        


    


class Options:
    """Class containing strings for each option. This enables easier editing of names and arrangements if needed."""
    merge_folder = "Merge All PDFs in a Folder"
    merge_two = "Merge Two PDFs"
    merge_list = "Merge List of PDFs"
    export_link = "Export Link as Single PDF"
    export_list = "Export List of Links as Single PDF"
    export_crawl = "Export Link and Links within Links as Single PDF"
    rearrange_one = "Rearrange Pages in Single PDF (Copy)"
    remove_from_one = "Cut Pages in Single PDF (Copy)"

    # Attach the UI elements which will be shown when an option is selected
    option_dict = {
        merge_folder: ["Input Folder", "Merge Folder"] ,
        # TODO
        merge_two: ["Input 2 Files"],
        merge_list: [],
        export_link: [],
        export_list: [],
        export_crawl: [],
        rearrange_one: [],
        remove_from_one: [],
        }


def show_option_dict(main, values, LEB):
    # Alias the Coordinates class as XY
    XY = Coordinates
    
    # Input Folder
    if "Input Folder" in values:
        # Show the Input Folder Labels, Entries and Buttons if needed
        # Group together input_folder_label and input_folder_button as "Input Folder"
        # Input folder
        LEB.input_folder_label.grid(row=XY.input_folder_label.x, column=XY.input_folder_label.y, sticky='NESW')
        LEB.input_folder.grid(row=XY.input_folder.x, column=XY.input_folder.y, sticky='NESW')
        # Input Folder Button
        LEB.input_folder_button.grid(row=XY.input_folder_button.x, column=XY.input_folder_button.y, sticky='NESW')
    elif "Input Folder" not in values:
        # Hide the Input Folder Labels if they are not required
        try:
            LEB.input_folder_label.grid_forget()
            LEB.input_folder.grid_forget()
            LEB.input_folder_button.grid_forget()
        except Exception as e:
            print(str(e))

    # Input 2 Files
    if "Input 2 Files" in values:
        # Show the Input Folder Labels, Entries and Buttons if needed
        # Group together input_folder_label and input_folder_button as "Input Folder"

        # Input file 1
        LEB.input_file1_label.grid(row=XY.input_file1_label.x, column=XY.input_file1_label.y, sticky='NESW')
        LEB.input_file1.grid(row=XY.input_file1.x, column=XY.input_file1.y, sticky='NESW')

        # Input Button 1
        LEB.input_file1_button.grid(row=XY.input_file1_button.x, column=XY.input_file1_button.y, sticky='NESW')

        # Input file 2
        LEB.input_file2_label.grid(row=XY.input_file2_label.x, column=XY.input_file2_label.y, sticky='NESW')
        LEB.input_file2.grid(row=XY.input_file2.x, column=XY.input_file2.y, sticky='NESW')

        # Input Button 2
        LEB.input_file2_button.grid(row=XY.input_file2_button.x, column=XY.input_file2_button.y, sticky='NESW')
        
    elif "Input 2 Files" not in values:
        # Hide the Input File 1 and 2 Labels if they are not required
        try:
            LEB.input_file1_label.grid_forget()
            LEB.input_file1.grid_forget()
            LEB.input_file1_button.grid_forget()
            LEB.input_file2_label.grid_forget()
            LEB.input_file2.grid_forget()
            LEB.input_file2_button.grid_forget()
        except Exception as e:
            print(str(e))
    
    if "Merge Folder" in values:
        LEB.folder_merge_button.grid(row=XY.final_button.x, column=XY.final_button.y, sticky='NESW')
    elif "Merge Folder" not in values:
        try:
            LEB.folder_merge_button.grid_forget()
        except Exception as e:
            print(str(e))




def show(main, string_var, LEB):
    """Show relevant options"""
    
    show_option_dict(main, Options.option_dict[string_var], LEB)
        
