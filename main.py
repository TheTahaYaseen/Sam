# Schedule Announcer Mate

# Imports
import datetime


# Get Structured Date Function
def get_current_structure_date():
    current_datetime = datetime.datetime.now()
    current_day_of_the_month = current_datetime.strftime("%d")
    current_month = current_datetime.strftime("%B")
    current_year = current_datetime.strftime("%Y")
    current_date = f"{current_day_of_the_month} {current_month} {current_year}"
    return current_date

# Getting Schedule Accordingly From Google Sheets


# Current Date


# Dictionary For Announcements With Their Times


# Thread For Checking And Updating Date | Accordingly, Configuring The Dictionary


# Thread For Schedule Announcement For The Day | Going Through The Dictionary, Checking For Each's Time


# Main With Everything Compiled