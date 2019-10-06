class ShortURL:
    """
    ShortURL: Bijective conversion between natural numbers (IDs) and short strings
    ShortURL.encode() takes an ID and turns it into base62 short string
    ShortURL.decode() takes a short string base62 and turns it into an ID

    Example output:
    123456789 <=> pgK8p
    """

    _alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    _base = len(_alphabet)

    def encode(self, number):
        string = ''
        while(number > 0):
            string = self._alphabet[number % self._base] + string
            number //= self._base
        return string

    def decode(self, string):
        number = 0
        for char in string:
            number = number * self._base + self._alphabet.index(char)
        return number