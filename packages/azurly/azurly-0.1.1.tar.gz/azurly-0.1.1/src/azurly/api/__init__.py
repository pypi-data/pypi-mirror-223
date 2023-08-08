from json import load
from time import sleep
from os import environ, path, mkdir
from logging import getLogger, INFO, basicConfig, Logger

from requests import put, delete, post, get, Response


class AzureError(Exception):
    def __init__(self, message):
        super().__init__(message)


class AuthenticationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class AzureGroupAPI:
    """
    Parent class of all resource child classes and used to send requests using the Azure API.
    Send resource requests related to Microsoft Management.
    """
    def __init__(self, subscription_id: str = None, client_id: str = None, client_secret: str = None,
                 tenant_id: str = None, logfile: str = './logs/group.log'):
        """
        Parameters
        ----------
        subscription_id: str
            None to use environment variable 'AZURE_SUBSCRIPTION_ID', otherwise as specified.
        client_id: str
            None to use environment variable 'AZURE_CLIENT_ID', otherwise as specified.
        client_secret: str
            None to use environment variable 'AZURE_CLIENT_SECRET', otherwise as specified.
        tenant_id: str
            None to use environment variable 'AZURE_TENANT_ID', otherwise as specified.
        logfile: str
            Path to store the logfile (e.g. /path/to/logfile.txt).
        """
        # Attributes related to the Azure service principal used for authentication.
        try:
            self._subscription_id = environ['AZURE_SUBSCRIPTION_ID'] if subscription_id is None else subscription_id
            self._client_id = environ['AZURE_CLIENT_ID'] if client_id is None else client_id
            self._client_secret = environ['AZURE_CLIENT_SECRET'] if client_secret is None else client_secret
            self._tenant_id = environ['AZURE_TENANT_ID'] if tenant_id is None else tenant_id
            self._get_access_token()
        except KeyError:
            raise AuthenticationError(message='Authentication is not configured, or incorrect!')

        # Attributes related to the Azure subscription.
        self._subscription_scope = 'https://management.azure.com'
        self._subscription_url = f'{self._subscription_scope}/subscriptions/{self._subscription_id}'

        # Attributes related to logging.
        self._logfile = logfile
        self._logger = self._create_logger()

    def _create_logger(self) -> Logger:
        # Create log directory if it does not exist.
        if not path.exists('./logs'):
            mkdir('./logs')

        # Create logger which catches everything up to and including 'info' messages.
        format_message = '%(asctime)s | %(levelname)s | %(message)s'
        format_date = '%d/%m/%Y %H:%M:%S'

        basicConfig(format=format_message, datefmt=format_date, filename=self._logfile, level=INFO, filemode='w')

        return getLogger('azure')

    def _get_access_token(self, scope: str = 'https://management.azure.com') -> str:
        # Send an authentication request based on the service principal credentials.
        url = f'https://login.microsoftonline.com/{self._tenant_id}/oauth2/token'
        data = {'grant_type': 'client_credentials', 'client_id': self._client_id,
                'client_secret': self._client_secret, 'resource': scope}

        return post(url=url, data=data).json()['access_token']

    def _send_request(self, url: str, request: callable, data: str or bytes = None, options: dict = None,
                      scope: str = 'https://management.azure.com', check: bool = True, json=False) -> (Response, dict):
        # To prevent the options variable from mutation.
        if options is None:
            options = {}

        # Get the service principal authentication token.
        access_token = self._get_access_token(scope=scope)

        # Merge the default header with optional items.
        headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
        headers.update(options)

        # Send the data in the request in JSON format if json is True.
        if json:
            response = request(url=url, json=data, headers=headers)
        else:
            response = request(url=url, data=data, headers=headers)

        # Check the response for errors if check is True.
        if check:
            return self._check_response(response=response), headers
        else:
            return response, headers

    def _check_response(self, response: Response) -> Response:
        message = response.content.decode().lower()

        # Check if the message contains an error and raise an AzureError if this is the case.
        if 'error' in message:
            self._logger.error(message)
            raise AzureError(message)
        else:
            return response

    def _check_existence(self, url: str, data: str or dict = None, json: bool = False,
                         scope: str = 'https://management.azure.com', options: dict = None) -> bool:

        response, _ = self._send_request(url=url, data=data, request=get, scope=scope,
                                         options=options, json=json, check=False)
        message = response.content.decode().lower()

        if 'not' in message and ('found' in message or 'exist' in message):
            return False
        else:
            return True

    def _check_status(self, response: Response, headers: dict, resource: str, create: bool = True) -> True:
        message = f'Creating {resource} ...' if create else f'Deleting {resource} ...'
        self._logger.info(message)
        print(message)

        # Wait for resource status code to change from 202 to 200 before continuing.
        while response.status_code == 202:
            url = response.headers['location']
            response = get(url=url, headers=headers)
            sleep(1)

        message = f'{resource} created successfully!\n' if create else f'{resource} deleted successfully!\n'
        self._logger.info(message)
        print(message)

        return True

    def _check_state(self, url: str, resource: str, scope: str = 'https://management.azure.com', options: dict = None,
                     data: str or dict = None, json: bool = False,
                     indices: list = None, condition: str = 'active', create: bool = True) -> True:
        # To prevent the indices variable from mutation.
        if indices is None:
            indices = ['state']

        message = f'Creating {resource} ...' if create else f'Deleting {resource} ...'
        self._logger.info(message)
        print(message)

        while True:
            # In case of successful deletion the response will cause an AzureError as the resource can not be found.
            try:
                response, _ = self._send_request(url=url, request=get, data=data, scope=scope, options=options,
                                                 json=json)
                state = response.json()

                for index in indices:
                    state = state[index]

                # In case of creation, wait until the resource is active before continuing.
                if state.lower() != condition:
                    sleep(1)
                else:
                    break
            # Continue only if the AzureError is caused by the deletion of the resource.
            except AzureError as e:
                if self._check_existence(url=url, data=data, scope=scope, options=options, json=json):
                    raise e
                else:
                    break

        message = f'{resource} created successfully!\n' if create else f'{resource} deleted successfully!\n'
        self._logger.info(message)
        print(message)
        return True

    def create_resource_group(self, name: str, template: str) -> bool:
        """
        Create a resource group.

        Parameters
        ----------
        name: str
            Name of the resource group.
        template: str
            Path to the resource group template (e.g. /path/to/template.json).

        Returns
        -------
        bool:
            True, the resource group is created.
            False, the resource group is not created, because it exists already.
        """
        # Check if the resource group already exists before continuing.
        url = f'{self._subscription_url}/resourcegroups/{name}?api-version=2021-04-01'

        if self._check_existence(url=url):
            self._logger.warning(f'{name} already exists.\n')
            return False

        # Get the resource group template.
        with open(template, 'r') as file:
            data = str(load(file))

        # Send the create resource group request.
        url = f'{self._subscription_url}/resourcegroups/{name}?api-version=2021-04-01'
        response, headers = self._send_request(url=url, request=put, data=data)
        return self._check_status(response=response, headers=headers, resource=name)

    def delete_resource_group(self, name: str) -> bool:
        """
        Delete a resource group.

        Parameters
        ----------
        name: str
            Name of the resource group.

        Returns
        -------
        bool:
            True, the resource group has been deleted.
            False, the resource group has not been deleted, because it does not exist.
        """
        # Check if the resource group exists before continuing.
        url = f'{self._subscription_url}/resourcegroups/{name}?api-version=2021-04-01'

        if not self._check_existence(url=url):
            self._logger.warning(f'{name} cannot be deleted, as it does not exist.\n')
            return False

        # Send the delete resource group request.
        url = f'{self._subscription_url}/resourcegroups/{name}?api-version=2021-04-01'
        response, headers = self._send_request(url=url, request=delete)
        return self._check_status(response=response, headers=headers, resource=name, create=False)
