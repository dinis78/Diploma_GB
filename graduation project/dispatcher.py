import time
from datetime import datetime, timedelta
import csv
import platform

# Определение функции для воспроизведения звукового сигнала
if platform.system() == 'Windows':
    import winsound
    def play_sound():
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
elif platform.system() in ['Linux', 'Darwin']:
    import playsound
    def play_sound():
        playsound.playsound('/usr/share/sounds/ubuntu/stereo/system-ready.ogg')
else:
    def play_sound():
        print("Звуковой сигнал не поддерживается на этой платформе.")

class Brigada:
    def __init__(self, nomer, fio1, fio2):
        self.nomer = nomer
        self.fio1 = fio1
        self.fio2 = fio2
        self.status = "ожидание"
        self.rejs_nomer = None  # Номер рейса
        self.naznachenie = None  # Назначение
        self.raschetnoe_vremya = None  # Расчётное время
        self.svobodno_v = None  # Время, когда бригада освободилась

    def zagruzit_dannie(self, rejs_nomer, naznachenie, raschetnoe_vremya):
        self.rejs_nomer = rejs_nomer
        self.naznachenie = naznachenie
        self.raschetnoe_vremya = raschetnoe_vremya

class Traktorist:
    def __init__(self, nomer, fio):
        self.nomer = nomer
        self.fio = fio
        self.status = "ожидание"
        self.rejs_nomer = None  # Номер рейса
        self.naznachenie = None  # Назначение
        self.raschetnoe_vremya = None  # Расчётное время
        self.svobodno_v = None  # Время, когда тракторист освободился

    def zagruzit_dannie(self, rejs_nomer, naznachenie, raschetnoe_vremya):
        self.rejs_nomer = rejs_nomer
        self.naznachenie = naznachenie
        self.raschetnoe_vremya = raschetnoe_vremya

brigady = [
    Brigada(1, "Павлинский А.И.", "Климов Р.П."),
    Brigada(2, "Гордеев А.С.", "Шрейдер С.К."),
    Brigada(3, "Митюшкин Р.М.", "Воронцов Д.О."),
    Brigada(4, "Сердцев Р.Л.", "Образцов О.С."),
    Brigada(5, "Пожогин А.М.", "Черный А.П."),
    Brigada(6, "Климов А.И.", "Павлов И.Н."),
    Brigada(7, "Яковец Е.Е.", "Жанобаев А.Ф."),
    Brigada(8, "Ильин П.И.", "Зырянов Д.К."),
    Brigada(9, "Хохлов В.П.", "Рахвалов Г.С."),
    Brigada(10, "Шкурко Д.С", "Данилов И.А.")
]

traktory = [
    Traktorist(303, "Чистюхин С.И."),
    Traktorist(345, "Байтимиров Н.П."),
    Traktorist(301, "Фоменко С.С."),
    Traktorist(348, "Никульшин С.К."),
    Traktorist(349, "Гайнутдинов В.М."),
    Traktorist(350, "Омаров С.О."),
    Traktorist(351, "Пичюгин С.Л."),
    Traktorist(306, "Соколов К.С.")
]

def otpravit_brigadu_na_rejs():
    if any(b.status == "ожидание" for b in brigady):
        for i, b in enumerate(brigady):
            if b.status == "ожидание":
                if any(t.status == "ожидание" for t in traktory):
                    for j, t in enumerate(traktory):
                        if t.status == "ожидание":
                            b.status = "на рейсе"
                            t.status = "на рейсе"
                            print(f"Бригада {b.nomer}: {b.fio1}, {b.fio2} отправлена на рейс с трактором {t.nomer} - {t.fio}.")
                            brigady.append(brigady.pop(i))
                            traktory.append(traktory.pop(j))
                            break
                else:
                    print("Все тракторы на рейсе, ждите возвращения.")
                break
    else:
        print("Все бригады на рейсе, ждите возвращения.")

def prinyat_brigadu_s_rejsa():
    nomer_brigady = int(input("Введите номер бригады, вернувшейся с рейса: "))
    found = False
    for i, brigada in enumerate(brigady):
        if brigada.nomer == nomer_brigady and brigada.status == "на рейсе":
            brigada.status = "ожидание"
            brigada_status = "ожидание"

            # Найдите соответствующего тракториста для этой бригады
            traktorist = next((t for t in traktory if t.rejs_nomer == brigada.rejs_nomer), None)
            if traktorist:
                traktorist.status = "ожидание"
                traktorist_status = "ожидание"
            else:
                traktorist_status = "Нет данных"

            print(f"Бригада {brigada.nomer}: {brigada.fio1}, {brigada.fio2} вернулась с рейса и встала в конец очереди.")
            brigady.append(brigady.pop(i))
            found = True

            # Вызов функции save_completed_trips_to_csv()
            save_completed_trips_to_csv(str(brigada.rejs_nomer), brigada.naznachenie, str(brigada.raschetnoe_vremya), str(brigada.nomer), str(traktorist.nomer) if traktorist else "Нет данных")

            break
    if not found:
        print(f"Бригада с номером {nomer_brigady} не найдена или не находится на рейсе.")




