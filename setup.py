"""Скрипт настройки системы Eora Chat Bot."""

import os
import sys
from dotenv import load_dotenv
from scraper import SimpleScraper
from enricher import ProjectEnricher


def check_requirements():
    """
    Функция для проверки необходимых файлов и настроек.
    :return: True если все требования выполнены, False иначе
    :rtype: bool
    """
    print("🔍 Проверка требований...")

    if not os.path.exists('.env'):
        print("❌ Файл .env не найден")
        print("Создайте файл .env с содержимым:")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        return False

    try:
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            print("❌ OPENAI_API_KEY не установлен правильно в .env")
            return False
    except ImportError:
        print("❌ Установите зависимости: pip install -r requirements.txt")
        return False

    if not os.path.exists('links.txt'):
        print("❌ Файл links.txt не найден")
        print("Создайте файл links.txt со ссылками на проекты")
        return False

    print("✅ Все требования выполнены")
    return True


def run_scraping():
    """
    Функция для запуска сбора данных с сайтов.
    :return: True если сбор прошел успешно, False иначе
    :rtype: bool
    """
    print("\n📥 Шаг 1: Сбор данных с сайта...")

    if os.path.exists('projects_raw.json'):
        choice = input("Файл projects_raw.json уже существует. Пересобрать? (y/n): ")
        if choice.lower() != 'y':
            print("✅ Используем существующие данные")
            return True

    try:
        scraper = SimpleScraper()
        projects = scraper.scrape_from_file('links.txt')
        successful = len([p for p in projects if p['status'] == 'success'])
        print(f"✅ Собрано {successful} из {len(projects)} проектов")
        if successful == 0:
            print("❌ Не удалось собрать данные")
            return False
        return True
    except Exception as e:
        print(f"❌ Ошибка сбора данных: {e}")
        return False


def run_enrichment():
    """
    Функция для запуска обогащения данных через OpenAI API.
    :return: True если обогащение прошло успешно, False иначе
    :rtype: bool
    """
    print("\n🧠 Шаг 2: Обогащение данных через OpenAI...")

    if os.path.exists('projects_enriched.json'):
        msg = "Файл projects_enriched.json уже существует. Пересоздать? (y/n): "
        choice = input(msg)
        if choice.lower() != 'y':
            print("✅ Используем существующие обогащенные данные")
            return True

    try:
        enricher = ProjectEnricher()
        enriched_projects = enricher.enrich_all_projects()
        if enriched_projects:
            successful = len([p for p in enriched_projects if 'enriched' in p])
            print(f"✅ Обогащено {successful} проектов")
            return True
        else:
            print("❌ Не удалось обогатить данные")
            return False
    except Exception as e:
        print(f"❌ Ошибка обогащения: {e}")
        print("Возможные причины:")
        print("- Проблемы с OpenAI API")
        print("- Недостаточно средств на аккаунте")
        print("- Неверный API ключ")
        return False


def main():
    """
    Функция для настройки системы.
    :return: True если настройка прошла успешно, False иначе
    :rtype: bool
    """
    print("🚀 Настройка системы Eora Chat Bot")
    print("=" * 40)

    if not check_requirements():
        print("\n❌ Настройка прервана. Исправьте ошибки и запустите снова.")
        return False

    if not run_scraping():
        print("\n❌ Ошибка на этапе сбора данных")
        return False

    if not run_enrichment():
        print("\n❌ Ошибка на этапе обогащения данных")
        print("Можно попробовать запустить без обогащения (будет работать хуже)")
        return False

    print("\n🎉 Настройка завершена!")
    print("\n📁 Созданные файлы:")
    print("  ✅ projects_raw.json - исходные данные")
    print("  ✅ projects_enriched.json - обогащенные данные")

    print("\n🚀 Для запуска чат-бота:")
    print("python chat_bot.py")

    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
