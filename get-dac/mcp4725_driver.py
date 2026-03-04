import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)

        self.address = address
        self.wm = 0x00   
        self.pds = 0x00  

        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать только целые числа")
            return

        if not (0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
            return

        first_byte = self.wm | self.pds | (number >> 8)
        second_byte = number & 0xFF

        self.bus.write_byte_data(self.address, first_byte, second_byte)

        if self.verbose:
            i2c_data = [self.address << 1, first_byte, second_byte]
            formatted_data = ", ".join([f"0x{b:02X}" for b in i2c_data])
            print(f"Число: {number}, отправленные по I2C данные: [{formatted_data}]\n")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            return

        number = int((voltage / self.dynamic_range) * 4095)
        self.set_number(number)

if __name__ == "__main__":
    try:
        dac = MCP4725(5.11, address=0x61, verbose=True)

        while True:
            try:
                line = input("Введите напряжение в Вольтах: ")
                if not line: continue

                voltage = float(line)
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
            except KeyboardInterrupt:
                break

    finally:
        dac.deinit()