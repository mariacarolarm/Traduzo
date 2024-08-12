from src.models.history_model import HistoryModel


def test_request_history():
    list_json = HistoryModel.list_as_json()

    assert "Hello, I like videogame" in list_json
    assert "Do you love music?" in list_json
