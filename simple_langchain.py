"""Module for simple LangChain RAG system."""

import json
import os
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.prompts import PromptTemplate

load_dotenv()


class SimpleLangChain:
    """LangChain RAG система."""

    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            raise Exception("Установите OPENAI_API_KEY в файле .env")

        self.vectorstore = None
        self.qa = None

    def setup(self, json_file='projects_enriched.json'):
        """
        Функция для настройки RAG системы из JSON файла с проектами.
        :param json_file: Путь к JSON файлу с обогащенными проектами
        :type json_file: str
        """
        print("📚 Загрузка данных...")

        with open(json_file, 'r', encoding='utf-8') as f:
            projects = json.load(f)

        documents = []
        for project in projects:
            if project['status'] == 'success':
                text = f"{project['title']}\n{project['content']}"

                if 'enriched' in project:
                    enriched = project['enriched']
                    text += f"\nИндустрия: {enriched.get('industry', '')}"
                    text += f"\nКлиент: {enriched.get('company', '')}"

                metadata = {
                    'url': project['url'],
                    'title': project['title']
                }
                doc = Document(page_content=text, metadata=metadata)
                documents.append(doc)

        print(f"📄 Создано {len(documents)} документов")

        print("🧠 Создание векторов...")
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=OpenAIEmbeddings(),
            persist_directory='./chroma'
        )

        prompt_template = """Ты - консультант компании. Отвечай на вопросы о проектах.

ПРАВИЛА ОТВЕТА:
- Всегда приводи КОНКРЕТНЫЕ примеры проектов из контекста
- Обязательно указывай названия КОМПАНИЙ-КЛИЕНТОВ (Магнит, KazanExpress, Lamoda и др.)
- Давай короткий, но информативный ответ в формате "Мы делали X для компании Y"
- Если в контексте нет релевантных примеров, честно скажи об этом

ПРИМЕРЫ ХОРОШИХ ОТВЕТОВ:
ВОПРОС: Что вы можете сделать для ритейлеров?
ОТВЕТ: Мы разрабатывали HR-бота для Магнита и систему поиска по изображениям для KazanExpress.


Контекст проектов:
{context}

Вопрос: {question}

Конкретный ответ с примерами:"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        self.qa = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0.7),
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

    def ask(self, question):
        """
        Функция для обработки вопроса к RAG системе и возвращения ответа.
        :param question: Вопрос пользователя
        :type question: str
        :return: Ответ на основе контекста проектов
        :rtype: str
        """
        if not self.qa:
            return "Система не настроена. Запустите setup()."

        result = self.qa.invoke({"query": question})
        answer = result['result']
        return answer
