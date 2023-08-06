def roman_to_unicode_nepali(roman_text):
    nepali_mapping = {
        'a': 'अ', 'aa': 'आ', 'i': 'इ', 'ii': 'ई', 'u': 'उ', 'uu': 'ऊ',
        'e': 'ए', 'ai': 'ऐ', 'o': 'ओ', 'au': 'औ', 'k': 'क', 'kh': 'ख',
        'g': 'ग', 'gh': 'घ', 'ng': 'ङ', 'ch': 'च', 'chh': 'छ', 'j': 'ज',
        'jh': 'झ', 'ny': 'ञ', 't': 'ट', 'th': 'ठ', 'd': 'ड', 'dh': 'ढ',
        'n': 'ण', 't': 'त', 'th': 'थ', 'd': 'द', 'dh': 'ध', 'n': 'न',
        'p': 'प', 'ph': 'फ', 'b': 'ब', 'bh': 'भ', 'm': 'म', 'y': 'य',
        'r': 'र', 'l': 'ल', 'v': 'व', 'sh': 'श', 'shh': 'ष', 's': 'स',
        'h': 'ह', 'ksh': 'क्ष', 'tr': 'त्र', 'gy': 'ज्ञ', '0': '०',
        '1': '१', '2': '२', '3': '३', '4': '४', '5': '५', '6': '६',
        '7': '७', '8': '८', '9': '९',
    }

    words = roman_text.split()
    nepali_text = ""

    for word in words:
        nepali_word = ""
        idx = 0
        while idx < len(word):
            if word[idx:idx+2] in nepali_mapping:
                nepali_word += nepali_mapping[word[idx:idx+2]]
                idx += 2
            elif word[idx] in nepali_mapping:
                nepali_word += nepali_mapping[word[idx]]
                idx += 1
            else:
                nepali_word += word[idx]
                idx += 1

        nepali_text += nepali_word + " "

    return nepali_text.strip()
