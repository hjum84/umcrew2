from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Flask 애플리케이션 초기화
app = Flask(__name__)

# 홈 경로에서 index.html을 제공
@app.route('/')
def index():
    return render_template('index.html')

# 사용자 메시지에 대한 GPT 응답을 제공하는 엔드포인트
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "질문이 필요합니다."}), 400

    # GPT-3.5-turbo를 사용해 질문에 응답
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )
        chatbot_reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"reply": chatbot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render가 제공하는 포트에서 실행
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
