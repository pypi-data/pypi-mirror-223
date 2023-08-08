from json import load
from time import sleep

from requests import put, delete, post, get

from azurly.api import AzureGroupAPI


class PoolNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class TaskFailed(Exception):
    def __init__(self, message):
        super().__init__(message)


class AzureBatchAPI(AzureGroupAPI):
    """
    Send resource requests related to Microsoft Batch.
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

    def _get_endpoint(self, group: str, batch: str) -> str:
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Batch/batchAccounts/'
               f'{batch}?api-version=2022-10-01')
        response, _ = self._send_request(url=url, request=get)
        return response.json()['properties']['accountEndpoint']

    def create_batch_account(self, name: str, template: str, group: str, storage: str) -> bool:
        """
        Create a storage account.

        Parameters
        ----------
        name: str
            Name of the batch account.
        template: str
            Path to the batch account template (e.g. /path/to/template.json).
        group: str
            Name of the resource group in which the batch account is to be created.
        storage: str
            Name of the storage account used by the batch account to store generated files.

        Returns
        -------
        bool:
            True, the batch account is created.
            False, the batch account is not created, because it exists already.
        """
        # Check if the batch account already exists before continuing.
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Batch/batchAccounts/'
               f'{name}?api-version=2022-10-01')

        if self._check_existence(url=url):
            self._logger.warning(f'{name} already exists.')
            return False

        # Get the batch account template.
        with open(template, 'r') as file:
            data = load(file)

        # Add subscription ID and storage account to template.
        data['properties']['autostorage']['storageAccountId'] = (f'/subscriptions/{self._subscription_id}'
                                                                 f'/resourceGroups/{group}/providers/'
                                                                 f'Microsoft.Storage/storageAccounts/{storage}')
        data = str(data)

        # Send the create batch account request.
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Batch/batchAccounts/'
               f'{name}?api-version=2022-06-01')
        response, headers = self._send_request(url=url, request=put, data=data)
        return self._check_status(response=response, headers=headers, resource=name)

    def delete_batch_account(self, name: str, group: str) -> bool:
        """
        Delete a batch account.

        Parameters
        ----------
        name: str
            Name of the batch account.
        group: str
            Name of the resource group in which the batch account is located.

        Returns
        -------
        bool:
            True, the batch account is deleted.
            False, the batch account is not deleted, because it does not exist.
        """
        # Check if the batch account exists before continuing.
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Batch/batchAccounts/'
               f'{name}?api-version=2022-10-01')

        if not self._check_existence(url=url):
            self._logger.warning(f'{name} cannot be deleted, as it does not exist.\n')
            return False

        # Send the delete batch account request.
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Batch/batchAccounts/'
               f'{name}?api-version=2022-06-01')
        response, headers = self._send_request(url=url, request=delete)
        return self._check_status(response=response, headers=headers, resource=name, create=False)

    def create_pool(self, name: str, template: str, group: str, batch: str) -> bool:
        """
        Create a pool.

        Parameters
        ----------
        name: str
            Name of the pool.
        template: str
            Path to the pool template (e.g. /path/to/template.json).
        group: str
            Name of the resource group in which the pool is to be created.
        batch: str
            Name of the batch account in which the pool is to be created.

        Returns
        -------
        bool:
            True, the pool is created.
            False, the pool is not created, because it exists already.
        """
        # Get the batch account endpoint required for the check existence request.
        endpoint = self._get_endpoint(group=group, batch=batch)

        # Set the scope for the check existence request.
        scope = 'https://batch.core.windows.net'

        # Check if the pool already exists before continuing.
        url = f'https://{endpoint}/pools/{name}?api-version=2022-10-01.16.0'

        if self._check_existence(url=url, scope=scope):
            self._logger.warning(f'{name} already exists.\n')
            return False

        # Get the pool template.
        with open(template, 'r') as file:
            data = str(load(file))

        # Send the create pool request.
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Batch/batchAccounts/'
               f'{batch}/pools/{name}?api-version=2022-06-01')
        response, headers = self._send_request(url=url, request=put, data=data)
        return self._check_status(response=response, headers=headers, resource=name)

    def delete_pool(self, name: str, group: str, batch: str) -> bool:
        """
        Delete a pool.

        Parameters
        ----------
        name: str
            Name of the pool.
        group: str
            Name of the resource group in which the pool is located.
        batch: str
            Name of the batch account in which the pool is located.

        Returns
        -------
        bool:
            True, the pool is deleted.
            False, the pool is not deleted, because it does not exist.
        """
        # Get the batch account endpoint required for the check existence request.
        endpoint = self._get_endpoint(group=group, batch=batch)

        # Set the scope the check existence request.
        scope = 'https://batch.core.windows.net'

        # Check if the pool exists before continuing.
        url = f'https://{endpoint}/pools/{name}?api-version=2022-10-01.16.0'

        if not self._check_existence(url=url, scope=scope):
            self._logger.warning(f'{name} cannot be deleted, as it does not exist.\n')
            return False

        # Send the delete pool request.
        url = (f'{self._subscription_url}/resourceGroups/{group}/providers/Microsoft.Batch/batchAccounts/'
               f'{batch}/pools/{name}?api-version=2022-06-01')
        response, headers = self._send_request(url=url, request=delete)
        return self._check_status(response=response, headers=headers, resource=name, create=False)

    def create_job(self, name: str, path: str, group: str, batch: str, pool: str) -> bool:
        # Get the batch account endpoint required for all the requests.
        endpoint = self._get_endpoint(group=group, batch=batch)

        # Set the scope for all the requests.
        scope = 'https://batch.core.windows.net'

        # Check if the job already exists before continuing.
        url = f'https://{endpoint}/jobs/{name}?api-version=2022-10-01.16.0'

        if self._check_existence(url=url, scope=scope):
            self._logger.warning(f'{name} already exists.\n')
            return False

        # Check if the pool exists and raise a PoolNotFound if this is not the case.
        url = f'https://{endpoint}/pools/{pool}?api-version=2022-10-01.16.0'

        if not self._check_existence(url=url, scope=scope):
            message = f'{pool} required for {name} does not exist.'
            self._logger.error(message)
            raise PoolNotFound(message)

        # Set the header options for the create job request.
        options = {'Content-Type': 'application/json; odata=minimalmetadata'}

        # Get the job template.
        with open(path, 'r') as file:
            data = load(file)

        # Set custom parameters after loading the template.
        data['id'] = name
        data['poolInfo']['poolId'] = pool
        data = str(data)

        # Send the create job request.
        url = f'https://{endpoint}/jobs?api-version=2022-10-01.16.0'
        _, _ = self._send_request(url=url, request=post, data=data, scope=scope, options=options)

        # Wait until the job is created.
        url = f'https://{endpoint}/jobs/{name}?api-version=2022-10-01.16.0'
        return self._check_state(url=url, scope=scope, options=options, resource=name)

    def delete_job(self, name: str, group: str, batch: str) -> bool:
        # Get the batch account endpoint required for all the requests.
        endpoint = self._get_endpoint(group=group, batch=batch)

        # Set the scope for all the requests.
        scope = 'https://batch.core.windows.net'

        # Check if the job exists before continuing.
        url = f'https://{endpoint}/jobs/{name}?api-version=2022-10-01.16.0'

        if not self._check_existence(url=url, scope=scope):
            self._logger.warning(f'{name} cannot be deleted, as it does not exist.\n')
            return False

        # Set the header options for the delete job request.
        options = {'Content-Type': 'application/json; odata=minimalmetadata'}

        # Send the delete job request.
        url = f'https://{endpoint}/jobs/{name}?api-version=2022-10-01.16.0'
        _, _ = self._send_request(url=url, request=delete, scope=scope, options=options)

        # Wait until the job is deleted.
        url = f'https://{endpoint}/jobs/{name}?api-version=2022-10-01.16.0'
        return self._check_state(url=url, scope=scope, options=options, resource=name, create=False)

    def create_task(self, name: str, path: str, command: str, group: str, batch: str, job: str) -> True:
        # Get the batch account endpoint required for all the requests.
        endpoint = self._get_endpoint(group=group, batch=batch)

        # Set scope for all for the requests.
        scope = 'https://batch.core.windows.net'

        # Check if the task exists and delete it if this is the case.
        url = f'https://{endpoint}/jobs/{job}/tasks/{name}?api-version=2022-01-01.15.0'

        if self._check_existence(url=url, scope=scope):
            self._logger.warning(f'{name} already exists and will be deleted.')
            self.delete_task(name=name, group=group, batch=batch, job=job)

        # Set the header options for the create task request.
        options = {'Content-Type': 'application/json; odata=minimalmetadata'}

        # Get the task template.
        with open(path, 'r') as data:
            data = load(data)

        # Set custom parameters after loading the template.
        data['id'] = name
        data['commandLine'] = command
        data = str(data)

        # Send the create request.
        url = f'https://{endpoint}/jobs/{job}/tasks?api-version=2022-10-01.16.0'
        _, _ = self._send_request(url=url, request=post, data=data, scope=scope, options=options)

        # Get the state of the task and wait until it is completed.
        url = f'https://{endpoint}/jobs/{job}/tasks/{name}?api-version=2022-10-01.16.0'

        while True:
            # Response check is disabled as the response might contain the string 'error'.
            response, _ = self._send_request(url=url, request=get, scope=scope, options=options, check=False)
            response = response.json()
            state = response['state'].lower()

            if state == 'completed':
                break
            else:
                sleep(1)

        # Raise a TaskFailed with the failure message if the exit code is 1.
        if response['executionInfo']['exitCode']:
            message = response['executionInfo']['failureInfo']['message']
            self._logger.error(message)
            raise TaskFailed(message)
        else:
            print(f'{name} executed successfully!\n')
            self._logger.info(f'{name} executed successfully!\n')
            return True

    def delete_task(self, name: str, group: str, batch: str, job: str) -> bool:
        # Get the batch account endpoint required for all the requests.
        endpoint = self._get_endpoint(group=group, batch=batch)

        # Set the scope for all the requests.
        scope = 'https://batch.core.windows.net'

        # Check if the task exists before continuing.
        url = f'https://{endpoint}/jobs/{job}/tasks/{name}?api-version=2022-01-01.15.0'

        if not self._check_existence(url=url, scope=scope):
            self._logger.warning(f'{name} cannot be deleted, as it does not exist.\n')
            return False

        # Set the header options for the delete task request.
        options = {'Content-Type': 'application/json; odata=minimalmetadata'}

        # Send the delete task request.
        url = f'https://{endpoint}/jobs/{job}/tasks/{name}?api-version=2022-10-01.16.0'
        response, headers = self._send_request(url=url, request=delete, scope=scope, options=options)
        return self._check_status(response=response, headers=headers, resource=name, create=False)
