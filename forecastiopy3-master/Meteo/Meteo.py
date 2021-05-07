from sense_emu import SenseHat
from forecastiopy import *
import time
import mysql.connector
import socket

sense = SenseHat()
sense.clear()
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
orange = (234, 149, 0)
cyan = (102, 255, 255)
white = (0,0,0)
rotation = 0
selection = 0
saveselection = 0
nbmode = 5
displaymode = 2
Paris = [48.856711, 2.396876]
Lyon = [45.764043, 4.835659]
update = 0

OFFSET_LEFT = 1
OFFSET_TOP = 2

NUMS =[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,  # 0
       0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,  # 1
       1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,  # 2
       1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,  # 3
       1,0,0,1,0,1,1,1,1,0,0,1,0,0,1,  # 4
       1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,  # 5
       1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,  # 6
       1,1,1,0,0,1,0,1,0,1,0,0,1,0,0,  # 7
       1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,  # 8
       1,1,1,1,0,1,1,1,1,0,0,1,0,0,1,  # 9
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  # FULL
       0,0,0,0,0,0,0,1,1,0,0,0,0,0,0]  # MINUS


def show_digit(val, xd, yd, r, g, b):
  offset = val * 15
  for p in range(offset, offset + 15):
    xt = p % 3
    yt = (p-offset) // 3
    sense.set_pixel(xt+xd, yt+yd, r*NUMS[p], g*NUMS[p], b*NUMS[p])

def show_number(val, r, g, b):
    abs_val = abs(val)
    tens = abs_val // 10
    units = abs_val % 10
    if (abs_val > 9 and val >= 0):
        show_digit(tens, OFFSET_LEFT, OFFSET_TOP, r, g, b)
    elif(10 > val > -1):
        show_digit(10, OFFSET_LEFT, OFFSET_TOP, r, g, b)
    if(0 > val > -10):
      show_digit(11, OFFSET_LEFT, OFFSET_TOP, r, g, b)
    elif(val < -10):
      show_digit(tens, OFFSET_LEFT, OFFSET_TOP, 0, 0, 255)
    show_digit(units, OFFSET_LEFT+4, OFFSET_TOP, r, g, b)

def setposition():
  o = sense.get_orientation()
  roll = o["yaw"]
  if(roll < 45):
    rotation = 90
    sense.rotation = rotation
  elif(roll < 135):
    rotation = 0
    sense.rotation = rotation
  elif(roll < 225):
    rotation = 270
    sense.rotation = rotation
  else:
    rotation = 180
    sense.rotation = rotation

def gettemp():
  if(displaymode == 1 or int(sense.get_temperature()) >= 100):
    sense.show_message(str(int(sense.get_temperature())), 0.10, red)
  else:
    show_number(int(sense.get_temperature()), red[0], red[1], red[2])
  
def humidity():
  if(displaymode == 1 or int(sense.get_humidity() >= 100)):
    humidity = str(int(sense.get_humidity())) + "%" 
    sense.show_message(humidity, 0.10, blue)
  else:
    show_number(int(sense.get_humidity()), blue[0], blue[1], blue[2])
  
def pressur():
  if(displaymode == 1):
    sense.show_message(str(int(sense.get_pressure())), 0.10, orange)
  elif(int(sense.get_pressure()) >= 1000):
    show_number(int(int(sense.get_pressure())/100), orange[0], orange[1], orange[2])
  elif(int(sense.get_pressure()) <= 999):
    show_number(int(int(sense.get_pressure())/10), orange[0], orange[1], orange[2])
    
def parisTemp():
  try:
    fioParis = ForecastIO.ForecastIO("a6734c27e9a68100574fce1f07452214", latitude=Paris[0], longitude=Paris[1])
    currentParis = FIOCurrently.FIOCurrently(fioParis)
    parisTemp = int(currentParis.temperature)
    if(displaymode == 1):
      sense.show_message(str(parisTemp), 0.10, green)
    else:
      show_number(parisTemp, green[0], green[1], green[2])
    return nbmode + 1
  except:
    sense.show_letter("E")
    time.sleep(1)
    return 2

def lyonTemp():
  try:
    fioLyon = ForecastIO.ForecastIO("a6734c27e9a68100574fce1f07452214", latitude=Lyon[0], longitude=Lyon[1])
    currentLyon = FIOCurrently.FIOCurrently(fioLyon)
    lyonTemp = int(currentLyon.temperature)
    if(displaymode == 1):
      sense.show_message(str(lyonTemp), 0.10, cyan)
    else:
      show_number(lyonTemp, cyan[0], cyan[1], cyan[2])
    return -2
  except:
    sense.show_letter("E")
    time.sleep(1)
    return 2

def connexionBd():
  try:
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="phpmyadmin")
    cursor = conn.cursor()
    values = (int(sense.get_temperature()), int(sense.get_pressure()), int(sense.get_humidity()), time.strftime('%Y-%m-%d %H:%M:%S'))
    cursor.execute("""INSERT INTO Meteo(temp, pression, humidity, date) values (%s, %s, %s, %s)""", values)
    cursor.close()
    conn.commit()
    sense.show_letter("A")
  except:
    print("No Connection")
    sense.show_letter("E")

def showip():
  try:
    sense.show_message([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
  except:
    sense.show_message("E")

def choose(selection):
  connexionBd()
  global update
  if(selection == 0):
    gettemp()
  elif(selection == 1):
    humidity()
  elif(selection == 2):
    pressur()
  elif(selection == -1):
    sense.clear()
  elif(selection == 3):
    selection = parisTemp()
    if(selection == 2):
      sense.clear()
  elif(selection == 4):
    selection = lyonTemp()
    if(selection == 2):
      sense.clear()
  elif(-1000 <= selection <= -2):
    selection -= 1
  elif(nbmode + 1 <= selection <= 1000+nbmode+1):
    selection += 1
  elif(selection == 1000 + nbmode + 2):
    selection = 3
  elif(selection == -1001):
    selection = 4
  if(time.time() % 3600 <= 10 and update != 1):
    update = 1
    connexionBd()
    sense.clear()
  elif(time.time() % 3600 > 10 and update == 1):
    update = 0
  return selection
    
        
def action(selection, nbmode):
  global displaymode
  global saveselection
  events = sense.stick.get_events()
  for event in events:
    if event.action != "released" and event.action != "held":
      if(-1 < selection <= nbmode - 1):
        saveselection = selection
      if(event.direction == "left" and selection != -1):
        if(selection > 0 and selection < nbmode):
          selection -= 1
        elif(selection == 0):
          selection = nbmode - 1
        elif(selection <= -2):
          selection = 3
        elif(selection >= nbmode + 1):
          selection = 2
      elif(event.direction == "right" and selection != -1):
        if(-1 < selection < nbmode - 1):
          selection += 1
        elif(selection == nbmode - 1):
          selection = 0
        elif(selection <= -2):
          selection = 0
        elif(selection >= nbmode + 1):
          selection = 4
      elif(event.direction == "middle"):
        if(selection == -1):
          if(saveselection <= -2):
            selection = 4
          elif(saveselection >= nbmode+1):
            selection = 3
          else:
            selection = saveselection
        else:
          saveselection = selection
          selection = -1
          connexionBd()
      elif(event.direction == "up"):
        if(displaymode == 1):
          displaymode = 2
        elif(displaymode == 2):
          displaymode = 1
      elif(event.direction == "down"):
        showip()
        
  selection = choose(selection)
  return selection


while(True):
  setposition()
  selection = action(selection, nbmode)
