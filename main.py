# Schedule Announcer Mate

# Imports

import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build

from threading import Thread

import pyttsx3

import time

# Get Structured Date Function
def get_current_structured_date():
    current_datetime = datetime.datetime.now()
    current_day_of_the_month = current_datetime.strftime("%d")
    current_month = current_datetime.strftime("%B")
    current_year = current_datetime.strftime("%Y")
    current_date = f"{current_day_of_the_month} {current_month} {current_year}"
    return current_date

# Get Structured Time Function
def get_current_structured_time():
    current_datetime = datetime.datetime.now()
    current_hour = current_datetime.strftime("%H")
    current_minute = current_datetime.strftime("%M")
    current_time = f"{current_hour}:{current_minute}"
    return [current_time, current_hour] 

# pyttsx3 Variables

saying_engine = pyttsx3.init()
saying_engine.setProperty("rate", 200)

speaker_voices = saying_engine.getProperty("voices")
saying_engine.setProperty("voice", speaker_voices[1].id)

# For Sam To Be Able To Speak 
def speak(thing_to_say):
    saying_engine.say(thing_to_say)
    saying_engine.runAndWait()

# Google Sheets Variables

credentials = service_account.Credentials.from_service_account_file("../credentials.json",  scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build("sheets", "v4", credentials=credentials)

spreadsheet_id = "1R1ooZQYaSHPByec1VqjOjUUd1SFjH_YsCsgpeZGXssI"

# Getting Schedule Accordingly From Google Sheets
def get_schedule(schedule_date):
    sheet_name = schedule_date
    schedule_range = f"{sheet_name}!B3:D290"

    # Response Structure
    # response = {values: arrays_of(time, task, task_details)}

    response = service.spreadsheets().values().get(spreadsheetId = spreadsheet_id, range = schedule_range).execute()
    return response

# Dictionary For Announcements With Their Times

# Structure = {"time": {"task": "task details"}}
CURRENT_SCHEDULE = {}
SAYING_QUEUE = []

# Function For Populating Global Schedule Dictionary With A Proper Format

def populate_current_schedule(schedule_to_populate_with):
    
    global CURRENT_SCHEDULE
    
    schedule_values = schedule_to_populate_with["values"]
    
    current_hour = get_current_structured_time()[1]

    for schedule_value in schedule_values:

        length_of_schedule_value_array = len(schedule_value)

        if length_of_schedule_value_array != 1:
            task_time = schedule_value[0]
            task = schedule_value[1]

            task_hour = task_time.split(":")[0]

            if task_hour >= current_hour:

                if length_of_schedule_value_array == 3:
                    task_detail = schedule_value[2]
                    CURRENT_SCHEDULE[task_time] = f"{task}, {task_detail}"
                else:
                    CURRENT_SCHEDULE[task_time] = f"{task}"

# Thread For Properly Announcing
def announcing_stuff():
    
    global SAYING_QUEUE

    while True:
        for thing_to_say in SAYING_QUEUE:
            speak(thing_to_say)

announcing_stuff_thread = Thread(target=announcing_stuff)

# Thread For Checking And Updating Date | Accordingly, Configuring The Dictionary

# To Check:
    # Date Changes
    # New Changes In Sheet

def keeping_schedule_up_to_date():
    
    previous_date = get_current_structured_date()
    previous_schedule = get_schedule(previous_date)

    populate_current_schedule(previous_schedule)

    while True:

        new_date = get_current_structured_date()
        new_schedule = get_schedule(new_date)

        if new_date != previous_date:

            populate_current_schedule(new_schedule)
            previous_date = new_date

        else:

            if new_schedule != previous_schedule:
                populate_current_schedule(new_schedule)
                previous_schedule = new_schedule

        time.sleep(2)
    
thread_for_keeping_schedule_up_to_date = Thread(target=keeping_schedule_up_to_date)

# Thread For Schedule Announcement For The Day | Going Through The Dictiornary, Checking For Each's Time

def pushing_schedule_to_announcement():
    
    global CURRENT_SCHEDULE, SAYING_QUEUE

    while True:
        
        current_time = get_current_structured_time()[0]
        
        for task_time, task_announcement in CURRENT_SCHEDULE.items():
            
            if current_time == task_time:
                for iteration in range(3):
                    SAYING_QUEUE.append(task_announcement)

pushing_schedule_to_announcement = Thread(target=pushing_schedule_to_announcement)

# Main With Everything Compiled

if __name__ == "__main__":
    announcing_stuff_thread.start()
    thread_for_keeping_schedule_up_to_date.start()
    pushing_schedule_to_announcement.start()