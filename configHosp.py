# Config file for all global variables

import board
import busio
import adafruit_tcs34725
import adafruit_tca9548a
import time
import datetime
import Adafruit_ADS1x15
import PySimpleGUI as sg

# total number of excel entries per day
totEntries = 288

# Allow sensor access
i2c = busio.I2C(board.SCL, board.SDA)

# I2C Multiplexer
mux = adafruit_tca9548a.TCA9548A(i2c)

# Light Sensors
litSensorA = adafruit_tcs34725.TCS34725(mux[0])
litSensorB = adafruit_tcs34725.TCS34725(mux[1])
litSensorC = adafruit_tcs34725.TCS34725(mux[2])

# Sound Sensor
sndSensor = Adafruit_ADS1x15.ADS1115()

# modify sensor gains
litSensorA.gain = 4
litSensorB.gain = 4
litSensorC.gain = 4

# Modify light integration time
litSensorA.integration_time = 50
litSensorB.integration_time = 50
litSensorC.integration_time = 50

# Sound sensor gain:
#  Gain: 2/3 = +/-6.144V
#  Gain: 1 = +/-4.096V
#  Gain: 2 = +/-2.048V
#  Gain: 4 = +/-1.024V
#  Gain: 8 = +/-0.512V
#  Gain: 16 = +/-0.256V

sndGain = 1

# Lists stored for excel export
sensorTime = [0]*totEntries

redA = [0]*totEntries
redB = [0]*totEntries
redC = [0]*totEntries

greenA = [0]*totEntries
greenB = [0]*totEntries
greenC = [0]*totEntries

blueA = [0]*totEntries
blueB = [0]*totEntries
blueC = [0]*totEntries

luxA = [0]*totEntries
luxB = [0]*totEntries
luxC = [0]*totEntries

sound = [0]*totEntries
critLit = [0]*totEntries
critSnd = [0]*totEntries

sg.theme('Black')


# Clear Lists
def clearLists():
    sensorTime = [0]*totEntries
    redA = [0] * totEntries
    redB = [0] * totEntries
    redC = [0] * totEntries

    greenA = [0] * totEntries
    greenB = [0] * totEntries
    greenC = [0] * totEntries

    blueA = [0] * totEntries
    blueB = [0] * totEntries
    blueC = [0] * totEntries

    luxA = [0] * totEntries
    luxB = [0] * totEntries
    luxC = [0] * totEntries

    sound = [0] * totEntries
    critLit = [0] * totEntries
    critSnd = [0] * totEntries


# Update light bars
def updateLight(litGUI):
    if litGUI == "RED":
        rect1_1 = graph1.DrawRectangle((10,390),(370,310), fill_color='red')
        rect2_1 = graph1.DrawRectangle((10,290),(370,210), fill_color='yellow')
        rect3_1 = graph1.DrawRectangle((10,190),(370,110), fill_color='white')
    elif litGUI == "YELLOW":
        rect1_1 = graph1.DrawRectangle((10,390),(370,310), fill_color='black')
        rect2_1 = graph1.DrawRectangle((10,290),(370,210), fill_color='yellow')
        rect3_1 = graph1.DrawRectangle((10,190),(370,110), fill_color='white')
    else:
        rect1_1 = graph1.DrawRectangle((10,390),(370,310), fill_color='black')
        rect2_1 = graph1.DrawRectangle((10,290),(370,210), fill_color='black')
        rect3_1 = graph1.DrawRectangle((10,190),(370,110), fill_color='white')


# Update sound bars
def updateSound(sndGUI):
    if sndGUI == "RED":
        rect1_2 = graph1.DrawRectangle((400,390),(790,310), fill_color='red')
        rect2_2 = graph1.DrawRectangle((400,290),(790,210), fill_color='yellow')
        rect3_2 = graph1.DrawRectangle((400,190),(790,110), fill_color='white')
    elif sndGUI == "YELLOW":
        rect1_2 = graph1.DrawRectangle((400,390),(790,310), fill_color='black')
        rect2_2 = graph1.DrawRectangle((400,290),(790,210), fill_color='yellow')
        rect3_2 = graph1.DrawRectangle((400,190),(790,110), fill_color='white')
    else:
        rect1_2 = graph1.DrawRectangle((400,390),(790,310), fill_color='black')
        rect2_2 = graph1.DrawRectangle((400,290),(790,210), fill_color='black')
        rect3_2 = graph1.DrawRectangle((400,190),(790,110), fill_color='white')

# Define columns
LightCol = [[sg.Text("Light - 0(ftc)", font=("Helvetica", 35), key='-LIGHT-', size=(14,1))]]
SoundCol = [[sg.Text(" Sound - 0(dB)", font=("Helvetica", 35), key='-SOUND-', size=(19,1))]]

# Define the window's contents
layout = [[sg.Graph(canvas_size=(800, 300), graph_bottom_left=(0,100), graph_top_right=(800,400), background_color='black', key='graph1')],
          [sg.Column(LightCol, element_justification='left'), sg.Column(SoundCol, element_justification='left')]]

# Create the window
window = sg.Window('Sensor Readings', layout, no_titlebar=True, size=(800,400), finalize=True)

graph1 = window['graph1']

# Light Rectangles
rect1_1 = graph1.DrawRectangle((10,390),(370,310), fill_color='black')
rect2_1 = graph1.DrawRectangle((10,290),(370,210), fill_color='black')
rect3_1 = graph1.DrawRectangle((10,190),(370,110), fill_color='black')

rect1_2 = graph1.DrawRectangle((380,390),(790,310), fill_color='black')
rect2_2 = graph1.DrawRectangle((380,290),(790,210), fill_color='black')
rect3_2 = graph1.DrawRectangle((380,190),(790,110), fill_color='black')

# Dividing Lines
line1 = graph1.DrawLine((385,100),(385,400),color='white')
