import importlib
from typing import Any

from fastapi import HTTPException, Request


class Translator:

    def __init__(self, lang: str, word: str = ''):
        self._lang = lang
        self._word = word

    def translate(
        self,
        word_to_translate: str,
        key_word: str | None = None,
        **kwargs: dict[str, Any]
    ) -> str:
        """
        translater.translate(f'main_request.{key}')
        translater.main_request(key)
        translater.main_request.help()

        Для форматирования теста перевода
        translater.translate(f'main_request.{key}', foo='hi')
        translater.main_request(key, foo='hi')
        translater.main_request.help(foo='hi')

        Для вложенных словарей
        translater.translate(f'main_request.{key}.response.error')
        translater.main_request(f'{key}.response.error')
        translater.main_request.help.response.error()
        """
        if key_word:
            word_to_translate = word_to_translate + '.' + key_word
        path_to_word = word_to_translate.split('.')
        word = path_to_word[-1]
        dict_translate = path_to_word[0]

        locale_module = importlib.import_module(f'panels_project.languages.{self._lang}.translate')  # noqa

        translation_dict = eval(f'locale_module.{dict_translate}')
        if len(path_to_word) > 2:
            for dict_ in path_to_word[1:-1]:
                translation_dict = translation_dict[dict_]

        translation_word = translation_dict.get(word, None)
        if translation_word is None:
            raise HTTPException(status_code=500, detail=f'Key {word} not found in {self._lang} locale')

        if kwargs.keys():
            translation_word = translation_word.format(**kwargs)
        return translation_word

    def __getattr__(self, word):
        return Translator(
            self._lang,
            (self._word + '.' if self._word else '') + word
        )

    def __call__(self, key_word: str | None = None, **kwargs: dict[str, Any]) -> Any:
        if self._word is None:
            raise HTTPException(status_code=500, detail='word_to_translate is None')
        return self.translate(self._word, key_word, **kwargs)


def get_translate(request: Request):
    return Translator(request.state.locale)
