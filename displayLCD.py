#!/usr/bin/env python3
import time, datetime, sys, os
import threading
from tkinter import *
import random
import mysql.connector

#init db
db = mysql.connector.connect(
    host = "localhost",
    user = "client",
    passwd = "raspi",
    database= "iot_trafo_client")

#init tkinter
screen = Tk()
screen.title("IoT Trafo GUI")
screen.attributes('-fullscreen', True)
screen.configure(background = "#ffffff")
screen.attributes('-topmost', 1)
dataBank = [0]*53
statusBank = [3]*31
diBank = [0]*5

delayTime = 2

def Stop():
    global progStat
    progStat = False
    screen.destroy()

def RetrieveData():
    global dataBank, statusBank, diBank
    cursor0 = db.cursor()
    
    sql0 = "SELECT * FROM reading_data ORDER by data_id DESC LIMIT 1"
    cursor0.execute(sql0)
    a = cursor0.fetchall()[0]
    
    sql1 = "SELECT * FROM transformer_status"
    cursor0.execute(sql1)
    b = cursor0.fetchall()[0]
    
    sql2 = "SELECT state FROM di_scan WHERE number=0"
    cursor0.execute(sql2)
    c = cursor0.fetchall()[0]

    sql3 = "SELECT state FROM di_scan WHERE number=1"
    cursor0.execute(sql3)
    d = cursor0.fetchall()[0]

    sql4 = "SELECT state FROM di_scan WHERE number=2"
    cursor0.execute(sql4)
    e = cursor0.fetchall()[0]

    sql5 = "SELECT state FROM di_scan WHERE number=3"
    cursor0.execute(sql5)
    f = cursor0.fetchall()[0]

    sql6 = "SELECT state FROM di_scan WHERE number=4"
    cursor0.execute(sql6)
    g = cursor0.fetchall()[0]
    db.commit()

    diBank = list(c) + list(d) + list(e) + list(f) + list(g)
    for i in range(0, len(diBank)):
        if diBank[i] == 0:
            diBank[i] = "Inactive"
        else :
            diBank[i] = "Active"
    print(diBank)
    statusBank = list(b)
    statusBank.pop(0)
    for i in range(0, 31):
        if statusBank[i] == 3 or statusBank[i] == 0:
                statusBank[i] = "Safe"
        elif statusBank[i] == 1:
                statusBank[i] = "Low Trip"
        elif statusBank[i] == 2:
                statusBank[i] = "Low Alarm"
        elif statusBank[i] == 4:
                statusBank[i] = "High Alarm"
        elif statusBank[i] == 5:
                statusBank[i] = "High Trip"
    dataBank = list(a)
    dataBank.pop(0)
    dataBank.pop(0)
    for i in range(0, 34):
        dataBank[i] = (round(dataBank[i]*1000))/1000
    for i in range(38, 46):
        dataBank[i] = (round(dataBank[i]*1000))/1000
    if dataBank[46] == 0:
        dataBank[46] = "safe"
    elif dataBank[46] == 1:
        dataBank[46] = "low"
    elif dataBank[46] == 2: 
        dataBank[46] = "ext. low"

