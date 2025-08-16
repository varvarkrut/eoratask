

### 1. Настройка окружения
```bash
make env      # Create venv
make install  # Install dependencies
```

### 2. Настройка API ключа
Создайте файл `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Добавьте ссылки для парсинга
Создайте файл `links.txt` со ссылками на проекты:
```
https://eora.ru/cases/project1
https://eora.ru/cases/project2
...
```

### 4. Запуск настройки и чат-бота
```bash
make setup    # Setup project
make run      # Run chat bot
```




### 🎯 Архитектура решения
- RAG система с LangChain + Chroma для векторного поиска
- Обогащение данных через OpenAI API
- Автоматический парсинг веб-страниц
- CLI чат-интерфейс


### ✅ Что сработало
- RAG
- Обогащение данных через llm

### ⚠️ Что можно исправить или улучшить
- Добавить автотесты
- Логирование
- Валидация данных
- Рейт лимиты
- Кеширование
- Хардкод
- Синхронные вызовы

# ⭐ **Общая оценка  3- / 5**




