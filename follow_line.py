from gpiozero import LineSensor
from signal import pause

sensor_1 = 16
sensor_2 = 20
sensor_3 = 21
sensor_4 = 6
sensor_5 = 26

sensor1 = LineSensor(sensor_1)
sensor2 = LineSensor(sensor_2)
sensor3 = LineSensor(sensor_3)
sensor4 = LineSensor(sensor_4)
sensor5 = LineSensor(sensor_5)

sensor1.when_line = lambda: print('Line detected 1 ')
sensor1.when_no_line = lambda: print('No line detected 1')

sensor2.when_line = lambda: print('Line detected 2')
sensor2.when_no_line = lambda: print('No line detected 2')

sensor3.when_line = lambda: print('Line detected 3')
sensor3.when_no_line = lambda: print('No line detected 3')

sensor4.when_line = lambda: print('Line detected 4')
sensor4.when_no_line = lambda: print('No line detected 4')

sensor5.when_line = lambda: print('Line detected 5')
sensor5.when_no_line = lambda: print('No line detected 5')

print(sensor1.when_line)

pause()