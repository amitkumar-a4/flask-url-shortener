class ShortURL:
    """
    ShortURL: Bijective conversion between natural numbers (IDs)
    and strings
    ShortURL().encode() takes an ID and turns it into base62 short string
    ShortURL().decode() takes a short string base62 and turns it into an ID
    """

    _alphabet = ('0123456789abcdefghijklmnopqrstuvwxyz'
                 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    _base = len(_alphabet)

    def encode(self, number: int) -> str:
        string = ''
        while(number > 0):
            string = self._alphabet[number % self._base] + string
            number //= self._base
        return string

    def decode(self, string: str) -> str:
        number = 0
        for char in string:
            number = number * self._base + self._alphabet.index(char)
        return number
