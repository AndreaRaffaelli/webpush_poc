import firebase_admin
from firebase_admin import credentials, messaging
import os

# Sostituisci con il percorso effettivo del tuo file JSON
SERVICE_ACCOUNT_KEY_PATH = os.path.join(".", "webpush-mobile-exam-firebase-admin.json")

print(f"Attempting to initialize Firebase Admin SDK with credentials from: {SERVICE_ACCOUNT_KEY_PATH}")

try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized successfully.")
except Exception as e:
    print(f"Error during Firebase Admin SDK initialization: {e}")
    exit(1)

# Token di prova lungo per sembrare valido
# TEST_TOKEN = "e-un-token-di-prova-non-valido-ma-lungo-a-sufficienza-per-non-essere-subito-scartato-dal-client"
TEST_TOKEN = "d3H7nWCfTxO8E4C_punmRs:APA91bFXZM5EglDwyffS-GGJB7GuZ1aN8xE6NFt9NhxQDDvbxLgFyrjXgxtzdK_fkbwnJlCcXJRiMzktPfHigRtauG9wdunzrkI0m9SVe4IvT0-3X8CyJUw"

print(f"\nAttempting to send a dummy FCM message to token: {TEST_TOKEN}")

try:
    message = messaging.Message(
        notification=messaging.Notification(
            title="Test FCM",
            body="Questo è un messaggio di test dal tuo script Python.",
        ),
        token=TEST_TOKEN,
    )
    response = messaging.send(message)
    print(f"Dummy message sent successfully! Response: {response}")
except firebase_admin.exceptions.NotFoundError as e:
    print(f"ERROR: Still getting 404 Not Found. This indicates an issue with the SDK's ability to find the FCM endpoint.")
    print(f"Details: {e}")
except Exception as e:
    print(f"ERROR: Failed to send dummy message. This might be a valid FCM error (e.g., bad token) or another issue.")
    print(f"Details: {e}")
