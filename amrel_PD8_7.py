#tester class for all SCPI commands, using Amrel PD8-7 DC power supply over RS-232 interface

#REMEMBER: RS-232 I/V reads require a delay of at least 50ms
#Confirmed: on the PD8-7 female DB9 pinout, pin 2 is -9V vs gnd, pin 3 is 0V vs gnd.
#So, the null modem swap HAS ALREADY BEEN MADE, and a straight-through male DB9 connector should be used.
import pyvisa
import platform
import re

debug = True
prog_step_limit = 20
EOS_type = '3'
my_baud = 9600
os_eos = {'Darwin':'1','Linux':'2','Windows':'3'}
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
                print('other error for baud=' +str(i) + ', wterm=' + str(wterm) + ', rterm=' + str(rterm)

rm = pyvisa.ResourceManager()
print(rm.list_resources())
pd = rm.open_resource('ASRLn::INSTR') # replace 'n' with COM number
pd.query('SYST:CONS:EOS ' + os_eos[platform.system()])
#does the above do the same thing as the below?
pd.read_termination = '\n\r'
pd.write_termination = '\n\r'
if debug:
    print(pd.query('*IDN?')) # report instrument ID including the below info
    print(pd.query('CHANnel:MODel? 1'))  # report instrument model
    print(pd.query('CHANnel:SERial 1'))  # report instrument serial
    print(pd.query('CHANnel:VERSion 1'))  # report firmware version
    print(pd.query('CALibrate:SLOPe? 1'))

#confirm_EOS(): #ensure that device's end-of-signal string matches Windows NT (\r\n)
EOS_get = pd.query('SYST:CONS:EOS?')
#polish: if OS is important for more than just this check, replace '3' with platform.system() match
#   remember: Macs return system() = 'Darwin' not 'Mac'
if EOS_get[0] != '3':
    print('EOS mode set to ' + pd.query('SYST:CONS:EOS 3') + ' for ' + platform.system())
else:
    print('EOS mode is already ' + EOS_get[0] + ' for ' + platform.system())

def confirm_baud(): #ensure that device's end-of-signal string matches Windows NT (\r\n)
    baud_get = pd.query('SYST:CONS:BAUD?')
    if not re.match(str(my_baud),baud_get):
        print('Baud rate set to ' + pd.query('SYST:CONS:BAUD 9600'))
    else:
        print('Baud rate is already ' + baud_get)

#def setI(i = 0):
    i = 0
    Isetpt = i
    print('Current level set to ' + pd.query('CURR 1 ' + str(Isetpt)) + ' A')
#def setV(v = 3):
    v = 3
    Vsetpt = v
    print('Voltage level set to ' + pd.query('VOLT 1 ' + str(Vsetpt)) + ' V')
#def getI():
    Ivalue = pd.query('CURR 1?')
#def getV():
    Vvalue = pd.query('VOLT 1?')

#def output_ON():
    print('Power supply output is ' + pd.query('OUTP 1 ON'))
#def output_OFF():
    print('Power supply output is ' + pd.query('OUTP 1 OFF'))
#def get_on_off():
    if re.match(str(1),pd.query('OUTP? 1')):
        print('Power supply output is ON')
    elif re.match(str(1),pd.query('OUTP? 0')):
        print('Power supply output is OFF')
    else:
        print('OUTPUT STATUS READ ERROR')


def setMode(opmode='CV'):
    if opmode == 'CV':
        hardware.setMode('CV')
    elif opmode == 'CC':
        hardware.setMode('CC')
    else:


pass


def getMode():
    pass


#def setOVP

#def getOVP

#def setOCP

#def getOCP

#def write_I_profile

#def write_V_profile

#def get_I_prog():
    print('Current Program:')
    print('loop count = ' + pd.query('LIST:COUNt? 1'))
    for i in range(1,prog_step_limit+1):
        print(str(i) + ': ' + pd.query('LIST:CURRent? 1'))
#should this return a dict instead?

#def get_V_prog():
    print('Voltage Program:')
    print('loop count = ' + pd.query('LIST:COUNt? 1'))
    for i in range(1,prog_step_limit+1):
        print(str(i) + ': ' + pd.query('LIST:VOLTage? 1'))

###command list
###
pd.query('*CLS')
pd.query('*ESEn')
pd.query('*ESE?')
pd.query('*ESR?')
pd.query('*IDN?')
pd.query('*OPC')
pd.query('*OPC?')
pd.query('*RCL')
pd.query('*RSTc')
pd.query('*SAVcn')
pd.query('*SAV?c')
pd.query('*SREn')
pd.query('*SRE?')
pd.query('*STB?')
pd.query('*TRG')
pd.query('*TST?')
pd.query('ABORt') #Resets the trigger system to idle state

pd.query('CALibrate')
pd.query('CALibrate:CURRent')
pd.query('[CALibrate:CURRent:DATA] <channel> <value> Enters the current calibration value')
pd.query('CALibrate:CURRent:LEVel <channel> <n> Sets the current calibration point')
pd.query('CALibrate:CURRent:SAVe <channel> <n> Resaves current calibration data')
pd.query('CALibrate:OFFSet <channel> <n> <value> Sets / Queries calibration offset value')
pd.query('CALibrate:PASSword <channel> [<password>]') # Sets calibration password
pd.query('CALibrate:SAVe <channel>') # Saves new calibration constants
pd.query('CALibrate:SLOPe <channel> <n> <value>') # Sets / Queries calibration slope value
pd.query('CALibrate:STATe <channel> <bool> [<password>]') # Sets / Queries calibration state
pd.query('CALibrate:VOLTage') #
pd.query('[CALibrate:VOLTage:DATA] <channel> <value>') # Enters the voltage calibration value
pd.query('CALibrate:VOLTage:LEVel <channel> <n>') # Sets the voltage calibration point
pd.query('CALibrate:VOLTage:SAVe <channel> <n>') # Resaves voltage calibration data

pd.query('CHANnel') #
pd.query('CHANnel:MODel? <channel>') # Returns model number
pd.query('CHANnel:SERial <channel> <serial-number>') # Sets / Queries serial number
pd.query('CHANnel:VERSion? <channel>') # Returns channel version

pd.query('CURRent') #
pd.query('[CURRent:LEVel]') #
pd.query('[IMMediate] <channel> <value>') # Sets / Queries the output current level
pd.query('CURRent:LEVel:TRIGgered <channel> <value>') # Sets / Queries the current triggered level
pd.query('CURRent:PROTection') #
pd.query('CURRent:PROTection:CLEar <channel>') # Resets latched current protection
pd.query('CURRent:PROTection:STATe <channel> <bool>') # Sets / Queries current protection state

pd.query('LIST') #
pd.query('LIST:COUNt <channel> <count>') # Sets / Queries the number of times for a list
pd.query('LIST:CURRent <channel> <point> <value>') # Sets / Queries current value for a list point
pd.query('LIST:CURRent:STATe <channel> <bool>') # Sets / Queries current list state
pd.query('LIST:CURRent:STEP <channel> <n>') # Sets / Queries list step
pd.query('LIST:CURRent:TIMe <channel> <point> <value>') # Sets / Queries current dwelling time for a list point
pd.query('LIST:VOLTage <channel> <point> <value>') # Sets / Queries voltage value for a list point
pd.query('LIST:VOLTage:STATe <channel> <bool>') # Sets / Queries voltage list state
pd.query('LIST:VOLTage:STEP <channel> <n>') # Sets / Queries voltage list step
pd.query('LIST:VOLTage:TIMe <channel> <point> <value>') # Set / Queries voltage dwelling time for a list point

pd.query('MEASure') #
pd.query('MEASure:CURRent? <channel>') # Returns current measured value
pd.query('MEASure:DELay <n>') # Sets / Queries delay time for measuring
pd.query('MEASure:VCOUT? <channel>') # Returns both voltage and current measured value
pd.query('MEASure:VOLTage? <channel>') # Returns voltage measured value

pd.query('OUTPut') #
pd.query('[OUTPut:STATe] <channel> <bool>') # Sets / Queries output status
pd.query('OUTPut:PROTection') #
pd.query('OUTPut:PROTection:CLEar <channel>') # Resets latched protection
pd.query('OUTPut:RELay') #
pd.query('[OUTPut:RELay:STATe] <channel> <bool>') # Sets / Queries output relay state
pd.query('OUTPut:RELay:POLarity <channel> <polarity>') # Sets / Queries output relay polarity

pd.query('STATus') #
pd.query('STATus:OPERation') #
pd.query('[STATus:OPERation:EVENt]? <channel>') # Returns the value of operation event register
pd.query('STATus:QUEStionable') #
pd.query('[STATus:QUEStionable:EVENt]? <channel>') # Returns the value of questionable event register
pd.query('STATus:ENABle <channel>') # Enables / Queries the specific bit in the questionable enable register

pd.query('SYSTem') #
pd.query('SYSTem:BACK <NR1>') # Sets / Queries system LCD backlight mode
pd.query('SYSTem:BUZZer <bool>') # Sets / Queries system buzzer mode
pd.query('SYSTem:CHANnelSYSTem:MAXimum <NR1>') # Sets / Queries max # of channels in a system
pd.query('SYSTem:CONSol') #
pd.query('SYSTem:CONSol:BAUD <baudrate>') # Sets / Queries RS-232 baud rate value
pd.query('SYSTem:CONSol:EOS <NR1>') # Sets / Queries RS-232 EOS mode
pd.query('SYSTem:DEFaultSYSTem:OUTPut <NR1>') # Sets / Queries default power on output status
pd.query('SYSTem:EOS <NR1>') # Sets / Queries current interface EOS mode
pd.query('SYSTem:ERRor?') # Returns error number and string
pd.query('SYSTem:GPIBSYSTem:EOS') # Sets / Queries GPIB EOS mode
pd.query('SYSTem:NET') #
pd.query('SYSTem:NET:ADDRess') # Sets / Queries Ethernet IP address
pd.query('SYSTem:NET:DHCP?') # Queries if the DHCP is enabled
pd.query('SYSTem:NET:EOS') # Sets / Queries Ethernet EOS mode
pd.query('SYSTem:NET:GATE') # Sets / Queries Ethernet default gateway IP address
pd.query('SYSTem:NET:STATe?') # Queries Ethernet configuration state
pd.query('SYSTem:NET:SUBNet') # Sets / Queries Ethernet Subnet value
pd.query('SYSTem:PROT') # Returns value of Protect Event Status register
pd.query('SYSTem:VERSion?') # Returns the firmware version number
pd.query('SYSTem:INH:STAT <NR1>') # Sets / Queries Remote Inhibit (RI) shutdown mode

pd.query('TRIGger') #
pd.query('[TRIGger:STARt]') #
pd.query('[TRIGger:STARt:IMMediate]') # Enables output trigger immediately
pd.query('TRIGger:STARt:DELay <channel> <value>') # Sets / Queries delay time for output trigger
#does TRIG:DEL work? or is TRIG:STAR:DEL required?

pd.query('VOLTage') #
pd.query('[VOLTage:LEVel]') #
pd.query('[VOLTage:LEVel]:IMMediate] <channel> <value>') # Sets / Queries the output voltage level
pd.query('VOLTage:LEVel]:TRIGgered <channel> <value>') # Sets / Queries the voltage triggered level
pd.query('VOLTage:PROTection') #
pd.query('VOLTage:PROTection:CLEar <channel>') # Resets latched voltage protection
pd.query('[VOLTage:PROTection:LEVel] <channel> <value>') # Sets / Queries over voltage protection level
pd.query('VOLTage:PROTection:STATe <channel> <bool>') # Sets / Queries over voltage protection state