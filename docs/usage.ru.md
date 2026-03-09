# Использование

## Инициализация клиента

```python
from outline_vpn_api_client import OutlineClient

client = OutlineClient(management_url="your.management.url")
```

> **Примечание:** По умолчанию проверка SSL-сертификата отключена (`ssl_verify=False`). Это сделано намеренно,
> так как Outline серверы обычно используют самоподписанные сертификаты. Вы можете включить проверку,
> передав `ssl_verify=True`, если ваш сервер имеет валидный сертификат.

---

## Сервер

### Получить информацию о сервере

```python
info = client.server.get_information()
print(info.serverId)
print(info.name)
```

### Переименовать сервер

```python
client.server.rename("Мой VPN сервер")
```

### Изменить хостнейм

```python
client.server.change_hostname("vpn.example.com")
```

### Изменить порт по умолчанию для новых ключей доступа

```python
client.server.change_default_port_for_new_keys(12345)
```

### Установить лимит трафика по умолчанию для всех ключей

```python
client.server.set_server_default_limits(10 ** 9)  # 1 ГБ
```

### Убрать лимит трафика по умолчанию

```python
client.server.remove_server_default_limits()
```

---

## Ключи доступа

### Список всех ключей доступа

```python
keys = client.access_keys.get_all()
for key in keys.accessKeys:
    print(key.id, key.name)
```

### Получить конкретный ключ доступа

```python
key = client.access_keys.get(0)
print(key.accessUrl)
```

### Создать ключ доступа

```python
# Минимальный вариант
key = client.access_keys.create(name="Алиса")

# С лимитом трафика (в байтах)
key = client.access_keys.create(name="Боб", limit=10 ** 9)

# С произвольным паролем и портом
key = client.access_keys.create(name="Вася", password="MyPass123", port=12345)
```

### Создать ключ доступа с определённым ID

```python
key = client.access_keys.create_with_special_id(
    id=42,
    name="Петя",
    password="MyPass123",
    port=12345,
    limit=10 ** 9,
)
```

### Переименовать ключ доступа

```python
client.access_keys.rename(42, "Петя Переименованный")
```

### Установить лимит трафика на ключ доступа

```python
client.access_keys.change_data_limit(42, 5 * 10 ** 9)  # 5 ГБ
```

### Убрать лимит трафика с ключа доступа

```python
client.access_keys.remove_data_limit(42)
```

### Удалить ключ доступа

```python
client.access_keys.delete(42)
```

---

## Метрики

### Проверить, включена ли передача метрик

```python
print(client.metrics.check_enabled())
```

### Включить или отключить передачу метрик

```python
client.metrics.change_enabled_state(True)   # включить
client.metrics.change_enabled_state(False)  # отключить
```

### Получить объём переданных данных по ключам доступа

```python
transfer = client.metrics.get_data_transfer()
for key_id, bytes_used in transfer.bytesTransferredByUserId.items():
    print(f"Ключ {key_id}: {bytes_used / 10**6:.1f} МБ")
```

### Получить подробные метрики сервера (экспериментально)

```python
from datetime import datetime, timezone, timedelta

metrics = client.metrics.get_server_metrics(
    since=datetime.now(timezone.utc) - timedelta(days=30)
)

print(metrics.server.dataTransferred.bytes)
print(metrics.server.bandwidth.peak.data.bytes)

for key in metrics.accessKeys:
    bytes_used = key.dataTransferred.bytes if key.dataTransferred else 0
    print(f"Ключ {key.accessKeyId}: {bytes_used / 10**6:.1f} МБ")
```

> **Примечание:** Этот endpoint является экспериментальным и может измениться в будущих версиях Outline сервера.

---

## Асинхронное использование

Установите пакет с поддержкой async:

```bash
pip install outline-vpn-api-client[async]
```

Все методы идентичны синхронному клиенту, но требуют `await`:

```python
import asyncio
from datetime import datetime, timezone, timedelta
from outline_vpn_api_client.async_client import AsyncOutlineClient

client = AsyncOutlineClient(management_url="your.management.url")

async def main():
    # Информация о сервере
    info = await client.server.get_information()
    print(info.serverId)

    # Создать ключ
    key = await client.access_keys.create(name="Алиса", limit=10 ** 9)
    print(key.accessUrl)

    # Подробные метрики
    metrics = await client.metrics.get_server_metrics(
        since=datetime.now(timezone.utc) - timedelta(days=30)
    )
    print(metrics.server.dataTransferred.bytes)

asyncio.run(main())
```

---

## Обработка ошибок

Все методы выбрасывают `ResponseNotOkException` при ошибках на стороне сервера:

```python
from outline_vpn_api_client import OutlineClient, ResponseNotOkException

client = OutlineClient(management_url="your.management.url")

try:
    key = client.access_keys.get(999)
except ResponseNotOkException as e:
    print(e)
    # An error occurred: 404 - {'code': 'NotFound', 'message': 'Access key "999" not found'}
```
