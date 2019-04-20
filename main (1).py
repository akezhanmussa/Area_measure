from time import gmtime, strftime
import pyrebase
import json
import time
import serial

arduino_id = 10
apiKey = "AIzaSyCxPmVOXzW9AegWtR2wo_Jqy6iXb6DCXi8"
authDomain =  "temperature-26a3f.firebaseapp.com"
databaseURL = "https://temperature-26a3f.firebaseio.com"
projectId = "temperature-26a3f"
storageBucket = "temperature-26a3f.appspot.com"
messagingSenderId = "437107477072"

# messagingSenderId: "437107477072"
#830252631:AAH2uP--6-tYG28kzp9Hcs_pgQkhBlxHYeA token for bot

config = {
  "apiKey": apiKey,
  "authDomain": authDomain,
  "databaseURL": databaseURL,
  "storageBucket": storageBucket,
  "messagingSenderId":messagingSenderId
}


fb = pyrebase.initialize_app(config)
db = fb.database()


def fetch_data():
    
    arduino = serial.Serial("COM7", baudrate=9600)

    arduino.flushInput()
    arduino.flushOutput()
    data = arduino.readline()
    arduino.flushInput()
    arduino.flushOutput()
    json_decoded = json.loads(data.decode('utf8'))
    print(json_decoded)
    return json_decoded


def updatedb():
    active = db.child('data').child('arduino_id').child(arduino_id).get().val()

    if(active['flag'] != 1):
        isInitial = True
        db.child('data').child('arduino_id').child(arduino_id).child('flag').set(1)
    else:
        isInitial = False

    new_data = fetch_data()
    print(new_data)

    if(new_data):
        if(isInitial):
            push_array = [new_data]
            db.child('data').child('arduino_id').child(arduino_id).child('units').set(push_array)
        else:
            push_array = db.child('data').child('arduino_id').child(arduino_id).child('units').get().val()
            if(len(push_array) >= 100):
                push_array.pop(0)
            push_array.append(new_data)


            db.child('data').child('arduino_id').child(arduino_id).child('units').set(push_array)


while (True):
    updatedb()
