import allure
import requests

from data import UserCourier
from url_api import Api


class TestListOrders:
    @allure.title('Получение списка заказов')
    def test_list_orders(self, cleanup_courier, created_orders):

        # Создать курьера
        requests.post(Api.BASE_URL + Api.CREATE_COURIER, json=UserCourier.COURIER_DATA)

        # Логиниваемся, чтобы получить ID созданного курьера для последующего удаления
        login_response = requests.post(Api.BASE_URL + Api.COURIER_ID, json=UserCourier.COURIER_DATA_LOGINING)
        # Сохраняем ID курьера для последующего удаления
        courier_id = login_response.json().get('id')

        # Создать заказ
        order_data = {
            'firstName': "Ирина",
            'lastName': "Смирнова",
            'address': "Высотная",
            'metroStation': 4,
            'phone': "+79856457822",
            'rentTime': 5,
            'deliveryDate': "2024-10-06",
            'comment': "Позвоните при доставке",
            'color': ["BLACK"]
        }
        response_order = requests.post(Api.BASE_URL + Api.CREATE_ORDER, json=order_data)
        response_order_json = response_order.json()

        # Сохраняем track заказа для последующего удаления созданного заказа
        track = response_order_json['track']

        # Отправляем запрос на получения списка заказа metroStation = 4
        list_orders_data = {'courierId': {courier_id}, 'nearestStation': ["4"]}

        response = requests.get(Api.BASE_URL + Api.CREATE_ORDER, data=list_orders_data)
        response_json = response.json()

        assert response.status_code == 200 and response_json, \
            f"Ожидался статус-код 200, но получили статус-код {response.status_code} и ответ пустой, ожидались данные."

        cleanup_courier['courier_id'] = courier_id   # Удалаем курьера
        created_orders.append(track)   # Удалаем заказ
