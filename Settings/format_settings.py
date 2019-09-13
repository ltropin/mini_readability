FORMAT_SETTINGS = {
    'tag_format': [
        # Title
        {
            'tags': ['h1', 'h2'],
            'replacer': '*** %s\n'
        },
        # Links
        {
            'tags': ['a->href'],
            'replacer': '[%s]',
            'full_url': True
        },
        # Img
        {
            'tags': ['img->src'],
            'replacer': '[IMG] %s [/IMG]'
        },
        # Paragraph
        {
            'tags': ['p'],
            'end': '\n\n'
        },
        # New Line
        {
            'tags': ['div'],
            'end': '\n'
        },
        # Date
        {
            'tags': ['time'],
            'replacer': 'Дата: %s'
        },
    ],
    'word_wrap': 80
}