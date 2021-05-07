from sense_emu import SenseHat

sense = SenseHat()
print(str(int(sense.get_temperature())))
