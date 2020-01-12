import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import serial
import RPi.GPIO as GPIO
import logging
from pymongo_handler import MongoHandler

# initialize the log settings
logging.basicConfig(filename='app.log', format='%(process)d - %(levelname)s: %(asctime)s - %(message)s', level=logging.INFO)

# Configure the communication with HC-12 board using USART protocol
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ser = serial.Serial(
    port = "/dev/ttyS0",
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )

# initialize MongoHandler object
iot = MongoHandler('<YOUR-PASSWORD>')

# Configure for Google Sheets
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.co$
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Home Sensors").sheet1

# check the first row. If labels not exist then append the labels
if (len(sheet.row_values(1))== 0):
    sheet.append_row(labels)      
        
def main(scope, sheet):
    while(1):
       if creds.access_token_expired:
           logging.info('Access token expired.')
           client.login()
       try:
           data = ser.readline()
           if(data):
               # Split the data
               data = data.decode().split('#')
               data_format_db ={
                                "time": datetime.datetime.now(),
                                "H": float(data[0]),
                                "T": float(data[1]),
                                "M": float(data[2])
                                }
               iot.insert('YOUR_DEVICE_NAME', data_format_db)
               iot.disconnect()
               # Take the current time
               curr_time = str(datetime.datetime.now().time())
               # Insert in the first element of the list the time
               data.insert(0, curr_time)
               # same for date
               curr_day = str(datetime.date.today())
               data.insert(0, curr_day)
               # append row
               sheet.append_row(data)

       except KeyboardInterrupt:
           logging.info("Keyboard Interrupt")
           break

         
if __name__ == "__main__":
    main(scope, sheet)

