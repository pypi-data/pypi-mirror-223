
MODE = {
    0b10: 'Heating Mode',
    0b01: 'Cooling Mode',
    0b00: 'Near Cooling and Heating Boundary' 
}

BUCK_ILIM_HS = {
    '2.5': 0b00000000,
    '3.0': 0b00000100,
    '3.5': 0b00001000,
    '4.0': 0b00001100
}

BUCK_ILIM_LS = {
    '2.5': 0b00000000,
    '3.0': 0b00000001,
    '3.5': 0b00000010,
    '4.0': 0b00000011
}

LDO_ILIM_HS = {
    '1.2': 0b00000000,
    '1.5': 0b01000000,
    '1.8': 0b10000000,
    '2.1': 0b11000000
}

LDO_ILIM_LS = {
    '1.2': 0b00000000,
    '1.5': 0b00010000,
    '1.8': 0b00100000,
    '2.1': 0b00110000
}





#MP8833 Reg01 ILIM_HEAT and Reg02 ILIM_COOL in mA

ILIM = {
    '39': 0b00000,
    '78': 0b00001,
    '117': 0b00010,
    '156': 0b00011,
    '195': 0b00100,
    '234': 0b00101,
    '273': 0b00110,
    '312': 0b00111,
    '351': 0b01000,
    '390': 0b01001,
    '429': 0b01010,
    '468': 0b01011,
    '507': 0b01100,
    '546': 0b01101,
    '585': 0b01110,
    '624': 0b01111,
    '663': 0b10000,
    '702': 0b10001,
    '741': 0b10010,
    '780': 0b10011,
    '819': 0b10100,
    '858': 0b10101,
    '897': 0b10110,
    '936': 0b10111,
    '975': 0b11000,
    '1014': 0b11001,
    '1053': 0b11010,
    '1092': 0b11011,
    '1131': 0b11100,
    '1470': 0b11101,
    '1209': 0b11110,
    '1248': 0b11111,
    '1287': 0b100000,
    '1326': 0b100001,
    '1365': 0b100010,
    '1404': 0b100011,
    '1443': 0b100100,
    '1482': 0b100101,
    '1521': 0b100110,
    '1560': 0b100111,
    '1599': 0b101000,
    '1638': 0b101001,
    '1677': 0b101010,
    '1716': 0b101011,
    '1755': 0b101100,
    '1794': 0b101101,
    '1833': 0b101110,
    '1872': 0b101111,
    '1911': 0b110000,
    '1950': 0b110001,
    '1989': 0b110010,
    '2028': 0b110011
}

DIS_TIME = {
    '70': 0b00010000,
    '35': 0b00000000
}

SS_CURRENT = {
    '1X': 0b00000000,
    '2x': 0b00000100,
    '4x': 0b00001000,
    '8x': 0b00001100,
}


