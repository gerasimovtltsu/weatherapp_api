import requests
import tkinter as tk

# Создаем графический интерфейс
window = tk.Tk()
window.title("Погода")
window.geometry("300x200")

# Получаем координаты города
def city_to_coords(city_name):
  url = f"https://nominatim.openstreetmap.org/search.php?q={city_name}&format=json"
  response = requests.get(url)
  data = response.json()
  try:
    lat = data[0]['lat']
    lon = data[0]['lon']
    return lat, lon
  except IndexError:
    return "Неверное название города"

# Получаем погоду
def get_weather(coords):
  weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&current_weather=true&hourly=temperature_2m,windspeed_10m&windspeed_unit=ms"
  response = requests.get(weather_url)
  w_data = response.json()
  return w_data['current_weather']['temperature'], w_data['current_weather']['windspeed']

# Функция для обработки нажатия кнопки
def get_weather_info():
    city = entry.get()
    coords = city_to_coords(city)
    if isinstance(coords, str):
        result_label.config(text="Неверное название города")
    else:
        temperature = get_weather(coords)[0]
        windspeed = get_weather(coords)[1]
        result_label.config(text=f"г. {city}:\nТемпература: {temperature} °C\nСкорость ветра: {windspeed} м/с")

# Создаем элементы GUI
label = tk.Label(window, text="Введите название города:")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Получить погоду", command=get_weather_info)
button.pack()

result_label = tk.Label(window)
result_label.pack()

# Запускаем главный цикл GUI
window.mainloop()