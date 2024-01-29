# Question Tracker Widget
Small desktop widget built in Python using PySimpleGUI to make it easier for desk staff to track simple questions 

# About
This widget comes in two flavors: Original (appends data to a monthly .csv file) and LibInsight (sends data to Springshare's LibInsight API to go right into a dataset of your choosing).

Both versions share a front-end interface built using PySimpleGUI (https://www.pysimplegui.org/en/latest/). The widget is designed to be kept on top of all other windows `(keep_on_top = True)` and the standard title bar is not displayed `(no_titlebar = True)`. It's designed to make it hard to ignore while also being mostly unobtrusive. To close the widget, right-clicking on the window will bring up a menu with the Exit command. 

Each of the buttons is labeled for a different category of question, and the resulting data (either in CSV or what's pushed to LibInsight) contains the category as well as any additional entered information. 

# To-CSV Version
Much more cumbersome than the LibInsight version, but simpler to get working (because you don't need to have or configure LibInsight). 
- This version creates a monthly .csv file and writes to it over the month. 
- It will always check for the prescense of a file in the current directory with correct name format including the month.
- If it doesn't find one that matches (like at the start of a new month) it will create a new one.
- You can then do whatever you want with the resulting .csv files.

# To-LibInsight Version
This version takes the input and sends it to a specified LibInsight Dataset. Springshare has detailed instructions on how to set up a token and work with their API here: https://ask.springshare.com/libinsight/faq/2100

There is a placeholder in the code (line 31) to enter the POST URL, which should look something like:
https://YOURDOMAIN.libinsight.com/add.php?wid=#&type=#&token=API_TOKEN_STRING

- You must have a corresponding dataset for the data to go to (when you set up the API access you will associate it with that dataset)
- To view what the fields are listed as in the system go to:
  - "Widgets and APIs"
  - Find the API you set up for this
  - Click on the ... icon at the end of the row
  - Select "View Code" to see the sample data and JSON schema
- Your field names in the JSON data **MUST MATCH** the sample data described above. In the posted code they're listed as "field_4", "field_5", and "field_7" but yours may differ. 
- It does seem that Springshare updated this recently, this is set to follow the "Legacy" instructions

## About My LibInsight Dataset
If you're curious, my dataset is set up as:
- Type: Reference
- Users can add more than one at a time: No
- Limit "Entered by": No
- Automatically calculate timestamp
- Dataset fields:
  - Timestamp (automatically added, required)
  - Question type (single select, required)
    - Choices for single select correspond to the buttons and variables in my code
  - Additional info (text, optional)
    - From the free text that users can enter in the widget
  - Workstation (single select, optional)
    - Choices for single select correspond to the defined workstation names in the config for each workstation
