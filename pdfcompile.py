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

    # COMMON SOURCE FILE
    input_file = "Dynatrace Documentation Compiled for Associate Certification.pdf"

    #all_pages = []
    file_string = "10-1"
    print(make_list_of_pages_from_string(file_string))
    """
    all_pages.extend([x for x in range(17, 19)])
    all_pages.extend([x for x in range(20, 21)])
    # 1. Application Monitoring
    all_pages.extend([x for x in range(165, 167)])
    all_pages.extend([x for x in range(568, 569)])
    
    #From the hyperlinks, this is just Real User Monitoring
    #     a. Web
    
    #     b. Mobile
    #     c. Enterprise
    #     d. SaaS
    #     e. Performance Analysis
    #         i. Actions
    # TODO See below: all_pages.extend([x for x in range(269, 272)])

    #         ii. Metrics
    #TODO See 273 onwards below

    #         iii. JavaScript errors
    #TODO See also 255 onwards below
    all_pages.extend([x for x in range(266, 268)])

    #         iv. 3rd party providers
    #     f. Business Insights
    #         i. Business Transaction Monitoring
    all_pages.extend([x for x in range(462, 467)])
    all_pages.extend([x for x in range(549, 551)])
    all_pages.extend([x for x in range(894, 897)])
    #         ii. PurePath Technology
    all_pages.extend([x for x in range(513, 525)])
    all_pages.extend([x for x in range(526, 528)])
    
    # 2. Network Monitoring
    #     a. Traffic
    #     b. Retransmissions
    #     c. Connectivity
    all_pages.extend([x for x in range(708, 714)])
    all_pages.extend([x for x in range(715, 718)])

    # 3. Full Stack Monitoring
    #     a. Application Discovery
    #         i. Smartscape
    #             A. Dependencies
    #             B. Topology
    all_pages.extend([x for x in range(927, 933)])
    
    #     b. Infrastructure Monitoring
    all_pages.extend([x for x in range(650, 651)])
    all_pages.extend([x for x in range(652, 653)])
    #         i. Hosts
    #             A. Process Groups
    all_pages.extend([x for x in range(654, 655)])
    
    #                 I. Services
    #                     (1) Service Flow
    
    all_pages.append(282)
    all_pages.extend([x for x in range(500, 506)])
    all_pages.extend([x for x in range(509, 512)])
    #                     (2) Service Types
    #                 II. Processes
    #TODO

    #             B. Host Health
    all_pages.extend([x for x in range(662, 664)])
    all_pages.extend([x for x in range(665, 670)])
    #         ii. Databases
    #             A. Response Time
    all_pages.extend([x for x in range(875, 877)])
    all_pages.extend([x for x in range(491, 494)])
    all_pages.extend([x for x in range(494, 497)])
    #             B. Load and Failure Rate
    all_pages.extend([x for x in range(482, 490)])
    all_pages.extend([x for x in range(812, 822)])
    #         iii. Log Files
    #             A. Log Monitoring
    all_pages.extend([x for x in range(671, 672)])
    all_pages.extend([x for x in range(673, 686)])
    #         iv. Virtual Machines
    all_pages.extend([x for x in range(673, 686)])
    #         v. PaaS
    #TODO
    #     c. Artificial Intelligence
    #TODO

    # 4. Digital Experience Management (DEM)
    #     a. Availability Monitoring
    #         i. Synthetic Monitoring
    all_pages.append(319)
    all_pages.append(331)
    all_pages.extend([x for x in range(389, 396)])
    #             A. Browser Clickpath
    all_pages.extend([x for x in range(352, 358)])
    all_pages.extend([x for x in range(337, 342)])
    all_pages.extend([x for x in range(369, 372)])
    #             B. Browser Monitor
    all_pages.extend([x for x in range(343, 352)])
    all_pages.append(367)
    #             C. HTTP Monitor
    all_pages.extend([x for x in range(372, 375)])
    all_pages.extend([x for x in range(376, 380)])
    
    #     b. Real User Monitoring
    #         i. User sessions
    #             A. Charts
    all_pages.extend([x for x in range(253, 255)])
    
    #             B. Details
    all_pages.extend([x for x in range(256, 260)])
    all_pages.extend([x for x in range(261, 266)])
    
    #             C. Actions
    #                 I. Entry
    #                 II. Exit
    
    #                 III. Key
    all_pages.extend([x for x in range(269, 271)])
    #                 IV. Metrics
    all_pages.extend([x for x in range(272, 274)])
    all_pages.extend([x for x in range(276, 278)])
    all_pages.extend([x for x in range(279, 280)])
    all_pages.extend([x for x in range(281, 282)])
    all_pages.extend([x for x in range(286, 288)])
    all_pages.extend([x for x in range(290, 292)])
    #         ii. Configuration Options
    all_pages.extend([x for x in range(225, 228)])
    #         iii. Tagging
    all_pages.extend([x for x in range(315, 317)])
    #         iv. User behaviour analytics
    #             A. Sessions
    all_pages.extend([x for x in range(300, 302)])
    all_pages.extend([x for x in range(313, 314)])
    #                 I. Session Replay
    all_pages.extend([x for x in range(195, 197)])
    all_pages.extend([x for x in range(221, 222)])
    all_pages.extend([x for x in range(213, 216)])
    #             B. Bounce Rate
    #             C. Conversion

    all_pages.extend([x for x in range(274, 275)])
    all_pages.append(155)
    
    # 5. Configuration
    #     a. Installation
    #         i. ActiveGate
    all_pages.extend([x for x in range(21, 22)])
    all_pages.extend([x for x in range(23, 24)])
    all_pages.extend([x for x in range(24, 26)])
    all_pages.extend([x for x in range(28, 29)])
    all_pages.extend([x for x in range(41, 42)])
    all_pages.extend([x for x in range(59, 60)])
    #             A. Environment
    all_pages.extend([x for x in range(53, 54)])
    all_pages.extend([x for x in range(61, 64)])
    all_pages.extend([x for x in range(68, 71)])
    
    #             B. Cluster

    #https://www.dynatrace.com/support/help/setup-and-configuration/dynatrace-managed/installation/how-to-install-a-cluster-activegate/

    #         ii. OneAgent

    all_pages.extend([x for x in range(1, 2)])
    all_pages.extend([x for x in range(9, 11)])
    all_pages.extend([x for x in range(11, 13)])
    all_pages.extend([x for x in range(13, 14)])
    all_pages.extend([x for x in range(15, 17)])
    #         iii. Agentless RUM

    all_pages.extend([x for x in range(157, 160)])
    #         iv. RUM browser extension
    all_pages.extend([x for x in range(161, 164)])
    #     b. System Settings
    #         i. Global settings
    all_pages.extend([x for x in range(537, 538)])
    all_pages.extend([x for x in range(539, 549)])
    #             A. Monitoring
    #                 I. Web and Mobile
    #                 II. Server-side service
    all_pages.extend([x for x in range(537, 538)])

    #             B. Tagging
    all_pages.extend([x for x in range(934, 935)])
    all_pages.extend([x for x in range(936, 938)])
    all_pages.extend([x for x in range(939, 942)])
    #             C. Preferences
    #                 I. Updates
    #     c. Entity
    all_pages.extend([x for x in range(779, 780)]) #an "entity" is any host, service, or process monitored by Dynatrace)
    #         i. Hosts

    #         ii. Databases
    all_pages.extend([x for x in range(601, 611)])
    #         iii. Applications
    #         iv. Process Groups
    #             A. Services
    all_pages.extend([x for x in range(611, 614)])
    all_pages.extend([x for x in range(615, 616)])
    all_pages.extend([x for x in range(617, 621)])
    all_pages.extend([x for x in range(637, 640)])
    #         v. Tagging
    #TODO See others
    # 6. Data
    #     a. Dashboards
    #         i. Tiles
    #         ii. Charting
    all_pages.append(719)
    all_pages.extend([x for x in range(721, 727)])
    all_pages.extend([x for x in range(732, 742)])
    all_pages.append(749)
    
    #     b. Reports
    #         i. Availability
    
        #TODO

    #         ii. Service Quality
    all_pages.extend([x for x in range(751, 754)])

    #     c. Dynatrace Mobile Application
    
    all_pages.append(447) 

        # OneAgent for Mobile starts with monitoring disabled. Monitoring must then be enabled manually via an API call for each user.

    #     d. Retention
    
    all_pages.extend([x for x in range(431, 438)])
    all_pages.extend([x for x in range(869, 871)]) # Must do triage within 14 days of problem detection

    # 7. Problems
    #     a. Detection
    #         i. Baselines
    
    all_pages.extend([x for x in range(837, 840)]) 
    all_pages.extend([x for x in range(866, 868)])
    all_pages.extend([x for x in range(875, 879)])
    all_pages.extend([x for x in range(879, 881)])
    all_pages.extend([x for x in range(881, 883)])
    all_pages.extend([x for x in range(908, 912)])
    
    #     b. Resolution
    #         i. Root Cause Analysis
    all_pages.extend([x for x in range(838, 840)])
    all_pages.extend([x for x in range(897, 899)])
    all_pages.extend([x for x in range(903, 907)])
    #     c. Events
    all_pages.extend([x for x in range(840, 841)])
    all_pages.extend([x for x in range(842, 846)])
    all_pages.extend([x for x in range(848, 851)])
    all_pages.extend([x for x in range(853, 857)])
    all_pages.extend([x for x in range(858, 863)])
    all_pages.extend([x for x in range(863, 866)])
    all_pages.extend([x for x in range(900, 903)])
    #     d. Anomaly Detection
    all_pages.extend([x for x in range(884, 888)])
    all_pages.extend([x for x in range(888, 891)])


    # ALERTS
    all_pages.extend([x for x in range(912, 916)]) 

    print(all_pages)
    print(len(all_pages))
    print(879 in all_pages)
    print(all_pages.index(875))

    rearrange_pdf(input_file, all_pages, "Dynatrace Documentation for Associate Compiled and Cut.pdf")
"""
'''
MindMap:
1. Application Monitoring
    a. Web
    b. Mobile
    c. Enterprise
    d. SaaS
    e. Performance Analysis
        i. Actions
        ii. Metrics
        iii. JavaScript errors
        iv. 3rd party providers
    f. Business Insights
        i. Business Transaction Monitoring
        ii. PurePath Technology

2. Network Monitoring
    a. Traffic
    b. Retransmissions
    c. Connectivity

3. Full Stack Monitoring
    a. Application Discovery
        i. Smartscape
            A. Dependencies
            B. Topology
    b. Infrastructure Monitoring
        i. Hosts
            A. Process Groups
                I. Services
                    (1) Service Flow
                    (2) Service Types
                II. Processes
            B. Host Health
        ii. Databases
            A. Response Time
            B. Load and Failure Rate
        iii. Log Files
            A. Log Monitoring
        iv. Virtual Machines
        v. PaaS
    c. Artificial Intelligence

4. Digital Experience Management (DEM)
    a. Availability Monitoring
        i. Synthetic Monitoring
            A. Browser Clickpath
            B. Browser Monitor
            C. HTTP Monitor
    b. Real User Monitoring
        i. User sessions
            A. Charts
            B. Details
            C. Actions
                I. Entry
                II. Exit
                III. Key
                IV. Metrics
        ii. Configuration Options
        iii. Tagging
        iv. User behaviour analytics
            A. Sessions
                I. Session Replay
            B. Bounce Rate
            C. Conversion

5. Configuration
    a. Installation
        i. ActiveGate
            A. Environment
            B. Cluster
        ii. OneAgent
        iii. Agentless RUM
        iv. RUM browser extension
    b. System Settings
        i. Global settings
            A. Monitoring
                I. Web and Mobile
                II. Server-side service
            B. Tagging
            C. Preferences
                I. Updates
    c. Entity
        i. Hosts
        ii. Databases
        iii. Applications
        iv. Process Groups
            A. Services
        v. Tagging

6. Data
    a. Dashboards
        i. Tiles
        ii. Charting
    b. Reports
        i. Availability
        ii. Service Quality
    c. Dynatrace Mobile Application
    d. Retention

7. Problems
    a. Detection
        i. Baselines
    b. Resolution
        i. Root Cause Analysis
    c. Events
    d. Anomaly Detection

        
'''
