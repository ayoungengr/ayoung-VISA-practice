"""interrogates any detected instruments to determine what portion of the essential
SCPI command set is recognized
"""

import pyvisa
import time
import platform
import re

#the following constants must be updated by the user based on available information before this class can be used
#end of constants that user must update

#tuple of IEEE 488.2 mandated commands for SCPI instruments
IEEE488_2_CMDS_TRY = (
    '*IDN?',
    '*CLS',
    '*ESE 0',
    '*ESE?',
    '*ESR?',
    '*RST 0',
    '*SRE 0',
    '*SRE?',
    '*STB?',
    '*TST?',
    '*OPC',
    '*OPC?',
    '*WAI'
)
SCPI_CMDS_TRY = (
    'SYSTem:ERRor?',
    'SYSTem:ERRor:NEXT?', #only required since release of IEEE 488.2 1995.1
    'SYSTem:VERSion?', #only required since release of IEEE 488.2 1990.0
    'STATus:OPERation? ',
    'STATus:OPERation:EVENt? ', #should behave same as previous command
    'STATus:OPERation:CONDition? ',
    'STATus:OPERation:ENABle',
    'STATus:OPERation:ENABle?',
    'STATus:QUEStionable?',
    'STATus:QUEStionable:EVENt?',  # should behave same as previous command
    'STATus:QUEStionable:CONDition?',
    'STATus:QUEStionable:ENABle 1',
    'STATus:QUEStionable:ENABle? 1',
    'STATus:PREset'
)
# mandated and commonly included optional SCPI commands specific to power supplies
PS_CMDS_TRY = (
    'CURRent 0',
    'CURRent?',
    'MEASure:CURRent?'
    'VOLTage 0',
    'VOLTage?',
    'MEASure:VOLTage?',
    'OUTPut 1',
    'OUTPut?',
    'OUTPut 0'
)

#interrogation of MULTiple command tree for multi-instrument networks may be implemented later

_bauds = (2400, 4800, 9600, 19200, 38400, 57600, 115200)

LF = pyvisa.resources.messagebased.MessageBasedResource.LF
CR = pyvisa.resources.messagebased.MessageBasedResource.CR
_terms = ('', LF, CR, LF+CR, CR+LF)




rm = pyvisa.ResourceManager()
reslist = rm.list_resources()
if len(reslist) == 0:
    print('no valid, unopened resources found')
else:
    try:
        pd = rm.open_resource(reslist[0])
    except:
        print('connection error')
        quit()

#attempt to ping device with all combinations of baud rate, write termination, and read termination
#loop through all possible termination characters and common baud rates
btrue = 0
wtermtrue = 'not found'
rtermtrue = 'not found'

for b in _bauds:
    pd.baud_rate = b
    for wterm in _terms:
        for rterm in _terms:
            try:
                pd.write('*IDN?',wterm)
                time.sleep(0.1)
                print(pd.read(rterm))
                btrue = b
                wtermtrue = wterm
                rtermtrue = rterm
            except pyvisa.errors.VisaIOError:
                IDN_success = False
                print('IO timeout for baud=' +str(b) + ', wterm=' + str(wterm)+ ', rterm=' + str(rterm) + ': ' +  str(pyvisa.errors.VisaIOError))
            except:
                IDN_success = False
                print('other error for baud=' +str(b) + ', wterm=' + str(wterm) + ', rterm=' + str(rterm))
print('Serial parameter results: ')
if btrue == 0:
    print('baud rate: not found')
else:
    print('baud rate: ' + str(btrue))
print('write termination: ' + wtermtrue.encode('ascii'))
print('read termination: ' + rtermtrue.encode('ascii'))


