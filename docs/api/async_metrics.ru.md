# AsyncMetrics

::: outline_vpn_api_client.async_client.AsyncMetrics

## Примечание о `get_server_metrics`

Метод `get_server_metrics` использует endpoint `GET /experimental/server/metrics`,
который является **экспериментальным** и может быть недоступен в зависимости от версии
вашего Outline сервера.

**Требования:**

- Передача метрик должна быть включена: `await client.metrics.change_enabled_state(True)`
- Поведение endpoint'а и формат ответа могут измениться без предупреждения в будущих релизах сервера
