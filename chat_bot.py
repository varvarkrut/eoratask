"""Простой чат-бот Eora с RAG системой."""

from simple_langchain import SimpleLangChain
import os


def main():
    """
    Функция для запуска чат-бота Eora с RAG системой.
    """
    print("🤖 Простой LangChain чат-бот Eora!")
    print("Введите 'exit' для выхода.\n")

    if not os.path.exists('.env'):
        print("❌ Создайте файл .env с вашим OpenAI API ключом:")
        print("OPENAI_API_KEY=your_api_key_here\n")
        return

    try:
        print("🔄 Настройка LangChain...")
        rag = SimpleLangChain()
        rag.setup()
        print("✅ Готово!\n")

    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        print("\nВозможные причины:")
        print("1. Неверный API ключ в .env файле")
        print("2. Отсутствуют обогащенные данные (запустите setup.py)")
        print("3. Проблемы с интернет-соединением\n")
        return

    print("💡 Примеры вопросов:")
    examples = [
        "Что вы можете сделать для ритейлеров?",
        "Есть ли опыт с HR автоматизацией?",
        "Работали с поиском по изображениям?",
        "Какие решения для банков?"
    ]

    for example in examples:
        print(f"   • {example}")
    print()

    while True:
        try:
            question = input("❓ Ваш вопрос: ").strip()

            if question.lower() in ['exit', 'quit', 'выход', 'q']:
                print("👋 Спасибо за обращение! До свидания!")
                break

            if not question:
                continue

            print("🤔 Думаю...")
            answer = rag.ask(question)

            print("\n" + "=" * 50)
            print(answer)
            print("=" * 50 + "\n")

        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            break

        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")
            print("Попробуйте еще раз или напишите 'quit' для выхода\n")


if __name__ == "__main__":
    main()
