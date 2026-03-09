# outline-vpn-api-client

Добро пожаловать в документацию **outline-vpn-api-client** — Python-библиотеки для управления Outline VPN сервером через официальный Management API.

## Возможности

- Управление ключами доступа: создание, переименование, удаление, установка лимитов трафика
- Настройка параметров сервера: хост, порт, лимиты по умолчанию
- Получение метрик сервера, включая статистику по трафику и ключам доступа
- Полная поддержка асинхронного режима через `AsyncOutlineClient`

## Установка

```bash
pip install outline-vpn-api-client
```

Для поддержки async:

```bash
pip install outline-vpn-api-client[async]
```

## Быстрый старт

```python
from outline_vpn_api_client import OutlineClient

client = OutlineClient(management_url="your.management.url")
print(client.get_information().model_dump())
```
