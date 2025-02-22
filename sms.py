from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route('/')
def Tichika():
    return 'Tichika(edutech)'

@app.route('/sms', methods=['POST'])
def sms_callback():
    print(request.method)
    print(request.form)
    print(request.form["from"])
    response_to_sms(request.form["from"], "Hello! How can I help you?")
    return "Success", 201 

SANDBOX_API_KEY = ('atsk_c7a40396674f0724f4a43cdb4c6591192c074f1fad02604ea7ac2e88285c79df1cb5ac9f')
def response_to_sms(recipient_phone_number, message):
    requests.post("https://api.sandbox.africastalking.com/version1/messaging",
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
                  }
                  )

if __name__ == '__main__':
    app.run(debug=True)