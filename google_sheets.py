import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define Google Sheets API scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from JSON key file
creds = ServiceAccountCredentials.from_json_keyfile_name("heroic-icon-448706-v2-eff3eecaa0a9.json", scope)

# Authorize client
client = gspread.authorize(creds)

# Open the Google Sheet by URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1gK0weajSY21pUznq5AKaGk7zq30HDrcFqiI41EaeO_Q/edit?gid=0#gid=0L"
sheet = client.open_by_url(SHEET_URL).sheet1  # First sheet

# Function to retrieve food list
def get_food_list():
    """Read the current food list from Google Sheets"""
    foods = sheet.col_values(1)  # Read first column
    quantity = sheet.col_values(2) 
    res = [f"{foods[i]} x {quantity[i]}\n" for i in range(1,len(foods)-1)]
    return ''.join(res) if foods else ''  # Skip header row

# Function to add foods
def add_foods(new_foods):
    """Add new foods to Google Sheets"""
    for food in new_foods.split(','):
        sheet.append_row([food.lower()])
    return get_food_list()

# Function to remove foods
def remove_foods(foods_to_remove):
    """Remove foods from Google Sheets"""
    all_foods = get_food_list()
    updated_foods = [food for food in all_foods if food not in foods_to_remove]

    # Clear and rewrite the sheet
    sheet.clear()
    sheet.append_row(["Food Inventory"])  # Add header
    for food in updated_foods:
        sheet.append_row([food])
    
    return updated_foods

print(get_food_list())