import mcp3021_driver as mcp_lib
import adc_plot as plot
import time

dynamic_range = 5.08
duration = 5.0
voltage_values = []
time_values = []
adc = mcp_lib.MCP3021(dynamic_range=dynamic_range, verbose=False)
try:
    print(f"Запуск записи данных с MCP3021 на {duration} секунд...")
    start_time = time.time()
    while (time.time() - start_time) < duration:
        current_time = time.time() - start_time
        v = adc.get_voltage()
        voltage_values.append(v)
        time_values.append(current_time)
    print("Сбор данных завершен. Отрисовка графиков...")
    plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)
    plot.plot_sampling_period_hist(time_values)
except KeyboardInterrupt:
    print("\nПроцесс прерван пользователем.")
finally:
    adc.deinit()
