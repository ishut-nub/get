import mcp4725_driver as mcp
import signal_generator as sg
import time

amplitude = 4.0
signal_frequency = 2
sampling_frequency = 500

dynamic_range = 5.11
i2c_address = 0x61

try:
    dac = mcp.MCP4725(dynamic_range, address=i2c_address, verbose=False)

    start_time = time.time()
    print(f"Генерация сигнала: {signal_frequency} Гц...")


    while True:
        current_time = time.time() - start_time

        norm_amp = sg.get_triangle_wave_amplitude(signal_frequency, current_time)

        voltage = norm_amp * amplitude
        dac.set_voltage(voltage)

        sg.wait_for_sampling_period(sampling_frequency)

except KeyboardInterrupt:
    print("\ngeneration stopped")

finally:
    if 'dac' in locals():
        dac.set_number(0)
        dac.deinit()
