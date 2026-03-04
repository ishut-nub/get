import pwm_dac as pwm
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 5
sampling_frequency = 1000

pwm_pin = 12
pwm_freq = 1000
dynamic_range = 3.29

try:
    dac = pwm.PWM_DAC(pwm_pin, pwm_freq, dynamic_range, verbose = False)
    start_time = time.time()

    print(f"Генерация сигнала: {signal_frequency} Гц...")

    while True:
        current_time = time.time() - start_time

        norm_amp = sg.get_sin_wave_amplitude(signal_frequency, current_time)

        target_voltage = norm_amp * amplitude
        dac.set_voltage(target_voltage)

        sg.wait_for_sampling_period(sampling_frequency)

except KeyboardInterrupt:
    print("generation stopped")

finally:
    dac.deinit()
    