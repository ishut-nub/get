import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time


        self.bits_gpio = [11,25,12,13,16,19,20,26]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)

        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()
        if self.verbose:
            print("GPIO cleaned up. ADC power off.")

    def number_to_dac(self, number):

        bin_str = bin(number)[2:].zfill(8)
        for i in range(8):

            bit_val = (number >> i) & 1
            GPIO.output(self.bits_gpio[i], bit_val)

    def sequential_counting_adc(self):
        for value in range(256):

            self.number_to_dac(value)
            time.sleep(self.compare_time)

            if GPIO.input(self.comp_gpio) == 1:
                if self.verbose:
                    print(f"Digital value: {value}")
                return value
        return 255

    def get_sc_voltage(self):
        digital_value = self.sequential_counting_adc()

        voltage = (digital_value / 255) * self.dynamic_range
        return voltage
    def successive_approximation_adc(self):
        value = 0
        for i in range(7, -1, -1):
            test_value = value + (1 << i)
            self.number_to_dac(test_value)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 0:
                value = test_value
        return value
    def indian_successive_approximation_adc(self):
        value = 128
        self.number_to_dac(value)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio) == 0:
            value += 64
        else:
            value -= 64

        self.number_to_dac(value)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio) == 0:
            value += 32
        else:
            value -= 32

        self.number_to_dac(value)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio) == 0:
            value += 16
        else:
            value -= 16

        self.number_to_dac(value)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio) == 0:
            value += 8
        else:
            value -= 8

        self.number_to_dac(value)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio) == 0:
            value += 4
        else:
            value -= 4

        self.number_to_dac(value)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio) == 0:
            value += 2
        else:
            value -= 2

        self.number_to_dac(value)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio) == 0:
            value += 1
        else:
            value -= 1

        self.number_to_dac(value)
        time.sleep(self.compare_time)
        if GPIO.input(self.comp_gpio) == 1:
            value -= 1

        return value
    def get_sar_voltage(self):
        digital_value = self.indian_successive_approximation_adc()
        voltage = (digital_value / 255) * self.dynamic_range
        return voltage
if __name__ == "__main__":
    try:
        adc = R2R_ADC(dynamic_range=3.28, verbose=False)

        print("SAR ADC запущен. Вращайте ручку потенциометра...")
        print("Для выхода нажмите Ctrl+C")

        while True:
            voltage = adc.get_sar_voltage()
            print(f"Измеренное напряжение (SAR): {voltage:.2f} V")

    except KeyboardInterrupt:
        print("\nПрограмма остановлена.")
    finally:
        adc.deinit()