def mainLoop(thread_name, interval):
    while True:
        RetrieveData()
        #Page 1 - 3
        firstLbl['text'] = "Oil Temp. : " + str(dataBank[41]) + " C"
        secondLbl['text'] = "Oil Lvl Stat. : " + str(dataBank[46])
        #thirdLbl['text'] = "Bucholz Relay Stat. : Safe"
        #fourthLbl['fg'] = '#0096FF'
        for i in range(1, 4):
            #fourthLbl['text']  = "H2 / Moisture : " + str((random.randint(100, 7500))/100) + " ppm / " + str((random.randint(100, 5000))/100) + " ppm"
            thirdLbl['text'] = "Busbar Temp. phase " + str(i) + " : " + str(dataBank[i + 37]) + " C"
            fourthLbl['text'] = "Winding Temp. phase " + str(i) + " : " + str(dataBank[i + 41]) + " C"
            fifthLbl['text'] = "KRated phase " + str(i) + " : " + str(dataBank[((i-1)*2) + 47])
            sixthLbl['text'] = "Max Load phase " + str(i) + " : " + str(dataBank[((i-1)*2) + 48]) + " %"
            #seventhLbl['text'] = "Current Load phase " + str(i) + " : " + str(dataBank[((i-1)*9) + 8]) + " A"
            #ninthLbl['text'] = "Winding Temp. phase " + str(i) + " : " + str((random.randint(400, 500))/10) + " C"
            scrollLbl['text'] = "page " + str(i) +"/7"
            time.sleep(delayTime)
        #Page 4 - 6
        Vlib = ["ab", "bc", "ac"]
        fourthLbl['fg'] = '#000'
        for i in range(1, 4):
            firstLbl['text'] = "Vtg p-n phase " + str(i) + " : " + str(dataBank[i - 1]) + " V"
            secondLbl['text'] = "Vtg p-p phase " + Vlib[i-1] + " : " + str(dataBank[i + 2]) + " V"
            thirdLbl['text'] = "Current phase " + str(i) + " : " + str(dataBank[i + 5]) + " A"
            fourthLbl['text'] = "Power Factor phase " + str(i) + " : " + str(dataBank[i + 28])
            fifthLbl['text'] = "Active Power phase " + str(i) + " : " + str(dataBank[i + 16]) + " W"
            sixthLbl['text'] = "Reactive Power phase " + str(i) + " : " + str(dataBank[i + 20]) + " VAR"
            seventhLbl['text'] = "Apparent Power phase " + str(i) + " : " + str(dataBank[i + 24]) + " VA"
            eighthLbl['text'] = "THD V phase " + str(i) + " : " + str(dataBank[i + 10]) + " %"
            ninthLbl['text'] = "THD I phase " + str(i) + " : " + str(dataBank[i + 13]) + " %"
            scrollLbl['text'] = "page " + str(i+3) +"/7"
            time.sleep(delayTime)
        #Page 7
        firstLbl['text'] = "Total Current : " + str(dataBank[9]) + " A"
        secondLbl['text'] = "System Power Factor : " + str(dataBank[32])
        thirdLbl['text'] = "Total Active Power : " + str(dataBank[20]) + " W"
        fourthLbl['text'] = "Total Reactive Power : " + str(dataBank[24]) + " VAR"
        fifthLbl['text'] = "Total Apparent Power : " + str(dataBank[28]) + " VA"
        sixthLbl['text'] = "System Frequency : " + str(dataBank[33]) + " Hz"
        seventhLbl['text'] = "Neutral Current : " + str(dataBank[10]) + " A"
        eighthLbl['text'] = "Total Active Energy : " + str(dataBank[34] + dataBank[35]) + " kWh"
        ninthLbl['text'] = "Total Reactive Energy : " + str(dataBank[36] + dataBank[37]) + " kVARh"
        scrollLbl['text'] = "page 7/7"
        time.sleep(delayTime)

        #Page Alarm 1
        firstLbl['text'] = "V u-n : " + statusBank[0]
        if statusBank[0] != "Safe" :
            firstLbl['fg'] = '#FF0000'
        else:
            firstLbl['fg'] = '#000000'
        secondLbl['text'] = "V v-n : " + statusBank[1]
        if statusBank[1] != "Safe" :
            secondLbl['fg'] = '#FF0000'
        else:
            secondLbl['fg'] = '#000000'
        thirdLbl['text'] = "V w-n : " + str(statusBank[2])
        if statusBank[2] != "Safe" :
            thirdLbl['fg'] = '#FF0000'
        else:
            thirdLbl['fg'] = '#000000'
        fourthLbl['text'] = "V u-v : " + str(statusBank[3])
        if statusBank[3] != "Safe" :
            fourthLbl['fg'] = '#FF0000'
        else:
            fourthLbl['fg'] = '#000000'
        fifthLbl['text'] = "V v-w : " + str(statusBank[4])
        if statusBank[4] != "Safe" :
            fifthLbl['fg'] = '#FF0000'
        else:
            fifthLbl['fg'] = '#000000'
        sixthLbl['text'] = "V u-w : " + str(statusBank[5])
        if statusBank[5] != "Safe" :
            sixthLbl['fg'] = '#FF0000'
        else:
            sixthLbl['fg'] = '#000000'
        seventhLbl['text'] = "Frequency : " + str(statusBank[9])
        if statusBank[9] != "Safe" :
            seventhLbl['fg'] = '#FF0000'
        else:
            seventhLbl['fg'] = '#000000'
        eighthLbl['text'] = "Power Factor : " + str(statusBank[17])
        if statusBank[17] != "Safe" :
            eighthLbl['fg'] = '#FF0000'
        else:
            eighthLbl['fg'] = '#000000'
        ninthLbl['text'] = "I Neut. : " + str(statusBank[30])
        if statusBank[30] != "Safe" :
            ninthLbl['fg'] = '#FF0000'
        else:
            ninthLbl['fg'] = '#000000'
        scrollLbl['text'] = "page A/C"
        time.sleep(delayTime)

        #Page Alarm 2
        firstLbl['text'] = "Current u : " + str(statusBank[18])
        if statusBank[18] != "Safe" :
            firstLbl['fg'] = '#FF0000'
        else:
            firstLbl['fg'] = '#000000'
        secondLbl['text'] = "Current v : " + str(statusBank[19])
        if statusBank[19] != "Safe" :
            secondLbl['fg'] = '#FF0000'
        else:
            secondLbl['fg'] = '#000000'
        thirdLbl['text'] = "Current w : " + str(statusBank[20])
        if statusBank[20] != "Safe" :
            thirdLbl['fg'] = '#FF0000'
        else:
            thirdLbl['fg'] = '#000000'
        fourthLbl['text'] = "THDi u : " + str(statusBank[24])
        if statusBank[24] != "Safe" :
            fourthLbl['fg'] = '#FF0000'
        else:
            fourthLbl['fg'] = '#000000'
        fifthLbl['text'] = "THDi v : " + str(statusBank[25])
        if statusBank[25] != "Safe" :
            fifthLbl['fg'] = '#FF0000'
        else:
            fifthLbl['fg'] = '#000000'
        sixthLbl['text'] = "THDi w : " + str(statusBank[26])
        if statusBank[26] != "Safe" :
            sixthLbl['fg'] = '#FF0000'
        else:
            sixthLbl['fg'] = '#000000'
        seventhLbl['text'] = "THDv u : " + str(statusBank[27])
        if statusBank[27] != "Safe" :
            seventhLbl['fg'] = '#FF0000'
        else:
            seventhLbl['fg'] = '#000000'
        eighthLbl['text'] = "THDv v : " + str(statusBank[28])
        if statusBank[28] != "Safe" :
            eighthLbl['fg'] = '#FF0000'
        else:
            eighthLbl['fg'] = '#000000'
        ninthLbl['text'] = "THDv w : " + str(statusBank[29])
        if statusBank[29] != "Safe" :
            ninthLbl['fg'] = '#FF0000'
        else:
            ninthLbl['fg'] = '#000000'
        scrollLbl['text'] = "page B/C"
        time.sleep(delayTime)

        #Page Alarm 3
        ninthLbl['text'] = ""
        firstLbl['text'] = "Oil Temp. : " + str(statusBank[10])
        if statusBank[10] != "Safe" :
            firstLbl['fg'] = '#FF0000'
        else:
            firstLbl['fg'] = '#000000'
        secondLbl['text'] = "Winding u : " + str(statusBank[11])
        if statusBank[11] != "Safe" :
            secondLbl['fg'] = '#FF0000'
        else:
            secondLbl['fg'] = '#000000'
        thirdLbl['text'] = "Winding v : " + str(statusBank[12])
        if statusBank[12] != "Safe" :
            thirdLbl['fg'] = '#FF0000'
        else:
            thirdLbl['fg'] = '#000000'
        fourthLbl['text'] = "Winding w : " + str(statusBank[13])
        if statusBank[13] != "Safe" :
            fourthLbl['fg'] = '#FF0000'
        else:
            fourthLbl['fg'] = '#000000'
        fifthLbl['text'] = "Bus temp u : " + str(statusBank[14])
        if statusBank[14] != "Safe" :
            fifthLbl['fg'] = '#FF0000'
        else:
            fifthLbl['fg'] = '#000000'
        sixthLbl['text'] = "Bus temp v : " + str(statusBank[15])
        if statusBank[15] != "Safe" :
            sixthLbl['fg'] = '#FF0000'
        else:
            sixthLbl['fg'] = '#000000'
        seventhLbl['text'] = "Bus temp w : " + str(statusBank[16])
        if statusBank[16] != "Safe" :
            seventhLbl['fg'] = '#FF0000'
        else:
            seventhLbl['fg'] = '#000000'
        eighthLbl['text'] = "Oil Level : " + str(statusBank[23])
        if statusBank[23] != "Safe" :
            eighthLbl['fg'] = '#FF0000'
        else:
            eighthLbl['fg'] = '#000000'
        scrollLbl['text'] = "page C/C"
        time.sleep(delayTime)

        #Page Contact
        ninthLbl['text'] = ""
        firstLbl['text'] = "Push Button : " + str(diBank[0])
        secondLbl['text'] = "Oil Level Alarm : " + str(diBank[1])
        thirdLbl['text'] = "Oil Level Trip : " + str(diBank[2])
        fourthLbl['text'] = "PRD : " + str(diBank[3])
        fifthLbl['text'] = "Bucholz : " + str(diBank[4])
        sixthLbl['text'] = ""
        seventhLbl['text'] = ""
        eighthLbl['text'] = ""
        scrollLbl['text'] = "Input TMU"
        time.sleep(delayTime)

        firstLbl['fg'] = '#000000'
        secondLbl['fg'] = '#000000'
        thirdLbl['fg'] = '#000000'
        fourthLbl['fg'] = '#000000'
        fifthLbl['fg'] = '#000000'
        sixthLbl['fg'] = '#000000'
        seventhLbl['fg'] = '#000000'
        eighthLbl['fg'] = '#000000'
        ninthLbl['fg'] = '#000000'

        
