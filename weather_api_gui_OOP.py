import requests
import tkinter as tk

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Погода")
        self.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Введите название города:")
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text="Получить погоду", command=self.get_weather_info)
        self.button.pack()

        self.result_label = tk.Label(self)
        self.result_label.pack()

    def city_to_coords(self, city_name):
        url = f"https://nominatim.openstreetmap.org/search.php?q={city_name}&format=json"
        response = requests.get(url)
        data = response.json()
        try:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        except IndexError:
            return "Неверное название города"

    def get_weather(self, coords):
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&current_weather=true&hourly=temperature_2m,windspeed_10m&windspeed_unit=ms"
        response = requests.get(weather_url)
        w_data = response.json()
        return w_data['current_weather']['temperature'], w_data['current_weather']['windspeed']

    def get_weather_info(self):
        city = self.entry.get()
        coords = self.city_to_coords(city)
        if isinstance(coords, str):
            self.result_label.config(text="Неверное название города")
        else:
            temperature = self.get_weather(coords)[0]
            windspeed = self.get_weather(coords)[1]
            self.result_label.config(text=f"г. {city}:\nТемпература: {temperature} °C\nСкорость ветра: {windspeed} м/с")

app = WeatherApp()
app.mainloop()