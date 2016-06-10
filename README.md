# CsCntlr (Color-sensor Controller)

A python package for the color sensor S11059-02DT.

# Installation

```
pip install CsCntlr
```

# Getting Started

```
# First, create a CsCntlr instance
from CsCntlr import *
cs = CsCntlr()

# Then, select the mode to be used
cs.useFixedPeriodMode()
cs.useManualSettingMode()

# You can measure colors by using the code below
cs.cntlr.auto()
```

# Examples for Fixed Period Mode

```
from CsCntlr import *
cs = CsCntlr()
cs.useFixedPeriodMode()

# You can specify the gain and the integration time (tint)
cs.cntlr.auto(gain='low', tint=2)

# gain should be 'low' or 'high' (low:high = 1:10)
cs.cntlr.auto(gain='lolo')
cs.cntlr.auto(gain='hi')

# tint should be from 0 to 3 
# 3: 179.2 ms, 2: 22.4 ms, 1: 1.4 ms, 0: 0.0875 ms (per color)
cs.cntlr.auto(tint=100)
cs.cntlr.auto(tint='hi')
```

# Examples for Manual Setting Mode

In this mode, the sensor goes to standby mode after the measurement.

```
from CsCntlr import *
cs = CsCntlr()
cs.useManualSettingMode()

# You can specify the manual integration time (man_tint)
cs.cntlr.auto(gain='high', man_tint=100, tint=0)
cs.cntlr.auto(man_tint=1)

# gain should be 'low' or 'high' (low:high = 1:10)
cs.cntlr.auto(gain='lolo')
cs.cntlr.auto(gain='hi')

# tint should be from 0 to 3
# 3: 358.4 ms, 2: 44.8 ms, 1: 2.8 ms, 0: 0.175 ms (per color)
cs.cntlr.auto(tint=100)
cs.cntlr.auto(tint='hi')

# man_tint should be from 0 to 65535
# measurement_time = tint * man_tint (per color)
cs.cntlr.auto(gain='high', man_tint=70000, tint=1)
cs.cntlr.auto(man_tint='hi')
```

# Note: CsCntlr is Singleton

```
from CsCntlr import *
cs = CsCntlr()
cs.useManualSettingMode()

cs1 = CsCntlr()
cs1.useFixedPeriodMode()

# now, cs is changed to the Fixed Period Mode
print(cs.cntlr_mode)
# Fixed Period Mode
```
