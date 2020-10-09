import requests
import json

api_key = "0d85e73c488e8b4db1fc5a14cd04dc27"
base_url = "http://api.openweathermap.org/data/2.5/weather?"


def get_weather(event, context):
    """
        Takes the currentinternt and the context value from
        aws lex.
        This handler only works after the slots are filled.
        This handler response back to aws lex at Fulfilled state only.
        It doesn't do any initialization and validation works. 
        Make sure you untick intialization and validation option in aws lex.
    """
    city_name = event["currentIntent"]["slots"]["city"]
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    resp_json = response.json()

    if resp_json["cod"] != "404":
        main_value = resp_json["main"]
        
        # temperature in kelvin value, changed to celsius
        current_temperature = main_value["temp"] - 273.15 
        
        current_pressure = main_value["pressure"]
        current_humidiy = main_value["humidity"]
        
        weather_value = resp_json["weather"] 
        weather_description = weather_value[0]["description"]
        content = f"""
            Temperature(in celsius) = {str("%.2f" % current_temperature)}
            Athmospheric Pressure (in hPa) = {str(current_pressure)}
            Humidity(in percentage) = {str(current_humidiy)}\n
            Description = {str(weather_description)}
            """
    else:
        content = "City not found"

    return {
        "sessionAttributes": event["sessionAttributes"],
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": content
            }
        }
    }
