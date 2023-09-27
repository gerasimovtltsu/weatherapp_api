import requests

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

city = input("Введите название города: ")
coords = city_to_coords(city)
temperature = get_weather(coords)[0]
windspeed = get_weather(coords)[1]
print(f"г. {city}:\nТемпература: {temperature} °C\nСкорость ветра: {windspeed} м/с")