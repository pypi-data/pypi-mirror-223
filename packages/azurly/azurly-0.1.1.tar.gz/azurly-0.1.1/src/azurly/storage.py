from os import path

from azurly import _AzureResource, AzureGroup
from azurly.api.storage import AzureStorageAPI


class AzureStorage(_AzureResource):
    """
    Deploy a blob storage account.
    """
    def __init__(self, name: str, group: AzureGroup):
        """
        Parameters
        ----------
        name: str
            Name of the blob storage account.
        group: AzureGroup
            Resource group in which the blob storage account is to be deployed.
        """
        super().__init__(name=name, group=group)

        self._template = None
        self._storage = AzureStorageAPI()

    def _build_template(self) -> dict:
        template = {
                      "location": self._group._region,
                      "kind": "blobstorage",
                      "sku": {
                        "name": "standard_LRS"},
                      "properties": {
                        "accessTier": "hot",
                        "deleteRetentionPolicy": "false"
                      }
                    }
        return template

    def _deploy_api(self) -> bool:
        return self._storage.create_storage_account(name=self._name, group=self._group._name, template=self._template)

    def _destroy_api(self) -> bool:
        return self._storage.delete_storage_account(name=self._name, group=self._group._name)


class AzureContainer(_AzureResource):
    """
    Deploy a container.
    """
    def __init__(self, name: str, group: AzureGroup, storage: AzureStorage):
        """
        Parameters
        ----------
        name: str
            Name of the container.
        group: AzureGroup
            Resource group in which the container is to be deployed.
        storage: AzureStorage
            Storage account in which the container is to be deployed.
        """
        super().__init__(name=name, group=group)

        self._template = None
        self._storage = storage

    def _build_template(self) -> dict:
        template = {
                      "properties": {
                        "publicAccess": "Container"
                      }
                    }
        return template

    def _deploy_api(self) -> bool:
        return self._storage._storage.create_container(name=self._name, group=self._group._name,
                                                       storage=self._storage._name, template=self._template)

    def _destroy_api(self):
        return self._storage._storage.delete_container(name=self._name, group=self._group._name,
                                                       storage=self._storage._name)


class AzureBlob(_AzureResource):
    """
    Deploy a blob.
    """
    def __init__(self, name: str, group: AzureGroup, storage: AzureStorage, container: AzureContainer, file: str):
        """
        Parameters
        ----------
        name: str
            Desired path to the blob in the container (e.g. /path/to/blob.txt).
        group: AzureGroup
            Resource group in which the blob is to be deployed.
        storage: AzureStorage
            Storage account in which the blob is to be deployed.
        container: AzureContainer
            Container in which the blob is to be deployed.
        file: str
            Path to the local file (e.g. /path/to/file.txt).
        """
        super().__init__(name=name, group=group)

        self._template = file
        self._storage = storage
        self._container = container

    def _build(self) -> bool:
        return path.exists(path=self._template)

    def _deploy_api(self):
        return self._storage._storage.upload_blob(name=self._name, storage=self._storage._name,
                                                  container=self._container._name, file=self._template)

    def _destroy_api(self):
        return self._storage._storage.delete_blob(name=self._name, storage=self._storage._name,
                                                  container=self._container._name)
