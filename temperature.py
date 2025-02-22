from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def Tichika():
    return 'Temperature'

@app.route('/send_sms', methods=['POST'])
def send_sms():
    if request.is_json:
        data = request.get_json()
        print(f"Received data: {data}")  
        temperature = data.get('temperature')
        if temperature and temperature > 23.0:
            recipient_phone_number = "+255694021848"
            message = f"Alert! The temperature is {temperature}°C."
            response_to_sms(recipient_phone_number, message)
            return jsonify({"status": "SMS sent"}), 200
        return jsonify({"status": "Temperature is normal"}), 200
    else:
        return jsonify({"status": "Unsupported Media Type"}), 415

SANDBOX_API_KEY = os.getenv('SANDBOX_API_KEY')

def response_to_sms(recipient_phone_number, message):
    response = requests.post("https://api.sandbox.africastalking.com/version1/messaging",
                             data={
                                 "username": "sandbox", 
                                 "to": recipient_phone_number,
                                 "message": message,
                                 "from": "98781"
                             },
                             headers={
                                 "apikey": SANDBOX_API_KEY,
                                 "Accept": "application/json",
                                 "Content-Type": "application/x-www-form-urlencoded"
                             })
    print(f"SMS API response: {response.text}") 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  