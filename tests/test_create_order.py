import allure
import pytest
import requests
from url_api import Api



class TestCreateOrder:
    @allure.title('Курьера может авторизоваться')
    @pytest.mark.parametrize(
        "firstName, lastName, address, metroStation, phone, rentTime, deliveryDate, comment, color",
        [
            ("Ирина", "Смирнова", "Высотная", 4, "+79856457822", 5, "2024-10-06", "Позвоните при доставке", ["BLACK"]),
            ("Ирина", "Смирнова", "Высотная", 4, "+79856457822", 5, "2024-10-06", "Позвоните при доставке", ["GREY"]),
            ("Ирина", "Смирнова", "Высотная", 4, "+79856457822", 5, "2024-10-06", "Позвоните при доставке", ["BLACK", "GREY"]),
            ("Ирина", "Смирнова", "Высотная", 4, "+79856457822", 5, "2024-10-06", "Позвоните при доставке", [])
        ]
    )
    def test_create_order(self, firstName, lastName, address, metroStation, phone, rentTime, deliveryDate, comment,
                          color, created_orders):
        order_data = {
            'firstName': firstName,
            'lastName': lastName,
            'address': address,
            'metroStation': metroStation,
            'phone': phone,
            'rentTime': rentTime,
            'deliveryDate': deliveryDate,
            'comment': comment,
            'color': color
        }
        response = requests.post(Api.BASE_URL + Api.CREATE_ORDER, json=order_data)
        response_json = response.json()

        # Проверка, что заказ создан
        assert response.status_code == 201 and response_json['track'] > 0, (
            f"Ошибочный результат: статус-код {response.status_code} и значение 'track' {response_json.get('track', 'не найдено')}"
        )

        # Сохраняем track заказа для последующего удаления созданного заказа
        track = response_json['track']
        created_orders.append(track)
