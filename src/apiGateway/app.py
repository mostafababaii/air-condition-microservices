from flask import Flask, request, jsonify
from settings import base as base_settings
from api.air_condition import get_air_pollution, AirConditionPayload
from api.air_condition import ValidationError


app = Flask(__name__)
app.env = base_settings.ENV


@app.route('/air-pollution/', strict_slashes=False, methods=["POST"])
async def air_pollution_endpoint():
    payload = request.get_json()

    try:
        result = get_air_pollution(AirConditionPayload(
            lat=payload["lat"],
            lon=payload["lon"],
            date_string=payload["date_string"]
        ))
    except ValidationError as e:
        return jsonify({"error": str(e)}), 422

    if result:
        return jsonify(result)

    return jsonify({"message": "Wait for 2 seconds"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
