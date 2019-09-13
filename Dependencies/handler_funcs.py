import re

REGEX_DOMAIN = re.compile(r'(https{0,1}:\/\/[a-zA-Z0-9.]{1,})')
REGEX_HTTP_S = re.compile(r'https{0,1}:\/\/')
REMOVE_NL = re.compile(r'\n{0,}')


def get_domain(url):
    """ Получает домен через URL. """
    return REGEX_DOMAIN.findall(url)[0]


def get_path_by_url(url):
    url = REMOVE_NL.sub('', url)
    path = REGEX_HTTP_S.sub('', url)
    if path[-1] == '/':
        path = path[:-1]
    lastWord = path.split('/')[-1]
    newLaswWord = ''
    if '.' in lastWord:
        newLaswWord = lastWord.split('.')[0] + '.txt'
    else:
        newLaswWord = lastWord + '.txt'
    
    return path.replace(lastWord, ''), newLaswWord


def find_argument(key: str, arguments: list):
    """ Поиск аргумента по ключу """
    for argument in arguments:
        if f'--{key}' in argument and '=' in argument:
            return argument.split('=')[1]
    return None