from rag.services.llm_service import LLMService


def main():
    llm_service = LLMService()

    prompt = """
You are a helpful assistant.

Explain what a relational database is in
three short sentences.
"""

    response = llm_service.generate(prompt)

    print()
    print("=" * 70)
    print("LLM RESPONSE")
    print("=" * 70)
    print(response)
    print("=" * 70)


if __name__ == "__main__":
    main()