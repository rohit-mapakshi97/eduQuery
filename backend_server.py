from flask import request, jsonify, Flask
from flask_cors import CORS
from src.graph_pipeline import GraphEduQuery

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Flask API is running!", 200

@app.route('/message', methods=['POST'])
def chat_response():
    prompt = request.json['prompt']
    resp = None
    eq = GraphEduQuery()
    try:
        resp = eq.ask(question=prompt)
    except Exception as e:
        return jsonify({
            "error": "An internal error occoured. Please try again later.",
            "details": str(e)
        }), 500
    return jsonify({"assistant_message": resp}), 200

if __name__ == '__main__':
    # app.run(debug=True, port=8080) ## FOR LOCAL
    app.config['DEBUG'] = 1
    app.run() # FOR DEPLOY
