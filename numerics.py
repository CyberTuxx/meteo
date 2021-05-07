from sense_emu import SenseHat

sense = SenseHat()

OFFSET_LEFT = 1
OFFSET_TOP = 2

NUMS =[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,  # 0
       0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,  # 1
       1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,  # 2
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

show_number(25, 255, 0, 0)
