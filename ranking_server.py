
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "scores.json"

# Inicializa o arquivo se não existir
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

@app.route("/score", methods=["POST"])
def save_score():
    data = request.get_json()
    if not all(k in data for k in ("name", "stage", "time")):
        return jsonify({"error": "Invalid data"}), 400

    with open(DATA_FILE, "r") as f:
        scores = json.load(f)

    scores.append(data)

    # Salva novamente
    with open(DATA_FILE, "w") as f:
        json.dump(scores, f)

    return jsonify({"message": "Score saved"}), 200

@app.route("/top5", methods=["GET"])
def top5_scores():
    with open(DATA_FILE, "r") as f:
        scores = json.load(f)

    # Ordena por stage (desc) e tempo (asc)
    top_scores = sorted(scores, key=lambda x: (-x["stage"], x["time"]))[:5]
    return jsonify(top_scores)

if __name__ == "__main__":
    app.run(debug=True)
