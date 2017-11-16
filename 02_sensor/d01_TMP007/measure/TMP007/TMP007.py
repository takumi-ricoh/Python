# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 13:08:11 2017

@author: root
"""

#!/usr/bin/python

import logging
import Adafruit_GPIO.I2C as I2C

#%% 
"""CONFIG (R/W)"""
REG_CONFIG             = 0x02
VALUE_CFG_RESET        = 0x8000
VALUE_CFG_MODEON       = 0x8000>>3
VALUE_CFG_CR2          = 0x8000>>4
VALUE_CFG_CR1          = 0x8000>>5
VALUE_CFG_CR0          = 0x8000>>6
VALUE_CFG_SAMPLE       = 0x0000  #ex 8sample:b|c
VALUE_CFG_ALERTEN      = 0x8000>>7
VALUE_CFG_ALERTF       = 0x8000>>8
VALUE_CFG_TRANSC       = 0x8000>>9
VALUE_CFG_COMPMODE     = 0x8000>>10

"""RESULT (R)"""
REG_VOBJ             = 0x00
REG_TDIE             = 0x01
REG_TOBJ             = 0x03

"""STATUS (R)"""
REG_STATUS           = 0x04

"""STATUS MASK (R/W)"""
REG_STATMASK           = 0x05
VALUE_STAT_ALERTEN     = 0x8000
VALUE_STAT_CRTEN       = 0x8000>>1
VALUE_STAT_OHEN        = 0X8000>>2
VALUE_STAT_OLEN        = 0X8000>>3
VALUE_STAT_LHEN        = 0X8000>>4
VALUE_STAT_LLEN        = 0X8000>>5  
VALUE_STAT_DVEN        = 0X8000>>6  
VALUE_STAT_MEM_C_EN    = 0X8000>>7
  
"""ALERT LIMIT (R/W)"""
REG_LIMIT_HDET          = 0x06
REG_LIMIT_LDET          = 0x07
REG_LIMIT_HDIE          = 0x08
REG_LIMIT_LDIE          = 0x09
VALUE_LIMIT_HDET        = 0x4100
VALUE_LIMIT_LDET        = 0x3C00
VALUE_LIMIT_HDIE        = 0x7FC0
VALUE_LIMIT_LDIE        = 0x3200

"""COEFFICIENT"""
REG_COEF_S0          = 0x0A
REG_COEF_A1          = 0x0B
REG_COEF_A2          = 0x0C
REG_COEF_B0          = 0x0D
REG_COEF_B1          = 0x0E
REG_COEF_B2          = 0x0F
REG_COEF_C2          = 0x10
REG_COEF_TC0         = 0x11
REG_COEF_TC1         = 0x12
VALUE_COEF_S0          = 0x6A16
VALUE_COEF_A1          = 0x01CB
VALUE_COEF_A2          = 0xFEE6
VALUE_COEF_B0          = 0x0000
VALUE_COEF_B1          = 0x6148
VALUE_COEF_B2          = 0x851F
VALUE_COEF_C2          = 0x0119
VALUE_COEF_TC0         = 0x0034
VALUE_COEF_TC1         = 0x0000

""" I2C address and device ID"""
TMP007_I2CADDR          = 0x40
TMP007_DEVID            = 0x1F


class TMP007(object):
        def __init__(self, mode=VALUE_CFG_SAMPLE, address=TMP007_I2CADDR,busnum=I2C.get_default_bus()):
                                                         
                self._logger = logging.getLogger('TMP007')

                #samplingmode
                self._mode = VALUE_CFG_SAMPLE
                # Create I2C device.
                self._device = I2C.Device(address, busnum)

                #setting/write
                self._set_configuration()
                self._set_statusmask()             
                self._set_alertlimit()                               
                self._set_coefficients() 

#%%
        """SETTING/WRITE methods"""
        def _set_configuration(self):
                #confON = VALUE_CFG_MODEON | VALUE_CFG_SAMPLE | VALUE_CFG_ALERTEN | VALUE_CFG_COMPMODE
                confON = VALUE_CFG_MODEON | VALUE_CFG_SAMPLE | VALUE_CFG_COMPMODE | VALUE_CFG_ALERTEN
                self._device.write16(REG_CONFIG, I2C.reverseByteOrder(confON))                

        def _set_statusmask(self):
                #maskON = VALUE_STAT_ALERTEN |VALUE_STAT_CRTEN | VALUE_STAT_OHEN | VALUE_STAT_OLEN| VALUE_STAT_LHEN | VALUE_STAT_LLEN
                maskON = VALUE_STAT_ALERTEN | VALUE_STAT_OHEN
                self._device.write16(REG_STATMASK, I2C.reverseByteOrder(maskON))

        def _set_alertlimit(self):
                self._device.write16(REG_LIMIT_HDET, I2C.reverseByteOrder(VALUE_LIMIT_HDET))
                self._device.write16(REG_LIMIT_LDET, I2C.reverseByteOrder(VALUE_LIMIT_LDET))
                self._device.write16(REG_LIMIT_HDIE, I2C.reverseByteOrder(VALUE_LIMIT_HDIE))
                self._device.write16(REG_LIMIT_LDIE, I2C.reverseByteOrder(VALUE_LIMIT_LDIE))                

        def _set_coefficients(self):
                self._device.write16(REG_COEF_S0, I2C.reverseByteOrder(VALUE_COEF_S0)) 
                self._device.write16(REG_COEF_A1, I2C.reverseByteOrder(VALUE_COEF_A1)) 
                self._device.write16(REG_COEF_A2, I2C.reverseByteOrder(VALUE_COEF_A2)) 
                self._device.write16(REG_COEF_B0, I2C.reverseByteOrder(VALUE_COEF_B0)) 
                self._device.write16(REG_COEF_B1, I2C.reverseByteOrder(VALUE_COEF_B1)) 
                self._device.write16(REG_COEF_B2, I2C.reverseByteOrder(VALUE_COEF_B2)) 
                self._device.write16(REG_COEF_C2, I2C.reverseByteOrder(VALUE_COEF_C2)) 
                self._device.write16(REG_COEF_TC0, I2C.reverseByteOrder(VALUE_COEF_TC0)) 
                self._device.write16(REG_COEF_TC1, I2C.reverseByteOrder(VALUE_COEF_TC1))

#%%
        """RESULT methods"""
        # read Die Temp in C
        def readDieTempC(self):
                raw = self._device.readU16BE(REG_TDIE)
                v = raw/4
                v *= 0.03125
                raw >>= 2
                Tdie = raw
                Tdie *= 0.03125 # convert to celsius
                self._logger.debug('Die temperature {0} C'.format(Tdie))
                return Tdie

        # read Obj Temp in C
        def readObjTempC(self):
                raw = self._device.readU16BE(REG_TOBJ)
                raw >>=2
                Tobj = raw
                Tobj *= 0.03125 # convert to celsius
                self._logger.debug('Obj temperature {0} C'.format(Tobj))
                return Tobj

        # read voltage
        def readVoltage(self):
                raw = self._device.readU16BE(REG_VOBJ)
                raw *= 156.25 # convert to nV
                raw /= 1000 # convert to uV
                self._logger.debug('Voltage {0} uV'.format(raw))
                return raw

#%%
        """SETTING/READ methods"""
        def readConfig(self):
                CONFIG = self._device.readU16BE(REG_CONFIG)
                #RST     = bin(CONFIG)[2]
                MOD     = bin(CONFIG)[2]
                CR2     = bin(CONFIG)[3]
                CR1     = bin(CONFIG)[4]
                CR0     = bin(CONFIG)[5] 
                ALRTEN  = bin(CONFIG)[6]
                ALRTF   = bin(CONFIG)[7]
                TC      = bin(CONFIG)[8]
                INTCOMP = bin(CONFIG)[9]
                print("--------------------------CONFIG---------------------------------")
                print("MOD:"+MOD,"CR2:"+CR2,"CR1:"+CR1,"CR0:"+CR0,
                      "ALRTEN:"+ALRTEN,"ALRTF:"+ALRTF,"TC:"+TC,"INTCOMP:"+INTCOMP)

        def readStatus(self):
                STATUS = self._device.readU16BE(REG_STATUS)
                ALRTF = bin(STATUS)[2]
                CRTF  = bin(STATUS)[3]
                OHF   = bin(STATUS)[4]
                OLF   = bin(STATUS)[5]
                LHF   = bin(STATUS)[6] 
                LLF   = bin(STATUS)[7]
                nVDF  = bin(STATUS)[8]
                MCRPT = bin(STATUS)[9]
                SNRL  = bin(STATUS)[10]
                print("--------------------------STATUS---------------------------------")
                print("ALRTF:"+ALRTF,"CRTF:"+CRTF,"OHF:"+OHF,"OLF:"+OLF,
                      "LHF:"+LHF,"LLF:"+LLF,"nVDF:"+nVDF,"MCRPT:"+MCRPT,"SNRL:"+SNRL)
                      
        def readStatusmask(self):
                STATMASK = self._device.readU16BE(REG_STATMASK)
                ALRTEN = bin(STATMASK)[2]
                CRTEN  = bin(STATMASK)[3]
                OHEN   = bin(STATMASK)[4]
                OLEN   = bin(STATMASK)[5]
                LHEN   = bin(STATMASK)[6] 
                LLEN   = bin(STATMASK)[7]
                DVEN  = bin(STATMASK)[8]
                MEM_C_EN = bin(STATMASK)[9]
                print("---------------------STATUSMASK----------------------------")
                print("ALRTEN:"+ALRTEN,"CRTEN:"+CRTEN,"OHEN:"+OHEN,"OLEN:"+OLEN,
                      "LHEN:"+LHEN,"LLEN:"+LLEN,"DVEN:"+DVEN,"MEM_C_EN:"+MEM_C_EN)

        def readAlert(self):
                Det_high = str(self._device.readU16BE(REG_LIMIT_HDET)>>6) #read left 10bit
                Det_low  = str(self._device.readU16BE(REG_LIMIT_LDET)>>6)
                Die_high = str(self._device.readU16BE(REG_LIMIT_HDIE)>>6)
                Die_low  = str(self._device.readU16BE(REG_LIMIT_LDIE)>>6)
                print("---------------------ALERT LIMIT----------------------------")                
                print("Det_high:"+Det_high,"Det_low:"+Det_low,"Die_high:"+Die_high,"Die_low:"+Die_low)

        def readCoeff(self):
                S0 = str(self._device.readU16BE(REG_COEF_S0))
                A1 = str(self._device.readU16BE(REG_COEF_A1))
                A2 = str(self._device.readU16BE(REG_COEF_A2))
                B0 = str(self._device.readU16BE(REG_COEF_B0))
                B1 = str(self._device.readU16BE(REG_COEF_B1))
                B2 = str(self._device.readU16BE(REG_COEF_B2))
                C2 = str(self._device.readU16BE(REG_COEF_C2))
                TC0 = str(self._device.readU16BE(REG_COEF_TC0))
                TC1 = str(self._device.readU16BE(REG_COEF_TC1))
                print("--------------------------COEFF---------------------------------")                
                print("S0:"+S0,"A1:"+A1,"A2:"+A2,"B0:"+B0,"B1:"+B1,"B2:"+B2,
                      "C2:"+C2,"TC0:"+TC0,"TC1:"+TC1)
