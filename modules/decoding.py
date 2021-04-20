
'''
Decoding functions
'''

import base64

def de_b64(word):

    word = word.strip()
    b64_bytes = word.encode('ascii')

    msg_bytes = base64.b64decode(b64_bytes)
    msg = msg_bytes.decode('ascii')

    return {'decoded':msg ,'word':word}
