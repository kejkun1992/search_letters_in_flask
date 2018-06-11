def search4vowels(phrase: str) -> set:
    '''Return vowels found in phrase'''
    vowels = set('aieou')
    return vowels.intersection(set(phrase))


def search4letters(phrase: str, letters: str='aieou') -> set:
    '''Return letters found in phrase'''
    return set(letters).intersection(set(phrase))
