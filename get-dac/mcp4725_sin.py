import mcp4725_driver as mcp
import signal_generator as sg
import time

amplitude = 4.5
signal_frequency = 5
sampling_frequency = 500

i2c_address = 0x61
dynamic_range = 5.11

try:
    dac = mcp.MCP4725(dynamic_range, address=i2c_address, verbose=False)
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
    