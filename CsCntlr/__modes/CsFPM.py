from CsABC import *
import time

class CsFPM(CsABC):
    
    """
    TINT (fixed period mode):
        11: 179.2 ms, 10: 22.4 ms, 01: 1.4 ms, 00: 0.0875 ms
    """
    TINT_0 = 0.0875
    TINT_1 = 1.4
    TINT_2 = 22.4
    TINT_3 = 179.2
    
    def __init__(self):
        self.name = "Fixed Period Mode"
    
    def calcMeasurementTime(self):
        control_bits = self.get_ctrl_bits()
        tint = control_bits & self.TINT
        if tint == 0:
            measurement_time = self.TINT_0 * 4
        elif tint == 1:
            measurement_time = self.TINT_1 * 4
        elif tint == 2:
            measurement_time = self.TINT_2 * 4
        elif tint == 3:
            measurement_time = self.TINT_3 * 4
        return measurement_time
    
    def auto(self, gain='', tint=-1, quiet=False):
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
                if not quiet:
                    print('\ngain shold be \'high\' or \'low\'\n')
        if not tint == -1:
            self.set_tint(tint, quiet=quiet)
        measurement_time = self.calcMeasurementTime()
        if not quiet:
            print('Measurement time: ' + str(measurement_time) + ' ms\n')
            """
            print('before')
            d = self.getData()
            print( 'ctrl: ' + str(bin(d['ctrl'])) )
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
            print( 'red: ' + str(d['red']) )
            print( 'green: ' + str(d['green']) )
            print( 'blue: ' + str(d['blue']) )
            print( 'ir: ' + str(d['ir']) )
        return d
