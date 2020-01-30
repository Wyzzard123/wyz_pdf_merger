"""The functionality of the PDF Merger."""

import os

import PyPDF2
import re


def check_inputs(*inputs):
    """Check that the input files exist. Otherwise, raise a FileNotFoundError."""
    for input in inputs:
        if os.path.exists(input):
            continue
        else:
            raise FileNotFoundError(f"File {input} does not exist")
    else:
        return True


def check_folder(output_dir):
    """Check if an output_dir exists. Otherwise, create a new one."""
    if os.path.isdir(output_dir):
        return True
    else:
        os.makedirs(f"{output_dir}")


def sanitize_input(input_file):
    """Get rid of \\ in inputstring."""
    input_file = re.sub(r"\\", "/", input_file)
    return input_file


def sanitize_file_path(output_dir, output_file_name):
    """Get rid of \\, and make sure there are slashes between and .pdf at the end of the file name. Returns the
    sanitized file path. """

    destination = ""

    # Change all \ to / to avoid issues with reading file names:
    output_dir = re.sub(r"\\", "/", output_dir)

    # If the output_dir has a slash at the end, do not add an extra slash.
    if output_dir[-1] == '/':
        # If the output_file_name has .pdf, do not add .pdf to the end
        if re.match(r"^.+\.pdf$", output_file_name):
            destination = f"{output_dir}{output_file_name}.pdf"
        else:
            destination = f"{output_dir}{output_file_name}"
    elif output_dir[-1] != '/':
        if re.match(r"^.+\.pdf$", output_file_name):
            destination = f"{output_dir}/{output_file_name}"
        else:
            destination = f"{output_dir}/{output_file_name}.pdf"

    return destination


def check_output_file_exists(destination):
    """If an output file already exists, raise an error."""
    if os.path.exists(destination):
        raise FileExistsError(f"File already exists at {destination}. Change the output_file_name.")

    else:
        return True


def merge_two_pdfs(input1, input2, output_dir, output_file_name="mergedpdf"):
    """Simply merges two given PDFs together, with input1 first and input2 second. The PDF will be sent to the output
    directory (output_dir), which has a default name "mergedpdf.pdf". """

    sanitized_input1 = sanitize_input(input1)
    sanitized_input2 = sanitize_input(input2)

    # Check that the input file exists
    check_inputs(sanitized_input1, sanitized_input2)

    # Create a File Merger.
    merger = PyPDF2.PdfFileMerger()
    errors =[]
    # Append both files to merger. import_bookmarks is set to False to avoid errors. 
    merger.append(sanitized_input1, import_bookmarks=False)
    merger.append(sanitized_input2, import_bookmarks=False)

    # Check that the output folder exists, otherwise create a new folder. In merge_two_pdfs, this is done later than
    # checking the inputs as there are only two inputs. We can then avoid creating a new directory where there is no
    # need for one.

    check_folder(output_dir)

    destination = sanitize_file_path(output_dir, output_file_name)

    check_output_file_exists(destination)

    # Write to outfile
    with open(f'{destination}', 'wb') as outfile:
        merger.write(outfile)
    print(f"Output file to {destination}")
    return (destination, errors)


def merge_many_pdfs(output_dir, output_file_name="mergedpdf", *inputs):
    """Merges PDFs according to their order in a list. The PDF will be sent to the output directory (output_dir), which has a default name "mergedpdf.pdf".

    Make sure to input the file paths for the input and output folders as raw strings. Returns the destination and any errors."""

    # Check that the output folder exists, otherwise create a new folder.
    check_folder(output_dir)

    # Check if output file exists.
    destination = sanitize_file_path(output_dir, output_file_name)

    # This is done first as there may be numerous inputs.
    check_output_file_exists(destination)
    print(inputs)
    sanitized_inputs = []
    # Check if the input files all exist. To facilitate this, first sanitize the names and add to sanitized inputs.
    # Raise an error once a file does not exist.

    # TODO: Sanitize even when there is a backslash or when the string is not raw.
    for input in inputs:
        sanitized_input = sanitize_input(input)
        check_inputs(sanitized_input)
        sanitized_inputs.append(sanitized_input)
    # Create a File Merger.
    merger = PyPDF2.PdfFileMerger()

    # Append all files to merger. import_bookmarks is set to False to avoid errors.
    errors = []
    for sanitized_input in sanitized_inputs:
        try:
            print(sanitized_input)
            merger.append(sanitized_input, import_bookmarks=False)
        except OSError:
            print(f"OSError: The file {sanitized_input} might be corrupted.")
            errors.append(f"OSError: The file {sanitized_input} might be corrupted.")

    # Write to outfile
    with open(f'{destination}', 'ab') as outfile:
        merger.write(outfile)
    print(f"Output file to {destination}")
    return (destination, errors)


def merge_pdfs_from_folder(input_dir, output_dir, output_file_name="mergedpdf"):
    """Merges many pdfs from one folder, and simply follows the order they are found in the folder. Return the
    destination folder and any errors encountered. """

    # Regex filter at the end is to make sure only pdfs are merged.
    input_list = [r'{}/{}'.format(input_dir, f) for f in os.listdir(input_dir) if re.match(r"^.*\.pdf$", f)]

    destination, errors = merge_many_pdfs(output_dir, output_file_name, *input_list)
    return (destination, errors)


def main():
    """Test scripts."""
    test_output_dir = 'test_outputs'
    test_output_file = 'File2'

    # merge_two_pdfs(test_input_list[0], test_input_list[1], test_output_dir, test_output_file)

    test_input_dir = 'test_inputs'
    test_input_list = [r'{}/{}'.format(test_input_dir, f) for f in os.listdir(test_input_dir)]

    # merge_many_pdfs(test_output_dir,test_output_file,*test_input_list)
    merge_pdfs_from_folder(test_input_dir, test_output_dir, "no.pdf")


if __name__ == "__main__":
    main()
