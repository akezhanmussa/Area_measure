from telegram.ext import Updater, CommandHandler
import requests
import re
import pyrebase
from congif import config
from congif import arduino_id as id 
import numpy as np
import os
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

fb = pyrebase.initialize_app(config)
db = fb.database()

def compute(bot, update):
    
    ref_units = db.child('data').child('arduino_id').child(id).child('units')
    normal_list = []
    total_area = 0    
    data = ref_units.get().val()

    dx = 2.75
    if len(normal_list) == 0:
        for num in data:
            print(num)
            total_area = total_area + (num['Distance'] + 3)*dx
            normal_list.append(num['Distance'] + 3)

    total_area = round(total_area, 2)
    
    
    plt.plot(normal_list, color = 'red')
    plt.title('GRAPH OF MEASURED AREA')
    plt.xlabel('MEASURE INDEX')
    plt.ylabel('THE UNIT OF AREA, CM')

    path_file = os.path.abspath("area.png")
    plt.savefig(path_file)
    area_photo = open('./area.png', 'rb')
    chat_id = update.message.chat_id
    
    message = "{} - the approximated total area of the surrounding region".format(total_area)

    bot.send_message(chat_id, message)
    bot.send_photo(chat_id, area_photo)
    plt.figure()
    plt.hold(False)

def main():
    print("HEHEHDJ")
    updater = Updater('830252631:AAH2uP--6-tYG28kzp9Hcs_pgQkhBlxHYeA')
    dp = updater.dispatcher
    print("ds")
    dp.add_handler(CommandHandler('compute',compute))
    updater.start_polling()
    updater.idle()


def update_line(hl, new_data):
    hl.set_xdata(np.append(hl.get_xdata(), new_data))
    hl.set_ydata(np.append(hl.get_ydata(), new_data))

if __name__ == '__main__':
    main()
