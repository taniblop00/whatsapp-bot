from flask import Flask, request
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# מילון לניהול הזמנות זמניות
temp_reservations = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    resp = MessagingResponse()
    msg = resp.message()
    
    if sender not in temp_reservations:
        temp_reservations[sender] = {}
        msg.body("שלום! איזה שירות תרצה להזמין?\n1️⃣ שולחן במסעדה\n2️⃣ תור למספרה\n3️⃣ טיפול פנים")
    elif 'service' not in temp_reservations[sender]:
        temp_reservations[sender]['service'] = incoming_msg
        msg.body("מתי תרצה להזמין? (הכנס תאריך ושעה בפורמט DD-MM-YYYY HH:MM)")
    elif 'date' not in temp_reservations[sender]:
        temp_reservations[sender]['date'] = incoming_msg
        msg.body("מה שמך המלא?")
    else:
        temp_reservations[sender]['name'] = incoming_msg
        msg.body(f"תודה {incoming_msg}! ההזמנה שלך נקבעה ל-{temp_reservations[sender]['date']}. נתראה בקרוב! 😊")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
