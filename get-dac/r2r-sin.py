import r2r_dac as r2r
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

dac_pins = [22,27,17,26,25,21,20,16]
dynamic_range = 3.3

try:
    dac = r2r.R2R_DAC(dac_pins, dynamic_range, verbose = False)
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
    