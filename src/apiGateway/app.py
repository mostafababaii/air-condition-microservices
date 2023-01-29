from flask import Flask, request, jsonify
from settings import base as base_settings
from api.air_condition import get_air_pollution, AirConditionPayload
from api.air_condition import ValidationError


app = Flask(__name__)
app.env = base_settings.ENV


@app.route("/air-pollution/", strict_slashes=False, methods=["POST"])
async def air_pollution_endpoint():
    payload = request.get_json()

    try:
        result = get_air_pollution(AirConditionPayload(**payload))
    except (ValidationError, TypeError) as e:
        message = (
            str(e)
            if isinstance(e, ValidationError)
            else "The request payload is invalid"
        )
        status = 422 if isinstance(e, ValidationError) else 400
        return jsonify({"error": message}), status

    if result:
        return jsonify(result)

    return jsonify({"message": "Wait for 2 seconds"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
