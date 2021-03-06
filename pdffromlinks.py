"""
With this module, you can get a link, and all the links within that link, as PDFs, up to a given recursion depth. This utilises pdfkit, wkhtmltopdf.exe and BeautifulSoup.

    See
    https://pythonspot.com/extract-links-from-webpage-beautifulsoup/

To make this work, you will need to set your PATH_TO_WKHTMLTOPDF_EXE to the location of wkhtmltopdf.exe. You need to download wkhtmltopdf.exe for your OS. 

    PATH_TO_WKHTMLTOPDF_EXE = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    
    config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF_EXE)

    See: https://www.tutorialexample.com/fix-oserror-no-wkhtmltopdf-executable-found-in-win-10-for-pdfkit-beginner-python-pdfkit-tutorial/

    See: https://pypi.org/project/pdfkit/

    See also https://wkhtmltopdf.org/

    See also https://pdfkit.org/docs/getting_started.html

    

At the moment, this file also writes a LINKS_.txt file to keep all the links, and also to keep track of any split files. This is needed because the download_to_pdf function can be rather unreliable when used repeatedly. 

If the file size of a particular file is too small, it is likely there was an error and the page could not be fetched. In that case, please use the list written in LINKS_.txt for the relevant file and use download_as_pdf on the relevant list of links directly.

See example.py for an example of how to implement this.

See also example_workaround to see how to get a file directly.

A smaller scale example is provided in if __name__ = "__main__" at the bottom of linkpdfs.py.

NOTE: Sometimes the number of pages or filesize may vary slightly because the elements on a page (especially the graphic elements) don't all load. 
"""


import os
# This is to get all the links on each page so we can feed it into our pdf extractor
from bs4 import BeautifulSoup
import urllib.request
import re
import pdfkit
import math
import sys

CURRENT_RECURSION_LIMIT = sys.getrecursionlimit()


PATH_TO_WKHTMLTOPDF_EXE = 'wkhtmltopdf/bin/wkhtmltopdf.exe'

def check_integer(input_string):
    if re.search(r"[^0-9]", input_string):
        raise ValueError("Input should be an integer.")
    else:
        return int(input_string)

def check_and_set_recursion_depth(max_depth):
    """If the max_depth is lower than the current recursion limit, nothing changes. If the max depth is higher, this function tries to set the recursion depth to the specified max depth. If it fails, it will raise an overflow error early. 200 is added to the max_depth just as a safety buffer."""
    SAFETY_BUFFER = 200

    # Checking that max_depth is not too close to the maximum number of allowed recursions.
    if (max_depth + SAFETY_BUFFER) > CURRENT_RECURSION_LIMIT:
        try:
            sys.setrecursionlimit(max_depth + SAFETY_BUFFER)
            print(f"Recursion limit changed from {CURRENT_RECURSION_LIMIT} to {max_depth + SAFETY_BUFFER}.")
            
        except OverflowError as e:
            raise(OverflowError, "Max Depth too high. Set your max depth lower. It is unlikely that you need so many recursions anyway. As a baseline, the default max recursion depth is around 1000. See details:\n\n{e}")
        else:
            return (max_depth + SAFETY_BUFFER)
    else: 
        return max_depth

