# Schedule Announcer Mate

# Imports

import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build

# Get Structured Date Function
def get_current_structure_date():
    current_datetime = datetime.datetime.now()
    current_day_of_the_month = current_datetime.strftime("%d")
    current_month = current_datetime.strftime("%B")
    current_year = current_datetime.strftime("%Y")
    current_date = f"{current_day_of_the_month} {current_month} {current_year}"
    return current_date

# Google Sheets Variables

credentials = service_account.Credentials.from_service_account_file("../credentials.json", ["https://www.googleapis.com/auth/spreadsheets"])
service = build("sheets", "v4", credentials=credentials)

spreadsheet_id = "1R1ooZQYaSHPByec1VqjOjUUd1SFjH_YsCsgpeZGXssI"

# Getting Schedule Accordingly From Google Sheets


# Current Date


# Dictionary For Announcements With Their Times


# Thread For Checking And Updating Date | Accordingly, Configuring The Dictionary


# Thread For Schedule Announcement For The Day | Going Through The Dictionary, Checking For Each's Time


# Main With Everything Compiled