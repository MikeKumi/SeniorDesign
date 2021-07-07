# Runs for two weeks generating one excel file per day
# Light sensor records light intensity (luxes) and rgb values (0-255)
# Sound sensor records sound intensity (dBA)
# Exports saved light and sound sensor values to csv file 

import board
import busio
import adafruit_tcs34725
import time
import datetime
import Adafruit_ADS1x15
import configHosp as c


# Read and store sensor values into above lists
def readSensors():
    count = 0
    
    # Totals to get the average every 5 min
    redA = 0
    redB = 0
    redC = 0

    greenA = 0
    greenB = 0
    greenC = 0

    blueA = 0
    blueB = 0
    blueC = 0

    lightTotA = 0
    lightTotB = 0
    lightTotC = 0

    sndTot = 0
    critLight = 0
    critSound = 0
    
    miscount = 0  # Count for when none values are read by light sensors

    entries = 0  # Number of entries in excel file
    
    litGUI = ""
    prevLitGUI = ""
    
    sndGUI = ""
    prevSndGUI = ""

    t1 = time.perf_counter()  # Get time before sequence
    t3 = time.perf_counter()
    # Run for one day before generating excel file
    while entries<c.totEntries: # 288 five minute entries per day
        event, values = c.window.read(timeout=30)
        
        # Gather RGB values
        colorsA = c.litSensorA.color_rgb_bytes
        colorsB = c.litSensorB.color_rgb_bytes
        colorsC = c.litSensorC.color_rgb_bytes
        
        # Add rgb values to respective totals
        redA += colorsA[0]
        redB += colorsB[0]
        redC += colorsC[0]

        greenA += colorsA[1]
        greenB += colorsB[1]
        greenC += colorsC[1]

        blueA += colorsA[2]
        blueB += colorsB[2]
        blueC += colorsC[2]
        
        # Gather light values
        luxValA = c.litSensorA.lux * 1.13 * 0.0929
        luxValB = c.litSensorB.lux * 1.13 * 0.0929
        luxValC = c.litSensorC.lux * 1.13 * 0.0929
        
        try:
            luxAve = (luxValA + luxValB + luxValC)/3  # Average light value for GUI
            lightTotA += luxValA
            lightTotB += luxValB
            lightTotC += luxValC
        except TypeError:
            miscount += 1
            if isinstance(luxValB, float):
                luxAve = luxValB
            elif isinstance(luxValA, float):
                luxAve = luxValA
            elif isinstance(luxValC, float):
                luxAve = luxValC
        
        # Read Sound
        sndVal = c.sndSensor.read_adc(0, gain=c.sndGain)/1024 * 6
        sndTot += sndVal
        
        # Update Light readings on GUI
        try:
            c.window['-LIGHT-'].update(f'Light - {luxAve:.1f}(ftc)')
            if luxAve >= 20:
                litGUI = "RED"
                critLight = 1
            elif luxAve >= 16:
                litGUI = "YELLOW"
            elif luxAve >= 0:
                litGUI = "WHITE"
                
            if litGUI != prevLitGUI:
                c.updateLight(litGUI)
            prevLitGUI = litGUI
        except TypeError:
            pass
        
        # Update Sound readings on GUI
        c.window['-SOUND-'].update(f'Sound - {sndVal:.1f}(dB)')
        if sndVal >= 80:
            sndGUI = "RED"
            critSound = 1
        elif sndVal >= 45:
            sndGUI = "YELLOW"
        elif sndVal >= 0:
            sndGUI = "WHITE"
                
        if sndGUI != prevSndGUI:
            c.updateSound(sndGUI)
        prevSndGUI = sndGUI
        
        count += 1
        
        # Every five minutes
        t2 = time.perf_counter() # get second timer
        if t2 - t1 >= 300:
            # Append rgb and sound values
            c.redA[entries] = redA/count
            c.redB[entries] = redB/count
            c.redC[entries] = redC/count

            c.greenA[entries] = greenA/count
            c.greenB[entries] = greenB/count
            c.greenC[entries] = greenC/count

            c.blueA[entries] = blueA/count
            c.blueB[entries] = blueB/count
            c.blueC[entries] = blueC/count

            c.sound[entries] = sndTot/count
            
            # Append time
            now = datetime.datetime.now()
            c.sensorTime[entries] = f"{now.hour}:{now.minute}"
            
            # Append light value
            c.luxA[entries] = lightTotA/(count - miscount)
            c.luxB[entries] = lightTotB/(count - miscount)
            c.luxC[entries] = lightTotC/(count - miscount)
            
            # Append Critical Values
            c.critLit[entries] = critLight
            c.critSnd[entries] = critSound
            
            # Reset totals
            redA = 0
            redB = 0
            redC = 0

            greenA = 0
            greenB = 0
            greenC = 0

            blueA = 0
            blueB = 0
            blueC = 0

            lightTotA = 0
            lightTotB = 0
            lightTotC = 0

            sndTot = 0
            critLight = 0
            critSound = 0

            miscount = 0
            
            count = 0  # reset counter
            entries += 1  # increment entries
            t1 = time.perf_counter()  # reset timer 1
            
    t4 = time.perf_counter()
    print(t4-t3)
    
    
# Function to export light data to excel file on external USB drive
def generateExcel():
    # Save current date
    date = datetime.datetime.now()
    
    # Create and open file in USB drive
    f = open(f"/media/flash/{date.month}_{date.day}_{date.year}.csv", "w")
    
    # Add header
    f.write(f"Date:,{date.month}/{date.day}/{date.year}\n")
    f.write("Isolette 1\n\n")
    
    # Add data fields
    f.write("Time,Light A (ftc),Red A,Green A,Blue A,Light B (ftc),Red B,Green B,Blue B,Light C (ftc),Red C,Green C,Blue C,Sound (dBA),Critical Light,Critical Sound\n")
    
    # Fill with example data
    for i in range(len(c.sensorTime)):
        # Write data to csv
        try:
            f.write(f"{c.sensorTime[i]},{c.luxA[i]:.2f},{c.redA[i]:.0f},{c.greenA[i]:.0f},{c.blueA[i]:.0f},"
                    f"{c.luxB[i]:.2f},{c.redB[i]:.0f},{c.greenB[i]:.0f},{c.blueB[i]:.0f},{c.luxC[i]:.2f},"
                    f"{c.redC[i]:.0f},{c.greenC[i]:.0f},{c.blueC[i]:.0f},{c.sound[i]:.2f},{c.critLit[i]},"
                    f"{c.critSnd[i]}\n")
        except TypeError:
            f.write(f"{c.sensorTime[i]},{c.luxA[i]},{c.redA[i]:.0f},{c.greenA[i]:.0f},{c.blueA[i]:.0f},{c.luxB[i]},"
                    f"{c.redB[i]:.0f},{c.greenB[i]:.0f},{c.blueB[i]:.0f},{c.luxC[i]},{c.redC[i]:.0f},{c.greenC[i]:.0f},"
                    f"{c.blueC[i]:.0f},{c.sound[i]:.2f},{c.critLit[i]},{c.critSnd[i]}\n")

    c.clearLists()
        

if __name__ == "__main__":
    # Run for 14 days
    for day in range(14):
        readSensors()
        generateExcel()
        print("File uploaded")


