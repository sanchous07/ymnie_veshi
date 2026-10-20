import smbus
import time

class MCP3021:
    def __init__(self,d_range,verbose=False):
        self.bus=smbus.SMBus(1)
        self.d_range=d_range
        self.address=0x4D
        self.verbose=verbose

    def get_number(self):
        data=self.bus.read_word_data(self.address,0)
        lower_data_byte=data>>8
        upper_data_byte=data&0xFF
        number=(upper_data_byte<<6)|(lower_data_byte>>2)
        if self.verbose:
            print(f"Принятые данные: {data}, Старший байт: {upper_data_byte}, Младший байт: {lower_data_byte}, Число: {number}")
        return number
    
    def get_voltage(self):
        n=self.get_number()
        return self.d_range*n/2**10

    def deinit(self):
        self.bus.close()

if __name__ =="__main__":
    try:
        mcp=MCP3021(3.2)

        while True:
            voltage=mcp.get_voltage()
            print(voltage)
            time.sleep(1)
    finally:
        mcp.deinit()