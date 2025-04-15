from flask import Flask, request
import openai
import requests
import traceback
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SANDBOX_API_KEY = os.getenv('SANDBOX_API_KEY')

@app.route('/')
def Tichika():
    return 'Tichika(edutech)'

@app.route('/sms', methods=['POST'])
def sms_callback():
    try:
        print(request.method)
        print(request.form)
        user_message = request.form.get("text")
        sender = request.form.get("from")

        if not user_message or not sender:
            return "Bad Request: Missing 'text' or 'from' parameter", 400

        bot_response = chat_with_gpt(user_message)
        response_to_sms(sender, bot_response)
        return "Success", 201

    except openai.error.RateLimitError as e:
        print(f"OpenAI Rate Limit Error: {str(e)}")
        return "Rate Limit Exceeded", 429

    except Exception as e:
        traceback.print_exc()
        return "Internal Server Error", 500

def chat_with_gpt(user_message):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']

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