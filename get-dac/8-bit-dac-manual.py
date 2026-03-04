import RPi.GPIO as GPIO
dac_bits = [22,27,17,26,25,21,20,16]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac_bits, GPIO.OUT)

dynamic_range = 3.17

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} B)")
        print("Устанавливаем в 0.0 В")
        return 0
    
    return int(voltage/dynamic_range * 255)

def number_to_dac(number):
    bits_list = []

    for i in range(8):
        bit = (number >> i) & 1
        bits_list.append(bit)
        GPIO.output(dac_bits[i], bit)

    print(f"Число на выход ЦАП: {number} {bits_list}\n")
try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)

        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")

finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()