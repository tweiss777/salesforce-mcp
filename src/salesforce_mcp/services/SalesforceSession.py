import json
from urllib.parse import urljoin
import requests
import re
from typing import Optional, Dict, Pattern, TypeVar
import logging


T = TypeVar('T')

class SalesforceSession:
    def __init__(self, domain: str,
                 client_id: str,
                 client_secret: str,
                 username: str,
                 password: str,
                 timeout = None):
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self._validate_domain(domain)
        self.url = self._build_endpoint(domain)
        self.session = self._build_instance(base_url=self.url,timeout = timeout)

    @staticmethod
    def _validate_domain(domain) -> None:
        """
        Raise a ValueError if *domain* does not match the DNS‑name pattern.

        Parameters
        ----------
        domain : str
            The string to be validated.

        Raises
        ------
        ValueError
            If the string does not satisfy the regular expression.
        """
        domain_re: Pattern[str] = re.compile(
            r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
            r"(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*"
            r"\.[A-Za-z]{2,63}$"
        )
        if not domain_re.fullmatch(domain):
            raise ValueError(f"Invalid domain name: {domain!r}")

    def _build_instance(
            self,
            base_url: str,
            *,
            headers: Optional[Dict[str, str]] = None,
            timeout: Optional[float] = None,
    ) -> requests.Session:
        """
        Create a reusable requests.Session with optional defaults.

        Parameters
        ----------
        base_url : str
            The root URL for all requests (e.g. "https://bigthink.my.salesforce.com").
        headers : dict, optional
            Default headers to include in every request.
        timeout : float, optional
            Default timeout (seconds) for all requests.

        Returns
        -------
        requests.Session
            Configured session object.
        """
        session = requests.Session()
        session.base_url = base_url.rstrip("/")  # handy attribute

        if headers:
            session.headers.update(headers)

        if timeout is not None:
            session.timeout = timeout

        return session

    def _build_endpoint(self, domain):
        '''
        build endpoint url
        :return: endpoint url
        '''
        return f"https://{domain}/"

    def authenticate(self) -> str:
        '''
           Authenticate with Salesforce using oauth.
           :return sf token
        '''
        # invoke self.post
        auth_endpoint = "/services/oauth2/token"
        url = urljoin(self.url + "/", auth_endpoint.lstrip("/"))
        form_data: Dict[str,str] = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password
        }
        response =  self.session.post(url, data=form_data)
        response.raise_for_status()
        token_data = response.json()
        return token_data["access_token"]

    def create(self, path: str, body):
        '''
            create a record
        '''
        try:

            full_url = self.url + path
            token = self.authenticate()
            headers: Dict[str,str] = {
                "Authorization": f"Bearer {token}"
            }
            response = self.session.post(full_url, json=body, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            return response_data
        except Exception as err:
            logging.error("error")
            logging.error(err)
            raise err



    def update(self, path: str, id: str, body):

        '''
            update a record
        '''
        full_url = self.url + path
        try:

            token = self.authenticate()
            headers: Dict[str,str] = {
                "Authorization": f"Bearer {token}"
            }
            full_url+= id
            response = self.session.patch(full_url, json=body, headers=headers)
            response.raise_for_status()
            response_data = {"success": True } if response.status_code == 204 else response.json()
            return response_data
        except Exception as err:
            logging.error("error")
            logging.error(err)
            raise


    def delete(self, path):
        '''
           delete a record
        '''
        try:
            full_url = self.url + path
            token = self.authenticate()
            headers: Dict[str,str] = {
                "Authorization": f"Bearer {token}"
            }

            response = self.session.delete(full_url, headers=headers)
            response.raise_for_status()
            response_data = {"success": True } if response.status_code == 204 else response.json()
            return response_data
        except Exception as  err:
            logging.error("error")
            logging.error(err)
            raise err


    def get(self, path):
        full_url = self.url + path
        try:
            token = self.authenticate()
            headers: Dict[str,str] = {
                "Authorization": f"Bearer {token}"
            }
            response =  self.session.get(full_url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            return response_data
        except Exception as err:
            logging.error("error")
            logging.error(err)
            raise err


