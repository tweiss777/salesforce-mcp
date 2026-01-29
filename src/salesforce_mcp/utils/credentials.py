from dataclasses import dataclass
import os

@dataclass
class Credentials:
    url: str
    client_id: str
    client_secret: str
    username: str
    password: str




def get_credentials() -> Credentials:
    '''
        helper function to get the credentials
    :return: Credential object
    '''
    return Credentials(
        url=os.environ["URL"],
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        username=os.environ["USERNAME"],
        password=os.environ["PASSWORD"],
    )
