"""
SpaceX Launch Data Fetcher
Получает данные о запусках ракет SpaceX
"""

import requests
import json
from datetime import datetime
import csv

def get_spacex_launches():
    """Получить данные о запусках SpaceX"""

    print("Подключаемся к SpaceX API...")

    # URL API SpaceX для запроса данных
    url = "https://api.spacexdata.com/v4/launches/query"

    # Настройки запроса: какие поля получить и сколько записей
    payload = {
        "query": {},
        "options": {
            "select": ["name", "date_utc", "success", "details", "flight_number"],
            "limit": 500,  # Можно изменить на большее число (макс 200)
            "sort": {"date_utc": "desc"}  # Сортировка по дате (новые сверху)
        }
    }

    try:
        # Отправляем запрос к API
        print("📡 Отправляем запрос к серверу SpaceX...")
        response = requests.post(url, json=payload, timeout=10)

        # Проверяем успешность запроса
        if response.status_code == 200:
            print("✅ Данные успешно получены!")

            # Парсим JSON ответ
            data = response.json()
            launches = data.get("docs", [])

            print(f"\nПолучено {len(launches)} запусков")
            print("=" * 70)

            # Выводим данные в консоль
            for i, launch in enumerate(launches, 1):
                name = launch.get("name", "Без названия")
                date_utc = launch.get("date_utc", "")
                success = launch.get("success")

                # Преобразуем дату
                if date_utc:
                    try:
                        date_obj = datetime.fromisoformat(date_utc.replace("Z", "+00:00"))
                        date_str = date_obj.strftime("%d.%m.%Y %H:%M UTC")
                    except:
                        date_str = date_utc
                else:
                    date_str = "Дата неизвестна"

                # Определяем статус
                if success is True:
                    status = "УСПЕШНО"
                elif success is False:
                    status = "НЕУДАЧА"
                else:
                    status = "НЕИЗВЕСТНО"

                # Выводим информацию
                print(f"{i}. {name}")
                print(f"   Дата: {date_str}")
                print(f"   Статус: {status}")

                # Выводим детали, если они есть
                details = launch.get("details", "")
                if details:
                    # Обрезаем длинный текст
                    if len(details) > 100:
                        details = details[:100] + "..."
                    print(f"   {details}")

                print("-" * 70)

            # Возвращаем данные для сохранения в файл
            return launches

        else:
            print(f"Ошибка при запросе: {response.status_code}")
            print(f"Причина: {response.text}")
            return None

    except requests.exceptions.Timeout:
        print("Таймаут: сервер не ответил вовремя")
        return None
    except requests.exceptions.ConnectionError:
        print("Ошибка подключения: проверьте интернет-соединение")
        return None
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return None

def save_to_json(launches, filename="spacex_launches.json"):
    """Сохранить данные в JSON файл"""
    if not launches:
        print("Нет данных для сохранения")
        return

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(launches, f, indent=2, ensure_ascii=False)
        print(f"\nДанные сохранены в файл: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении JSON: {e}")

def save_to_csv(launches, filename="spacex_launches.csv"):
    """Сохранить данные в CSV файл (можно открыть в Excel)"""
    if not launches:
        return

    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            # Определяем заголовки столбцов
            fieldnames = ["Номер полета", "Миссия", "Дата запуска (UTC)",
                         "Успешность", "Детали"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # Записываем заголовки

            for launch in launches:
                # Преобразуем данные
                name = launch.get("name", "")
                date_utc = launch.get("date_utc", "")
                success = launch.get("success")
                details = launch.get("details", "")
                flight_number = launch.get("flight_number", "")

                # Преобразуем статус в читаемый вид
                if success is True:
                    status_str = "Успешно"
                elif success is False:
                    status_str = "Неудача"
                else:
                    status_str = "Неизвестно"

                # Записываем строку
                writer.writerow({
                    "Номер полета": flight_number,
                    "Миссия": name,
                    "Дата запуска (UTC)": date_utc,
                    "Успешность": status_str,
                    "Детали": details[:200] if details else ""  # Обрезаем длинный текст
                })

        print(f"Данные сохранены в CSV (Excel): {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении CSV: {e}")

def show_menu():
    """Показать меню выбора"""
    print("\n" + "="*70)
    print("SPACEX LAUNCH DATA FETCHER")
    print("="*70)
    print("Что вы хотите сделать?")
    print("1. Получить данные о запусках и вывести на экран")
    print("2. Получить данные и сохранить в JSON файл")
    print("3. Получить данные и сохранить в CSV (для Excel)")
    print("4. Получить данные и сохранить во все форматы")
    print("5. Выход")

    choice = input("\nВыберите действие (1-5): ").strip()
    return choice

def main():
    """Главная функция программы"""
    print("="*70)
    print("SpaceX Launch Data Fetcher")
    print("="*70)

    while True:
        choice = show_menu()

        if choice == "1":
            # Просто получить и показать данные
            launches = get_spacex_launches()

        elif choice == "2":
            # Сохранить в JSON
            launches = get_spacex_launches()
            if launches:
                save_to_json(launches)

        elif choice == "3":
            # Сохранить в CSV
            launches = get_spacex_launches()
            if launches:
                save_to_csv(launches)

        elif choice == "4":
            # Сохранить во все форматы
            launches = get_spacex_launches()
            if launches:
                save_to_json(launches)
                save_to_csv(launches)

        elif choice == "5":
            print("\nВыход из программы. Удачи!")
            break

        else:
            print("\nНеверный выбор. Попробуйте снова.")

        if choice in ["1", "2", "3", "4"]:
            continue_choice = input("\n▶ Продолжить? (y/n): ").strip().lower()
            if continue_choice != "y":
                print("\nВыход из программы. Удачи!")
                break

# Эта строка запускает программу при выполнении скрипта
if __name__ == "__main__":
    main()