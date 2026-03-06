import pyvisa
import platform
import re

rm = pyvisa.ResourceManager()
print(rm.list_resources())

try:
    pd = rm.open_resource('ASRL3::INSTR')
except:
    print('connection error')
bauds = (2400, 4800, 9600, 19200, 38400, 57600, 115200)
terms = ('','\n','\r','\n\r','\r\n')
for i in bauds:
    pd.baud_rate = i
    for wterm in terms:
        for rterm in terms:
            try:
                pd.write('*PDN?',wterm)
                time.sleep(0.1)
                print(pd.read(rterm))
            except pyvisa.errors.VisaIOError:
                print('IO timeout for baud=' +str(i) + ', wterm=' + str(wterm)+ ', rterm=' + str(rterm) + ': ' +  str(pyvisa.errors.VisaIOError))
            except:
                print('other error for baud=' +str(i) + ', wterm=' + str(wterm) + ', rterm=' + str(rterm))


# PD8-7 debug mode displays rx memory as 0255 0255 0255 0255 (etc) where 0001-0127 are converted to ASCII and 0000, 0128-0255 remain as-is
# how can this be parsed to relate back to the literals sent over the serial cable by Python?
# written string to serial values:
msg = '*IDN?'.encode('ascii')
for n in range(len(msg)):
    print(msg[n])
for