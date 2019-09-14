import sys, os
sys.path.insert(0, '')

import requests
import textwrap
from bs4 import BeautifulSoup
import re
import json
import csv
from Dependencies.replace_tags import Replacer
from Dependencies.finder_block import FinderMeaningfulContent
from Dependencies.save_file import SaveContent
from Settings.format_settings import FORMAT_SETTINGS
from Settings.main_settings import MAIN_SETTINGS
from Dependencies.handler_funcs import *

currentPath = os.getcwd()

main_json_settings = None
format_json_settings = None
# Создание директории
if not os.path.exists(f'{currentPath}\\settings'):
    os.makedirs(f'{currentPath}\\settings')
# Создание/Использование настроек
try:
    with open(f'{currentPath}\\settings\\main_settings.json', 'r') as f:
        main_json_settings = json.load(f)
except:
    with open(f'{currentPath}\\settings\\main_settings.json', 'w', encoding='utf-8') as f:
        json.dump(MAIN_SETTINGS, f, indent=4)
        print(f'Файл с главными настройками сохранен по пути: \\settings\\main_settings.json')
    # Устанавливаем дефолтные настройки
    main_json_settings = MAIN_SETTINGS

try:
    with open(f'{currentPath}\\settings\\format_settings.json', 'r') as f:
        format_json_settings = json.load(f)
except:
    with open(f'{currentPath}\\settings\\format_settings.json', 'w', encoding='utf-8') as f:
        json.dump(FORMAT_SETTINGS, f, indent=4)
        print(f'Файл с главными настройками сохранен по пути: \\settings\\format_settings.json')
    # Устанавливаем дефолтные настройки
    format_json_settings = FORMAT_SETTINGS

# Работа с контентом
if len(sys.argv) >= 2:

    user_agents = find_argument('user-agent-txt', sys.argv)
    proxies = find_argument('proxy-json', sys.argv)
    file_txt = find_argument('file', sys.argv)
    url = find_argument('url', sys.argv)
    logging = find_argument('logging', sys.argv)
    save_page = find_argument('save-page', sys.argv)

    if url != None:
        saver = SaveContent(url=url,
                            main_settings=main_json_settings,
                            format_setings=format_json_settings,
                            file_user_agents=user_agents,
                            file_proxies=proxies,
                            logging=logging,
                            save_page=save_page)
        saver.save_content()
    elif file_txt != None:
        urls = []
        with open(f"{currentPath}/{file_txt}", 'r') as f:
            urls = f.readlines()
        for url_txt in urls:
            sess = requests.session()
            saver = SaveContent(url=url_txt.replace('\n', ''),
                                main_settings=main_json_settings,
                                format_setings=format_json_settings,
                                file_user_agents=user_agents,
                                file_proxies=proxies,
                                requester=sess,
                                logging=logging,
                                save_page=save_page)
            saver.save_content()
    else:
        raise OSError('Ошибка при передаче параметров!')
else:
    raise OSError('Ошибка при передаче параметров!')