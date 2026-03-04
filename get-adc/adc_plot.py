import matplotlib.pyplot as plt

def plot_voltage_vs_time(time_list, voltage_list, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time_list, voltage_list)
    plt.title('Зависимость напряжения от времени (8-bit SC ADC)')
    plt.xlabel('Время, с')
    plt.ylabel('Напряжение, В')
    plt.xlim(0, max(time_list) if time_list else 1)
    plt.ylim(0, max_voltage + 0.5)
    plt.grid(True)
    plt.show()
def plot_sampling_period_hist(time_list):
    sampling_periods = []
    for i in range(len(time_list) - 1):
        delta = time_list[i+1] - time_list[i]
        sampling_periods.append(delta)
    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods, bins=50, color='skyblue', edgecolor='black')
    plt.title('Распределение периодов дискретизации АЦП')
    plt.xlabel('Продолжительность одного измерения, с')
    plt.ylabel('Количество измерений')
    plt.xlim(0, 0.06)
    plt.grid(True)
    plt.show()
