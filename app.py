import os
from flask import Flask, request, jsonify, render_template
from rag.chatbot import get_answer, OWNER_NAME

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", owner_name=OWNER_NAME)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    question = (data.get("message") or "").strip()

    if not question:
        return jsonify({"error": "Message can't be empty."}), 400

    try:
        answer = get_answer(question)
        return jsonify({"reply": answer})
    except RuntimeError as e:
        # Missing index or API key - a setup problem, not a user error.
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Something went wrong. Please try again."}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)
