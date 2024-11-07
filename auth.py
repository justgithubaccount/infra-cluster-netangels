import requests

def get_token(API_KEY_NETANGELS):
    api_url_token = "https://panel.netangels.ru/api/gateway/token/"
    print("[INFO] Attempting to retrieve token using API key.")

    try:
        # Лог полного ключа перед отправкой запроса для проверки значений
        print(f"[DEBUG] Using API key: {API_KEY_NETANGELS}")

        # Формируем и отправляем запрос
        response = requests.post(api_url_token, data={"api_key": API_KEY_NETANGELS})
        
        # Логи для отладки запроса
        print("[DEBUG] Request details:")
        print(f"  URL: {api_url_token}")
        print(f"  Payload: {{'api_key': '{API_KEY_NETANGELS}'}}")  # Временно отображаем ключ полностью для отладки

        # Лог для статуса ответа
        print(f"[INFO] Response received with status code: {response.status_code}")

        if response.status_code == 200:
            token = response.json().get('token')
            if token:
                # Успешный случай с частично скрытым токеном для безопасности
                print(f"[SUCCESS] Token retrieved successfully: {token[:4]}***hidden***")
                return token
            else:
                # Если токен отсутствует в ответе
                print("[ERROR] No token found in response JSON.")
                raise ValueError("Token missing in response JSON.")
        else:
            # Ошибка в случае, если ответ содержит код статуса отличный от 200
            print(f"[ERROR] Failed to retrieve token. Status code: {response.status_code}")
            print(f"[ERROR] Response text: {response.text}")
            raise Exception("Failed to get token: " + response.text)

    except requests.exceptions.RequestException as e:
        # Лог ошибок запроса
        print(f"[ERROR] Request to API failed: {str(e)}")
        raise
