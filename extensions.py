import requests
import json
from config import TOKEN


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> float:
        try:
            amount = float(amount)
            if amount <= 0:
                raise APIException("❌ Количество должно быть больше 0")
        except ValueError:
            raise APIException(f"❌ Неправильное количество: {amount}")

        base = base.upper()
        quote = quote.upper()

        if base == quote:
            raise APIException(f"❌ Нельзя конвертировать {base} в {quote}")

        # Используем API ЦБ РФ
        try:
            response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
            data = response.json()

            # Для рубля (RUB) - особый случай
            if base == "RUB":
                if quote not in data["Valute"]:
                    raise APIException(f"❌ Валюта {quote} не поддерживается")
                rate = 1 / data["Valute"][quote]["Value"]
            elif quote == "RUB":
                if base not in data["Valute"]:
                    raise APIException(f"❌ Валюта {base} не поддерживается")
                rate = data["Valute"][base]["Value"]
            else:
                if base not in data["Valute"] or quote not in data["Valute"]:
                    raise APIException("❌ Одна из валют не поддерживается")
                rate = data["Valute"][base]["Value"] / data["Valute"][quote]["Value"]

            return round(rate * amount, 2)

        except requests.exceptions.RequestException:
            raise APIException("❌ Ошибка соединения с API ЦБ")
        except KeyError:
            raise APIException("❌ Ошибка в структуре данных API")
        except Exception as e:
            raise APIException(f"❌ Неизвестная ошибка: {str(e)}")
