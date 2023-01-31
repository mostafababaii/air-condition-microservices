from flask import Flask, request, jsonify
from settings import base as base_settings
from api.air_condition import get_air_pollution, AirConditionPayload
from api.exceptions.validation import (
    ValidationError,
    BadPayload,
    handle_422,
    handle_400
)


app = Flask(__name__)
app.debug = base_settings.DEBUG
app.register_error_handler(ValidationError, handle_422)
app.register_error_handler(BadPayload, handle_400)


@app.route("/air-pollution/", strict_slashes=False, methods=["POST"])
async def air_pollution_endpoint():
    try:
        payload = AirConditionPayload(**request.get_json())
    except TypeError:
        raise BadPayload("Invalid payload")

    result = get_air_pollution(payload)
    if result:
        return jsonify(result)

    return jsonify({"message": "Wait for 2 seconds"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