def gather_links(start_html_page, root_html_page, regex_link_filter=r"(?!.*feed\.xml)(?!\#)", attribute='href', html_tag='a'):
    """
    Gathers all the links fitting the required criteria in a list. Takes as arguments: Returns the list.

    start_html_page -> Where we will begin our search.

    root_html_page -> This is normally the same as start_html_page, save where the filter is 'suffix' rather than 'prefix'. 

    filter -> Either 'prefix' or 'suffix'. This denotes whether the regex_link_filter provided searches for the beginning or the end of the link respectively. Suffix would be used if, for example, the regex filter is for '/help/support' rather than 'https://'.

    'regex_link_filter -> Sieves out relevant links with a regular expression.

    'attribute' -> The html attribute to search for. Generally 'href'.

    'html_tag' -> The html tag to search for, generally 'a'.
    """

    # Our search starts at the start_html_page and moves on recursively through the links therein. 

    # All our links will be appended to this list. We initialise it with start_html_page, as the search itself will not return this page.
    links = [start_html_page]

    # link_set is to check to make sure that all the links which are added are unique. Using a set reduces time complexity for this operation to O(1)
    link_set = set(links)
    
    # We open the start_html_page with urllib.request (urllib2 in Python 2) and store it as html_page
    html_page = urllib.request.urlopen(start_html_page)

    # BeautifulSoup parses the HTML page. 
    soup = BeautifulSoup(html_page, features="html.parser")
    
    # soup.findAll will return a list of all the links (by default found with html_tag='a' and attrs='href': 'http(s)?://)
    for link in soup.findAll(name=html_tag, attrs={attribute: re.compile(regex_link_filter)}):
        print(link)
        if (newlink:=link.get('href')) not in link_set:
            print(f"{link} not in link_set")
            # If the link begins with http/https:// or www. or has <something>.<something> (ad infinitum for co.uk etc)/, then we can take it to be a full link.
            if re.match(r"http(s?)://", newlink) or re.match(r"www.", newlink) or re.search(r"(.+)(\.(.+))+/", newlink):
                new_string = newlink
            
            # Otherwise, the link is likely truncated, and we must add it to the root_html_page.
            else:
                # If the newlink starts with a /, we simply append the page to the root_html_page
                if re.match(r"/", newlink):
                    new_string = f"{root_html_page}{newlink}"
                # Otherwise, we add a slash in the middle
                else:
                    new_string = f"{root_html_page}/{newlink}"
            
            links.append(new_string)
            link_set.add(new_string)
        else:
            print(f"{link} in new_set, moving on")
    return links





def gather_links_within_links(start_html_page, root_html_page,regex_link_filter=r"(?!.*feed\.xml)(?!\#)", attribute='href', html_tag='a', max_depth = 1, current_depth = 0, links=[], link_set=set()):
    """
    Performs gather_links, but also appends to the list every link which meets the same requirements which can be found within each link. In other words, this recursively finds more and more links. Set a recursion limit with max_depth. 
    
    The arguments, current_depth, links and link_set should not generally be modified. These are just to facilitate the recursion.

    However, it may be a good idea to reset these every time the function is called, especially if the function is being called multiple times in a row. Otherwise, you may face multiple repeated pages.

    Do not use a slash at the end of the root_html_page name, or the links generated will be invalid.
    """
    # Increase current_depth to prevent us from recursing too far.
    current_depth += 1

    # TODO - Rewrite this as an iterative function so it does not face the issues of memory that come with recursion.
    
    # This is to initialise the list with start_html_page
    links.append(start_html_page)

    
    link_set.add(start_html_page)

    check_and_set_recursion_depth(max_depth)
    
    # To notify how far more we have to go based on the max_depth and current_depth.
    print(f"Current depth is {current_depth}. Max Depth is {max_depth}.\nNumber of layers to go is {max_depth - current_depth}.")
    print(links[-1])

    # We first gather the links on the page itself.
    current_links = list(dict.fromkeys(gather_links(start_html_page, root_html_page, regex_link_filter, attribute, html_tag)))


    # links.extend(current_links)
    # links = list(dict.fromkeys(links))
    # link_set.update(current_links)
    
    # Recursion base case. We set a max_depth to prevent an infinite loop if every single page we go into has additional links.
    if current_depth >= max_depth:
        links.extend(current_links)
        links = list(dict.fromkeys(links))
        link_set.update(current_links)
        
        return links

    # This is to go into each link and get a list of every link in that link.
    else:
        
        # We add the links and all the links that can be found on the pages within those links, assuming they are not within the link_set, which is passed in the arguments in the recursive gather_links_within_links.
        for link in current_links:
            if link not in link_set:

                # Recursive call, replacing start_html_page with link, and keeping all other parameters. 
                new_links = gather_links_within_links(link, root_html_page, regex_link_filter, attribute, html_tag, max_depth, current_depth, links, link_set)
                
                links.extend(new_links)
                links = list(dict.fromkeys(links))
                link_set.update(current_links)
                
        # This is the fastest method to sanitize a list of non-unique values and retain the order, and relies on the fact that regular dicts retain insertion order. 

        return list(dict.fromkeys(links))

        # See original by Raymond Hettinger at https://twitter.com/raymondh/status/944125570534621185

        # See benchmarking done at this link https://www.peterbe.com/plog/
    

