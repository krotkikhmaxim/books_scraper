# Books Scraper 📚

Проект для автоматического парсинга данных о книгах с сайта [Books to Scrape](http://books.toscrape.com/).

## 🎯 Цель проекта

Разработать систему для сбора информации о книгах, включая:
- Название, автора, цену и рейтинг
- Описание и доступность
- Дополнительную информацию из таблицы продукта
- URL изображения обложки

## 🚀 Быстрый старт

### Установка и запуск

```bash
# Клонирование репозитория
git clone https://github.com/krotkikhmaxim/books_scraper.git
cd books_scraper

# Установка зависимостей
pip install -r requirements.txt

# Запуск парсера
python scraper.py
```

### Основные функции

```python
from scraper import get_book_data, scrape_books

# Парсинг одной книги
book_data = get_book_data('http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')

# Парсинг всех книг с сохранением
all_books = scrape_books(is_save=True, stop=2)
```

## 📁 Структура проекта

```
books_scraper/
├── artifacts/           # Результаты парсинга
│   └── books_data.txt
├── notebooks/          # Jupyter ноутбуки
│   └── HW_03_python_ds_2025.ipynb
├── tests/              # Автотесты
│   └── test_scraper.py
├── scraper.py          # Основной скрипт парсера
├── requirements.txt    # Зависимости
└── README.md
```

## 🛠 Технологии

- **Python 3.8+**
- **BeautifulSoup4** - парсинг HTML
- **Requests** - HTTP-запросы
- **Schedule** - автоматизация запуска
- **Pytest** - тестирование

## 📊 Возможности

- ✅ Парсинг данных с одной страницы книги
- ✅ Обход всех страниц каталога
- ✅ Автоматическое сохранение в файл
- ✅ Ежедневный автоматический запуск
- ✅ Обработка ошибок и повторные попытки
- ✅ Комплексное тестирование

## 🧪 Тестирование

```bash
# Запуск всех тестов
python -m pytest tests/ -v

# Запуск с покрытием
python -m pytest --cov=scraper tests/
```

## ⚙️ Конфигурация

Настройки можно изменить в коде:
- Таймауты запросов
- Количество повторных попыток
- Форматы вывода данных
- Расписание автоматического запуска

## 📈 Результаты

Проект собирает полную информацию о книгах:
- Основные данные (название, цена, рейтинг)
- Детальное описание
- Технические характеристики
- Ссылки на изображения
- Информация о доступности

## 🔗 Ссылки

- [Исходный сайт для парсинга](http://books.toscrape.com/)
- [Документация BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Документация Requests](https://docs.python-requests.org/)

