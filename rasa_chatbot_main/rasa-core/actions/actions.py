# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from deep_translator import GoogleTranslator
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
from datetime import datetime, timedelta


class action_get_weather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

# ------------------------------- Phục vụ mục đích test------------------------------------------------------------------------------------------------
        print("---------------------------------------------------------------------------------------------------------")
        # Lấy các slots
        slots = tracker.slots

        # Lấy intent và confidence từ latest_message
        latest_intent = tracker.latest_message['intent']['name']
        latest_confidence = tracker.latest_message['intent']['confidence']

        # Lấy các entities từ latest_message
        entities = tracker.latest_message['entities']

        # Lấy intent ranking từ latest_message
        intent_ranking = tracker.latest_message['intent_ranking']

        # In các giá trị
        print("Slots:")
        for slot_name, slot_value in slots.items():
            print(f"{slot_name}: {slot_value}")

        print(f"\nLatest Intent: {latest_intent}, Confidence: {latest_confidence}")

        print("\nEntities:")
        for entity in entities:
            print(entity)

        print("\nIntent Ranking:")
        for intent in intent_ranking:
            print(f"Intent: {intent['name']}, Confidence: {intent['confidence']}")

        print("---------------------------------------------------------------------------------------------------------")

# ------------------------------- Phục vụ mục đích test------------------------------------------------------------------------------------------------

        # Đặt giá trị của api_key là khóa API cho OpenWeather API, dùng để truy cập thông tin thời tiết
        api_key = 'e7c0da0d1e27ebd35e173a262333b74f'
        loc = tracker.get_slot('location')
        forecastPeriod = tracker.get_slot('forecast_period')
        weatherType = tracker.get_slot('weather_type')
        guess = tracker.get_slot('guess')

        response = ''
        today = datetime.now()
        tomorrow = str(today + timedelta(days=1))
        next2Day = str(today + timedelta(days=2))
        if not loc:  # Nếu trong câu không có địa điểm
            response = "Bạn muốn biết về thời tiết tại địa điểm nào?"
        else:
            # dispatcher.utter_message(text=f'Địa điểm: {loc}')
            # sử dụng API lấy toạ độ
            coordinates = requests.get(
                'http://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid={}'.format(loc, api_key)).json()
            lat = round(coordinates[0]['lat'], 2)
            lon = round(coordinates[0]['lon'], 2)
            if coordinates:
                # sử dụng API để dự báo thời tiết
                weathers = requests.get(
                    'http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'.format(lat, lon,
                                                                                                    api_key)).json()
                # sử dụng API lấy dữ liệu thời tiết hiện tại
                current = requests.get(
                    'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(loc, api_key)).json()
                # country = weathers['city']['country']
                city = loc

                if weathers:

# -------------------------------------------------------Dự báo thời tiết cho hôm nay ----------------------------------------------------------------------#

                    if forecastPeriod is None or forecastPeriod == 'hôm nay':
                        ##current

                        # Lấy thông tin thời tiết
                        conditionCurrent = current['weather'][0]['main'] # Dịch
                        conditionDesc = current['weather'][0]['description'] # Dịch
                        temperature_cCurrent = round(current['main']['temp'] - 273.15, 2)
                        feelLike = round(current['main']['feels_like'] - 273.15, 2)
                        humidityCurrent = current['main']['humidity']
                        wind_mphCurrent = current['wind']['speed']
                        wind_dirCurrent = self.wind_direction(current['wind']['deg']) # Lấy tên hướng gió

                        if weatherType is None or weatherType == 'thời tiết':
                            response = GoogleTranslator(source='en', target='vi').translate("""It is currently {} in {} at the moment. The temperature is {} degrees in C, feel like {} degrees in C, the humidity is {}% and the wind speed is {} mph."""
                                                                                            .format(conditionCurrent, city, temperature_cCurrent, feelLike, humidityCurrent, wind_mphCurrent))
                        elif weatherType == 'nhiệt độ':
                            response = GoogleTranslator(source='en', target='vi').translate("""The current temperature is {} degrees in C, feel like {} degrees in C """.format(temperature_cCurrent,
                                                                                                  feelLike))
                        elif weatherType == 'độ ẩm':
                            response = GoogleTranslator(source='en', target='vi').translate("""The humidity now is {}%""".format(humidityCurrent))
                        elif weatherType == 'gió':
                            response = GoogleTranslator(source='en', target='vi').translate("""The wind today is {} mph with direction is {} and gust is {} mph""".format(
                                wind_mphCurrent, wind_dirCurrent, current['wind']['gust']))
                        elif weatherType == 'nắng':
                            if conditionCurrent == 'Rain':
                                response = GoogleTranslator(source='en', target='vi').translate(f"""No, today is not sunny, it {conditionDesc}""")
                            if conditionDesc == 'clear sky':
                                response = GoogleTranslator(source='en', target='vi').translate("""Yes, the weather today is sunny, you should use sunscreen if you want to go out 😉""")
                            elif conditionDesc == 'few clouds' or conditionDesc =='scattered clouds':
                                response = GoogleTranslator(source='en', target='vi').translate("""Hmmm, it's not exactly sunny today, maybe a little because there are scattered clouds today 😉""")
                            else:
                                response = GoogleTranslator(source='en', target='vi').translate(f"""No, today is not sunny, it {conditionDesc}""")
                        elif weatherType == 'Rain':
                            if conditionCurrent == 'Rain':
                                if conditionDesc == 'light rain':
                                    response = GoogleTranslator(source='en', target='vi').translate("""Yes, The weather today is rain but it is light rain, you may be bring umbrella ☔""")
                                elif conditionDesc == 'moderate rain':
                                    response = GoogleTranslator(source='en', target='vi').translate("""Yes, The weather today is rain with moderate rain, you should bring a raincoat and move carefully if you go out 😭""")
                                else:
                                    response = GoogleTranslator(source='en', target='vi').translate("""VYes, The weather today is rain, you should bring a raincoat and move carefully if you go out 😭""")
                            elif conditionCurrent == "Clouds":
                                if conditionDesc == 'broken clouds' or conditionDesc == 'overcast clouds':
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""Today's weather is likely to be rainy with {conditionDesc}, you should bring umbrella""")
                                else:
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""No, today is not rain, it is {conditionDesc}""")
                            else:
                                response = GoogleTranslator(source='en', target='vi').translate(f"""No, today is not rain, it is {conditionDesc}""")

# -------------------------------------------------------Dự báo thời tiết cho ngày mai ----------------------------------------------------------------------#

                    elif forecastPeriod == 'ngày mai':
                        ##tomorrow
                        tomorrows = [item for item in weathers['list'] if tomorrow[0:10] in item['dt_txt']]
                        morning = [item for item in tomorrows if item['dt_txt'][11:] == '09:00:00']
                        afternoon = [item for item in tomorrows if item['dt_txt'][11:] == '15:00:00']
                        evening = [item for item in tomorrows if item['dt_txt'][11:] == '21:00:00']
                        conditionCurrent = afternoon[0]['weather'][0]['main']
                        conditionDesc = afternoon[0]['weather'][0]['description']
                        if weatherType is None or weatherType == 'thời tiết':
                            response = GoogleTranslator(source='en', target='vi').translate(("""The weather tomorrow in {}: \n
                            - Morning will be {} with {}: temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.\n
                            - Afternoon will feel {} with {}: temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.\n
                            - Evening will like {} with {}: temperature is {} degrees, the humidity is {}% and the wind speed is {}mph.\n
                            """.format(city, morning[0]['weather'][0]['main'],
                                           morning[0]['weather'][0]['description'],
                                           round(morning[0]['main']['temp'] - 273.15, 2),
                                           morning[0]['main']['humidity'], morning[0]['wind']['speed'],
                                           afternoon[0]['weather'][0]['main'],
                                           afternoon[0]['weather'][0]['description'],
                                           round(afternoon[0]['main']['temp'] - 273.15, 2),
                                           afternoon[0]['main']['humidity'], afternoon[0]['wind']['speed'],
                                           evening[0]['weather'][0]['main'], evening[0]['weather'][0]['description'],
                                           round(evening[0]['main']['temp'] - 273.15, 2),
                                           evening[0]['main']['humidity'], evening[0]['wind']['speed'])))
                        elif weatherType == 'nhiệt độ':
                            response = GoogleTranslator(source='en', target='vi').translate("""The temperature in the next day morning is {} degrees in C, in afternoon is {} and in the evening is {}""".format(
                                round(morning[0]['main']['temp'] - 273.15, 2),
                                round(afternoon[0]['main']['temp'] - 273.15, 2),
                                round(evening[0]['main']['temp'] - 273.15, 2)))
                        elif weatherType == 'độ ẩm':
                            response = GoogleTranslator(source='en', target='vi').translate("""The humidity tomorrow is {}% in morning, {}% in afternoon and the evening is {}%""".format(
                                morning[0]['main']['humidity'], afternoon[0]['main']['humidity'],
                                evening[0]['main']['humidity']))
                        elif weatherType == 'gió':
                            response = GoogleTranslator(source='en', target='vi').translate("""The wind tomorrow is {} mph with direction is {} and gust is {} mph in the morning, is {} mph with direction is {} and gust is {} mph in the afternoon and {} mph with direction is {} and gust is {} mph in the evening""".format(
                                morning[0]['wind']['speed'], self.wind_direction(morning[0]['wind']['deg']), morning[0]['wind']['gust'],
                                afternoon[0]['wind']['speed'], self.wind_direction(afternoon[0]['wind']['deg']),
                                afternoon[0]['wind']['gust'], evening[0]['wind']['speed'], self.wind_direction(evening[0]['wind']['deg']),
                                evening[0]['wind']['gust']))
                        elif weatherType == 'nắng':
                            if conditionCurrent == 'Rain':
                                response = GoogleTranslator(source='en', target='vi').translate(f"""No, tomorrow is not sunny, it {conditionDesc}""")
                            if conditionDesc == 'clear sky':
                                response = GoogleTranslator(source='en', target='vi').translate("""Yes, the weather tomorrow is sunny, you should use suncreen if you want to go out 😉""")
                            elif conditionDesc == 'few clouds' or conditionDesc == 'scattered clouds':
                                response = GoogleTranslator(source='en', target='vi').translate("""Hmmm, it's not exactly sunny tomorrow, maybe a little because there are scattered clouds 😉""")
                            else:
                                response = GoogleTranslator(source='en', target='vi').translate(f"""No, the next day is not sunny, it {conditionDesc}""")
                        elif weatherType == 'mưa':
                            if conditionCurrent == 'Rain':
                                if conditionDesc == 'light rain':
                                    response = GoogleTranslator(source='en', target='vi').translate("""Yes, The weather tomorrow is rain but it is light rain, you may be bring umbrella ☔""")
                                elif conditionDesc == 'moderate rain':
                                    response = GoogleTranslator(source='en', target='vi').translate("""Yes, The weather next day is rain with moderate rain, you should bring a raincoat and move carefully if you go out 😭""")
                                else:
                                    response = GoogleTranslator(source='en', target='vi').translate("""Yes, The weather tomorrow is rain, you should bring a raincoat and move carefully if you go out 😭""")
                            elif conditionCurrent == "Clouds":
                                if conditionDesc == 'broken clouds' or conditionDesc == 'overcast clouds':
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""Tomorrow's weather is likely to be rainy with {conditionDesc}, you should bring umbrella""")
                                else:
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""No, the next day is not rain, it is {conditionDesc}""")
                            else:
                                response = GoogleTranslator(source='en', target='vi').translate(f"""No, the next day is not rain, it is  {conditionDesc}""")

# -------------------------------------------------------Dự báo thời tiết cho hai ngày tới ----------------------------------------------------------------------#

                    elif forecastPeriod.lower() == "Hai ngày tới".lower():
                        tomorrows = [item for item in weathers['list'] if tomorrow[0:10] in item['dt_txt']]
                        afternoonTomorrow = [item for item in tomorrows if item['dt_txt'][11:] == '15:00:00']
                        conditionTomor = afternoonTomorrow[0]['weather'][0]['main']
                        conditionTomorDesc = afternoonTomorrow[0]['weather'][0]['description']
                        ##next 2 days
                        next2Days = [item for item in weathers['list'] if next2Day[0:10] in item['dt_txt']]
                        morning = [item for item in next2Days if item['dt_txt'][11:] == '09:00:00']
                        afternoon = [item for item in next2Days if item['dt_txt'][11:] == '15:00:00']
                        evening = [item for item in next2Days if item['dt_txt'][11:] == '21:00:00']
                        conditionCurrent = afternoon[0]['weather'][0]['main']
                        conditionDesc = afternoon[0]['weather'][0]['description']

                        if guess == '' or guess is None:
                            if weatherType is None or weatherType == 'thời tiết':
                                response = GoogleTranslator(source='en', target='vi').translate("""The weater next 2 days in {}: \n
                                - Morning will be {} with {}: temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.\n
                                - Afternoon will feel {} with {}: temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.\n
                                - Evening will like {} with {}: temperature is {} degrees, the humidity is {}% and the wind speed is {}mph.\n
                            """.format(city, morning[0]['weather'][0]['main'], morning[0]['weather'][0]['description'],
                                       round(morning[0]['main']['temp'] - 273.15, 2), morning[0]['main']['humidity'],
                                       morning[0]['wind']['speed'], afternoon[0]['weather'][0]['main'],
                                       afternoon[0]['weather'][0]['description'],
                                       round(afternoon[0]['main']['temp'] - 273.15, 2),
                                       afternoon[0]['main']['humidity'], afternoon[0]['wind']['speed'],
                                       evening[0]['weather'][0]['main'], evening[0]['weather'][0]['description'],
                                       round(evening[0]['main']['temp'] - 273.15, 2), evening[0]['main']['humidity'],
                                       evening[0]['wind']['speed']))
                            elif weatherType == 'nhiệt độ':
                                response = GoogleTranslator(source='en', target='vi').translate("""The temperature in the next day after tomorrow morning is {} degrees in C, in afternoon is {} and in the evening is {}""".format(
                                    round(morning[0]['main']['temp'] - 273.15, 2),
                                    round(afternoon[0]['main']['temp'] - 273.15, 2),
                                    round(evening[0]['main']['temp'] - 273.15, 2)))
                            elif weatherType == 'độ ẩm':
                                response = GoogleTranslator(source='en', target='vi').translate("""The humidity next 2 days is {}% in morning, {}% in afternoon and the evening is {}%""".format(
                                    morning[0]['main']['humidity'], afternoon[0]['main']['humidity'],
                                    evening[0]['main']['humidity']))
                            elif weatherType == 'gió':
                                response = GoogleTranslator(source='en', target='vi').translate("""The wind next two days is {} mph with direction is {} and gust is {} mph in the morning, is {} mph with direction is {} and gust is {} mph in the afternoon and {} mph with direction is {} and gust is {} mph in the evening""".format(
                                    morning[0]['wind']['speed'], self.wind_direction(morning[0]['wind']['deg']), morning[0]['wind']['gust'],
                                    afternoon[0]['wind']['speed'], self.wind_direction(afternoon[0]['wind']['deg']),
                                    afternoon[0]['wind']['gust'], evening[0]['wind']['speed'],
                                    self.wind_direction(evening[0]['wind']['deg']), evening[0]['wind']['gust']))
                            elif weatherType == 'nắng':
                                if conditionCurrent == 'Rain':
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""No, the next 2 days is not sunny, it {conditionDesc}""")
                                if conditionDesc == 'clear sky':
                                    response = GoogleTranslator(source='en', target='vi').translate("""Yes, the weather the next 2 days is sunny, you should use suncreen if you want to go out 😉""")
                                elif conditionDesc == 'few clouds' or conditionDesc == 'scattered clouds':
                                    response = GoogleTranslator(source='en', target='vi').translate("""Hmmm, it's not exactly sunny the next 2 days, It's not really sunny the next 2 days, maybe a little because there are scattered clouds the next 2 days 😉""")
                                else:
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""No, the next 2 days is not sunny, it {conditionDesc}""")
                            elif weatherType == 'mưa':
                                if conditionCurrent == 'Rain':
                                    if conditionDesc == 'light rain':
                                        response = GoogleTranslator(source='en', target='vi').translate("""Yes, The weather the day after tomorrow is rain but it is light rain, you may be bring umbrella ☔""")
                                    elif conditionDesc == 'moderate rain':
                                        response = GoogleTranslator(source='en', target='vi').translate("""Yes, The weather the next 2 days is rain with moderate rain, you should bring a raincoat and move carefully if you go out 😭""")
                                    else:
                                        response = GoogleTranslator(source='en', target='vi').translate("""Yes, The weather the next 2 days is rain, you should bring a raincoat and move carefully if you go out 😭""")
                                elif conditionCurrent == "Clouds":
                                    if conditionDesc == 'broken clouds' or conditionDesc == 'overcast clouds':
                                        response = GoogleTranslator(source='en', target='vi').translate(f"""The next 2 days's weather is likely to be rainy with {conditionDesc}, you should bring umbrella""")
                                    else:
                                        response = GoogleTranslator(source='en', target='vi').translate(f"""No, the day after tomorrow is not rain, it is {conditionDesc}""")
                                else:
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""No, the next day after tomorrow is not rain, it is {conditionDesc}""")

                        else:
                            if weatherType == 'mưa':
                                if conditionTomor == 'Rain':
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""It's will be rain tomorrow ({afternoonTomorrow[0]['dt_txt'][0:10]}), you may be bring umbrella ☔""")
                                elif conditionCurrent == 'Rain':
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""t's will be rain in next 2 days({afternoon[0]['dt_txt'][0:10]}), you may be bring umbrella ☔""")
                                elif conditionCurrent == 'Rain' and conditionTomor == 'Rain':
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""It's will be rain both 2 days), you may be bring umbrella ☔""")
                                else:
                                    response = GoogleTranslator(source='en', target='vi').translate("""There will be no rain in the next 2 days, rest assured! 😉""")
                                    SlotSet('guess', None)
                            elif weatherType == 'nắng':
                                if conditionTomor == 'Clear' or conditionTomorDesc == 'few clouds' or conditionTomorDesc == 'scattered clouds':
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""It's will be sunny tomorrow ({afternoonTomorrow[0]['dt_txt'][0:10]}), you should be use sunscreen""")
                                elif conditionCurrent == 'Clear' or conditionDesc == 'few clouds' or conditionDesc == 'scattered clouds':
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""It's will have sunny in next 2 days({afternoon[0]['dt_txt'][0:10]}), you should be use sunscreen""")
                                elif (
                                        conditionTomor == 'Clear' or conditionTomorDesc == 'few clouds' or conditionTomorDesc == 'scattered clouds') and conditionCurrent == 'Clear' or conditionDesc == 'few clouds' or conditionDesc == 'scattered clouds':
                                    response = GoogleTranslator(source='en', target='vi').translate(f"""It's will be sunny all, rest assured 😉""")
                                else:
                                    response = GoogleTranslator(source='en', target='vi').translate("""There will be no sun both days, rest assured! 😉""")

                    else:
                        response = GoogleTranslator(source='en', target='vi').translate("""Sorry, I can only forecast the weather within 2 days. Please purchase the ChatBot VIP Member package to unlock forecasts for more days 😉""")

                else:
                    response = GoogleTranslator(source='en', target='vi').translate("""Something went wrong with the Weather Map API, please try again later!""")

            else:
                response = GoogleTranslator(source='en', target='vi').translate("""Sorry, I couldn't get coordinates from OpenWeatherApi, please try again later!""")

        dispatcher.utter_message(response)

        return [SlotSet('location', loc), SlotSet('guess', None)]

    @staticmethod
    def wind_direction(degree):
        # Chuyển giá trị độ sang hướng gió
        if degree is None:
            return 'None'

        if degree >= 337.5 or degree < 22.5:
            return 'North'
        elif 22.5 <= degree < 67.5:
            return 'North-East'
        elif 67.5 <= degree < 112.5:
            return 'East'
        elif 112.5 <= degree < 157.5:
            return 'South-East'
        elif 157.5 <= degree < 202.5:
            return 'South'
        elif 202.5 <= degree < 247.5:
            return 'South-West'
        elif 247.5 <= degree < 292.5:
            return 'West'
        else:
            return 'North-West'