import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import gspread
from google.oauth2 import service_account
import requests
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Telegram bot token
TOKEN = '7875240241:AAFYF5ZKsqnMgQhOf9IxrzYr6HjTN_Y9Wy4'

# Google Sheets API credentials
from google.oauth2 import service_account
import gspread

scope = ['https://spreadsheets.google.com/feeds']
credentials = service_account.Credentials.from_service_account_file(
    'C:/Users/Steph/tele/intrepid-seat-436305-t5-634ca9ba8f75.json',
    scopes=scope
)

client = gspread.Client(credentials)
sheet = client.open('Order Information').sheet1
# Photoshop API credentials
api_key = '70e96df4d0ba4e10972d1b6c9dee5f4c'
api_secret = 'p8e-uaLKyOnSwStkP6xpLdIfx-clL08GAPiY'

# Crypto payment verification API credentials
crypto_api_key = 'YOUR_CRYPTO_API_KEY'
crypto_api_secret = 'YOUR_CRYPTO_API_SECRET'

# Define the states for the conversation
SELECT_ITEM, ENTER_FIRST_NAME, ENTER_LAST_NAME, ENTER_STREET, ENTER_CITY, ENTER_STATE, ENTER_ZIP, ENTER_DOB, ENTER_DL_NUMBER, SELECT_EYE_COLOR, SELECT_HAIR_COLOR, SELECT_RESTRICTIONS, SELECT_ENDORSEMENTS, SELECT_SEX, SELECT_HEIGHT = range(15)

# Define the keyboard layouts
item_keyboard = [['SS Card'], ['Cali Drivers License']]
eye_color_keyboard = [['Blue'], ['Green'], ['Hazel'], ['Gray'], ['Brown'], ['Black']]
hair_color_keyboard = [['Brown'], ['Blonde'], ['Black'], ['Red'], ['Gray'], ['Bald'], ['White']]
restrictions_keyboard = [['Corr lens'], ['NONE']]
endorsements_keyboard = [['NONE'], ['Motorcycle']]
height_keyboard = [['5\' 00"'], ['5\' 01"'], ['5\' 02"'], ['5\' 03"'], ['5\' 04"'], ['5\' 05"'], ['5\' 06"'], ['5\' 07"'], ['5\' 08"'], ['5\' 09"'], ['5\' 10"'], ['5\' 11"'], ['6\' 00"'], ['6\' 01"'], ['6\' 02"'], ['6\' 03"'], ['6\' 04"']]
sex_keyboard = [['Male'], ['Female']]

# Define the dictionaries for the keyboard layouts
EYE_COLORS = {
    'Blue': 'Blu',
    'Green': 'Grn',
    'Hazel': 'Hzl',
    'Gray': 'Gry',
    'Brown': 'Brn',
    'Black': 'Blk'
}

HAIR_COLORS = {
    'Brown': 'BRO',
    'Blonde': 'BLD',
    'Black': 'BLK',
    'Red': 'RED',
    'Gray': 'GRY',
    'Bald': 'BAL',
    'White': 'WHI'
}

RESTRICTIONS = {
    'Corr lens': 'Corr lens',
    'NONE': 'NONE'
}

ENDORSEMENTS = {
    'NONE': 'NONE',
    'Motorcycle': 'M'
}

HEIGHTS = {
    '5\' 00"': '60',
    '5\' 01"': '61',
    '5\' 02"': '62',
    '5\' 03"': '63',
    '5\' 04"': '64',
    '5\' 05"': '65',
    '5\' 06"': '66',
    '5\' 07"': '67',
    '5\' 08"': '68',
    '5\' 09"': '69',
    '5\' 10"': '70',
    '5\' 11"': '71',
    '6\' 00"': '72',
    '6\' 01"': '73',
    '6\' 02"': '74',
    '6\' 03"': '75',
    '6\' 04"': '76'
}

SEX = {
    'Male': 'M',
    'Female': 'F'
}

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome! Please select an item to design.', reply_markup=ReplyKeyboardMarkup(item_keyboard, one_time_keyboard=True))
    return SELECT_ITEM

def select_item(update, context):
    item = update.message.text
    context.user_data['item'] = item
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter your first name.', reply_markup=ReplyKeyboardRemove())
    return ENTER_FIRST_NAME

