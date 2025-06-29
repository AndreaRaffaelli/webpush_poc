# push_proxy.py
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

app = Flask(__name__)

cred = credentials.Certificate(os.path.join(".", "webpush-mobile-exam-firebase-admin.json"))

with open("webpush-mobile-exam-firebase-admin.json") as f:
    sa_json = json.load(f)

firebase_admin.initialize_app(cred, {
    'projectId': sa_json.get("project_id")
})

#firebase_admin.initialize_app(cred)

# In-memory list of subscribers (token strings)
subscribers = ["d3H7nWCfTxO8E4C_punmRs:APA91bFXZM5EglDwyffS-GGJB7GuZ1aN8xE6NFt9NhxQDDvbxLgFyrjXgxtzdK_fkbwnJlCcXJRiMzktPfHigRtauG9wdunzrkI0m9SVe4IvT0-3X8CyJUw"]
# subscribers = []

@app.route("/register", methods=["POST"])
def register():
    token = request.json.get("token")
    if token and token not in subscribers:
        subscribers.append(token)
    print("Registered subscriber:", token)
    return jsonify({"status": "registered", "subscribers": len(subscribers)})

@app.route("/publish", methods=["POST"])
def publish():
    title = request.json.get("title")
    body = request.json.get("body")

    success_count = 0
    failure_count = 0
    errors = []

    for token in subscribers:
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                token=token,
            )
            response = messaging.send(message)
            print(f"Sent to {token[:10]}...: {response}")
            success_count += 1
        except Exception as e:
            print(f"Failed to send to {token[:10]}...: {e}")
            failure_count += 1
            errors.append(str(e))

    return jsonify({
        "status": "partial" if failure_count else "sent",
        "success": success_count,
        "failure": failure_count,
        "errors": errors[:3]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
