'''
After merging all the pdfs in the documentation together, I want to keep only the relevant pages and sort them in an order that is more conducive to studying.

Testing out solution from this Stack Overflow Answer: 
https://stackoverflow.com/questions/39574096/how-to-delete-pages-from-pdf-file-using-python
'''

from PyPDF2 import PdfFileWriter, PdfFileReader
import re
import pdfmerge

def rearrange_pdf(input_file, pages_to_use, output_dir, output_file_name="rearrangedpdf"):
    '''Takes a string containing a source file name, a list with the pages from that file, and the name of a file to write to to create a new pdf. The page numbers start from 1.'''

    sanitized_input = pdfmerge.sanitize_input(input_file)
    
    # Check that the input file exists
    pdfmerge.check_inputs(sanitized_input)

    # Check that the output folder exists, otherwise create a new folder. As we do this after checking if the input is valid, we can avoid creating a new directory where there is no
    # need for one.
    pdfmerge.check_folder(output_dir)

    destination = pdfmerge.sanitize_file_path(output_dir, output_file_name)

    pdfmerge.check_output_file_exists(destination)

    infile = PdfFileReader(sanitized_input, 'rb')
    output = PdfFileWriter()
    
    for page_no in pages_to_use:
        p = infile.getPage(page_no - 1)
        output.addPage(p)
    
    with open(destination, 'wb') as f:
        output.write(f)
    return destination

def remove_pages_from_pdf(input_file, pages_to_remove, output_dir, output_file_name="rearrangedpdf"):
    '''Writes a new PDF from an input PDF, removing the page numbers in pages_to_remove.'''

    sanitized_input = pdfmerge.sanitize_input(input_file)
    
    # Check that the input file exists
    pdfmerge.check_inputs(sanitized_input)

    # Check that the output folder exists, otherwise create a new folder. As we do this after checking if the input is valid, we can avoid creating a new directory where there is no
    # need for one.
    pdfmerge.check_folder(output_dir)

    destination = pdfmerge.sanitize_file_path(output_dir, output_file_name)

    pdfmerge.check_output_file_exists(destination)

    infile = PdfFileReader(sanitized_input, 'rb')
    number_of_pages = infile.numPages
    output = PdfFileWriter()

    page_range = range(1, number_of_pages + 1)

    # Convert the list of pages to remove to a set for faster checking. Also remove any extra pages.
    pages_to_remove_set = set(pages_to_remove).intersection(set(page_range))
    
    if not pages_to_remove_set:
        raise ValueError("No pages to remove. Did you specify pages beyond the actual number of pages the document has?")

    for page_no in (page_range := range(1, number_of_pages + 1)):
        if page_no in pages_to_remove_set:
            continue
        else:
            p = infile.getPage(page_no - 1)
            output.addPage(p)
    
    with open(destination, 'wb') as f:
        output.write(f)
    
    # Return the pages actually removed (i.e. excluding extra pages)
    return destination, sorted(list(pages_to_remove_set))

def make_list_of_pages_from_string(page_string):
    """Creates a list of pages to be sent into rearrange_pdf from an input string."""
    page_no_list = []
    page_string_list = page_string.split(",")
    for page_no in page_string_list:
        print(page_string_list)
        if "-" in page_no:
            # Remove whitespace from left and right
            page_no = page_no.strip()

            # Search for pattern. ( *) included in case of extraneous white spaces between the numbers.
            page_no_pattern = r"([0-9]+)( *)(-)( *)([0-9]+)"

            if page_range := re.match(page_no_pattern, page_no):
                start_page = int(page_range.group(1))
                end_page = int(page_range.group(5))
                if end_page >= start_page:
                    page_no_list.extend([page_no for page_no in range(start_page, (end_page + 1))])
                # If start_page is higher, create a list of numbers in reverse
                elif end_page < start_page:
                    page_no_list.extend([page_no for page_no in range(start_page, (end_page - 1), -1)])
            else:
                raise TypeError("Invalid page range. Type individual page_no_list separated by commas and ranges with -.")
        else:
            try:
                page_no_list.append(int(page_no))
            except:
                raise TypeError("Invalid input. Type individual pages separated by commas and ranges with -.")
    return page_no_list
        
        




if __name__ == "__main__":

    pass