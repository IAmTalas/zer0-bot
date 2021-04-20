
'''
Encoding functions
'''

import base64

def en_b64(word):

    word = word.strip()
    msg_bytes = word.encode('ascii')

    b64_bytes = base64.b64encode(msg_bytes)
    b64_msg = b64_bytes.decode('ascii')

    return {'encoded':b64_msg ,'word':word}
