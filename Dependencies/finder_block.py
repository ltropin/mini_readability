import sys, os
sys.path.insert(0, '')

from bs4 import BeautifulSoup, Tag
import requests
import re
import numpy as np


class FinderMeaningfulContent:
    """
    Класс отвечающий за поиск блока с основным содержимым страницы.
    
    Параметры:
    ----------
    cleaned_content : BeautifulSoup, Tag
        Отчищенная HTML страница или определенный кусок
        HTML страницы.
    tag_list : list
        Список тегов всего HTML-документа.
    """
    # Только значимые символы
    ONLY_STR = re.compile(r'[^a-zA-Zа-яА-Я0-9]{1,}')
    # Множественные переходы на новую строчку
    MANY_NL = re.compile(r'\n{3,}')

    def __init__(self, cleaned_content, tag_list, main_settings):
        self.cleaned_content = BeautifulSoup(str(cleaned_content), 'lxml')
        self.tag_list = tag_list
        self.main_settings = main_settings


    def count_hyper_chars(self, tag_element):
        """ Метрика, возращающая кол-во символов заключенных в ссылке."""
        hyper_char_count = 0
        for tag in tag_element.find_all('a'):
            hyper_char_count += len(str(tag.text).strip())

        return  hyper_char_count

    def count_all_tags(self, tag_element):
        """ Метрика, возращающая кол-во всех тегов. """
        char_count = 0

        for tag in self.tag_list:
            tager = [ct for ct in tag_element.find_all(tag)]
            char_count += len(tager)
        
        return char_count

    def count_chars(self, tag_element):
        """ Метрика, возращающего значимого текста в документе/теге. """
        return len(self.ONLY_STR.sub('', str(tag_element.text)))
    
    def scorer_func(self, chars, tags, hyperchars):
        if chars == 0 or tags == 0:
            return -1
        elif hyperchars == 0:
            return chars / tags
        return (chars / tags) * np.log2(chars / hyperchars)

    def score(self, tag_element):
        """ Вычисление чистой оценки для указанного тега. """
        return self.scorer_func(self.count_chars(tag_element),
                                self.count_all_tags(tag_element),
                                self.count_hyper_chars(tag_element))

    def match_words(self, words):
        """ Преобразует массив слов регулярное выражение. """
        pattern_str = [f'.*{el}.*' for el in words]
        return re.compile('|'.join(pattern_str))

    def find_block_str(self) -> str:
        """ Основной алгоритм поиска главного контента на странице. """
        MAX_EL = None
        MAX_VAL = 0
        for tag_el in self.cleaned_content.recursiveChildGenerator():

            if type(tag_el) == Tag:
                tag_count = self.count_all_tags(tag_el)
                hyper_count = self.count_hyper_chars(tag_el)
                char_count = self.count_chars(tag_el)
                pure_score = self.scorer_func(char_count, tag_count, hyper_count)
                new_score = pure_score
                # Получаем штраф/награду за присутствие значимых слов в тексте. (Arc90)
                for positiveEl in self.main_settings['meaningful_words']:
                    if positiveEl['attr'] in tag_el.attrs:
                        elemAttrs = tag_el.attrs[positiveEl['attr']]
                        # Если у атрибута только одно значение
                        if type(elemAttrs) == str:
                            if self.match_words(positiveEl['words']).match(elemAttrs):
                                new_score += positiveEl['term']
                        # Если у атрибута несколько значений. Например: class='btn btn-warning'
                        elif type(elemAttrs) == list:
                            for elAttr in elemAttrs:
                                if self.match_words(positiveEl['words']).match(elAttr):
                                    new_score += positiveEl['term']
                                    break
                # Награда за длину текста > 10 в параграфе
                for award_tag in self.main_settings['good_tags']:
                    for current_tag in award_tag['tags']:
                      for tag_html in tag_el.find_all(current_tag):
                        if len(tag_html.text) >= award_tag['min_len']:
                            new_score += award_tag['award']  
                # for paragraph in tag_el.find_all('p'):
                #     if len(paragraph.text) >= self.main_settings['paragraph']['min_len']:
                #         new_score += self.main_settings['paragraph']['award']

                # Запоминаем тег с наилучшей оценкой
                if new_score > MAX_VAL and tag_count > 10:
                    MAX_VAL = new_score
                    MAX_EL = tag_el
                    # Debug
                    # print(f'Tag name: {tag_el.name}')
                    # print(f'Char count: {char_count}')
                    # print(f'Tag count: {tag_count}')
                    # print(f'Hyper count: {hyper_count}')
                    # print(f'Pure score: {pure_score}')
                    # print(f'Final score: {new_score}')
                    # print(f'Tag(150): {str(MAX_EL)[:150]}')
                    # print(f'Text(150): {str(MAX_EL.text)[:150]}')

        # print(str(MAX_EL))

        return self.MANY_NL.sub('\n\n', str(MAX_EL.text))