def enter_first_name(update, context):
    first_name = update.message.text
    context.user_data['first_name'] = first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter your last name.')
    return ENTER_LAST_NAME

def enter_last_name(update, context):
    last_name = update.message.text
    context.user_data['last_name'] = last_name
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter your street address.')
    return ENTER_STREET

def enter_street(update, context):
    street = update.message.text
    context.user_data['street'] = street
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter your city.')
    return ENTER_CITY

def enter_city(update, context):
    city = update.message.text
    context.user_data['city'] = city
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter your state.')
    return ENTER_STATE

def enter_state(update, context):
    state = update.message.text
    context.user_data['state'] = state
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter your zip code.')
    return ENTER_ZIP

def enter_zip(update, context):
    zip_code = update.message.text
    context.user_data['zip_code'] = zip_code
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter your date of birth (MM/DD/YYYY).')
    return ENTER_DOB

def enter_dob(update, context):
    dob = update.message.text
    context.user_data['dob'] = dob
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter your driver\'s license number.')
    return ENTER_DL_NUMBER

def enter_dl_number(update, context):
    dl_number = update.message.text
    context.user_data['dl_number'] = dl_number
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please select your eye color.', reply_markup=ReplyKeyboardMarkup(eye_color_keyboard, one_time_keyboard=True))
    return SELECT_EYE_COLOR

def select_eye_color(update, context):
    eye_color = update.message.text
    context.user_data['eye_color'] = EYE_COLORS[eye_color]
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please select your hair color.', reply_markup=ReplyKeyboardMarkup(hair_color_keyboard, one_time_keyboard=True))
    return SELECT_HAIR_COLOR

def select_hair_color(update, context):
    hair_color = update.message.text
    context.user_data['hair_color'] = HAIR_COLORS[hair_color]
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please select any restrictions.', reply_markup=ReplyKeyboardMarkup(restrictions_keyboard, one_time_keyboard=True))
    return SELECT_RESTRICTIONS

def select_restrictions(update, context):
    restrictions = update.message.text
    context.user_data['restrictions'] = RESTRICTIONS[restrictions]
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please select any endorsements.', reply_markup=ReplyKeyboardMarkup(endorsements_keyboard, one_time_keyboard=True))
    return SELECT_ENDORSEMENTS

def select_endorsements(update, context):
    endorsements = update.message.text
    context.user_data['endorsements'] = ENDORSEMENTS[endorsements]
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please select your sex.', reply_markup=ReplyKeyboardMarkup(sex_keyboard, one_time_keyboard=True))
    return SELECT_SEX

def select_sex(update, context):
    sex = update.message.text
    context.user_data['sex'] = SEX[sex]
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please select your height.', reply_markup=ReplyKeyboardMarkup(height_keyboard, one_time_keyboard=True))
    return SELECT_HEIGHT

def select_height(update, context):
    height = update.message.text
    context.user_data['height'] = HEIGHTS[height]
    # Write the data to the Google Sheets spreadsheet
    scope = ['https://spreadsheets.google.com/feeds']
ccredentials = service_account.Credentials.from_service_account_file(
    'C:/Users/Steph/tele/intrepid-seat-436305-t5-634ca9ba8f75.json',
    scopes=['https://spreadsheets.google.com/feeds']
)
client = gspread.authorize(credentials) 
sheet = client.open('Order Information').sheet1
def automate_photoshop(data):
    # Get the PSD file name from the user's input
    psd_file_name = data['item']

    # Open the PSD file in Adobe Creative Cloud
    creativecloud = adobe.creativecloud.CreativeCloud(api_key, api_secret)
    photoshop = creativecloud.photoshop
    document = photoshop.open_document("https://alpha.photoshop.adobe.com/id/urn:aaid:sc:VA6C2:354631dc-1ba2-4d56-b39b-64a101aadca1")

    # Perform actions on the PSD file
    # For example, you could add text to the document
    text_layer = document.layers.add_text_layer('Hello, World!')
    text_layer.text = 'Hello, World!'

    # Save the PSD file to Adobe Creative Cloud
    document.save()