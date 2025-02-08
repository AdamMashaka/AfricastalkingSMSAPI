from flask import Flask, request
import requests

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

# SANDBOX_API_KEY = "atsk_292d1cb1da1769170f460c0853a163a897280aeb1df67fef632f46ae67b7760768cf7a38"

def response_to_sms(recipient_phone_number, message):
    requests.post("https://api.sandbox.africastalking.com/version1/messaging",
                  data={
                      "username": "sandbox",
                      "to": recipient_phone_number,
                      "message": message,
                      "from": "76345"
                  },
                  headers={
                      "apikey": SANDBOX_API_KEY,
                      "Accept": "application/json",
                      "Content-Type": "application/x-www-form-urlencoded"
                  }
                  )

if __name__ == '__main__':
    app.run(debug=True)