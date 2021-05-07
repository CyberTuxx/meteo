import mysql.connector
from sense_emu import SenseHat
import time

sense = SenseHat()

try:
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="phpmyadmin")
    cursor = conn.cursor()
    values = (int(sense.get_temperature()), int(sense.get_pressure()), int(sense.get_humidity()), time.strftime('%Y-%m-%d %H:%M:%S'))
    cursor.execute("""INSERT INTO Meteo(temp, pression, humidity, date) values (%s, %s, %s, %s)""", values)
    cursor.close()
    conn.commit()
    print("Effectuer")
except:
    print("Erreur")
