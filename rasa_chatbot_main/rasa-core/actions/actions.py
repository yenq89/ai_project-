# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List
from deep_translator import GoogleTranslator

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
from datetime import datetime, timedelta


#
#



class action_get_weather(Action):

    # def translate_weather(weather):
    #     if weather == 'Clear':
    #         return 'quang đãng'
    #     elif weather == 'Clouds':
    #         return 'có mây'
    #     elif weather == 'Rain':
    #         return 'mưa'
    #     elif weather == 'Thunderstorm':
    #         return 'bão'
    #     elif weather == 'Snow':
    #         return 'tuyết'
    #     elif weather == 'Mist':
    #         return 'sương mù'
    #     elif weather == 'Drizzle':
    #         return 'mưa phùn'
    #     elif weather == 'Wind':
    #         return 'gió mạnh'
    #     else:
    #         return weather  # Trả lại nguyên văn nếu không tìm thấy điều kiện
    #
    # def translate_descripption(description):
    #     if description == 'clear sky':
    #         return 'quang đãng'
    #     elif description == 'few clouds':
    #         return 'mây thưa'
    #     elif description == 'scattered clouds':
    #         return 'mây rải rác'
    #     elif description == 'broken clouds':
    #         return 'mây đan xen'
    #     elif description == 'overcast clouds':
    #         return 'mây phủ kín'
    #     elif description == 'light rain':
    #         return 'mưa nhẹ'
    #     elif description == 'moderate rain':
    #         return 'mưa vừa'
    #     elif description == 'heavy rain':
    #         return 'mưa to'
    #     elif description == 'very heavy rain':
    #         return 'mưa rất to'
    #     elif description == 'extreme rain':
    #         return 'mưa cực kỳ to'
    #     elif description == 'freezing rain':
    #         return 'mưa tuyết'
    #     elif description == 'light snow':
    #         return 'tuyết nhẹ'
    #     elif description == 'moderate snow':
    #         return 'tuyết vừa'
    #     elif description == 'heavy snow':
    #         return 'tuyết dày'
    #     elif description == 'thunderstorm':
    #         return 'bão'
    #     elif description == 'light thunderstorm':
    #         return 'bão nhẹ'
    #     elif description == 'heavy thunderstorm':
    #         return 'bão lớn'
    #     elif description == 'fog':
    #         return 'sương mù'
    #     elif description == 'drizzle':
    #         return 'mưa phùn'
    #     elif description == 'haze':
    #         return 'khói bụi'
    #     else:
    #         return description  # Trả lại nguyên văn nếu không tìm thấy mô tả
    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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
            dispatcher.utter_message(text=f'Địa điểm: {loc}')
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

                        if weatherType is None or weatherType == 'thời tiết':
                            response = GoogleTranslator(source='en', target='vi').translate("""It is currently {} in {} at the moment. The temperature is {} degrees in C, feel like {}, the humidity is {}% and the wind speed is {} mph."""
                                                                                            .format(conditionCurrent, city, temperature_cCurrent, feelLike, humidityCurrent, wind_mphCurrent))
                        elif weatherType == 'nhiệt độ':
                            response = """Nhiệt độ hiện tại là {} độ C, cảm giác như {}""".format(temperature_cCurrent,
                                                                                                  feelLike)
                        elif weatherType == 'độ ẩm':
                            response = """Độ ẩm hiện tại là {}%""".format(humidityCurrent)
                        elif weatherType == 'gió':
                            response = """Tốc độ gió hôm nay là {} mph với góc gió là {} và gió mạnh {}""".format(
                                wind_mphCurrent, current['wind']['deg'], current['wind']['gust'])
                        elif weatherType == 'nắng':
                            if conditionCurrent == 'Rain':
                                response = f"""Không, hôm nay trời không nắng, trời {conditionDesc}"""
                            if conditionDesc == 'clear sky':
                                response = """Hôm nay trời nắng, bạn nên sử dụng kem chống nắng khi ra ngoài 😉"""
                            elif conditionDesc == 'few clouds' or conditionDesc =='scattered clouds':
                                response = """Hmmm, trời có vẻ không nắng, có thể một chút vì hôm nay có mây rải rác 😉"""
                            else:
                                response = f"""Không, hôm nay trời không nắng, nó {conditionDesc}"""
                        elif weatherType == 'Rain':
                            if conditionCurrent == 'Rain':
                                if conditionDesc == 'light rain':
                                    response = """Vâng, thời tiết hôm nay có mưa nhưng là mưa nhẹ, bạn có thể mang theo ô ☔"""
                                elif conditionDesc == 'moderate rain':
                                    response = """Vâng, thời tiết hôm nay có mưa với mưa vừa, bạn nên mang theo áo mưa và di chuyển cẩn thận nếu ra ngoài 😭"""
                                else:
                                    response = """Vâng, thời tiết hôm nay có mưa, bạn nên mang theo áo mưa và di chuyển cẩn thận nếu ra ngoài 😭"""
                            elif conditionCurrent == "Clouds":
                                if conditionDesc == 'broken clouds' or conditionDesc == 'overcast clouds':
                                    response = f"""Thời tiết hôm nay có khả năng sẽ mưa với {conditionDesc}, bạn nên mang theo ô"""
                                else:
                                    response = f"""Không, hôm nay trời không mưa, trời {conditionDesc}"""
                            else:
                                response = f"""Không, hôm nay trời không mưa, trời {conditionDesc}"""

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
                            response = ("""Thời tiết ngày mai tại {}: \n
                            - Buổi sáng sẽ {} với {}: nhiệt độ là {} độ, độ ẩm là {}% và tốc độ gió là {} mph. \n
                            - Buổi chiều sẽ cảm thấy {} với {}: nhiệt độ là {} độ, độ ẩm là {}% và tốc độ gió là {} mph. \n
                            - Buổi tối sẽ giống như {} với {}: nhiệt độ là {} độ, độ ẩm là {}% và tốc độ gió là {} mph. \n
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
                                           evening[0]['main']['humidity'], evening[0]['wind']['speed']))
                        elif weatherType == 'nhiệt độ':
                            response = """Nhiệt độ vào sáng ngày mai là {} độ C, buổi chiều là {} và buổi tối là {}""".format(
                                round(morning[0]['main']['temp'] - 273.15, 2),
                                round(afternoon[0]['main']['temp'] - 273.15, 2),
                                round(evening[0]['main']['temp'] - 273.15, 2))
                        elif weatherType == 'độ ẩm':
                            response = """Độ ẩm ngày mai là {}% vào buổi sáng, {}% vào buổi chiều và buổi tối là {}%""".format(
                                morning[0]['main']['humidity'], afternoon[0]['main']['humidity'],
                                evening[0]['main']['humidity'])
                        elif weatherType == 'gió':
                            response = """Tốc độ gió ngày mai là {} mph với góc gió là {} và gió mạnh là {} vào buổi sáng, là {} mph với góc gió là {} và gió mạnh là {} vào buổi chiều và cuối cùng: {} mph với góc gió là {} và gió mạnh là {} vào buổi tối""".format(
                                morning[0]['wind']['speed'], morning[0]['wind']['deg'], morning[0]['wind']['gust'],
                                afternoon[0]['wind']['speed'], afternoon[0]['wind']['deg'],
                                afternoon[0]['wind']['gust'], evening[0]['wind']['speed'], evening[0]['wind']['deg'],
                                evening[0]['wind']['gust'])
                        elif weatherType == 'nắng':
                            if conditionCurrent == 'Rain':
                                response = f"""Không, ngày mai trời không nắng, mà trời {conditionDesc}"""
                            if conditionDesc == 'clear sky':
                                response = """Hôm nay trời nắng, bạn nên sử dụng kem chống nắng khi ra ngoài 😉"""
                            elif conditionDesc == 'few clouds' or conditionDesc == 'scattered clouds':
                                response = """Hmmm, ngày mai trời không hoàn toàn nắng, có thể một chút vì có mây rải rác 😉"""
                            else:
                                response = f"""Không, ngày mai trời không nắng, trời {conditionDesc}"""
                        elif weatherType == 'mưa':
                            if conditionCurrent == 'Rain':
                                if conditionDesc == 'light rain':
                                    response = """Vâng, thời tiết ngày mai có mưa nhưng là mưa nhẹ, bạn nên mang theo ô ☔"""
                                elif conditionDesc == 'moderate rain':
                                    response = """Vâng, thời tiết ngày kia có mưa với mưa vừa, bạn nên mang theo áo mưa và di chuyển cẩn thận nếu ra ngoài 😭"""
                                else:
                                    response = """Vâng, thời tiết ngày mai có mưa, bạn nên mang theo áo mưa và di chuyển cẩn thận nếu ra ngoài 😭"""
                            elif conditionCurrent == "Clouds":
                                if conditionDesc == 'broken clouds' or conditionDesc == 'overcast clouds':
                                    response = f"""Thời tiết ngày mai có khả năng sẽ mưa với {conditionDesc}, bạn nên mang theo ô"""
                                else:
                                    response = f"""Không, ngày mai không có mưa, mà là {conditionDesc}"""
                            else:
                                response = f"""Không, ngày mai không mưa, mà là {conditionDesc}"""

# -------------------------------------------------------Dự báo thời tiết cho hai ngày tới ----------------------------------------------------------------------#
                    elif forecastPeriod == 'hai ngày tới':
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
                            if weatherType is None:
                                response = """Thời tiết ngày kia ở {}: \n
                            - Buổi sáng sẽ là {} với {}: nhiệt độ là {} độ C, độ ẩm là {}% và tốc độ gió là {} mph. \n
                            - Buổi chiều sẽ cảm thấy {} với {}: nhiệt độ là {} độ C, độ ẩm là {}% và tốc độ gió là {} mph. \n
                            - Buổi tối sẽ là {} với {}: nhiệt độ là {} độ C, độ ẩm là {}% và tốc độ gió là {} mph.
                            """.format(city, morning[0]['weather'][0]['main'], morning[0]['weather'][0]['description'],
                                       round(morning[0]['main']['temp'] - 273.15, 2), morning[0]['main']['humidity'],
                                       morning[0]['wind']['speed'], afternoon[0]['weather'][0]['main'],
                                       afternoon[0]['weather'][0]['description'],
                                       round(afternoon[0]['main']['temp'] - 273.15, 2),
                                       afternoon[0]['main']['humidity'], afternoon[0]['wind']['speed'],
                                       evening[0]['weather'][0]['main'], evening[0]['weather'][0]['description'],
                                       round(evening[0]['main']['temp'] - 273.15, 2), evening[0]['main']['humidity'],
                                       evening[0]['wind']['speed'])
                            elif weatherType == 'nhiệt độ':
                                response = """Nhiệt độ vào ngày kia buổi sáng là {} độ C, buổi chiều là {} và buổi tối là {}""".format(
                                    round(morning[0]['main']['temp'] - 273.15, 2),
                                    round(afternoon[0]['main']['temp'] - 273.15, 2),
                                    round(evening[0]['main']['temp'] - 273.15, 2))
                            elif weatherType == 'độ ẩm':
                                response = """Độ ẩm vào ngày kia là {}% buổi sáng, {}% buổi chiều và buổi tối là {}%""".format(
                                    morning[0]['main']['humidity'], afternoon[0]['main']['humidity'],
                                    evening[0]['main']['humidity'])
                            elif weatherType == 'gió':
                                response = """Gió vào ngày kia là {} mph với góc gió là {} và gió mạnh là {} buổi sáng, là {} mph với góc gió là {} và gió mạnh là {} buổi chiều, và cuối cùng là {} mph với góc gió là {} và gió mạnh là {} buổi tối""".format(
                                    morning[0]['wind']['speed'], morning[0]['wind']['deg'], morning[0]['wind']['gust'],
                                    afternoon[0]['wind']['speed'], afternoon[0]['wind']['deg'],
                                    afternoon[0]['wind']['gust'], evening[0]['wind']['speed'],
                                    evening[0]['wind']['deg'], evening[0]['wind']['gust'])
                            elif weatherType == 'nắng':
                                if conditionCurrent == 'Rain':
                                    response = f"""Không, ngày kia không nắng, trời {conditionDesc}"""
                                if conditionDesc == 'clear sky':
                                    response = """Vâng, thời tiết ngày kia nắng, bạn nên dùng kem chống nắng nếu ra ngoài 😉"""
                                elif conditionDesc == 'few clouds' or conditionDesc == 'scattered clouds':
                                    response = """Hmmm, không hoàn toàn nắng vào ngày kia, có thể là một chút vì trời có mây rải rác 😉"""
                                else:
                                    response = f"""Không, ngày kia không nắng, trời {conditionDesc}"""
                            elif weatherType == 'mưa':
                                if conditionCurrent == 'Rain':
                                    if conditionDesc == 'light rain':
                                        response = """Vâng, thời tiết ngày kia có mưa nhẹ, bạn có thể mang theo ô ☔"""
                                    elif conditionDesc == 'moderate rain':
                                        response = """Vâng, thời tiết ngày kia có mưa vừa, bạn nên mang áo mưa và di chuyển cẩn thận nếu ra ngoài 😭"""
                                    else:
                                        response = """Vâng, thời tiết ngày kia có mưa, bạn nên mang áo mưa và di chuyển cẩn thận nếu ra ngoài 😭"""
                                elif conditionCurrent == "Clouds":
                                    if conditionDesc == 'broken clouds' or conditionDesc == 'overcast clouds':
                                        response = f"""Thời tiết ngày kia có khả năng sẽ mưa với {conditionDesc}, bạn nên mang theo ô"""
                                    else:
                                        response = f"""Không, ngày kia không có mưa, trời là {conditionDesc}"""
                                else:
                                    response = f"""Không, ngày kia không có mưa, trời là {conditionDesc}"""

                        else:
                            if weatherType == 'mưa':
                                if conditionTomor == 'Rain':
                                    response = f"""Ngày mai sẽ có mưa ({afternoonTomorrow[0]['dt_txt'][0:10]}), bạn có thể mang theo ô ☔"""
                                elif conditionCurrent == 'Rain':
                                    response = f"""Ngày kia sẽ có mưa ({afternoon[0]['dt_txt'][0:10]}), bạn có thể mang theo ô ☔"""
                                elif conditionCurrent == 'Rain' and conditionTomor == 'Rain':
                                    response = f"""Cả hai ngày sẽ có mưa, bạn có thể mang theo ô ☔"""
                                else:
                                    response = """Ngày kia sẽ không mưa, bạn có thể yên tâm! 😉"""
                                    SlotSet('guess', None)
                            elif weatherType == 'nắng':
                                if conditionTomor == 'Clear' or conditionTomorDesc == 'few clouds' or conditionTomorDesc == 'scattered clouds':
                                    response = f"""Ngày mai sẽ nắng ({afternoonTomorrow[0]['dt_txt'][0:10]}), bạn nên dùng kem chống nắng"""
                                elif conditionCurrent == 'Clear' or conditionDesc == 'few clouds' or conditionDesc == 'scattered clouds':
                                    response = f"""Ngày kia sẽ nắng ({afternoon[0]['dt_txt'][0:10]}), bạn nên dùng kem chống nắng"""
                                elif (
                                        conditionTomor == 'Clear' or conditionTomorDesc == 'few clouds' or conditionTomorDesc == 'scattered clouds') and conditionCurrent == 'Clear' or conditionDesc == 'few clouds' or conditionDesc == 'scattered clouds':
                                    response = f"""Ngày kia sẽ nắng cả ngày, bạn có thể yên tâm 😉"""
                                else:
                                    response = """Cả hai ngày sẽ không có nắng, bạn có thể yên tâm! 😉"""

                    else:
                        response = """Xin lỗi, tôi chỉ có thể dự báo thời tiết trong vòng 2 ngày. Hãy mua gói ChatBot VIP Member để mở khoá dự báo trong nhiều ngày hơn nhé 😉"""

                else:
                    response = """Có lỗi gì đó đã xảy ra với API của Weather Map, hãy thử lại sau nhé!"""

            else:
                response = """Xin lỗi, tôi không thể lấy tọa độ từ OpenWeatherApi, hãy thử lại sau nhé!"""

        dispatcher.utter_message(response)

        return [SlotSet('location', loc), SlotSet('guess', None)]