def download_as_pdf(link_or_list, file_name="outfile", folder_name=".", config =pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF_EXE), options={"window-status":"ready","run-script":"window.setTimeout(function(){window.status='ready';}, 1000);","load-error-handling":"ignore"}):
    """Allows us to set the config within this function, create a folder if one does not already exist, and create a new file. Serves as a wrapper around pdfkit.from_url(). Returns False if a file already exists, causing an error, or if the operation is otherwise unsuccessful. Returns True if successful.
    
    'options' -> To pass options to pdfkit"""
    unexpected_errors = []


    try:
        os.mkdir(folder_name)
        print(f"Directory, '{folder_name}', created.")
    except FileExistsError:
        print(f"Directory, '{folder_name}', already exists. Attempting to create file...")
    
    if os.path.exists(f'{folder_name}/{file_name}.pdf'):
        print(f"'{folder_name}/{file_name}.pdf' already exists.")
        print(f"{folder_name}/{file_name}.pdf FAILED")
        return False
        raise FileExistsError(f"Output File {folder_name}/{file_name} already exists!")
    else:
        if (type(link_or_list) is not str) and (type(link_or_list) is not list) :
            raise TypeError(f"Input is of type {type(link_or_list)}, but link_or_list should be a string or a list.")

        try:

            # KNOWN ERROR: The download_as_pdf function appears to break with a list of more than around 200 links. Usually there is a [WinError206] for the length of the list being too long. Even if this error does not occur, too high a length usually results in the PDF file being unreadable or completely in plaintext. 

            # Current WORKAROUND: If the list length is greater than 100 we will split the PDF into parts of length 150 to feed into download_as_pdf.

            # WORKAROUND 2: If the files do not come out right, please simply use download_as_pdf() individually on the lists of links recorded in the output txt file.

            # WORKAROUND 3: If the pages come out as plaintext, set the 'javascript-delay' to a higher number (of milliseconds).

            # REDUNDANCY: This is repeated in download_all_pdf.
            if type(link_or_list) == list:
                links = link_or_list
            
                number_of_links = len(links)

                # Serves as a number to split the PDF at. 
                # TODO: Implement this as an argument to be passed in.
                part_split = 150
                if number_of_links <= part_split:
                    print(f"\nCreating file: {folder_name}/{file_name}.pdf")

                    # Noting down all the links so we can retry downloading them if there are any errors
                    with open(f"{folder_name}/LINKS_{file_name}.txt", "w") as f:
                        
                        f.write(f"{link_or_list}")

                    pdfkit.from_url(link_or_list, f'{folder_name}/{file_name}.pdf', configuration=config, options=options)
                else:
                    
                    # Number of times we will split the file.
                    max_counter = math.ceil(number_of_links / part_split)
                    
                    print(f"\nThere are too many (more than {part_split}) links ({number_of_links}). Splitting into {int(max_counter)} parts.")

                    # Indicates the number to be tacked on to the end of the file number and serves as a flag to stop splitting once we reach the end.
                    counter = 0
                    
                    # Noting down all the links so we can retry downloading them if there are any errors
                    with open(f"{folder_name}/LINKS_{file_name}.txt", "w") as f:
                    
                        f.write(f"Number of links = {number_of_links}\nSplitting into {max_counter} parts of {part_split} links each.")
                        while counter < max_counter:
                            try:
                                new_file_name = f"{file_name}{counter + 1}"
                                if counter < (max_counter - 1):
                                    start_index = (counter * part_split)
                                    end_index = ((counter + 1) * part_split)
                                    print(f"\nCreating file: {folder_name}/{new_file_name}.pdf with links number {start_index + 1} to {end_index}")
                                    
                                    
                                    split_link = links[start_index:end_index]
                                    print(split_link)

                                    f.write(f"Links number: {start_index + 1} to {end_index} \n{split_link}\n")

                                    pdfkit.from_url(split_link, f'{folder_name}/{new_file_name}.pdf', configuration=config, options=options)

                                elif counter == (max_counter - 1):
                                    start_index = (counter * part_split)
                                    end_index = number_of_links

                                    print(f"\nCreating file: {folder_name}/{new_file_name}.pdf with links number {start_index + 1} to {end_index}")

                                    split_link = links[start_index:end_index]
                                    print(split_link)
                                    
                                    f.write(f"Links number: {start_index + 1} to {end_index} \n{split_link}\n")

                                    pdfkit.from_url(split_link, f'{folder_name}/{new_file_name}.pdf', configuration=config, options=options)
                                counter += 1
                            except Exception as e:
                                # Carries on despite errors so as not to disrupt flow if there are multiple files. In most cases, ProtocolErrors will occur. Comment out and type "raise" here to see more details if needed.

                                print(f"Error for {folder_name}/{file_name}{counter + 1}.pdf: {str(e)}")

                                f.write(f"ERROR for {folder_name}/{file_name}{counter + 1}.pdf: {str(e)}\n\n")

                                unexpected_errors.append(e)


                                counter += 1
                    
            elif type(link_or_list) == str:
                pdfkit.from_url(link_or_list, f'{folder_name}/{file_name}.pdf', configuration=config, options=options)
            
        except FileNotFoundError as e:
            if "WinError 206" in str(e):
                print(f"FileNotFoundError for {folder_name}/{file_name}.pdf. 'FileNotFoundError: [WinError 206] There are too many links or the filenames are too long.")
                raise FileNotFoundError(f"FileNotFoundError for {folder_name}/{file_name}.pdf. 'FileNotFoundError: [WinError 206] There are too many links or the filenames are too long.")
            else:
                print(str(e))
                raise FileNotFoundError(str(e))
            
        except Exception as e:
            print(f"Error for {folder_name}/{file_name}.pdf: {str(e)}\n\n")
            
        print("Done.")

        return True



