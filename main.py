import sys
import os
from dotenv import load_dotenv
from openai import OpenAI
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ---------------------------
# ① ダミー会議テキスト（ここ変えてOK）
# ---------------------------
with open("meeting.m4a", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_file
    )

meeting_text = transcript.text

# ---------------------------
# ② 議事録作成
# ---------------------------
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "あなたは優秀な秘書です。議事録を作成してください。項目ごとに整理してください。"},
        {"role": "user", "content": meeting_text}
    ]
)

minutes = response.choices[0].message.content
print("===== 議事録 =====")
print(minutes)

# ---------------------------
# ③ Google Docs API認証
# ---------------------------
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os

SCOPES = ["https://www.googleapis.com/auth/documents"]

creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
        token.write(creds.to_json())

docs_service = build("docs", "v1", credentials=creds)

# ---------------------------
# ④ ドキュメント作成
# ---------------------------
doc = docs_service.documents().create(body={
    'title': '自動議事録'
}).execute()

doc_id = doc['documentId']

# ---------------------------
# ⑤ 書き込み
# ---------------------------
docs_service.documents().batchUpdate(
    documentId=doc_id,
    body={
        'requests': [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': minutes
                }
            }
        ]
    }
).execute()

print(f"✅ Googleドキュメント作成完了！")
print(f"https://docs.google.com/document/d/{doc_id}")
