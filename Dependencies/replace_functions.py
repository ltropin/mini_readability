import re
from bs4 import Tag, BeautifulSoup, NavigableString
def replacer(html_soup, formater, url=''):
    """
    Функция `Замена` для определенного тега.
    Параметры:
    ----------
    html_soup : BeautifulSoup, Tag
        Содержимое документа/тега.
    formater : dict
        `tags` -> теги
        `replacer` -> обработка строки 
        P.S. В значении по ключу `replacer` должен содержаться строчка `%s`, которая обозначает
        содержимое тега.
    """
    for tag in formater['tags']:
        # В случае если форматирование происходит содержимого атрибута
        if '->' in tag:
            contentAppend = ''
            attributeKey = tag.split('->')[1]
            tagKey = tag.split('->')[0]
            for htmlElement in html_soup.find_all(tagKey):
                # TODO: Сейчас добавление происходи в конец содержимого.
                # Как таковую структуру нельзя настроить через настройки.
                # Пример: <a href='#'>Link</a> -> Link [#]

                if attributeKey in htmlElement.attrs.keys():
                    attributeContent = ''
                    path = htmlElement.attrs[attributeKey]
     
                    if not('http' in path) and 'full_url' in formater and formater['full_url']:
                        slash = '/' if '/' == url[-1] else ''
                        if len(path) <= 1:
                            path = ''
                        else:
                            path = path[1:] if path[1] == '/' else path
                        attributeContent = url + slash + path
                    else:
                        attributeContent = path
                    urlFormat = formater['replacer'].replace('%s', attributeContent)
                    newContent = htmlElement.text + " " + urlFormat
                    # Заменяем контент вместе с тегом.
                    # if type(htmlElement.string) == Tag and htmlElement.string != None:
                        # htmlElement.string.inser_after(f" {urlFormat}")
                    htmlElement.replaceWith(newContent)
        else:
            for htmlElement in html_soup.find_all(tag):
                htmlElement.replace_with(formater['replacer'].replace('%s', htmlElement.text))
    return html_soup


def end(html_soup, formater):
    """
    Функция `Добавления в конец` для определенного тега.
    Параметры:
    ----------
    html_soup : BeautifulSoup, Tag
        Содержимое документа/тега.
    formater : dict
        `tags` -> теги
        `end` -> обработка строки
    """
    for tag in formater['tags']:
        for htmlElement in html_soup.find_all(tag):
            htmlElement.append(formater['end'])
    
    return html_soup