import os
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from dotenv import load_dotenv
from agent import agent_decision

load_dotenv()

slack_token = os.getenv("SLACK_BOT_TOKEN")
slack_channel = os.getenv("SLACK_CHANNEL_ID")

web_client = WebClient(token=slack_token)

def handle_events(req: SocketModeRequest):
    if req.type == "events_api":
        event = req.payload["event"]
        if "text" in event and event.get("channel") == slack_channel:
            user_message = event["text"]
            response = agent_decision(user_message)
            if response.startswith("✅"):
                web_client.chat_postMessage(
                    channel=event["channel"],
                    thread_ts=event.get("ts"),
                    text=response
                )
        return SocketModeResponse(envelope_id=req.envelope_id)

# --- Launch the Socket Mode Client ---
if __name__ == "__main__":
    app_token = os.getenv("SLACK_APP_TOKEN")  # You’ll need this next
    if not app_token:
        raise ValueError("SLACK_APP_TOKEN not set in .env")

    client = SocketModeClient(
        app_token=app_token,
        web_client=web_client
    )
    client.socket_mode_request_listeners.append(handle_events)
    client.connect()
    print("🤖 Agent is running and listening to Slack...")

print("🔐 SLACK_BOT_TOKEN:", os.getenv("SLACK_BOT_TOKEN"))
print("🔐 SLACK_APP_TOKEN:", os.getenv("SLACK_APP_TOKEN"))
print("🔐 SLACK_CHANNEL_ID:", os.getenv("SLACK_CHANNEL_ID"))
