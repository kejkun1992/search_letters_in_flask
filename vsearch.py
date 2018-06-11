def search4vowels(phrase: str) -> set:
    '''Return vowels found in phrase'''
    vowels = set('aieou')
    return vowels.intersection(set(phrase))
