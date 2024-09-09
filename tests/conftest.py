import allure
import pytest
import requests

from url_api import Api


# Фикстура для удаления курьера"
@allure.step('Удаление созданного курьера')
@pytest.fixture(scope='function')
def cleanup_courier():
    # Контейнер для передачи данных из теста в фикстуру
    container = {}
    yield container

    # После завершения теста, если был создан курьер, удалим его
    if 'courier_id' in container:
        courier_id = container['courier_id']
        response = requests.delete(f'{Api.BASE_URL + Api.CREATE_COURIER}/{courier_id}',
                                   json={'id': courier_id})
        assert response.status_code == 200, f"Не удалось удалить курьера с идентификатором {courier_id}"

@allure.step('Удаление созданного заказа')
@pytest.fixture
def created_orders():
    # Контейнер для передачи данных из теста в фикстуру
    container_orders = []
    yield container_orders

    # После выполнения тестов удаляем созданные заказы
    for track in container_orders:
        requests.delete(f'{Api.BASE_URL + Api.CREATE_ORDER}/{track}')
