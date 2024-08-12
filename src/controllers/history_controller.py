from flask import Blueprint
from models.history_model import HistoryModel
from flask import jsonify

history_controller = Blueprint("history_controller", __name__)


@history_controller.route("/history/", methods=["GET"])
def recover_history():
    try:
        history = HistoryModel.list_as_json()
        return jsonify(history), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500
