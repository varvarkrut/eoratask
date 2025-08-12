"""Module for enriching project data using OpenAI API."""

import json
import openai
import os
from dotenv import load_dotenv
import time

load_dotenv()


class ProjectEnricher:
    """Класс для обогащения проектов через OpenAI."""

    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            raise Exception("Установите OPENAI_API_KEY в файле .env")

        self.client = openai.OpenAI(api_key=api_key)

    def enrich_project(self, project):
        """
        Функция для обогащения одного проекта через OpenAI API.
        :param project: Словарь с данными проекта
        :type project: dict
        :return: Обогащенный проект с дополнительной информацией
        :rtype: dict
        """
        if project['status'] != 'success' or not project['content']:
            return project

        print(f"Обогащаем: {project['title'][:50]}...")

        prompt = f"""
Проанализируй проект и добавь структурированную информацию:

НАЗВАНИЕ: {project['title']}
КОНТЕНТ: {project['content'][:1000]}

Ответь СТРОГО в JSON формате:
{{
  "industry": "основная индустрия (ритейл, финтех, и т.д.)",
  "solution_type": "тип решения (чат-бот, анализ данных, и т.д.)",
  "technologies": ["технология1", "технология2"],
  "target_audience": "целевая аудитория",
  "company": "название компании-клиента",
  "keywords": ["ключевое слово1", "ключевое слово2", "ключевое слово3"],
  "summary": "краткое описание проекта в 1-2 предложения"
}}

Отвечай только JSON, без дополнительного текста:"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3
            )

            content = response.choices[0].message.content.strip()

            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]

            enrichment = json.loads(content)

            project['enriched'] = enrichment
            project['enriched'] = enrichment
            project['enriched']['created_at'] = time.time()

            return project

        except json.JSONDecodeError as e:
            print(f"Ошибка JSON: {e}")
            project['enriched'] = self._fallback_enrichment(project)
            return project
        except Exception as e:
            print(f"Ошибка API: {e}")
            project['enriched'] = self._fallback_enrichment(project)
            return project

    def _fallback_enrichment(self, project):
        """
        Функция для простого обогащения если AI не сработал.
        :param project: Словарь с данными проекта
        :type project: dict
        :return: Словарь с базовым обогащением
        :rtype: dict
        """
        title_lower = project['title'].lower()
        content_lower = project['content'].lower()

        industry = "общее"
        if any(word in content_lower for word in
               ["магнит", "магазин", "ритейл", "торговля"]):
            industry = "ритейл"
        elif any(word in content_lower for word in ["банк", "финанс", "платеж"]):
            industry = "финтех"

        solution_type = "AI решение"
        if any(word in content_lower for word in ["бот", "чат"]):
            solution_type = "чат-бот"
        elif any(word in content_lower for word in ["поиск", "фото", "изображ"]):
            solution_type = "поиск и рекомендации"

        return {
            "industry": industry,
            "solution_type": solution_type,
            "technologies": ["AI"],
            "target_audience": "бизнес",
            "company": "неизвестно",
            "keywords": title_lower.split()[:3],
            "summary": project['content'][:100] + "...",
            "created_at": time.time()
        }

    def enrich_all_projects(self, input_file='projects_raw.json',
                            output_file='projects_enriched.json'):
        """
        Функция для обогащения всех проектов из входного файла.
        :param input_file: Путь к файлу с исходными проектами
        :type input_file: str
        :param output_file: Путь к файлу для сохранения обогащенных проектов
        :type output_file: str
        :return: Список обогащенных проектов
        :rtype: list
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                projects = json.load(f)
        except FileNotFoundError:
            print(f"Файл {input_file} не найден. Запустите сначала scraper.py")
            return

        print(f"Обогащение {len(projects)} проектов...")

        enriched_projects = []

        for i, project in enumerate(projects, 1):
            print(f"[{i}/{len(projects)}] ", end="")

            enriched_project = self.enrich_project(project)
            enriched_projects.append(enriched_project)

            time.sleep(1)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(enriched_projects, f, ensure_ascii=False, indent=2)

        successful = len([p for p in enriched_projects if 'enriched' in p])
        print(f"\nГотово! Обогащено {successful} из {len(projects)} проектов")
        print(f"Результат сохранен в {output_file}")

        return enriched_projects


if __name__ == "__main__":
    enricher = ProjectEnricher()
    enricher.enrich_all_projects()
