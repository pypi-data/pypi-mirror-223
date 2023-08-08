from json import load
from os import stat

from requests import put, delete, get

from azurly.api import AzureGroupAPI


class BlobNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class AzureStorageAPI(AzureGroupAPI):
    """
    Send resource requests related to Microsoft Storage.
    """
    def __init__(self, subscription_id: str = None, client_id: str = None, client_secret: str = None,
                 tenant_id: str = None, logfile: str = './logs/storage.log'):
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
        super().__init__(subscription_id=subscription_id, client_id=client_id, client_secret=client_secret,
                         tenant_id=tenant_id, logfile=logfile)

    def create_storage_account(self, name: str, template: str, group: str) -> bool:
        """
        Create a storage account.

        Parameters
        ----------
        name: str
            Name of the storage account.
        template: str
            Path to the storage account template (e.g. /path/to/template.json).
        group: str
            Name of the resource group in which the storage account is to be created.

        Returns
        -------
        bool:
            True, the storage account is created.
            False, the storage account is not created, because it exists already.
        """
        # Check if the storage account already exists before continuing.
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Storage/storageAccounts/'
               f'{name}?api-version=2022-09-01')

        if self._check_existence(url=url):
            self._logger.warning(f'{name} already exists.\n')
            return False

        # Get the storage account template.
        with open(template, 'r') as file:
            data = str(load(file))

        # Send the create storage account request.
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Storage/storageAccounts/'
               f'{name}?api-version=2018-02-01')
        response, headers = self._send_request(url=url, request=put, data=data)
        return self._check_status(response=response, headers=headers, resource=name)

    def delete_storage_account(self, name: str, group: str) -> bool:
        """
        Delete a storage account.

        Parameters
        ----------
        name: str
            Name of the storage account.
        group: str
            Name of the resource group in which the storage account is located.

        Returns
        -------
        bool:
            True, the storage account is deleted.
            False, the storage account is not deleted, because it does not exist.
        """
        # Check if the storage account exists before continuing.
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Storage/storageAccounts/'
               f'{name}?api-version=2022-09-01')

        if not self._check_existence(url=url):
            self._logger.warning(f'{name} cannot be deleted, as it does not exist.\n')
            return False

        # Send the delete storage account request.
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Storage/storageAccounts/'
               f'{name}?api-version=2018-02-01')
        response, headers = self._send_request(url=url, request=delete)
        return self._check_status(response=response, headers=headers, resource=name, create=False)

    def create_container(self, name: str, template: str, group: str, storage: str) -> bool:
        """
        Create a container.

        Parameters
        ----------
        name: str
            Name of the container.
        template: str
            Path to the container template (e.g. /path/to/template.json).
        group: str
            Name of the resource group in which the container is to be created.
        storage: str
            Name of the storage account in which the container is to be created.

        Returns
        -------
        bool:
            True: the container is created.
            False, the container is not created, because it exists already.
        """
        # Set the scope for the check existence request.
        scope = f'https://{storage}.blob.core.windows.net'

        # Set the header options for all the requests.
        options = {'x-ms-version': '2020-04-08'}

        # Check if the container already exists before continuing.
        url = f'https://{storage}.blob.core.windows.net/{name}?restype=container'

        if self._check_existence(url=url, scope=scope, options=options):
            self._logger.warning(f'{name} already exists.\n')
            return False

        # Get the container template (this is not checked by Azure!).
        with open(template, 'r') as file:
            data = str(load(file))

        # Send the create container request.
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Storage/storageAccounts/'
               f'{storage}/blobServices/default/containers/{name}?api-version=2022-05-01')
        response, headers = self._send_request(url=url, request=put, data=data)
        return self._check_status(response=response, headers=headers, resource=name)

    def delete_container(self, name: str, group: str, storage: str) -> bool:
        """
        Delete a container.

        Parameters
        ----------
        name: str
            Name of the container.
        group: str
            Name of the resource group in which the container is located.
        storage: str
            Name of the storage account in which the container is located.

        Returns
        -------
        bool:
            True, the container is deleted.
            False, the container is not deleted, because it does not exist.
        """
        # Set the scope for the check existence request.
        scope = f'https://{storage}.blob.core.windows.net'

        # Set the header options for all the requests.
        options = {'x-ms-version': '2020-04-08'}

        # Check if the container exists before continuing.
        url = f'https://{storage}.blob.core.windows.net/{name}?restype=container'

        if not self._check_existence(url=url, scope=scope, options=options):
            self._logger.warning(f'{name} cannot be deleted, as it does not exist.\n')
            return False

        # Send the delete container request.
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Storage/storageAccounts/'
               f'{storage}/blobServices/default/containers/{name}?api-version=2022-05-01')
        response, headers = self._send_request(url=url, request=delete)
        return self._check_status(response=response, headers=headers, resource=name, create=False)

    def upload_blob(self, name: str, file: str, storage: str, container: str, overwrite: bool = True) -> bool:
        """
        Upload a blob.

        Parameters
        ----------
        name: str
            Desired path to the blob in the container (e.g. /path/to/blob.txt).
        file: str
            Path to the local file (e.g. /path/to/file.txt).
        storage: str
            Name of the storage account in which the blob is to be created.
        container: str
            Name of the container in which the blob is to be created.
        overwrite: bool
            Overwrites the blob if it already exists.

        Returns
        -------
        bool:
            True, the blob is created.
            False, the blob already exists and overwriting is disabled.
        """
        # Set the scope for the check existence request.
        scope = f'https://{storage}.blob.core.windows.net'

        # Set the header options for the check existence the request.
        options = {'x-ms-version': '2020-04-08'}

        # Check if the blob already exists and if so, if overwrite is True before continuing.
        url = f'https://{storage}.blob.core.windows.net/{container}/{name}'

        if self._check_existence(url=url, scope=scope, options=options) and not overwrite:
            self._logger.warning(f'{name} already exists in {container} and will not be overwritten.\n')
            return False

        # Set the header options for the upload request.
        blob_size = str(stat(file).st_size)
        options = {'x-ms-blob-type': 'BlockBlob', 'x-ms-version': '2020-04-08', 'Content-Length': blob_size,
                   'Content-Type': 'application/octet-stream'}

        # Get the content from the file.
        with open(file, 'rb') as file:
            data = file.read()

        # Send the upload blob request.
        url = f'https://{storage}.blob.core.windows.net/{container}/{name}'
        _, _ = self._send_request(url=url, request=put, data=data, scope=scope, options=options)

        self._logger.info(f'Uploaded "{name}" from "{file}" to "{container}"!\n')
        return True

    def download_blob(self, name: str, file: str, storage: str, container: str) -> True:
        """
        Download a blob.

        Parameters
        ----------
        name: str
            Path to the blob in the container (e.g. /path/to/blob.txt).
        file: str
            Desired path to the local file (e.g. /path/to/file.txt).
        storage: str
            Name of the storage account in which the blob is located.
        container: str
            Name of the container in which the blob is located.

        Returns
        -------
        True: the blob is downloaded and written to the specified file path.
        """
        # Set the scope for the check existence request.
        scope = f'https://{storage}.blob.core.windows.net'

        # Set the header options for all the requests.
        options = {'x-ms-version': '2020-04-08'}

        # Check if the blob exists before continuing.
        url = f'https://{storage}.blob.core.windows.net/{container}/{name}'

        if not self._check_existence(url=url, scope=scope, options=options):
            message = f'{name} cannot be downloaded, as it does not exist in {container}.'
            self._logger.error(message)
            raise BlobNotFound(message)

        # Send the download blob request to obtain the blob content.
        # Response check is disabled as the blob content might contain the string 'error'.
        url = f'https://{storage}.blob.core.windows.net/{container}/{name}'
        response, _ = self._send_request(url=url, request=get, scope=scope, options=options, check=False)
        blob = response.content

        # Write the blob content to the provided destination path.
        with open(file, 'wb') as file:
            file.write(blob)

        self._logger.info(f'Downloaded "{name}" from "{container}" to "{file}"!\n')
        return True

    def delete_blob(self, name: str, storage: str, container: str) -> bool:
        """
        Delete a blob.

        Parameters
        ----------
        name: str
            Path to the blob in the container (e.g. /path/to/blob.txt).
        storage: str
            Name of the storage account in which the blob is located.
        container: str
            Name of the container in which the blob is located.

        Returns
        -------
        bool:
            True, the blob is deleted.
            False, the blob is not deleted, because it does not exist.
        """
        # Set the scope for the check existence request.
        scope = f'https://{storage}.blob.core.windows.net'

        # Set the header options for all the requests.
        options = {'x-ms-version': '2020-04-08'}

        # Check if the blob exists before continuing.
        url = f'https://{storage}.blob.core.windows.net/{container}/{name}'

        if not self._check_existence(url=url, scope=scope, options=options):
            self._logger.warning(f'{name} cannot be deleted, as it does not exist in {container}.\n')
            return False

        # Send the delete blob request.
        url = f'https://{storage}.blob.core.windows.net/{container}/{name}'
        _, _ = self._send_request(url=url, request=delete, scope=scope, options=options)

        self._logger.info(f'Deleted "{name}" from "{container}"!\n')
        return True
