# Pull in external libraries, if you don't have these in your coding environment you'll need to install them
import PySimpleGUI as sg
from pathlib import Path
import os
import datetime
from datetime import date
import pandas as pd
import configparser

#Gets the working directory so it knows where the CSV output file will go
working_directory = os.getcwd()

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


#Check that output file I want to use is there, if not, create it
def outputfile_check (outputname):
    path = (f"./{outputname}.csv")
    check_file = os.path.isfile(path)
    print(path)
    print(check_file)

    if check_file == False:
        pd.DataFrame(columns=['Log Date', 'Question Type', 'Additional Info']).to_csv(f"{outputname}.csv", index=False)

#Checks that the filepath is there in the first place
def is_valid_path(filepath):
    if filepath and Path(filepath).exists():
        return True
    sg.popup_error('Missing File Path')
    return False

#The main function that takes variables from the widget and appends them to a .csv file
def question_collector(outputname, questiontype, extrainfo):
    #Define empty dictionary for later
    dict = {}
    dict['logdate'] = []
    dict['question type'] = []
    dict['additional info'] = []

    #Calculate the timestamp using Datetime and add to dictionary
    fulltime = datetime.datetime.now()
    logdate = fulltime.strftime("%Y-%m-%d %H:%M")
    dict['logdate'].append(logdate)

    #Append question type to dictionary
    dict['question type'].append(questiontype)

    #If there were extra details entered, append those to the dictionary, otherwise just put a blank string
    if len(extrainfo) == 0:
        extrainfo = str(" ")
    dict['additional info'].append(extrainfo)

    #Turn that dictionary into the world's smallest dataframe
    df = pd.DataFrame(dict)

    #Append that dataframe to the existing .csv file
    df.to_csv(f"{outputname}.csv", mode='a', index=False, header=False)

#Configures the layout of the main window using PySimpleGUI
def main_window():
    layout = [
        [sg.T('Log Questions Here:', justification='c')],
        [sg.HorizontalSeparator()],

        [sg.T('Additional Information: (optional)')],
        
        [sg.Input(default_text='', do_not_clear=False, s=26, key='-EXTRA_INFO-')],
        
        [sg.Button('Directions', s=12), sg.Button('Technology', s=12)],
        
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
            question_collector(outputname, questiontype, extrainfo=values['-EXTRA_INFO-'])

        if event == "Technology":
            questiontype = "Technology"
            question_collector(outputname, questiontype, extrainfo=values['-EXTRA_INFO-'])

        if event == "Finding Books":
            questiontype = "Finding Books"
            question_collector(outputname, questiontype, extrainfo=values['-EXTRA_INFO-'])

        if event == "Other":
            questiontype = "Other"
            question_collector(outputname, questiontype, extrainfo=values['-EXTRA_INFO-'])

        #Redundant extra code to make sure if the window is closed the program will exit.
        if event == sg.WIN_CLOSED or event == 'Quit':
            break

    window.close()

#Sets default filename for monthly .csv file (would look something like "workstation 1-2023-06.csv" if it was June 2023)
outputname = workstation + "-" + date.today().strftime("%Y-%m")


#The thing that actually runs the window and sets global parameters for the theme and appearance.
if __name__ == '__main__':
    SETTINGS_PATH = Path.cwd()
    theme = 'TealMono'
    font_family = 'Arial'
    #Sets value as integer
    font_size = 12
    sg.theme(theme)
    sg.set_options(font=(font_family, font_size))
    outputfile_check(outputname)
    main_window()
    