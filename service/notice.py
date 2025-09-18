# main.py (Your FastAPI application file)

from fastapi import HTTPException
import firebase_admin
from firebase_admin import credentials, messaging

from crud.notice import delete_notification_token
from schemas.notice import SendNotificationRequest

try:
    if not firebase_admin._apps: 
        cred = credentials.Certificate("firebase-credential.json")
        firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized successfully.")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    # Depending on your setup, you might want to exit or handle this more gracefully.

# --- FastAPI Endpoint to Send FCM Notification ---
def send_notification(request: SendNotificationRequest):
    """
    Sends an FCM notification to a specified device token.
    """
    try:
        # Construct the message payload
        message = messaging.Message(
            notification=messaging.Notification(
                title=request.title,
                body=request.body,
            ),
            data=request.data, # Custom data key-value pairs
            token=request.token, # Target the specific device token
        )

        # Send the message
        response = messaging.send(message)
        
        # 만일 response.code에서 토큰이 유효하지 않다고 하면 DB에서 해당 토큰 삭제
        if "registration-token-not-registered" in response or "invalid-registration-token" in response:
            delete_notification_token(request.token)

        print(f"Successfully sent message to token {request.token}: {response}")
        return {"status": "success", "message_id": response}

    except ValueError as e:
        # Handles cases where the token is invalid or other message validation issues
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}")
    except Exception as e:
        # Catch any other unexpected errors during message sending
        print(f"Error sending FCM message: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {e}")

def send_daily_reminder_9():
    pass 
    # 1. DB에서 유저 목록을 가져옴 
    
    # 2. 각 유저에게 알림 보냄
    # send_notification(user)