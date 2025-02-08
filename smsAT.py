from flask import Flask, request
import openai
import requests
import traceback

app = Flask(__name__)

# Set your API keys directly in the script
# OPENAI_API_KEY = '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'
# SANDBOX_API_KEY = "atsk_292d1cb1da1769170f460c0853a163a897280aeb1df67fef632f46ae67b7760768cf7a38"

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