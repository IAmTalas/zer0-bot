
'''
Decoding functions
'''

import base64
import urllib

all_encoding_algs = ['b64','url']

def de_base64(word):

    word = word.strip()
    b64_bytes = word.encode('ascii')

    msg_bytes = base64.b64decode(b64_bytes)
    msg = msg_bytes.decode('ascii')

    return {'decoded':msg ,'word':word}

def de_url(word):

    decoded_url = urllib.parse.unquote(word)

    return {'decoded':decoded_url ,'word':word}

class Decoder:

    def __init__(self,msg=None):
        self.msg = msg

    def decode(self):
        if self.msg:
            return self.check_alg()

    def check_alg(self):
        encoding_alg_and_string = self.msg.split(' ')
        if len(encoding_alg_and_string) >= 2:
            if encoding_alg_and_string[0] in all_encoding_algs:
                string = " ".join(encoding_alg_and_string[1:])
                alg = encoding_alg_and_string[0]

                if alg == 'b64':
                    return de_base64(string)
                elif alg == 'url':
                    return de_url(string)

        else:
            return None

    def show_help(self):
        temp_msg = "\n\t\t\t".join(all_encoding_algs)
        help_msg = '''
        ```
z! de algorithm your_string
z! de b64 eGVub24=

    available algorithmes :
            {}
        ```
        '''
        help_msg = help_msg.format(temp_msg)
        return help_msg
