from typing import List
import random
import json
from Utils.singleton import Singleton


class Translation:
    def __init__(self, translation: str, type: str):
        self.translation = translation
        self.type = type

    def __str__(self):
        return json.dumps({"translation": self.translation, "type": self.type}, ensure_ascii=False)


class Phrase:
    def __init__(self, phrase: str, translation: str):
        self.phrase = phrase
        self.translation = translation

    def __str__(self):
        return json.dumps({"phrase": self.phrase, "translation": self.translation}, ensure_ascii=False)


class Word:
    def __init__(self, word_id: int, word: str, translations: [Translation], phrases: [Phrase]):
        self.word_id = word_id
        self.word = word
        self.translations = translations
        self.phrases = phrases

    def to_dict(self):
        return {
            "word_id": self.word_id,
            "word": self.word,
            "translations": self.translations,
            "phrases": self.phrases
        }

    def __str__(self):
        # return in json
        return json.dumps(self.to_dict(), ensure_ascii=False)


@Singleton
class WordController:
    def __init__(self):
        self.words: List[Word] = []
        self.load_words("CET4")

    def load_words(self, word_file: str):
        with open(f'static/{word_file}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            word_id = 0
            for item in data:
                if not 'phrases' in item:
                    item['phrases'] = []
                word = Word(word_id, item['word'], item['translations'], item['phrases'])
                word_id = word_id + 1
                self.words.append(word)

    def get_random_word(self) -> Word | None:
        if not self.words:
            return None
        return random.choice(self.words)

    def get_word_by_id(self, word_id: int) -> Word | None:
        if word_id < 0 or word_id >= len(self.words):
            return None
        return self.words[word_id]

    def get_all_word_number(self) -> int:
        return len(self.words)


#test
if __name__ == "__main__":
    word_controller = WordController()
    random_word = word_controller.get_random_word()
    print(random_word)
    print(word_controller.get_word_by_id(1))
