import sys, os
sys.path.insert(0, '')

from Dependencies.replace_tags import Replacer
from Dependencies.finder_block import FinderMeaningfulContent
from Dependencies.handler_funcs import *
import requests
import textwrap
from bs4 import BeautifulSoup

class SaveContent:
    """
    Модуль для сохранения контента.
    
    Параметры:
    ----------
    url : str
        URL страницы.
    main_settings : dict
        Основные настройки.
    format_settings : dict
        Настройки форматирования тегов.
    """
    def __init__(self, url, main_settings, format_setings):
        self.url = url
        self.main_settings = main_settings
        self.format_settings = format_setings
        self.domain = get_domain(url)
        self.current_dir = os.getcwd()
        self.url_path, self.url_file = get_path_by_url(url)
    
    def save_content(self):
        htmlResult = requests.get(self.url).content
        soup = BeautifulSoup(htmlResult, 'lxml')

        replacer = Replacer(html_soup=soup,
                    main_settings=self.main_settings,
                    format_settings=self.format_settings,
                    url=self.domain)
        
        # Список тегов документа
        list_tags = replacer.get_all_tags()
        # Отчищенный HTML документ
        cleaned = replacer.cleaned_html()
        finder = FinderMeaningfulContent(cleaned_content=cleaned,
                                         tag_list=list_tags,
                                         main_settings=self.main_settings)

        result = finder.find_block_str()
        placeholder = ''

        for sentence in result.split('\n'):
            wraped_sentence = textwrap.wrap(sentence, width=self.format_settings['word_wrap'],
                                                      replace_whitespace=False,
                                                      drop_whitespace=False,
                                                      expand_tabs=False,
                                                      break_long_words=False,
                                                      fix_sentence_endings=True)
            if len(wraped_sentence) == 0:
                placeholder += '\n'
            for subsentence in wraped_sentence:
                placeholder += subsentence + '\n'
        
        # Создаем папку для файла
        if not os.path.exists(self.url_path):
            os.makedirs(self.url_path)

        fullPath = self.current_dir + '/' + self.url_path + '/' + self.url_file
        try:
            with open(fullPath, 'w') as f:
                print(placeholder, file=f)
                print(f'Файл сохранен по пути: {fullPath}')
        except:
            print('Ошибка при сохранении файла!')
    