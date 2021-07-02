
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)
potluck = {}


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    body = request.values.get('Body', None).lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    global potluck

    if '&' in body:
        name = body.split('&')[0]
        food = body.split('& ')[1]
        potluck[name] = food
        msg.body('Added!, Potluck List at Dell Valle July 31st @7am:')
        resp.message(str(json.dumps(potluck, sort_keys=False, indent=4)))
        responded = True

    if 'potluck' in body:
        msg.body(str(json.dumps(potluck, sort_keys=False, indent=4)))
        responded = True

    if 'nanay' in body:
        text = 'To add, type: YourName & YourFood' + '\n' + 'To remove, add a new food with same name and it will update automatically' + '\n' + 'Type: Potluck for status'
        msg.body(text)
        responded = True

    if not responded:
        msg.body('Sorry, I don\'t understand, type \"olds\" for help')

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)