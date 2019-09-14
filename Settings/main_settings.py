MAIN_SETTINGS = {
    # Теги подлежащие к обязательному удалению.
    'trash_tags': ['script', 'noscript', 'style', 'meta', 'footer', 'code', 'link', 'aside', 'iframe', 'svg'],
    # Награды/Штрафы за теги
    'good_tags': [
        {
            'tags': ['p'],
            'min_len': 10,
            'award': 10
        },
        {
            'tags': ['h1', 'h2'],
            'min_len': 10,
            'award': 250
        }
    ],
    'minimal_remove': [
        {
            'tag': 'td',
            'max_len': 10,
            'max_childrens': 2
        },
        {
            'tag': 'tr',
            'max_len': 10,
            'max_childrens': 2
        },
        {
            'tag': 'div',
            'max_len': 10,
            'max_childrens': 2
        },
        {
            'tag': 'table',
            'max_len': 10,
            'max_childrens': 2
        }
        
    ],
    # Награды за присутствие определенных слов в атрибуте
    'meaningful_words': [
        {
            'attr': 'class',
            'words': ['post', 'entry', 'content', 'text', 'body', 'news', 'article'],
            'term': 25
        },
        {
            'attr': 'id',
            'words': ['post', 'entry', 'content', 'text', 'body', 'news'],
            'term': 25
        },
        {
            'attr': 'class',
            'words': ['comment', 'foot', 'footer', 'navbar', 'header', 'Ad'],
            'term': -25
        },
        {
            'attr': 'id',
            'words': ['comment', 'foot', 'footer', 'navbar', 'header', 'Ad'],
            'term': -25
        },
    ]
}