# Pull in external libraries, if you don't have these in your coding environment you'll need to install them
import PySimpleGUI as sg
from pathlib import Path
import logging
import configparser
import requests
import json

#Pull in from an external configuration file to make it easier to make fiddly changes
config = configparser.ConfigParser()
config.read("question_logger_config.ini")

#Parameters! 
#Screenx and Screeny set the initial position of the window (otherwise default is center of screen)
#The workstation name was just so I could trace back to which computer sent the data
workstation = config.get("main", "workstation")
screenx = config.get("main", "screenposition_x")
screeny = config.get("main", "screenposition_y")

#Sets a menu that appears by right-clicking on the window to show a hidden "Exit" option to close the widget
menu_right_click = ['', ['Exit']]

#Sets up logging so if there's a problem you can trace it back
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, filename= f"{workstation}_transactions.log", datefmt='%Y-%m-%d %H:%M:%S')


#The main function that takes variables from the widget and passes them through to LibInisght
def send_to_libinsight(questiontype, workstation, extrainfo):
    
    #Get your request URL and token from LibInsight API settings. Springshare documentation is here: https://ask.springshare.com/libinsight/faq/2100 
    request_url = "[ENTER YOUR SPRINGSHARE API URL WITH TOKEN HERE]"

    #Get field names from LibInsight API code (Manage Widgets -> [Dataset] -> View Code )
    #These are just the ones I have with the fields that were relevant to my dataset as an example. Yours will likely differ.
    data_payload = {
        'field_4': questiontype,
        'field_5': extrainfo,
        'field_7': workstation
        }
    
    #Sends the JSON data to the API request URL
    record = requests.post(
        request_url,
        data=data_payload
        )
    
    #Checks response to make sure data was sent successfully
    return_data = {}
    fullstatus = json.loads(record.text)
    callstatus = fullstatus['response']

    if callstatus == 1:
        # Success
        responsestatus = "Submitted"
    else:
        responsestatus = "Failed"
    
    return responsestatus

#Configures the layout of the main window using PySimpleGUI
def main_window():
    layout = [
        [sg.T('Log Questions Here:', justification='c')],
        [sg.HorizontalSeparator()],

        [sg.T('Additional Information: (optional)')],
        
        [sg.Input(default_text='', do_not_clear=False, s=40, key='-EXTRA_INFO-')],
        
        [sg.Button('Directions', s=12), sg.Button('Technology', s=12), sg.Button('Printing', s=12)],
        
        [sg.Button('Finding Books', s=12), sg.Button('Other', s=12),]]



    window_title = "Question Tracker"

#Pulls in the window layout, title, location (from the parameters), secret right-click menu, and other settings to actually make the window
    window = sg.Window(window_title, layout, keep_on_top=True, location=(screenx, screeny), no_titlebar=True, grab_anywhere=True, right_click_menu=menu_right_click, finalize=True)

#The magic (While the program is running and the window is open, the program will respond to interactions with the window)
    while True:
        event, values = window.read()
        
        #If the window is closed or "Exit" is selected from the secret right-click menu, the program closes
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break

        #The next several are how the program handles the button presses. They're basically all the same except the question type is different (for categorization purposes)
        if event == 'Directions':
            questiontype = "Directional"
            responsestatus = send_to_libinsight(questiontype, workstation, extrainfo=values['-EXTRA_INFO-'])
            logging.info(f"Type: {questiontype}, Additional info: {values['-EXTRA_INFO-']}, Response: {responsestatus}")

        if event == 'Printing':
            questiontype = "Printing"
            responsestatus = send_to_libinsight(questiontype, workstation, extrainfo=values['-EXTRA_INFO-'])
            logging.info(f"Type: {questiontype}, Additional info: {values['-EXTRA_INFO-']}, Response: {responsestatus}")

        if event == "Technology":
            questiontype = "Technology"
            responsestatus = send_to_libinsight(questiontype, workstation, extrainfo=values['-EXTRA_INFO-'])
            logging.info(f"Type: {questiontype}, Additional info: {values['-EXTRA_INFO-']}, Response: {responsestatus}")


        if event == "Finding Books":
            questiontype = "Finding Books"
            responsestatus = send_to_libinsight(questiontype, workstation, extrainfo=values['-EXTRA_INFO-'])
            logging.info(f"Type: {questiontype}, Additional info: {values['-EXTRA_INFO-']}, Response: {responsestatus}")

        if event == "Other":
            questiontype = "Other"
            responsestatus = send_to_libinsight(questiontype, workstation, extrainfo=values['-EXTRA_INFO-'])
            logging.info(f"Type: {questiontype}, Additional info: {values['-EXTRA_INFO-']}, Response: {responsestatus}")

        #Redundant extra code to make sure if the window is closed the program will exit.
        if event == sg.WIN_CLOSED or event == 'Quit':
            break

    window.close()

#The thing that actually runs the window and sets global parameters for the theme and appearance. 
if __name__ == '__main__':
    SETTINGS_PATH = Path.cwd()
    theme = 'TealMono'
    font_family = 'Arial'
    #Sets value as integer
    font_size = 12
    sg.theme(theme)
    sg.set_options(font=(font_family, font_size))
    main_window()
    