from flask import Flask, request, jsonify

from scanner import analyze_tos

app = Flask(__name__)


@app.route('/scan-tos', methods=['POST'])
def scan_tos():
	data = request.get_json(silent=True) or {}

	body_obj = data.get("body")
	if body_obj is None:
		return jsonify({"error": "Missing 'body' in request JSON"}), 400

	if isinstance(body_obj, (dict, list)):
		import json as _json

		body_str = _json.dumps(body_obj)
	else:
		body_str = str(body_obj)

	score = analyze_tos(body_str)

	return jsonify({"status": "TOS scanned successfully", "score": score}), 200


if __name__ == '__main__':
	app.run(debug=True)