if __name__ == "__main__":
    exitBtn = Button(
        screen,
        text = "EXIT",
        command = Stop)
    firstLbl = Label(
            screen,
            font = ("Helvetica",42)
            )
    secondLbl = Label(
            screen,
            font = ("Helvetica",42)
            )
    thirdLbl = Label(
            screen,
            font = ("Helvetica",42)
            )
    fourthLbl = Label(
            screen,
            font = ("Helvetica",42)
            )
    fifthLbl = Label(
            screen,
            font = ("Helvetica",42)
            )
    sixthLbl = Label(
            screen,
            font = ("Helvetica",42)
            )
    seventhLbl = Label(
            screen,
            font = ("Helvetica",42)
            )
    eighthLbl = Label(
            screen,
            font = ("Helvetica",42)
            )
    ninthLbl = Label(
            screen,
            font = ("Helvetica",42)
            )
    scrollLbl = Label(
            screen,
            font = ("Helvetica",28)
            )        
    firstLbl.place(x = 40, y = 10)
    secondLbl.place(x = 40, y = 90)
    thirdLbl.place(x = 40, y = 170)
    fourthLbl.place(x = 40, y = 250)
    fifthLbl.place(x = 40, y = 330)
    sixthLbl.place(x = 40, y = 410)
    seventhLbl.place(x = 40, y = 490)
    eighthLbl.place(x = 40, y = 570)
    ninthLbl.place(x = 40, y = 650)
    exitBtn.place(x = 1200, y = 75)
    scrollLbl.place(x = 1100, y = 25)
    thread1 = threading.Thread(target=mainLoop, args=('thread1', 1))
    thread1.start()
    screen.mainloop()