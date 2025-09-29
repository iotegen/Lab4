# Lab #4 — Finding common issues (errors, secrets, deserialization)

## Репозиторий
https://github.com/iotegen/Lab4

## Описание
Минимальный Flask-сервер для демонстрации трёх классов проблем:
1. Internal information exposure (stack traces)
2. Hardcoded secrets / config with secrets
3. Unsafe deserialization

## Демонстрация
- `debug_output.json` — ответ `/debug` (содержит message и stack trace).
- `login_output.json` — ответ `/login` (демонстрация хардкод-токена).
- `deserialize_output.json` — ответ `/deserialize` (демонстрация десериализации).

## Анализ рисков
- **Stack traces** раскрывают внутренние пути и настройки, облегчают разведку.
- **Hardcoded secrets** — риск компрометации внешних сервисов и базы данных.
- **Unsafe deserialization** — потенциальный RCE и полная компрометация сервера.

## Pull Request (фиксы)
**Title:** fix: prevent info exposure, remove hardcoded secrets, secure input validation

**Description:**
- Не возвращать stack trace клиенту, только логировать сервер-side.
- Удалить хардкод паролей и токенов, использовать env vars и `config.example.json`.
- Убрать небезопасную десериализацию, заменить на строгую валидацию JSON.
- API совместимость сохранена, кроме более строгой проверки входных данных в `/deserialize`.
