
####### Тест чтения данных из CSV-файлов:
def test_read_csv_file():
    # Проверяем чтение файла "prillet.csv"
    data = read_csv("prillet.csv")
    assert len(data) > 0
    assert "РАСЧЕТНОЕ" in data[0]

    # Проверяем чтение файла "vylet.csv"
    data = read_csv("vylet.csv")

    assert len(data) > 0
    assert "РАСЧЕТНОЕ" in data[0]

    # Проверяем чтение несуществующего файла
    with pytest.raises(FileNotFoundError):
        read_csv("non_existent_file.csv")


###### Тест обработки данных о рейсах 
def test_process_flight_data(monkeypatch):
    # Мокаем вызов naiti_svobodnye_brigadu_i_traktoristu, чтобы вернуть заданные значения
    def mock_find_available(*args):
        return "Бригада 1", "Тракторист 1"
    monkeypatch.setattr("naiti_svobodnye_brigadu_i_traktoristu", mock_find_available)

    # Тестируем обработку рейсов из "prillet.csv"
    prillet_data = [
        {"РАСЧЕТНОЕ": "2024-08-01 14:15:00", "НОМЕР": "123", "НАЗНАЧЕНИЕ": "Москва"},
        {"РАСЧЕТНОЕ": "2024-08-01 14:25:00", "НОМЕР": "456", "НАЗНАЧЕНИЕ": "Санкт-Петербург"}
    ]
    with monkeypatch.context():
        obrabotka_dannyh_iz_tablits(prillet_data, "vylet.csv")
        # Проверяем, что бригада и тракторист были назначены на рейсы
        assert "Бригада 1" in obrabotka_dannyh_iz_tablits.called_with
        assert "Тракторист 1" in obrabotka_dannyh_iz_tablits.called_with


##### Тест поиска свободных бригад и трактористов
def test_find_available_crew_and_driver():
    # Создаем тестовые бригады и трактористов
    brigada1 = Brigada(1, "Иван Иванов", "ожидание")
    brigada2 = Brigada(2, "Петр Петров", "на рейсе")
    traktorist1 = Traktorist(1, "Сидор Сидоров", "ожидание")
    traktorist2 = Traktorist(2, "Николай Николаев", "на рейсе")

    # Проверяем поиск свободной бригады и тракториста
    brigada, traktorist = naiti_svobodnye_brigadu_i_traktoristu(123, "Москва", "2024-08-01 14:15:00")
    assert brigada == brigada1
    assert traktorist == traktorist1

    # Проверяем, что бригада и тракторист в статусе "на рейсе"
    assert brigada1.status == "на рейсе"
    assert traktorist1.status == "на рейсе"


##### Тест сохранения данных о завершённых рейсах:
def test_save_completed_trips_to_csv(tmp_path):
    # Создаем временный файл для теста
    completed_trips_file = tmp_path / "completed_trips.csv"

    # Сохраняем данные о рейсе
    save_completed_trips_to_csv(123, "Москва", "2024-08-01 14:15:00", "на рейсе", "на рейсе")

    # Проверяем содержимое файла
    with open(completed_trips_file, "r") as file:
        data = file.read()
        assert "123,Москва,2024-08-01 14:15:00,на рейсе,на рейсе" in data