def otpravit_traktoristu_na_rejs():
    if any(t.status == "ожидание" for t in traktory):
        for i, t in enumerate(traktory):
            if t.status == "ожидание":
                t.status = "на рейсе"
                print(f"Трактор {t.nomer} - {t.fio} отправлен на рейс.")
                traktory.append(traktory.pop(i))
                break
    else:
        print("Все тракторы на рейсе, ждите возвращения.")

def prinyat_traktoristu_s_rejsa():
    nomer_traktora = int(input("Введите номер трактора, вернувшегося с рейса: "))
    found = False
    for i, traktorist in enumerate(traktory):
        if traktorist.nomer == nomer_traktora and traktorist.status == "на рейсе":
            traktorist.status = "ожидание"
            print(f"Трактор {traktorist.nomer} - {traktorist.fio} вернулся с рейса и встал в конец очереди.")
            traktory.append(traktory.pop(i))
            found = True
            break
    if not found:
        print(f"Трактор с номером {nomer_traktora} не найден или не находится на рейсе.")

def obrabotka_dannyh_iz_tablits():
    # Чтение данных из CSV-файлов, представляющих таблицы "Прилёт" и "Вылет"
    prillet_data = read_csv("prillet.csv")
    vylet_data = read_csv("vylet.csv")

    if prillet_data is None or vylet_data is None:
        return

    # Анализ данных и назначение бригад/трактористов на рейсы
    for rejs in prillet_data:
        rejs_time = rejs["РАСЧЕТНОЕ"].split(":")
        if len(rejs_time) == 3:
            rejs_datetime = datetime.now().replace(hour=int(rejs_time[0]),
                                                  minute=int(rejs_time[1]),
                                                  second=int(rejs_time[2]))
        else:
            print(f"Некорректный формат времени в столбце 'РАСЧЕТНОЕ' для рейса {rejs['РЕЙС']}: {rejs['РАСЧЕТНОЕ']}")
            continue
        time_diff = rejs_datetime - datetime.now()
        if time_diff.total_seconds() >= 0 and time_diff.total_seconds() <= 600:  # 10 минут
            naiden_traktorist, naiden_brigada = naiti_svobodnye_brigadu_i_traktoristu(rejs["РЕЙС"], rejs["НАЗНАЧЕНИЕ"], rejs["РАСЧЕТНОЕ"])
            if naiden_traktorist and naiden_brigada:
                continue
            else:
                next_arrival = find_next_arrival(prillet_data, "РАСЧЕТНОЕ")
                next_departure = find_next_departure(vylet_data, "РАСЧЕТНОЕ")
                print(f"Рейс {rejs['РЕЙС']} - {rejs['НАЗНАЧЕНИЕ']} через {int(time_diff.total_seconds() // 60)} минут.")
                if next_arrival != "Нет данных" or next_departure != "Нет данных":
                    print(f"Ближайший прилет: {next_arrival}")
                    print(f"Ближайший вылет: {next_departure}")
                else:
                    print("Нет данных о ближайших рейсах.")
                print("Нет необходимости отправлять бригаду.")

    for rejs in vylet_data:
        rejs_time = rejs["РАСЧЕТНОЕ"].split(":")
        if len(rejs_time) == 3:
            rejs_datetime = datetime.now().replace(hour=int(rejs_time[0]),
                                                  minute=int(rejs_time[1]),
                                                  second=int(rejs_time[2]))
        else:
            print(f"Некорректный формат времени в столбце 'РАСЧЕТНОЕ' для рейса {rejs['РЕЙС']}: {rejs['РАСЧЕТНОЕ']}")
            continue
        time_diff = rejs_datetime - datetime.now()
        if time_diff.total_seconds() >= 0 and time_diff.total_seconds() <= 2400:  # 40 минут
            naiden_traktorist, naiden_brigada = naiti_svobodnye_brigadu_i_traktoristu(rejs["РЕЙС"], rejs["НАЗНАЧЕНИЕ"], rejs["РАСЧЕТНОЕ"])
            if naiden_traktorist and naiden_brigada:
                continue
            else:
                next_arrival = find_next_arrival(prillet_data, "РАСЧЕТНОЕ")
                next_departure = find_next_departure(vylet_data, "РАСЧЕТНОЕ")
                print(f"Рейс {rejs['РЕЙС']} - {rejs['НАЗНАЧЕНИЕ']} через {int(time_diff.total_seconds() // 60)} минут.")
                if next_arrival != "Нет данных" or next_departure != "Нет данных":
                    print(f"Ближайший прилет: {next_arrival}")
                    print(f"Ближайший вылет: {next_departure}")
                else:
                    print("Нет данных о ближайших рейсах.")
                print("Нет необходимости отправлять бригаду.")


