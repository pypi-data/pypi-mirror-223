import json
from requests import post
from .utils import generate_random_string
from .exceptions import Error

class Account:
    headers = {'Content-Type': 'application/json'}
    username: str = None
    prefix: str = None

    def __init__(self,username: str = None,prefix: str = 'mail'):
        if username is None:
            username = generate_random_string()
        elif not username.isalnum():
            raise Error('The username can only be letters and numbers.')
        if not prefix.isalnum():
            raise Error('The prefix can only be letters and numbers.')
        self.username = username
        self.prefix = prefix
        self.address = username+'@'+prefix+'.iemail.eu.org'
        
    def get_message(self, latest=0):
        assert latest >= 0, IndexError('Latest must be >= 0')
        r = post('https://api.iemail.eu.org/',headers=self.headers,data=json.dumps({'username': self.username,'prefix': self.prefix}),timeout=10)
        result = r.json()
        if len(result) <= latest:
            raise IndexError(f'No message found! There are only {len(result)} messages.')
        return result[latest]

    def get_messages(self):
        r = post('https://api.iemail.eu.org/',headers=self.headers,data=json.dumps({'username': self.username,'prefix': self.prefix}),timeout=10)
        return r.json()

if __name__ == '__main__':
    ...