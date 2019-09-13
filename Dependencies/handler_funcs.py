import re

REGEX_DOMAIN = re.compile(r'(https{0,1}:\/\/[a-zA-Z0-9.]{1,})')
REGEX_HTTP_S = re.compile(r'https{0,1}:\/\/')
def get_domain(url):
    """ Получает домен через URL. """
    return REGEX_DOMAIN.findall(url)[0]

def get_path_by_url(url):
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