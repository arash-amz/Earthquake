# -*- coding: utf-8 -*-
import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock


def get_earthquake_data():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": "2023-07-20T00:00:00.000Z",
        "endtime": "2023-07-20T23:59:59.999Z",
        "minmag": 4.0,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    earthquake_data = response.json()

    return earthquake_data


def check_for_nearby_earthquakes(earthquake_data, latitude_range, longitude_range):
    pass


class MyApp(App):
    def build(self):
        self.label = Label(text="**هشدار زلزله**")
        self.latitude_range = [35.689488, 35.776284]
        self.longitude_range = [51.240556, 51.402778]
        self.update_data()
        return self.label

    def on_start(self):
        self.timer = Clock.schedule_interval(self.update_data, 60)

    def on_stop(self):
        self.timer.cancel()

    def update_data(self):
        earthquake_data = get_earthquake_data()

        if check_for_nearby_earthquakes(earthquake_data, self.latitude_range, self.longitude_range):
            # تبدیل متن به UTF-16
            متن_فارسی = f"**هشدار! زلزله نزدیک تهران رخ داده است.**\n\nشدت: {earthquake_data['features'][0]['properties']['mag']} ریشتر\nمکان: {earthquake_data['features'][0]['properties']['place']}\nزمان: {earthquake_data['features'][0]['properties']['time']}"
            متن_فارسی_utf16 = متن_فارسی.encode('utf-16')

            # نمایش متن به UTF-16
            self.label.text = متن_فارسی_utf16
        else:
            self.label.text = f"**هشدار زلزله**\n\nزلزله‌ای در محدوده تهران رخ نداده است."


if __name__ == "__main__":
    MyApp().run()
