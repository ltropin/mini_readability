import sys, os
sys.path.insert(0, '')

from Dependencies.replace_tags import Replacer
from Dependencies.finder_block import FinderMeaningfulContent
from Dependencies.handler_funcs import *
import requests
import textwrap
import json
import random
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
    file_user_agents : list (optional)
        Список user-agen'ов
    file_proxies: dict (optional)
        Словарь проксей
    logging : str (flag) (optional)
        Включить выввод информации в консоль
    save_page : str (flag) (optional)
        Сохранение полученной HTML страницы
    """
    def __init__(self, url, main_settings, format_setings, file_user_agents=None,
                            file_proxies=None, logging=None, save_page=None):
        self.url = url
        self.logging = logging
        self.save_page = save_page
        self.main_settings = main_settings
        self.format_settings = format_setings
        self.domain = get_domain(url)
        self.current_dir = os.getcwd()
        self.user_agents = self.get_user_agents(file_user_agents) 
        self.proxies = self.get_proxies(file_proxies)
        self.url_path, self.url_file = get_path_by_url(url)
    
    def get_proxies(self, file_proxies):
        """ Получение списка проксей. Последующее их использование """
        result_proxies = []
        tempData = None
        if file_proxies != None:
            with open(f'{self.current_dir}/{file_proxies}', 'r') as f:
                tempData = json.load(f)
        # Трансформируем каждый элемент для requests
        if tempData != None:
            for proxy_element in tempData:
                temp_key, temp_value = list(proxy_element.items())[0]
                result_proxies.append({temp_key: f'{temp_key}://{temp_value}'})
        return result_proxies

    
    def get_user_agents(self, file_user_agents):
        """ Получение списка фиктивных User-Agent'ов. """
        result_user_agents = []
        if file_user_agents != None:
            with open(f'{self.current_dir}/{file_user_agents}', 'r') as f:
                result_user_agents = f.readlines()
        
        return result_user_agents


    def save_content(self):
        current_user_agent = random.choice(self.user_agents).replace('\n', '') if len(self.user_agents) > 0 else ''
        proxy = random.choice(self.proxies) if len(self.proxies) > 0 else {}

        htmlResult = None
        # Логгирование
        if self.logging == 'True' or self.logging == 'true':
            print(f'URL: {self.url}')
            print(f'Proxy: {list(proxy.values())[0]}')
            print(f'User-Agent: {current_user_agent}')
        
        htmlResult = requests.get(self.url, headers={'User-Agent': str(current_user_agent)},
                                            proxies=proxy).content
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
        # Путь до конечного файла с новостью
        fullPath = self.current_dir + '\\' + self.url_path + '\\' + self.url_file
        fullPath = fullPath.replace('/', '\\').replace('\\\\', '\\')
        # Путь до HTML страницы
        fullPath_saved = self.current_dir + '\\' + self.url_path + '\\saved_page\\' + self.url_file.replace('.txt', '.html')
        fullPath_saved = fullPath_saved.replace('/', '\\').replace('\\\\', '\\')

        try:
            with open(fullPath, 'w', encoding='utf-8') as f:
                print(placeholder, file=f)

                print(f'Файл сохранен по пути: {fullPath}')
            if self.save_page == 'true' or self.save_page == 'True':
                save_dir = self.current_dir + '\\' + self.url_path + '\\saved_page\\'
                save_dir = save_dir.replace('/', '\\').replace('\\\\', '\\')
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                with open(fullPath_saved, 'w', encoding='utf-8') as f:
                    print(soup.prettify(), file=f)
                    print(f'HTML сохранена по пути: {fullPath_saved}')
        except:
            print('Ошибка при сохранении файла!')
    