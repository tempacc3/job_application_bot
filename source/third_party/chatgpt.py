import base64
import json
import uuid
from time import sleep
from third_party.browser import Browser

class ChatGPT(Browser):
    response_div_id = "chatgpt-wrapper-conversation-response-data"
    session_div_id = "chatgpt-wrapper-session-data"

    def __init__(self):
        super().__init__(page_address="https://chat.openai.com/")
        self.parent_message_id = str(uuid.uuid4())
        self.conversation_id = None
        self.session = None

    def refresh_session(self):
        if not self.play:
            raise AssertionError("Browser hasen't been started")
        self.page.evaluate(
            """
        const xhr = new XMLHttpRequest();
        xhr.open('GET', 'https://chat.openai.com/api/auth/session');
        xhr.onload = () => {
          if(xhr.status == 200) {
            var mydiv = document.createElement('DIV');
            mydiv.id = "SESSION_DIV_ID"
            mydiv.innerHTML = xhr.responseText;
            document.body.appendChild(mydiv);
          }
        };
        xhr.send();
        """.replace(
                "SESSION_DIV_ID", self.session_div_id
            )
        )

        while True:
            session_datas = self.page.query_selector_all(f"div#{self.session_div_id}")
            if len(session_datas) > 0:
                break
            sleep(0.2)

        session_data = json.loads(session_datas[0].inner_text())
        self.session = session_data

        self.page.evaluate(f"document.getElementById('{self.session_div_id}').remove()")

    def ask(self, prompt: str, model: str = "gpt-3.5", timeout_s: int = 30):
        if not self.play:
            raise AssertionError("Browser hasn't been started")
        if self.session is None:
            self.refresh_session()

        new_message_id = str(uuid.uuid4())

        if "accessToken" not in self.session:
            self.stop()
            raise PermissionError("Unauthorized used of ChatGpt. Please login")

        request = {
            "messages": [
                {
                    "id": new_message_id,
                    "role": "user",
                    "content": {"content_type": "text", "parts": [prompt]},
                }
            ],
            "model": model,
            "conversation_id": self.conversation_id,
            "parent_message_id": self.parent_message_id,
            "action": "next",
        }


        code = (
            """
            const response_div = document.createElement('DIV');
            response_div.id = "RESPONSE_DIV_ID";
            document.body.appendChild(response_div);
            
            fetch('https://chat.openai.com/backend-api/conversation', {
                method: 'POST',
                headers: {
                    'Accept': 'text/event-stream',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer BEARER_TOKEN',
                },
                body: JSON.stringify(REQUEST_JSON),
            })
            .then(response => response.text())
            .then(data => {
                response_div.innerHTML = btoa(data);
            });
            """.replace(
                "BEARER_TOKEN", self.session["accessToken"]
            )
            .replace("REQUEST_JSON", json.dumps(request))
            .replace("RESPONSE_DIV_ID", self.response_div_id)
        )

        self.page.evaluate(code)

        response_datas = self.page.query_selector(f"div#{self.response_div_id}")

        try:
            response_raw = base64.b64decode(response_datas.inner_html())
            if len(response_raw) == 0:
                raise Exception("Failed to decode ChatGPT response")
            try:
                events = response_raw.split(b'\n\n')
                final_event = events[-3][6:]
            except Exception:
                raise Exception("Failed to parse ChatGPT response")

            response = json.loads(final_event)
            if response is None:
                raise Exception("Failed to load ChatGPT response as JSON")

            self.parent_message_id = response["message"]["id"]
            self.conversation_id = response["conversation_id"]
            full_response_message = "\n".join(response["message"]["content"]["parts"])

            self.page.evaluate(f"document.getElementById('{self.response_div_id}').remove()")
            return full_response_message
        except Exception as e:
            self.stop()
            raise e

    def new_conversation(self):
        if not self.play:
            raise AssertionError("Browser hasn't been started")
        self.parent_message_id = str(uuid.uuid4())
        self.conversation_id = None


