import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self,gpio_bits,dynamic_range,verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)
    def deinit(self):
        GPIO.output(self.gpio_bits,0)
        GPIO.cleanup()
    def set_number(self, number):
        bits_list = []

        for i in range(len(self.gpio_bits)):
            bit = (number >> i) & 1
            bits_list.append(bit)
            GPIO.output(self.gpio_bits[i], bit)
        if self.verbose:
            print(f"Число на выход ЦАП: {number} {bits_list}\n")
    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} B)")
            print("Устанавливаем в 0.0 В")
            self.set_number(0)
            return
    
        max_value = (2 ** len(self.gpio_bits)) -1
        number = int(voltage / self.dynamic_range * max_value)
        self.set_number(number)
if __name__ == "__main__":
    try:
        dac = R2R_DAC([22,27,17,26,25,21,20,16], 3.183, True)
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
            except KeyboardInterrupt:
                break
    finally:
        dac.deinit()