import r2r_adc as adc_lib
import adc_plot as plot
import time
dynamic_range = 3.28
duration = 3.0
voltage_values = []
time_values = []
adc = adc_lib.R2R_ADC(dynamic_range, compare_time=0.0001, verbose=False)
try:
    print(f"Сбор данных для анализа... ({duration} сек)")
    start_time = time.time()
    while (time.time() - start_time) < duration:
        current_time = time.time() - start_time
        v = adc.get_sc_voltage()
        voltage_values.append(v)
        time_values.append(current_time)
    print("Сбор завершен.")
    plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)
    plot.plot_sampling_period_hist(time_values)
except KeyboardInterrupt:
    print("\nПрервано.")
finally:
    adc.deinit()
