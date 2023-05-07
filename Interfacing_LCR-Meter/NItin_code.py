import numpy as np
import matplotlib.pyplot as plt
import pyvisa as pv
import time
import tqdm
import pandas as pd


rm = pv.ResourceManager("@py")
print(rm.list_resources())

lcrmeter = rm.open_resource('USB0::10893::12033::MY46622603::0::INSTR')
lcrmeter.write("*RST")

voltage_input = np.arange(0.1, 10, 0.1)
cap = []
voltage=[]
ou_cap = []

lcrmeter.write("FREQ 10000")
#lcrmeter.write("FUNC:IMPedance:TYPE CV")

for i in tqdm.tqdm (voltage_input):
    time.sleep(2)
    lcrmeter.write(':APER 32')
    lcrmeter.write(f":VOLT:LEVEL {i}")
#giving voltage input--> check the command inside the quote
    out_cap = float(lcrmeter.query("FETCH?").split(",")[0])
    voltage.append(i)
    ou_cap.append(out_cap)

mytable = pd.DataFrame({
    "Input Frequency " : voltage,
    "Output Capacitance (0.5 V)" : ou_cap,
    })

mytable.to_csv("/Users/ankitgupta/Desktop/nitin_lab5_2.csv")

lcrmeter.close() #disconnecting from the device

print(voltage)