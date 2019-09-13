MAIN_SETTINGS = {
    # Предположительно если в class или id содержится такие слова то такие теги c содержимым нужно удалить.
    'delete_cid': ['comment', 'foot', 'footer', 'navbar', 'header'],
    # Теги подлежащие к обязательному удалению.
    'trash_tags': ['script', 'noscript', 'style', 'meta', 'footer', 'code', 'link', 'aside', 'iframe', 'svg'],
    # Награды/Штрафы за теги
    'paragraph': {
        'min_len': 10,
        'award': 10
    },
    'meaningful_words': [
        {
            'tag': 'class',
            'words': ['post', 'entry', 'content', 'text', 'body', 'news'],
            'term': 100
        },
        {
            'tag': 'id',
            'words': ['post', 'entry', 'content', 'text', 'body', 'news'],
            'term': 75
        },
        {
            'tag': 'class',
            'words': ['comment', 'foot', 'footer', 'navbar', 'header', 'Ad'],
            'term': -1000
        },
        {
            'tag': 'id',
            'words': ['comment', 'foot', 'footer', 'navbar', 'header', 'Ad'],
            'term': -1000
        },
    ]
}