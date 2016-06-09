from abc import ABCMeta
from abc import abstractmethod
import smbus

class CsABC(object):
    __metaclass__ = ABCMeta
    
    """
    Abbreviations:
        ADDRESS: ADDR,
        NUM: NUMBER,
        CONTROL: CTRL,
        REGISTER: REG,
        MANUAL: MAN,
        TINT: INTEGRATION TIME SETTING,
        MSB: MOST SIGNIFICANT BIT,
        LSB: LEAST SIGNIFICANT BIT,
        IR: INFRARED
    """
    
    # I2C ADDRESS
    I2C_ADDR = 0x2A
    BUS_NUM = 1
    
    # REG MAP
    CTRL_REG = 0x00
    MAN_TINT_MSB = 0x01 # only for manual setting mode
    MAN_TINT_LSB = 0x02 # only for manual setting mode
    RED_MSB = 0x03
    RED_LSB = 0x04
    GREEN_MSB = 0x05
    GREEN_LSB = 0x06
    BLUE_MSB = 0x07
    BLUE_LSB = 0x08
    IR_MSB = 0x09
    IR_LSB = 0x0A
    
    # FUNCTIONS
    ADC_RESET = 0x80 # 1: reset, 0: operation
    STANDBY_MODE = 0x40 # 1: standby, 0: operation
    STANDBY_MODE_MASK = 0xbf
    STANDBY_MONITOR = 0x20 # 1: standby mode
    GAIN_SELECTION = 0x08 # 1: high gain, 0: low gain
    TINT_MODE = 0x04 # 1: manual setting mode, 0: fixed period mode
    TINT = 0x03 # see below
    
    # I2C METHODS
    def set_bus_num(self, number):
        self.BUS_NUM = number
    
    def create_bus(self):
        bus = smbus.SMBus(self.BUS_NUM)
        return bus
    
    def i2c_write(self, reg_addr, function):
        bus = self.create_bus()
        bus.write_i2c_block_data(self.I2C_ADDR, reg_addr, [function])
    
    def i2c_read(self, reg_addr, byte_len):
        bus = self.create_bus()
        data = bus.read_i2c_block_data(self.I2C_ADDR, reg_addr, byte_len)
        return data
    
    # METHODS
    def get_ctrl_bits(self):
        control_bits = self.i2c_read(self.CTRL_REG, 1)
        return control_bits[0]
    
    def is_adc_reseted(self):
        control_bits = self.get_ctrl_bits()
        is_adc_reseted = control_bits & self.ADC_RESET
        if is_adc_reseted:
            return True
        else:
            return False
    
    def reset_adc(self):
        control_bits = self.get_ctrl_bits()
        is_adc_reseted = self.is_adc_reseted()
        if is_adc_reseted:
            print('\nadc already reseted\n')
        else:
            control_bits ^= self.ADC_RESET
            self.i2c_write(self.CTRL_REG, control_bits)
    
    def run_adc(self):
        control_bits = self.get_ctrl_bits()
        is_adc_reseted = self.is_adc_reseted()
        if not is_adc_reseted:
            print('\nadc already running\n')
        else:
            control_bits ^= self.ADC_RESET
            self.i2c_write(self.CTRL_REG, control_bits)
    
    def is_standby_mode(self):
        control_bits = self.get_ctrl_bits()
        is_standby = control_bits & self.STANDBY_MONITOR
        if is_standby:
            return True
        else:
            return False
    
    def enable_standby_mode(self):
        control_bits = self.get_ctrl_bits()
        #is_standby_mode = self.is_standby_mode()
        #if is_standby_mode:
        #    print('already standby mode')
        #else:
        control_bits |= self.STANDBY_MODE
        self.i2c_write(self.CTRL_REG, control_bits)
    
    def disable_standby_mode(self):
        control_bits = self.get_ctrl_bits()
        #is_standby_mode = self.is_standby_mode()
        #if not is_standby_mode:
        #    print('standby mode already disabled')
        #else:
        control_bits &= self.STANDBY_MODE_MASK
        self.i2c_write(self.CTRL_REG, control_bits)
    
    def reset_adc_and_disable_standby_mode(self):
        control_bits = self.get_ctrl_bits()
        is_adc_reseted = self.is_adc_reseted()
        if is_adc_reseted:
            pass
        else:
            control_bits ^= self.ADC_RESET
        control_bits &= self.STANDBY_MODE_MASK
        self.i2c_write(self.CTRL_REG, control_bits)
    
    def is_high_gain_mode(self):
        control_bits = self.get_ctrl_bits()
        is_high_gain_mode = control_bits & self.GAIN_SELECTION
        if is_high_gain_mode:
            return True
        else:
            return False
    
    def is_low_gain_mode(self):
        control_bits = self.get_ctrl_bits()
        is_high_gain_mode = control_bits & self.GAIN_SELECTION
        if is_high_gain_mode:
            return False
        else:
            return True
    
    def set_to_high_gain(self):
        control_bits = self.get_ctrl_bits()
        is_high_gain_mode = self.is_high_gain_mode()
        if is_high_gain_mode:
            print('\nalready high gain mode\n')
            return
        else:
            control_bits ^= self.GAIN_SELECTION
            self.i2c_write(self.CTRL_REG, control_bits)
    
    def set_to_low_gain(self):
        control_bits = self.get_ctrl_bits()
        is_high_gain_mode = self.is_high_gain_mode()
        if not is_high_gain_mode:
            print('\nalready low gain mode\n')
            return
        else:
            control_bits ^= self.GAIN_SELECTION
            self.i2c_write(self.CTRL_REG, control_bits)
    
    def getData(self):
        data = self.i2c_read(self.CTRL_REG, self.IR_LSB+1)
        # setting information
        control_bits = data[self.CTRL_REG]
        man_tint = data[self.MAN_TINT_MSB]<<8 | data[self.MAN_TINT_LSB]
        # RGB and IR
        red = data[self.RED_MSB]<<8 | data[self.RED_LSB]
        green = data[self.GREEN_MSB]<<8 | data[self.GREEN_LSB]
        blue = data[self.BLUE_MSB]<<8 | data[self.BLUE_LSB]
        ir = data[self.IR_MSB]<<8 | data[self.IR_LSB]
        return {
            'ctrl': control_bits, 
            'man_tint': man_tint, 
            'red': red, 
            'green': green, 
            'blue': blue, 
            'ir': ir
        }
    
    """
    fixed period mode:
        11: 179.2 ms, 10: 22.4 ms, 01: 1.4 ms, 00: 0.0875 ms
    manual setting mode:
        11: 358.4 ms, 10: 44.8 ms, 01: 2.8 ms, 00: 0.175 ms
    """
    def set_tint(self, tint):
        if tint == 0 or tint == 1 or tint == 2 or tint == 3:
            control_bits = self.get_ctrl_bits()
            control_bits >>= 2
            control_bits = (control_bits<<2) | tint
            self.i2c_write(self.CTRL_REG, control_bits)
        else:
            print('\ninvalid tint value: ')
            print(tint)
            print('tint should be from 0 to 3\n')
    
    @abstractmethod
    def calcMeasurementTime(self):
        print('\nCsABC calcMeasurementTime()\n')
    
    @abstractmethod
    def auto(self):
        print('\nCsABC auto()\n')
