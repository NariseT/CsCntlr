from __modes.CsFPM import *
from __modes.CsMSM import *

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class CsCntlr(object):
    __metaclass__ = Singleton
    
    # return:
    # 1: manual setting mode, 0: fixed period mode
    def __read_current_mode(self, cntlr):
        control_bits = cntlr.get_ctrl_bits()
        current_mode = control_bits & cntlr.TINT_MODE
        return current_mode 
    
    def __toggle_mode(self, cntlr):
        control_bits = cntlr.get_ctrl_bits()
        control_bits ^= cntlr.TINT_MODE
        cntlr.i2c_write(cntlr.CTRL_REG, control_bits)
    
    def useFixedPeriodMode(self):
        self.cntlr = CsFPM()
        if not self.__read_current_mode(self.cntlr):
            self.cntlr_mode = 'Fixed Period Mode'
            return self.cntlr
        else:
            self.__toggle_mode(self.cntlr)
            self.cntlr_mode = 'Fixed Period Mode'
            return self.cntlr
    
    def useManualSettingMode(self):
        self.cntlr = CsMSM()
        if self.__read_current_mode(self.cntlr):
            self.cntlr_mode = 'Manual Setting Mode'
            return self.cntlr
        else:
            self.__toggle_mode(self.cntlr)
            self.cntlr_mode = 'Manual Setting Mode'
            return self.cntlr
