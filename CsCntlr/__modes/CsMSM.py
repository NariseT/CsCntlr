from CsABC import *
import time

class CsMSM(CsABC):
    
    """
    TINT (manual setting mode):
        11: 358.4 ms, 10: 44.8 ms, 01: 2.8 ms, 00: 0.175 ms
    """
    TINT_0 = 0.175
    TINT_1 = 2.8
    TINT_2 = 44.8
    TINT_3 = 358.4
    
    def __init__(self):
        self.name = "Manual Setting Mode"
    
    """
    MAN_TINT
        max: 0xFFFF, min: 0x0000
    """
    def set_man_tint(self, man_tint, quiet=False):
        if 0 <= man_tint <= 0xFFFF:
            man_tint = int(man_tint)
            man_tint_msb = man_tint >> 8
            man_tint_lsb = man_tint & 0xFF
            self.i2c_write(self.MAN_TINT_MSB, man_tint_msb)
            self.i2c_write(self.MAN_TINT_LSB, man_tint_lsb)
        else:
            if not quiet:
                print('\ninvalid man_tint value:')
                print(man_tint)
                print('man_tint should be from 0 to 65535\n')
    
    def calcMeasurementTime(self):
        control_bits = self.get_ctrl_bits()
        tint = control_bits & self.TINT
        man_tint_msb = self.i2c_read(self.MAN_TINT_MSB, 1)[0]
        man_tint_lsb = self.i2c_read(self.MAN_TINT_LSB, 1)[0]
        man_tint = man_tint_msb<<8 | man_tint_lsb
        if tint == 0:
            measurement_time = self.TINT_0 * man_tint * 4
        elif tint == 1:
            measurement_time = self.TINT_1 * man_tint * 4
        elif tint == 2:
            measurement_time = self.TINT_2 * man_tint * 4
        elif tint == 3:
            measurement_time = self.TINT_3 * man_tint * 4
        return measurement_time
    
    def auto(self, gain='', man_tint=-1, tint=-1, quiet=False):
        if not quiet:
            print('\n####################')
            print(self.name)
        self.reset_adc_and_disable_standby_mode()
        if gain:
            if gain.lower() == 'high':
                self.set_to_high_gain(quiet=quiet)
            elif gain.lower() == 'low':
                self.set_to_low_gain(quiet=quiet)
            else:
                print('\ngain shold be \'high\' or \'low\'\n')
        if not man_tint == -1:
            self.set_man_tint(man_tint, quiet=quiet)
        if not tint == -1:
            self.set_tint(tint, quiet=quiet)
        measurement_time = self.calcMeasurementTime()
        if not quiet:
            print('Measurement time: ' + str(measurement_time) + ' ms\n')
            """
            print('before')
            d = self.getData()
            print( 'ctrl: ' + str(bin(d['ctrl'])) )
            print( 'man_tint: ' + str(d['man_tint']) )
            print( 'red: ' + str(d['red']) )
            print( 'green: ' + str(d['green']) )
            print( 'blue: ' + str(d['blue']) )
            print( 'ir: ' + str(d['ir']) )
            """
        self.run_adc(quiet=quiet)
        time.sleep(measurement_time / 1000 * 1.5)
        #print('after')
        d = self.getData()
        if not quiet:
            #print( 'ctrl: ' + str(bin(d['ctrl'])) )
            #print( 'man_tint: ' + str(d['man_tint']) )
            print( 'red: ' + str(d['red']) )
            print( 'green: ' + str(d['green']) )
            print( 'blue: ' + str(d['blue']) )
            print( 'ir: ' + str(d['ir']) )
        return d
