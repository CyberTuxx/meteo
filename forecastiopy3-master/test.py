from sense_emu import SenseHat
from forecastiopy import *

sense = SenseHat()
sense.clear()
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
orange = (234, 149, 0)
white = (0,0,0)
sense.set_pixel(0,0, red)
rotation = 0
selection = 0
nbmode = 3
displaymode = 1
Paris = [48.856711, 2.396876]
Lyon = [45.764043, 4.835659]

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
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  # FULL

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
    if (abs_val > 9):
        show_digit(tens, OFFSET_LEFT, OFFSET_TOP, r, g, b)
    else:
        show_digit(10, OFFSET_LEFT, OFFSET_TOP, r, g, b)
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
  fioParis = ForecastIO.ForecastIO("a6734c27e9a68100574fce1f07452214", latitude=Paris[0], longitude=Paris[1])
  currentParis = FIOCurrently.FIOCurrently(fioParis)
  parisTemp = int(currentParis.temperature)
  if(displaymode == 1):
    sense.show_message(str(parisTemp), green)
  else:
    show_number(parisTemps, green[0], green[1], green[2])
  

def choose(selection):
  if(selection == 0):
    gettemp()
  elif(selection == 1):
    humidity()
  elif(selection == 2):
    pressur()
  elif(selection == -1):
    sense.clear()
        
def action(selection, nbmode):
  global displaymode
  events = sense.stick.get_events()
  for event in events:
    if event.action != "released":
      if(event.direction == "left" and selection > 0):
        selection -= 1
      elif(event.direction == "right" and -1 < selection < nbmode - 1):
        selection += 1
      elif(event.direction == "middle"):
        if(selection == -1):
          selection = 0
        else:
          selection = -1
      elif(event.direction == "up"):
        displaymode = 1
      elif(event.direction == "down"):
        displaymode = 2
  choose(selection)
  return selection


while(True):
  setposition()
  selection = action(selection, nbmode)