def naiti_svobodnye_brigadu_i_traktoristu(rejs_nomer, naznachenie, raschetnoe_vremya):
    for brigada in brigady:
        if brigada.status == "ожидание":
            for traktorist in traktory:
                if traktorist.status == "ожидание":
                    brigada.status = "на рейсе"
                    traktorist.status = "на рейсе"
                    return traktorist, brigada
    return None, None

import logging

# Настройка логгера
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s: %(message)s',
                    filename='completed_trips.log',
                    filemode='a')

def save_completed_trips_to_csv(rejs_nomer, naznachenie, raschetnoe_vremya, brigada_str, traktorist_str):
    # Формирование строки для записи в CSV-файл
    print("Функция save_completed_trips_to_csv() вызвана")
    
    # Поиск бригады по строке
    brigada = next((b for b in brigady if str(b.nomer) == brigada_str), None)
    
    # Поиск тракториста по строке
    traktorist = next((t for t in traktory if str(t.nomer) == traktorist_str), None)
    
    # Получение информации о бригаде
    if brigada:
        brigada_nomer = brigada.nomer
        brigada_fio1 = brigada.fio1
        brigada_fio2 = brigada.fio2
        brigada_status = brigada.status
    else:
        brigada_nomer = "Нет данных"
        brigada_fio1 = "Нет данных"
        brigada_fio2 = "Нет данных"
        brigada_status = "Нет данных"
    
    # Получение информации о тракторе
    if traktorist:
        traktorist_nomer = traktorist.nomer
        traktorist_fio = traktorist.fio
        traktorist_status = traktorist.status
    else:
        traktorist_nomer = "Нет данных"
        traktorist_fio = "Нет данных" 
        traktorist_status = "Нет данных"
    
    row = [rejs_nomer, naznachenie, raschetnoe_vremya, 
          brigada_nomer, brigada_fio1, brigada_fio2, brigada_status,
          traktorist_nomer, traktorist_fio, traktorist_status]

    # Открытие CSV-файла в режиме "дозаписи" с кодировкой UTF-8 (если файл не существует, он будет создан)
    with open("completed_trips.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

    logging.info(f"Информация о рейсе {rejs_nomer} сохранена в CSV-файл.")




def read_csv(filename):
    data = []
    try:
        with open(filename, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except UnicodeDecodeError:
        try:
            with open(filename, "r", encoding="cp1251") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(row)
        except UnicodeDecodeError:
            print(f"Ошибка кодировки при чтении файла {filename}.")
            return None
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {e}")
        return None
    return data




def upravlenie_ocherednoctyu():
    while True:
        print("Управление очередностью трактористов и бригад:")
        print("Тракторы:")
        for traktorist in traktory:
            print(f"Трактор {traktorist.nomer} - {traktorist.fio} - {traktorist.status}")
        print("\nБригады:")
        for brigada in brigady:
            print(f"Бригада {brigada.nomer}: {brigada.fio1}, {brigada.fio2} - {brigada.status}")

        print("\nВыберите действие:")
        print("1. Отправить следующую бригаду на рейс")
        print("2. Принять бригаду с рейса")
        print("3. Отправить следующего тракториста на рейс")
        print("4. Принять тракториста с рейса")
        print("5. Выход")
        vybor = input("Введите номер действия: ")

        if vybor == "1":
            otpravit_brigadu_na_rejs()
        elif vybor == "2":
            prinyat_brigadu_s_rejsa()
        elif vybor == "3":
            otpravit_traktoristu_na_rejs()
        elif vybor == "4":
            prinyat_traktoristu_s_rejsa()
        elif vybor == "5":
            break
        else:
            print("Неверный выбор, попробуйте еще раз.")

        # Автоматическая обработка данных из таблиц "Прилёт" и "Вылет"
        obrabotka_dannyh_iz_tablits()

        time.sleep(1)  # Ждём 30 секунд перед следующей итерацией

if __name__ == "__main__":
    upravlenie_ocherednoctyu()