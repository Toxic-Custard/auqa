import os

if os.environ["TEST"] != "y": # Make sure we are not testing as this will import error
    from sense_hat import SenseHat
import sqlite3
import time
import datetime
import random

conn = sqlite3.connect("database.db", check_same_thread=False) #SQLite3 Setup
c = conn.cursor() #SQL Cursor

c.execute("""CREATE TABLE IF NOT EXISTS `data` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`timestamp`	DATE NOT NULL DEFAULT (datetime('now','localtime')),
	`humidity`	REAL,
	`temperature`	REAL,
	`pressure`	REAL
);""")

conn.commit()

if os.environ["TEST"] != "y":
    s = SenseHat() #Sensehat Setup
else:
    s = None

def get_data(): #Get humidity and temperature
    if os.environ["TEST"] != "y":
        humidity = s.get_humidity()
        temp = s.get_temperature()
        pressure = s.get_pressure()
    else:
        # Generate Fake Data
        humidity = random.uniform(30, 80) # 30% to 80%
        temp = random.uniform(10, 30) # 10degC to 30degC
        pressure = random.uniform(1000, 2000) # 1000mbar to 2000mbar
    log("=========================================")
    log("Current Humidity:     " + str(humidity) + " %")
    log("Current Temperature:  " + str(temp) + " degC")
    log("Current Air Pressure: " + str(pressure) + " mbar")

    insert_data(humidity, temp, pressure)

def insert_data(humidity, temperature, pressure): # Put data into the database
    c.execute("INSERT INTO `data` (humidity, temperature, pressure) VALUES (?, ?, ?)", [humidity, temperature, pressure])
    conn.commit()
    return c.lastrowid

# TODO: Replace this with a CRON Job
def go():
    while True:
        get_data()
        time.sleep(10)

if __name__ == "__main__":
    go()

def log(message):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S %d/%m/%Y')
    print("[" + st + "] ", message)
