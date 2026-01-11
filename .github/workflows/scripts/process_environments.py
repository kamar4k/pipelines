#!/usr/bin/env python3
import os
import sys
import re
import yaml
from typing import Dict

def process_github_secrets(input_file: str, output_file: str = None) -> None:
    """
    Специализированная версия для GitHub Actions.
    Предполагает, что секреты передаются как переменные окружения.
    """
    # Читаем исходный файл
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Функция для замены секретов
    def replace_secret(match):
        secret_name = match.group(1)
        # Ищем секрет в переменных окружения
        secret_value = os.getenv(secret_name)

        if secret_value:
            return secret_value
        else:
            # Если секрет не найден, проверяем с префиксом (для совместимости)
            secret_value = os.getenv(f"SECRET_{secret_name}") or os.getenv(f"INPUT_{secret_name}")

            if secret_value:
                return secret_value
            else:
                print(f"Warning: Secret '{secret_name}' not found in environment variables")
                return match.group(0)  # Оставляем оригинальный текст

    # Регулярное выражение для поиска ${{ secrets.XXX }}
    pattern = r'\$\{\{\s*secrets\.([A-Za-z0-9_]+)\s*\}\}'

    # Выполняем замену
    processed_content = re.sub(pattern, replace_secret, content)

    # Сохраняем результат
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        print(f"✅ Processed config saved to: {output_file}")
    else:
        # Если выходной файл не указан, выводим в stdout
        print(processed_content)

    return processed_content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python github_secrets_processor.py <input_file> [output_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    process_github_secrets(input_file, output_file)