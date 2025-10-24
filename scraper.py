import time
import requests
import schedule
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def get_book_data(
    book_url: str,
    class_table: str = "table table-striped",
    must_have_data: list = None
) -> dict:
    """
    Извлекает данные о книге из HTML-таблицы на веб-странице.

    Args:
        book_url (str): URL-адрес страницы с информацией о книге
        class_table (str): CSS-класс таблицы (по умолчанию "table table-striped")
        must_have_data (list): Список обязательных полей для проверки

    Returns:
        dict: Словарь с данными о книге

    Raises:
        ValueError: При некорректных входных параметрах
        requests.exceptions.RequestException: При ошибках HTTP-запроса
        Exception: При ошибках парсинга HTML-контента
    """

    # Кастомные исключения
    class BookPageParseError(Exception):
        """Исключение для ошибок парсинга страницы книги."""
        pass

    class BookDataNotFoundError(Exception):
        """Исключение когда не найдены критические данные книги."""
        pass

    # Инициализация must_have_data по умолчанию
    if must_have_data is None:
        must_have_data = []

    parsed = urlparse(book_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}/"
    
    try:
        if not isinstance(book_url, str):
            raise ValueError(f"URL должен быть строкой, получен {type(book_url)}")

        # Выполнение HTTP-запроса
        try:
            response = requests.get(book_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                f"Ошибка выполнения HTTP-запроса {response.status_code}: {e}"
            )

        # Парсинг
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            raise BookPageParseError(f"Ошибка парсинга HTML: {e}")

        data = {}

        data['title'] = soup.find('h1').text
        data['price'] = soup.find('p', class_='price_color').text
        data['description'] = soup.find('meta', attrs={'name': 'description'})['content']

        rating_element = soup.find('p', class_='star-rating')
        data['rating'] = rating_element['class'][1] if rating_element else None

        availability = soup.find('p', class_='instock')
        data['availability'] = availability.text.strip() if availability else None

        breadcrumb = soup.find('ul', class_='breadcrumb')
        category_links = breadcrumb.find_all('li')
        data['category'] = category_links[2].text.strip() if len(category_links) > 2 else None

        table = soup.find(class_=class_table)

        headers = map(lambda x: x.get_text(strip=True), table.find_all('th'))
        data_cells = map(lambda x: x.get_text(strip=True), table.find_all('td'))

        data['product_info'] = dict(zip(headers, data_cells))

        image = soup.find('div', class_='item active').find('img')
        data['image_url'] = base_url + image['src'].replace('../..', '') if image else None

        none_data = set(must_have_data) & {key for key, value in data.items() if value is None}
        if none_data:
            raise BookDataNotFoundError(f"Обязательные поля не заполнены: {', '.join(none_data)}")

        return data

    except (ValueError, requests.exceptions.RequestException,
            BookPageParseError, BookDataNotFoundError):
        raise

    except Exception as e:
        raise BookPageParseError(f"Непредвиденная ошибка при обработке страницы: {e}")
    

def scrape_books(
    is_save=True, 
    base_url="http://books.toscrape.com/catalogue/page-{}.html", 
    page_num=1, 
    class_list="image_container",
    file_name='books_data.txt',
    format_data=str,
    stop=float('inf'),
    func_get=get_book_data
) -> dict: 

    """
    Парсит данные о книгах с сайта <base_url>.
    
    Функция проходит по указанному количеству страниц каталога, извлекает 
    ссылки на книги и собирает информацию о каждой книге.
    
    Args:
        is_save (bool): Сохранять ли данные в файл. По умолчанию True
        base_url (str): Шаблон URL для pagination. По умолчанию URL books.toscrape.com
        page_num (int): Номер страницы для начала парсинга. По умолчанию 1
        class_list (str): CSS класс для поиска контейнеров с книгами. По умолчанию "image_container"
        file_name (str): Имя файла для сохранения данных. По умолчанию 'books_data.txt'
        format_data (callable): Функция для форматирования данных перед сохранением. По умолчанию str
        stop (int): Номер страницы на которой остановиться. По умолчанию 2
        
    Returns:
        list: Список словарей с информацией о книгах
        
    Examples:
        >>> # Парсинг первых 2 страниц
        >>> books = scrape_books(stop=2)
        >>> # Парсинг с кастомным форматированием
    """
    
    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    
    data = {}
    book_num = 1
    
    while page_num <= stop:
        url = base_url.format(page_num)
        response = requests.get(url)
        
        if response.status_code != 200:
            break  # Закончились страницы

        try:
            soup = BeautifulSoup(response.text, 'html.parser').find_all(class_=class_list)
        
            for link in soup:
                full_url = "http://books.toscrape.com/catalogue/"+link.find('a', href=True)['href']
                data[book_num] = func_get(full_url)  
                book_num += 1
            
            page_num += 1
        
            time.sleep(0.5)
                  
            if is_save:        
                with open (file_name, 'w', encoding='utf-8') as f:
                    for book in data.items():
                        f.write(format_data(book)+'\n')
                        
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return {}
        except Exception as e:
            print(f"Ошибка парсинга: {e}")
            return {}     
        
    return data
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ 