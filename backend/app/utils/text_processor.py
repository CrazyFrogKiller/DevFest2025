import re
from typing import List, Tuple

class TextProcessor:
    """Utility class for text processing"""

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text - remove ONLY excessive spaces, preserve everything else"""
        if not text:
            return ""

        # ТОЛЬКО убираем множественные пробелы между словами
        text = re.sub(r' {2,}', ' ', text)

        # Убираем пробелы в начале/конце строк
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)

        # Убираем более 2 переводов строк подряд
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Общий trim
        text = text.strip()

        return text

    @staticmethod
    def count_tokens(text: str) -> int:
        """Estimate token count"""
        if not text:
            return 0

        words = len(text.split())
        chars = len(text)

        tokens_by_chars = chars / 3.8
        tokens_by_words = words * 1.3

        return int((tokens_by_chars + tokens_by_words) / 2)

    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """Split text into sentences"""
        if not text:
            return []

        # Защита сокращений
        text = re.sub(r'\bи\s+т\.д\.', 'и_т_д', text)
        text = re.sub(r'\bт\.е\.', 'т_е', text)
        text = re.sub(r'\bи\s+т\.п\.', 'и_т_п', text)
        text = re.sub(r'\b(Mr|Mrs|Dr|Ms|Sr|Jr)\.', r'\1<DOT>', text)

        sentences = re.split(r'(?<=[.!?])\s+(?=[А-ЯA-Z])', text)

        sentences = [
            s.replace('и_т_д', 'и т.д.')
             .replace('т_е', 'т.е.')
             .replace('и_т_п', 'и т.п.')
             .replace('<DOT>', '.')
             .strip()
            for s in sentences if s.strip()
        ]

        return sentences

    @staticmethod
    def smart_chunk_text(
        text: str,
        chunk_size: int = 800,
        overlap: int = 200
    ) -> List[Tuple[str, int, int]]:
        """Smart chunking with sentence boundary detection"""
        if not text:
            return []

        # Минимальная очистка
        text = TextProcessor.clean_text(text)

        avg_chars_per_token = 4
        chunk_chars = max(400, chunk_size * avg_chars_per_token)
        overlap_chars = max(100, int(overlap * avg_chars_per_token))

        chunks: List[Tuple[str, int, int]] = []
        text_len = len(text)
        start = 0

        while start < text_len:
            end = start + chunk_chars

            if end >= text_len:
                chunk_text = text[start:text_len].strip()
                if chunk_text:
                    chunks.append((chunk_text, start, text_len))
                break

            window = text[start:end]
            best_boundary = -1

            # Параграф
            para_break = window.rfind('\n\n')
            if para_break > int(0.3 * chunk_chars):
                best_boundary = para_break + 2

            # Конец предложения
            if best_boundary == -1:
                for match in re.finditer(r'[.!?]\s+(?=[А-ЯA-Z])', window):
                    pos = match.end()
                    if pos > int(0.4 * chunk_chars):
                        best_boundary = pos
                        break

            # Знаки препинания
            if best_boundary == -1:
                for char in ['. ', '! ', '? ', '.\n', '!\n', '?\n', '; ', ';\n']:
                    pos = window.rfind(char)
                    if pos > int(0.5 * chunk_chars):
                        best_boundary = pos + len(char)
                        break

            # Перевод строки
            if best_boundary == -1:
                pos = window.rfind('\n')
                if pos > int(0.6 * chunk_chars):
                    best_boundary = pos + 1

            # Пробел
            if best_boundary == -1:
                pos = window.rfind(' ')
                if pos > int(0.7 * chunk_chars):
                    best_boundary = pos + 1

            if best_boundary > 0:
                end = start + best_boundary

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append((chunk_text, start, end))

            start = end - overlap_chars

            if start <= (chunks[-1][1] if chunks else 0):
                start = end

        return chunks