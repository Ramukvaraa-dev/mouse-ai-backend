from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("GOOGLE_API_KEY")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json["message"]

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": user_message}
                    ]
                }
            ]
        }

        response = requests.post(url, json=payload)
        data = response.json()

        try:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            reply = "No response from AI."

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
