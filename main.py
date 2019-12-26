import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import serial
import json
import RPi.GPIO as GPIO

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

# Configure for Google Sheets
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.co$
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Home Sensors").sheet1

with open("info_file.json", "r+") as f:
    data = json.load(f)
    if(data["count"] == 1):
        labels = ['Date', 'Time', 'Humidity', 'Temperature', 'Moisture']
        # FIRST ROW
        sheet.insert_row(labels, 1)
        #print("A new sheet of measurements has begun")
        indexRow = 2
        data["count"] = 2
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    else:
        indexRow = data["count"]
        
        
def main(scope, sheet):

    while(1):
       if creds.access_token_expired:
           client.login()
       try:
           data = ser.readline()
           if(data):
               # Take the current time
               curr_time = str(datetime.datetime.now().time())
               # Split the data
               data = data.decode().split('#')
               # Insert in the first element of the list the time
               data.insert(0, curr_time)
               curr_day = str(datetime.date.today())
               data.insert(0, curr_day)
               # write the row in the Google Sheets
               with open("info_file.json", "r+") as f:
                   idx = json.load(f)
                   sheet.insert_row(data, idx["count"])
                   idx["count"] += 1
                   f.seek(0)
                   json.dump(idx, f, indent=4)
                   f.truncate()
                   #print("The json file has been modified")

       except Exception:
           traceback.print_exc()


if __name__ == "__main__":
    main(scope, sheet)

