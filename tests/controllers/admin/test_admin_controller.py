import pytest
from src.models.user_model import UserModel
from src.models.history_model import HistoryModel


@pytest.fixture
def valid_user(app_test):
    user = UserModel({
        "name": "valid_user",
        "token": "valid_token",
    })
    user.save()
    return user


@pytest.fixture
def empty_attributes_user(app_test):
    user = UserModel({
        "name": "empty_attributes_user",
        "token": "empty_name_token",
    })
    user.save()
    return user


@pytest.fixture
def invalid_token_user(app_test):
    user = UserModel({
        "name": "invalid_token_user",
        "token": "invalid_token",
    })
    user.save()
    return user


@pytest.fixture
def history_data(app_test):
    history1 = HistoryModel({
        "text_to_translate": "Hello, I like videogame",
        "translate_from": "en",
        "translate_to": "pt",
    })
    history1.save()

    history2 = HistoryModel({
        "text_to_translate": "Do you love music?",
        "translate_from": "en",
        "translate_to": "pt",
    })
    history2.save()

    return [history1, history2]


def test_history_delete_with_valid_user(app_test, valid_user, history_data):
    history_id = history_data[0].data["_id"]

    assert HistoryModel.find_one({"_id": history_id}) is not None

    response = app_test.delete(
        f"/admin/history/{history_id}",
        headers={
            "Authorization": valid_user.data["token"],
            "User": valid_user.data["name"]
        }
    )

    assert response.status_code == 204
    assert HistoryModel.find_one({"_id": history_id}) is None


def test_history_delete_with_empty_attributes_user(
        app_test, empty_attributes_user, history_data):
    history_id = history_data[0].data["_id"]

    assert HistoryModel.find_one({"_id": history_id}) is not None

    response = app_test.delete(
        f"/admin/history/{history_id}",
        headers={
            "Authorization": empty_attributes_user.data["token"],
            "User": ""
        }
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized Access"}

    assert HistoryModel.find_one({"_id": history_id}) is not None


def test_history_delete_with_invalid_token_user(
        app_test, invalid_token_user, history_data):
    history_id = history_data[0].data["_id"]

    assert HistoryModel.find_one({"_id": history_id}) is not None

    response = app_test.delete(
        f"/admin/history/{history_id}",
        headers={
            "Authorization": "no_token",
            "User": invalid_token_user.data["name"]
        }
    )

    assert response.status_code == 401


def test_history_delete_not_found(app_test, valid_user):
    non_existent_id = "63b8f3a3f1e2e8e5d6cbb24e"

    response = app_test.delete(
        f"/admin/history/{non_existent_id}",
        headers={
            "Authorization": valid_user.data["token"],
            "User": valid_user.data["name"]
        }
    )

    assert response.status_code == 404
    assert response.json == {"error": "History not found"}


def test_history_delete(
        app_test, history_data):
    history_id = history_data[0].data["_id"]

    assert HistoryModel.find_one({"_id": history_id}) is not None

    response = app_test.delete(
        f"/admin/history/{history_id}",
        headers={
            "Authorization": "same_info",
            "User": "same_info"
        }
    )

    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized Access"}
