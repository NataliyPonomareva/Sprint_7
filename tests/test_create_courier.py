import allure
import requests

from data import UserCourier
from url_api import Api


class TestCreateCourier:
    @allure.title('Курьера можно создать')
    def test_create_courier_successfully(self, cleanup_courier):
        response = requests.post(Api.BASE_URL + Api.CREATE_COURIER, json=UserCourier.COURIER_DATA)
        response_json = response.json()

        assert response.status_code == 201 and response_json == {"ok": True}, \
                f"Ожидался статус-код 201 и JSON {{'ok': True}}, но получили статус-код {response.status_code} и JSON {response_json}"

        # Логиниваемся, чтобы получить ID созданного курьера для последующего удаления
        login_response = requests.post(Api.BASE_URL + Api.COURIER_ID, json=UserCourier.COURIER_DATA_LOGINING)
        # Сохраняем ID курьера для последующего удаления
        courier_id = login_response.json().get('id')
        cleanup_courier['courier_id'] = courier_id


    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_cannot_create_two_identical_couriers(self, cleanup_courier):
        requests.post(Api.BASE_URL + Api.CREATE_COURIER, json=UserCourier.COURIER_DATA)
        response = requests.post(Api.BASE_URL + Api.CREATE_COURIER, json=UserCourier.COURIER_DATA)
        response_json = response.json()
        assert response.status_code == 409 and response_json == {"code": 409,
                                                             "message": "Этот логин уже используется. Попробуйте другой."}, \
            f"Ожидался статус-код 409 и JSON {{'code': 409, 'message': 'Этот логин уже используется. Попробуйте другой.'}}, но получили статус-код {response.status_code} и JSON {response_json}"

        # Логиниваемся, чтобы получить ID созданного курьера
        login_response = requests.post(Api.BASE_URL + Api.COURIER_ID, json=UserCourier.COURIER_DATA_LOGINING)
        # Сохраняем ID курьера для последующего удаления
        courier_id = login_response.json().get('id')
        cleanup_courier['courier_id'] = courier_id


    @allure.description('Без логина нельзя создать курьера')
    def test_cannot_create_without_login(self):
        response = requests.post(Api.BASE_URL + Api.CREATE_COURIER, json=UserCourier.COURIER_DATA_WITHOUT_LOGIN)
        response_json = response.json()

        assert response.status_code == 400 and response_json == {'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}, \
                f"Ожидался статус-код 400 и JSON {{'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}}, но получили статус-код {response.status_code} и JSON {response_json}"


    @allure.description('Без пароля нельзя создать курьера')
    def test_cannot_create_without_password(self):
        response = requests.post(Api.BASE_URL + Api.CREATE_COURIER, json=UserCourier.COURIER_DATA_WITHOUT_PASSWORD)
        response_json = response.json()

        assert response.status_code == 400 and response_json == {'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}, \
                f"Ожидался статус-код 400 и JSON {{'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}}, но получили статус-код {response.status_code} и JSON {response_json}"
