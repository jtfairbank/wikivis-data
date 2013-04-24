class Page:
    isNew_map = {
        '0': 'old',
        '1': 'new'
    }

    namespace_map = {
        '0': 'main',
        '1': 'talk',
        '2': 'user',
        '3': 'user_talk',
        '4': 'project',
        '5': 'project_talk',
        '6': 'file',
        '7': 'file_talk',
        '8': 'mediawiki',
        '9': 'mediawiki_talk',
        '10': 'template',
        '11': 'template_talk',
        '12': 'help',
        '13': 'help_talk',
        '14': 'category',
        '15': 'category_talk'
    }

def giveMeaning(data, a_map):
    for key, value in a_map.iteritems():
        if key in data:
            data[value] = data.pop(key)
