import sys, os
sys.path.insert(0, '')

import requests
import textwrap
from bs4 import BeautifulSoup
import re
import json
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
if len(sys.argv) == 2 and '=' in sys.argv[1]:
    argument = sys.argv[1].split('=')
    if 'url' in argument[0] and len(argument[1]) > 4:
        url = argument[1]
# url = 'https://russian.rt.com/russia/article/668008-pensiya-rossiya-rost'
        saver = SaveContent(url, main_json_settings, format_json_settings)
        saver.save_content()
    elif 'file' in argument[0] and len(argument[1]) > 0:
        urls = []
        with open(f"{currentPath}/{argument[1]}", 'r') as f:
            urls = f.readlines()
        for url in urls:
            saver = SaveContent(url, main_json_settings, format_json_settings)
            saver.save_content()
    else:
        raise OSError('Ошибка при передаче параметров!')
else:
    raise OSError('Ошибка при передаче параметров!')