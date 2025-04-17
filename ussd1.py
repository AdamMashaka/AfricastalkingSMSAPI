from flask import Flask, request
import africastalking
import os
import requests

app = Flask(__name__)

# Initialize Africa's Talking API
username = "sandbox"  # Use "sandbox" for testing; replace with your username for production
api_key = os.getenv("AT_API_KEY")  # Use environment variable for API key
africastalking.initialize(username, api_key)
sms = africastalking.SMS

@app.route('/ussd', methods=['POST', 'GET'])
def ussd_callback():
    # Retrieve USSD parameters
    session_id = request.values.get("sessionId", "")
    service_code = request.values.get("serviceCode", "*123#")
    phone_number = request.values.get("phoneNumber", "")
    text = request.values.get("text", "")

    # Initialize response
    response = ""

    if text == "":
        # Main menu
        response = "CON Karibu MAPATO AI Kupata Huduma Kuhusu KILIMO:\n"
        response += "Chagua sehemu unayotaka:\n"
        response += "1. Habari kuhusu Bei ya Mazao\n"
        response += "2. Ushauri wa Kilimo\n"
        response += "3. Habari kuhusu Hali ya Hewa\n"
        response += "4. Mnunuzi\n"
        response += "5. Msaada wa Kiufundi\n"

    elif text == "1":
        # Sub-menu for crop prices
        response = "CON Chagua Mazao unayotaka kujua Bei:\n"
        response += "1. Mahindi\n"
        response += "2. Maharage\n"
        response += "3. Mchele\n"
        response += "4. Viazi\n"

    elif text == "1*1":
        # Request location for maize prices
        response = "CON Ingiza eneo lako la kilimo la mahindi"

    elif text.startswith("1*1*"):
        # Fetch maize price based on location
        location = text.split('*')[2]
        maize_price = get_maize_price(location)

        if maize_price:
            response = f"END Bei ya mahindi katika eneo lako la {location} ni {maize_price} TSH/100kg."
            try:
                sms_response = sms.send(f"Bei ya mahindi katika eneo lako la {location} ni {maize_price} TSH/100kg.", [phone_number])
                print(sms_response)
            except Exception as e:
                print(f"Error sending SMS: {e}")
        else:
            response = "END Samahani, hatuna taarifa za bei kwa eneo hilo."

    elif text == "2":
        # Sub-menu for agricultural advice
        response = "CON Karibu kwenye Huduma ya Ushauri wa Kilimo:\n"
        response += "1. Ushauri wa Upandaji Mazao\n"
        response += "2. Ushauri wa Kudhibiti Wadudu\n"
        response += "3. Ushauri wa Kuboresha Udongo\n"

    elif text == "2*1":
        # Advice on planting crops
        response = "END USHAURI WA UPANDAJI MAZAO:\n"
        response += "- Tumia mbegu bora na zenye ubora.\n"
        response += "- Tumia mbolea kulingana na mahitaji ya mazao yako.\n"
        response += "- Panda kwa kuzingatia mpangilio na umbali sahihi.\n"

        try:
            sms_response = sms.send(response, [phone_number])
            print(sms_response)
        except Exception as e:
            print(f"Error sending SMS: {e}")

    elif text == "3":
        # Weather information
        response = "CON Ingiza jina la jiji au eneo lako ili kupata taarifa ya hali ya hewa."

    elif text.startswith("3*"):
        # Fetch weather data
        location = text.split('*')[1]
        weather_data = get_weather_data(location)

        if weather_data:
            response = f"END Hali ya hewa ya {location} ni:\n"
            response += f"Joto: {weather_data['temperature']}°C\n"
            response += f"Hali ya anga: {weather_data['description']}"
        else:
            response = "END Samahani, hatuna taarifa za hali ya hewa kwa eneo hilo."

    else:
        # Invalid input
        response = "END Uingiaji usiofaa. Tafadhali jaribu tena."

    return response


def get_maize_price(location):
    # Hardcoded maize prices for demonstration
    prices = {
        "Arusha": "100,000",
        "Dar es Salaam": "95,000",
        "Mbeya": "90,000",
        "Dodoma": "88,000",
        "Mwanza": "125,000"
    }
    return prices.get(location, None)


def get_weather_data(location):
    # Fetch weather data from OpenWeather API
    api_key = os.getenv("OPENWEATHER_API_KEY")  # Use environment variable for API key
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"]
            }
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))