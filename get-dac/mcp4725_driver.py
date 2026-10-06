import smbus
class MCP4725:
    def __init__(self, d_range, address=0x61, verbose=True):
        self.bus=smbus.SMBus(1)

        self.address=address
        self.wm=0x00
        self.pds=0x00

        self.verbose=verbose
        self.d_range=d_range

    def deinit(self):
        self.bus.close()

    def set_number(self,number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")

        if not (0<=number<=4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")

        first_byte= self.wm | self.pds | number >> 8
        second_byte= number & 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)

        if self.verbose:
            print(f"Число:{number}, отправленные по I2C данные: [0x{(self.address<<1):02X},0x{first_byte:02X},")

    def set_voltage(self,voltage):
        number=int(voltage/self.d_range*4095)
        self.set_number(number)

if __name__ =="__main__":
    try:
        mcp=MCP4725(5.00)

        while True:
            try:
                voltage=float(input("Введите напряжение в вольтах: "))
                mcp.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не числою Попробуйте еще раз.")

    finally:
        mcp.deinit()
