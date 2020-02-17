# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pickle
from collections import namedtuple

Message_Info = namedtuple('Message_Info', ['message', 'number', 'message_present'])

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()
    # Add a message
    resp.message("Your message has been sent!")

    body = request.values.get("Body", None)
    number = request.values.get("From")
    info = Message_Info(body, number, True)
    with open('Info', 'wb') as file:
        pickle.dump(info, file)


    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)