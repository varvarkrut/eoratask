"""Module for scraping project data from websites."""

import requests
from bs4 import BeautifulSoup
import json
import time


class SimpleScraper:
    """Простой парсер для сбора данных с сайта."""

    def __init__(self):
        self.headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/91.0.4472.124 Safari/537.36'),
            'Accept': ('text/html,application/xhtml+xml,application/xml;'
                       'q=0.9,image/webp,*/*;q=0.8'),
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def scrape_page(self, url):
        """
        Функция для парсинга одной страницы и извлечения контента.
        :param url: URL страницы для парсинга
        :type url: str
        :return: Словарь с результатом парсинга
        :rtype: dict
        """
        try:
            response = requests.get(url, timeout=10, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            title = ""
            if soup.title:
                title = soup.title.get_text().strip()

            content = soup.get_text()
            content = ' '.join(content.split())

            return {
                'url': url,
                'title': title,
                'content': content[:2000],
                'status': 'success'
            }
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"❌ Доступ запрещен (403) для {url}")
                print("   Возможно, сайт блокирует автоматические запросы")
            else:
                msg = f"❌ HTTP ошибка {e.response.status_code} для {url}: {e}"
                print(msg)
            return {
                'url': url,
                'title': '',
                'content': '',
                'status': 'error',
                'error': f"HTTP {e.response.status_code}: {str(e)}"
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка сети для {url}: {e}")
            return {
                'url': url,
                'title': '',
                'content': '',
                'status': 'error',
                'error': f"Network error: {str(e)}"
            }
        except Exception as e:
            print(f"❌ Неожиданная ошибка для {url}: {e}")
            return {
                'url': url,
                'title': '',
                'content': '',
                'status': 'error',
                'error': str(e)
            }

    def scrape_from_file(self, filename='links.txt'):
        """
        Функция для парсинга всех ссылок из файла и сохранения результата.
        :param filename: Путь к файлу со ссылками
        :type filename: str
        :return: Список спарсенных проектов
        :rtype: list
        """
        projects = []

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            return []

        print(f"Начинаем парсинг {len(urls)} ссылок...")

        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] Парсинг: {url}")

            project = self.scrape_page(url)
            projects.append(project)

            time.sleep(2)

        with open('projects_raw.json', 'w', encoding='utf-8') as f:
            json.dump(projects, f, ensure_ascii=False, indent=2)

        print(f"Сохранено {len(projects)} проектов в projects_raw.json")
        return projects


if __name__ == "__main__":
    scraper = SimpleScraper()
    scraper.scrape_from_file()
