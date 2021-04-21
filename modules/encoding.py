
'''
Encoding functions
'''

import base64

all_encoding_algs = ['b64']

def en_base64(word):

    word = word.strip()
    msg_bytes = word.encode('ascii')

    b64_bytes = base64.b64encode(msg_bytes)
    b64_msg = b64_bytes.decode('ascii')

    return {'encoded':b64_msg ,'word':word}

class Encoder:

    def __init__(self,msg=None):
        self.msg = msg

    def encode(self):
        if self.msg:
            return self.check_alg()

    def check_alg(self):
        encoding_alg_and_string = self.msg.split(' ')
        if len(encoding_alg_and_string) == 2:
            if encoding_alg_and_string[0] in all_encoding_algs :
                alg = encoding_alg_and_string[0]
                string = encoding_alg_and_string[1]

                if alg == 'b64':
                    return en_base64(string)

        else:
            return None

    def show_help(self):
        temp_msg = "\n\t\t\t".join(all_encoding_algs)
        help_msg = '''
        ```
z! en algorithm your_string
z! en b64 xenon

    available algorithmes :
            {}
        ```
        '''
        help_msg = help_msg.format(temp_msg)
        return help_msg
