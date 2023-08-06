try:
    import requests
    import json
    import Language as Languages
except Exception as e:
    print("Some Modules are Missing {}".format(e))


"""
    This is a language translation module, it will help you to translate any language to any language. 
    This library use Google tranlate to translata to your required language.

    How to used the this library ?
    Here is a demo:

    >>> from PPP_Language_Translation import Translator,Languages 
    >>> # "Languages" contain 188 language all over the world.
    >>> 
    >>> message="Hello, How are you?"
    >>> print(Translator(message,From_language=Languages.English,To_language=Languages.Hindi).translate)
"""

class _Translate(object):
    
    def __init__(self, data,From_language,To_language):
        self._headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        self._base_url = "https://translate.googleapis.com/translate_a/single"
        self.data = data
        self.params = {
            "client": "gtx",
            "sl": From_language,
            "tl": To_language,
            "dt": "t",
            "q": self.data}
    @property
    def get(self):
        try:

            r = requests.get(url=self._base_url,
                             headers=self._headers,
                             params=self.params)

            data = r.json()
            return data[0][0][0]

        except Exception as e :
            print("Failed to Make Response  {}".format(e))


class Translator(object):
    """
        This is a language translation module, it will help you to translate any language to any language. 
        This library use Google tranlate to translata to your required language.

        How to used the this library ?
        Here is a demo:

        >>> from PPP_Language_Translation import Translator,Languages 
        >>> # "Languages" contain 188 language all over the world.
        >>> 
        >>> message="Hello, How are you?"
        >>> print(Translator(message,From_language=Languages.English,To_language=Languages.Hindi).translate)
    """
    def __init__(self, message,From_language=Languages.English,To_language=Languages.Hindi):
        self.message = message
        self.TO,self.FROM=To_language,From_language
        self._crawler  = _Translate(data=self.message,\
                                    From_language=self.FROM,To_language=self.TO)
    @property
    def translate(self):
        return self._crawler.get
   

