import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define Google Sheets API scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from Replit Secrets (or other env variables)
google_sheets_key = os.getenv("GOOGLE_SHEETS_KEY")

if google_sheets_key:
    key_dict = json.loads(google_sheets_key)  # Convert string back to JSON
else:
    raise ValueError("Google Sheets API key is missing!")

# Authenticate with Google Sheets
creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
client = gspread.authorize(creds)

# Open the Google Sheet by URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1gK0weajSY21pUznq5AKaGk7zq30HDrcFqiI41EaeO_Q/edit"
sheet = client.open_by_url(SHEET_URL).sheet1  # First sheet

# Function to retrieve food list with quantities
def get_food_list():
    """Read the current food list and their quantities from Google Sheets"""
    foods = sheet.col_values(1)  # Read first column (Food)
    quantities = sheet.col_values(2)  # Read second column (Quantity)

    if len(foods) < 2 or len(quantities) < 2:
        return "🛒 Your food inventory is empty!"

    # Combine food names with quantities, skipping the header row
    res = [f"{foods[i]} x {quantities[i]}" for i in range(1, len(foods))]
    return "\n".join(res)
