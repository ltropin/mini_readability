import sys, os
sys.path.insert(0, '')
from bs4 import BeautifulSoup, Tag, Comment
from Dependencies.replace_functions import *
# from Main.mainSettings import MAIN_SETTINGS
# from settings import FORMAT_SETTINGS

class Replacer:
    """ Replacer
        =====

        Класс, отвечающий за замену/удаление/добавление определенных строк к содержимому тега.
        
        Параметры:
        ------------
        html_soup : BeautifulSoup
            Полное или главное содержимое страницы.

        main_settings : dict
            Основные настройки обработчика страниц.
        
        format_settings : dict
            Словарь настроек форматирования тегов
        url : str
            URL адрес сайта.
    """


    def __init__(self, html_soup, main_settings, format_settings, url):
        self.html_soup = html_soup
        self.main_settings = main_settings
        self.format_settings = format_settings
        self.url = url


    def cleaned_html(self):
        """
        Проводит полностью отчистку документа.
        Возращает отчищенный документ.

        Применяет функции:
        ------------------
        1. Выделение тега через селектор `body`
        2. remove_trash_tags
        3. remove_empty_strings
        4. formate_html
        """
        self.html_soup = self.html_soup.select_one('body')
        self.html_soup = self.remove_trash_tags()
        self.html_soup = self.remove_min_size()
        self.html_soup = self.remove_empty_strings()
        self.html_soup = self.formate_html()

        return self.html_soup


    def remove_trash_tags(self):
        """
        Удаляет из `self.html_soup` теги, которые захламляют документ
        и возращает отчищенный документ.

        Параметры:
        ----------
        trash_tags : list
            Список тего, которые необходимо удалить.
        Пример:
        -------
          >>> trash_tags = ['div', 'b', 'span']
        """

        for tag in self.main_settings['trash_tags']:
            for el in self.html_soup.find_all(tag):
                el.extract()
        
        return self.html_soup


    def get_all_tags(self):
        """ Возращает список всех тегов (без повторения) из документа `self.html_soup` """
        result = set()
        for tag in self.html_soup.find_all(True):
            result.add(str(tag.name))

        return list(result)


    def remove_empty_strings(self):
        """
        Удаляет теги с пустым текстом и возращает отчищенный документ.
        Так же удаляет комментарии.
        """
        for tag in self.html_soup.find_all(True):
            if type(tag) == Tag and len(str(tag.text.strip())) == 0:
                tag.extract()
            if type(tag) == Comment:
                tag.extract()
        
        return self.html_soup

    def remove_min_size(self):
        """
        Удаляет теги, где число потомков меньше `max_childrens`
        и максимальная длина меньше `max_len`
        """
        for tagElement in self.main_settings['minimal_remove']:
            for tag_html in self.html_soup.find_all(tagElement['tag']):
                if len(tag_html.text) < tagElement['max_len'] and len(tag_html) < tagElement['max_childrens']:
                    tag_html.extract()
        
        return self.html_soup

    def formate_html(self):
        """ Применяет последовательное форматирование для элементов."""
        for formatEl in self.format_settings['tag_format']:
            if 'replacer' in formatEl:
                self.html_soup = replacer(self.html_soup, formatEl, self.url)
            elif 'end' in formatEl:
                self.html_soup = end(self.html_soup, formatEl)
        
        return self.html_soup


    def __str__(self):
        return str(self.html_soup)