class mp8833:

    def __init__(self, device_addr = 0x60) -> None:
        self.self.i2cbus = self.i2cbus
        self.addr = device_addr

    #MP8833 Reg03 VLIM_HEAT and Reg04 VLIM_COOL in mV
    #mV = 97.6*(bin_value)+97.6
    def vlim(self, mV):
        if mV < 0:
            print('VLIM can not be less than 0!!')
            print('VLIM was set as 97.6mV.')
            mV = 0
        elif mV > 5563.2 :
            print('VLIM can not be grater than 5563.2!!')
            print('VLIM was set as 5563.2mV.')
            mV = 5563.2

        bin_value = (mV - 97.6)/97.6
        bin_value = round(bin_value)
        return bin_value

    def write_reg(self, reg, data):
        while not self.i2cbus.try_lock():
            pass
        try:
            buf = bytearray(1)
            buf[0] = reg
            buf.extend(data)
            self.i2cbus.writeto(self.addr, bytearray([buf]))
        finally:
            self.i2cbus.unlock()

    def read_reg(self, reg):
        while not self.i2cbus.try_lock():
            pass
        try:
            self.i2cbus.writeto(self.addr, bytes([reg]))
            result = bytearray(1)
            self.i2cbus.readfrom_into(self.addr, result)
            return result[0]
        finally:
            self.i2cbus.unlock()

    def I2C_ON(self):
        #Reg00 SYS_SET setting the I2C on state (datasheet pg. 29)
        SYS_SET_value = 0x00#bytearray(1)
        SYS_SET_value = self.read_reg( 0x00)
        i2c_on = SYS_SET_value | 0b1
        self.write_reg( 0x00, i2c_on)

    def read_address(self):
        #Reg06 self.ADDR reading the register (datasheet pg. 30)
        self.address_value = bytearray(1)
        self.address_value = self.read_reg( 0x06)
        #self.address_value = self.address_value[0] >> 1
        return self.address_value   
 
    def mp8833_read_IMON(self):
        #Reg07 IMON Reading (datasheet pg. 30)
        IMON_reg_value = bytearray(1)
        IMON_reg_value = self.read_reg( 0x07)

        return abs(19.53*(128 - IMON_reg_value))
    
    def mp8833_read_STATUS(self):
        #Reg09 STATUS Reading (datasheet pg. 31)
        status_value = bytearray(1)
        status_value = self.read_reg( 0x09) 
        return status_value

    def mp8833_decode_STATUS(self, status_value):
        mode = status_value >> 6
        vlim_status = status_value & 0b00100000
        vlim_status >>= 5
        ilim_status = status_value & 0b00010000
        ilim_status >>= 4
        pwor_status = status_value & 0b00001000
        pwor_status >>= 3
        ot_status = status_value & 0b00000010
        ot_status >>= 1
        otw_status = status_value & 0b00000001

        print("MODE:\t{mode}".format(mode=MODE[mode]))
        print("VLIM:\t", bool(vlim_status))
        print("ILIM:\t", bool(ilim_status))
        print("PWOR:\t", bool(pwor_status))
        print("OT:\t", bool(ot_status))
        print("OTW:\t", bool(otw_status))

    def mp8833_read_VTEC(self):
        #Reg08 VTEC Reading (datasheet pg. 30)
        VTEC_reg_value = bytearray(1)
        VTEC_reg_value = self.read_reg( 0x08)

        return abs(50*(128-VTEC_reg_value))
    
    def mp8833_refresh(self):
        # Reg00 SYS_SET Refresh (datasheet pg. 29)
        SYS_SET_value = bytearray(1)
        SYS_SET_value = self.read_reg( 0x00)
        refresh_instuctor = SYS_SET_value | 0b00000010
        self.write_reg( 0x00, bytearray([refresh_instuctor]))  # Pass data as a bytearray

    def mp8833_set_DIS_TIME(self,  dis_time):
        #Reg00 SYS_SET setting the DIS_TIME (datasheet pg. 29)
        SYS_SET_value = bytearray(1)
        SYS_SET_value = self.read_reg( 0x00)
        SYS_SET_value = SYS_SET_value & 0b11101111
        DIS_TIME_instructor = SYS_SET_value | dis_time
        self.write_reg( 0x00, bytes([DIS_TIME_instructor]))

    def mp8833_set_ILIM_COOL(self,  ilim_cool, on):
        #Reg02 ILIM_COOL setting (datasheet pg. 29)
        ILIM_COOL_value = bytearray(1)
        ILIM_COOL_value = self.read_reg( 0x02)
        state = on << 7
        #ILIM_COOL_value = ILIM_COOL_value & 0b10000000
        ILIM_COOL_value = state | ilim_cool
        self.write_reg( 0x02, bytes([ILIM_COOL_value]))

    def mp8833_set_ILIM_HEAT(self,  ilim_heat, on):
        #Reg01 ILIM_HEAT setting (datasheet pg. 29)
        ILIM_HEAT_value = bytearray(1)
        ILIM_HEAT_value = self.read_reg( 0x01)
        state = on << 7
        #ILIM_HEAT_value = ILIM_HEAT_value & 0b10000000
        ILIM_HEAT_value = state | ilim_heat
        self.write_reg( 0x01, bytes([ILIM_HEAT_value]))

    def mp8833_set_LIMIT(self,  ldo_ilim_hs = LDO_ILIM_HS['1.8'], ldo_ilim_ls = LDO_ILIM_LS['1.8'], buck_ilim_hs = BUCK_ILIM_HS['3.0'], buck_ilim_ls = BUCK_ILIM_LS['3.0']):
        #Reg05 LIMIT Setting (datasheet pg. 30)
        LIMIT_value = ldo_ilim_hs | ldo_ilim_ls | buck_ilim_hs | buck_ilim_ls
        self.write_reg( 0x05, bytes([LIMIT_value]))

    def mp8833_set_SS_CURRENT(self,  ss_current):
        #Reg00 SYS_SET setting the SS_CURRENT (datasheet pg. 29)
        SYS_SET_value = bytearray(1)
        SYS_SET_value = self.read_reg( 0x00)
        SYS_SET_value = SYS_SET_value & 0b11110011
        ss_current_value = SYS_SET_value | ss_current
        self.write_reg( 0x00, bytes([ss_current_value]))

    def mp8833_set_VLIM_COOL(self,  vlim_cool, on=True):
        #Reg04 VLIM_COOL setting (datasheet pg. 30)
        VLIM_COOL_value = bytearray(1)
        VLIM_COOL_value =  self.read_reg( 0x04)
        state = on << 7
        VLIM_COOL_value = state | vlim_cool
        self.write_reg( 0x01, bytes([VLIM_COOL_value]))

    def mp8833_set_VLIM_HEAT(self,  vlim_heat, on=True, ovp=True):
        #Reg03 VLIM_HEAT setting (datasheet pg. 29)
        VLIM_HEAT_value = bytearray(1)
        VLIM_HEAT_value = self.read_reg( 0x03)
        state = on << 7
        state = state & (ovp << 6)
        VLIM_HEAT_value = state | vlim_heat
        self.write_reg( 0x03, VLIM_HEAT_value)