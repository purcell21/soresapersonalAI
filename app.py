#!/usr/bin/env python

import urllib
import json
import os
import smtplib

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "ticket.open":
        return {}
    
    gmail_user = 'sdesk371@gmail.com'  
    gmail_password = 'ServiceDesk21'

    from = gmail_user  
    to = ['me@gmail.com', 'bill@gmail.com']  
    subject = 'Message'  
    body = 'Hey'

    email_text = """\  
        From: %s  
        To: %s  
        Subject: %s %s """ % (from, ", ".join(to), subject, body)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    msg = "YOUR MESSAGE!"
    server.sendmail("sdesk371@gmail.com","antonio.porcelli@hotmail.it",email_text)
    server.quit()
    
    result = req.get("result")
    parameters = result.get("parameters")
    descrizione = parameters.get("descrizione")
    cliente = parameters.get("cliente")
    prodotto = parameters.get("prodotto")

    #cost = {'Europe':200, 'North America':300, 'South America':400, 'Asia':500, 'Africa':600}
    #'AO Colli':200, 'AOU Federico II':300, 'AOU Ruggi':400, 'ASL Salerno':500, 'Soresa':600, 'Santobono':700, 'Pascale':800, 'ASL Caserta':900
    
    numtck = {'AO Colli':127892, 'AOU Federico II':871865, 'AOU Ruggi':787265, 'ASL Salerno':902876, 'Soresa':276734, 'Santobono':676754, 'Pascale':878971, 'ASL Caserta':897654}
    
    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
    speech = "In questo momento non posso aiutarla. Ho aperto il ticket n." + str(numtck[cliente]) + " per il Cliente " + cliente + " sul prodotto/servizio " + prodotto + " con la seguente descrizione '" + descrizione + "'.Posso fare altro?"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
