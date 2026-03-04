import numpy as np
import time

def get_sin_wave_amplitude(freq, current_time):
    sin_val = np.sin(2*np.pi * freq * current_time)
    normalized_amplitude = (sin_val + 1) / 2
    return normalized_amplitude

def wait_for_sampling_period(sampling_frequency):
    sampling_period = 1 / sampling_frequency
    time.sleep(sampling_period)

def get_triangle_wave_amplitude(freq, current_time):
    period = 1 / freq
    relative_pos = (current_time % period)/ period

    if relative_pos < 0.5:
        return 2 * relative_pos
    else:
        return 2 * (1-relative_pos)
        