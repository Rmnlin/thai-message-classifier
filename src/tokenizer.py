from pythainlp.tokenize import word_tokenize


def thai_tokenize(text):
    return word_tokenize(text, engine="newmm", keep_whitespace=False)
