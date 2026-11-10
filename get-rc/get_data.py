import rc_plot
import time
import smbus

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

voltage_values=[]
time_values=[]
duration=15.0
compare_time=0.001
d_range=10

mcp=MCP3021(d_range)
if __name__ =="__main__":
    try:
        t0=time.time()
        while time.time()-t0<duration:
                voltage=mcp.get_voltage()
                voltage_values.append(voltage)
                time_values.append(time.time()-t0)
        # rc_plot.plot_voltage_vs_time(time_values,voltage_values,d_range)
        rc_plot.grafik_voltage(time_values,voltage_values,d_range)
    finally:
        mcp.deinit()
