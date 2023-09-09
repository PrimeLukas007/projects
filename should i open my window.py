import json
import requests
from datetime import datetime
import tkinter as tk
import os


config_file_path = os.path.dirname(os.path.realpath(__file__))


def get_link(config_file_path):
    with open(config_file_path + '/config.json') as config_file:
        config_data = json.load(config_file)
        location_info = config_data.get('info', {}).get('location', {})
        lat = float(location_info.get('lat'))
        long = float(location_info.get('long'))
        timezone = config_data.get('info', {}).get('timezone', {})
        # print(lat, long, timezone)
        base_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m,rain&timezone={timezone}'
        return base_url


response = requests.get(get_link(config_file_path))
data = response.json()

hourly_data = data['hourly']
current_time = datetime.now().isoformat()
closest_time = min(hourly_data['time'], key=lambda x: abs(
    datetime.fromisoformat(current_time) - datetime.fromisoformat(x)))
closest_index = hourly_data['time'].index(closest_time)
temperature_at_closest_time = hourly_data['temperature_2m'][closest_index]


print(f'Current time: {current_time}')
print(f'Temperature at {closest_time}: {temperature_at_closest_time}°C')

saving = open(config_file_path + '/info.json', 'w')
json.dump(data, saving, indent=6)
saving.close()

window = tk.Tk()
window.geometry("400x400")

temperature_inside = tk.Label(window, text="Your Temperature:")
temperature_inside.pack()
temperature_inside_field = tk.Entry(window)
temperature_inside_field.pack()


def open_it():
    with open(config_file_path + '/config.json') as config_file:
        config_data = json.load(config_file)
        ideal_temperature = config_data.get(
            'info', {}).get('idealtemperature', {})
        ideal_temperature = float(ideal_temperature)
    temperature_inside = temperature_inside_field.get()
    print(temperature_inside)

    if float(temperature_inside) > ideal_temperature:
        if float(temperature_inside) > float(temperature_at_closest_time):
            should_i_open_my_window.config(
                text=f'Yes, it is {temperature_inside}°C inside and {temperature_at_closest_time}°C outside')
        else:
            should_i_open_my_window.config(
                text=f'No, it is {temperature_inside}°C inside and {temperature_at_closest_time}°C outside')
    else:
        if float(temperature_inside) > float(temperature_at_closest_time):
            should_i_open_my_window.config(
                text=f'No, it is {temperature_inside}°C inside and {temperature_at_closest_time}°C outside')
        else:
            should_i_open_my_window.config(
                text=f'Yes, it is {temperature_inside}°C inside and {temperature_at_closest_time}°C outside')


sumbit_button = tk.Button(window, text="Submit",
                          command=open_it)
sumbit_button.pack()

should_i_open_my_window = tk.Label(
    window, text="Should I open my window?")
should_i_open_my_window.pack()

window.mainloop()