def download_all_pdf(start_html_page, root_html_page="", file_name="outfile", folder_name=".",regex_link_filter=r"http(s)?://(?!.*feed\.xml)(?!\#)", max_depth = 1, attribute='href', html_tag='a', config = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF_EXE),  options={"window-status":"ready","run-script":"window.setTimeout(function(){window.status='ready';}, 1000);","load-error-handling":"ignore"}, current_depth = 0, links=[], link_set=set()):

    """Writes all links as well as links within those links up to a given recursion max_depth to a PDF file in a given folder name.
    
    Returns a list of links if successful, or False if unsuccessful."""
    
    # Immediately stop  without checking the links if there will be a file error because the file already exists.
    if os.path.exists(f'{folder_name}/{file_name}.pdf'):
        print(f"ERROR: '{folder_name}/{file_name}.pdf' already exists.")
        print(f"{folder_name}/{file_name}.pdf FAILED")
        raise FileExistsError(f"ERROR: '{folder_name}/{file_name}.pdf' already exists. {folder_name}/{file_name}.pdf FAILED.")
        return False
    if root_html_page == "":
        # If there is no entry for the root_html_page, the root will be the portion of the start_html_page before the slash.
        if match := (re.match(r"((http(s?)://)([A-Za-z0-9]+)((\.)([A-Za-z0-9]+))+)", start_html_page)):
            root_html_page = match.group(1)
        

    links = gather_links_within_links(start_html_page, root_html_page, regex_link_filter, attribute, html_tag, max_depth, current_depth, links, link_set)

    
    # KNOWN ERROR: The download_as_pdf function appears to break with a list of more than around 200 links. Usually there is a [WinError206] for the length of the list being too long. Even if this error does not occur, too high a length usually results in the PDF file being unreadable or completely in plaintext. 

    # Current WORKAROUND: If the list length is greater than 100 we will split the PDF into parts of length 100 to feed into download_as_pdf.

    # WORKAROUND 2: If the files do not come out right, please simply use download_as_pdf() individually on the lists of links recorded in the output txt file.

    # WORKAROUND 3: If the pages come out as plaintext, set the 'javascript-delay' to a higher number (of milliseconds).

    # REDUNDANCY: This is repeated in download_as_pdf.
    
    number_of_links = len(links)

    # Serves as a number to split the PDF at. 
    # TODO: Implement this as an argument to be passed in.
    part_split = 100
    if number_of_links <= part_split:
        print(f"\nCreating file: {folder_name}/{file_name}.pdf")

        download_as_pdf(links, file_name, folder_name, config=config, options=options)
    else:
        
        # Create folder here if needed as we will be opening a file in this block. Note that this is only required because with open is used here as well (because of the repetition of the file splitting function from download_as_pdf here)
        try:
            os.mkdir(folder_name)
            print(f"Directory, '{folder_name}', created.")
        except FileExistsError:
            print(f"ERROR: Directory, '{folder_name}', already exists. Attempting to create file...")
        # Number of times we will split the file.
        max_counter = math.ceil(number_of_links / part_split)
        
        print(f"\nThere are too many (more than {part_split}) links ({number_of_links}. Splitting into {max_counter} parts.) ")

        # Indicates the number to be tacked on to the end of the file number and serves as a flag to stop splitting once we reach the end.
        counter = 0
        
        # Noting down all the links for each file so we can retry downloading them if there are any errors
        with open(f"{folder_name}/LINKS_{file_name}.txt", "w") as f:
                        
            f.write(f"Number of links = {number_of_links}\nSplitting into {max_counter} parts of {part_split} links each.")
            # This will be repeated in download_as_pdf in case download_as_pdf is called directly
            while counter < max_counter:
                new_file_name = f"{file_name}{counter + 1}"
                if counter < (max_counter - 1):
                    start_index = (counter * part_split)
                    end_index = ((counter + 1) * part_split)
                    print(f"\nCreating file: {folder_name}/{new_file_name}.pdf with links number {start_index + 1} to {end_index}")
                    
                    split_link = links[start_index:end_index]
                    
                    f.write(f"Links number: {start_index + 1} to {end_index} \n{split_link}\n")

                    download_as_pdf(split_link, new_file_name, folder_name, config=config, options=options)
                    

                elif counter == (max_counter - 1):
                    start_index = (counter * part_split)
                    end_index = number_of_links

                    print(f"\nCreating file: {folder_name}/{new_file_name}.pdf with links number {start_index + 1} to {end_index}")

                    split_link = links[start_index:(end_index + 1)]
                    
                    f.write(f"Links number: {start_index + 1} to {end_index} \n{split_link}\n")

                    download_as_pdf(split_link, new_file_name, folder_name, config=config, options=options)

                counter += 1

    return links

if __name__ == "__main__":

    """In this test, we will download all the pages from Dynatrace's Cloud Foundry documentation. The reason why we have the regex filter the way it is is because all relevant links in this page come in the form of "/support/help/..." rather than "http://...". This is also why we use "filter = 'suffix'"."""

    # TEST 
    start_html_page = 'https://en.wikipedia.org/wiki/Main_Page'
    root_html_page = 'https://en.wikipedia.org' 
    file_name = "Wikipedia One English"
    folder_name = "test-outputs"
    
    

    # We also do a negative lookahead for feed.xml, as those links are not what we want.

    # Test with Wikipedia non-English main pages accessible from English Wikipedia main page.
    regex_link_filter=r"(?<!en\.)(http(s?)://)(.+)\.wikipedia.org/wiki/(?!feed\.xml)(?!\#)"
    attribute='href'
    html_tag='a'
    max_depth = 0
    current_depth = 0

    download_all_pdf(start_html_page, root_html_page, file_name, folder_name, regex_link_filter, max_depth, attribute, html_tag, options={"window-status":"ready","run-script":"window.setTimeout(function(){window.status='ready';}, 1000);","load-error-handling":"ignore"})

    