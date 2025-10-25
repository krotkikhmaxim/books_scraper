"""tests"""


from scraper import scrape_books, get_book_data
import pytest
import os
import requests
import json
import sys
import tempfile


# Добавляем корневую директорию в Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


TEST_URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"


def test_extract_data():
    """Проверяет запись данных в файл"""
    test_filename = 'test_books_data.txt'

    # Создаем временную директорию для теста
    with tempfile.TemporaryDirectory() as temp_dir:
        test_filename = os.path.join(temp_dir, 'test_books_data.txt')

        # Тестируем запись в файл
        result = scrape_books(
            is_save=True,
            file_name=test_filename,
            stop=1,
            folder=''
            )
        result
        # Проверяем, что файл создан и не пустой
        assert os.path.exists(test_filename)
        assert os.path.getsize(test_filename) > 0


def test_get_book_data():
    """Проверяет сбор данных об одной книге"""
    # Используем реальную книгу для тестирования
    test_url = TEST_URL

    try:
        book_data = get_book_data(test_url)

        # Проверяем структуру данных
        assert isinstance(book_data, dict)
        assert 'title' in book_data
        assert 'price' in book_data
        assert 'description' in book_data
        assert 'rating' in book_data
        assert 'availability' in book_data
        assert 'category' in book_data
        assert 'product_info' in book_data
        assert 'image_url' in book_data

        # Проверяем типы данных
        assert isinstance(book_data['title'], str)
        assert isinstance(book_data['price'], str)
        assert isinstance(book_data['description'], str)

    except requests.exceptions.RequestException:
        pytest.skip("Нет интернет-соединения для теста")
    except Exception as e:
        pytest.fail(f"Ошибка при получении данных книги: {e}")


def test_scrape_books():
    """Проверяет сбор данных обо всех книгах"""
    # Тестируем парсинг ограниченного количества страниц
    result = scrape_books(is_save=False, stop=2)

    assert isinstance(result, dict)
    # Проверяем, что получили данные
    assert len(result) > 0

    # Проверяем структуру данных первой книги
    if result:
        first_book = list(result.values())[0]
        assert isinstance(first_book, dict)
        assert 'title' in first_book


def test_every():
    """Проверяет работу регулярной выгрузки"""
    # Тестируем разные форматы данных
    formats_to_test = [
        str,
        json.dumps,
        lambda x: f"BOOK: {x[1]['title']}" if x[1].get('title') else "UNKNOWN"
    ]

    for fmt in formats_to_test:
        result = scrape_books(
            is_save=False,
            stop=1,
            format_data=fmt
        )
        assert isinstance(result, dict)
