from azurly import _AzureResource, AzureGroup
from azurly.storage import AzureStorage
# from azurly.api.batch import AzureBatchAPI


from src.azurly.api.batch import AzureBatchAPI


class AzureBatch(_AzureResource):
    """
    Deploy a batch account.
    """
    def __init__(self, name: str, group: 'AzureGroup', storage: 'AzureStorage'):
        """
        Parameters
        ----------
        name: str
            Name of the batch account.
        group: AzureGroup
            Resource group in which the blob storage account is to be deployed.
        """
        super().__init__(name=name, group=group)

        self._batch = AzureBatchAPI()
        self._storage = storage

    def _build_template(self) -> dict:
        template = {
                      "location": self._group._region,
                      "properties": {
                        "autostorage": {
                          "storageAccountId": (f'/subscriptions/{self._group._main._subscription_id}'
                                               f'/resourceGroups/{self._group}/providers/'
                                               f'Microsoft.Storage/storageAccounts/{self._storage._name}')
                        }
                      }
                    }
        return template

    def _deploy_api(self) -> bool:
        return self._batch.create_batch_account(name=self._name, group=self._group._name, template=self._template)

    def _destroy_api(self) -> bool:
        return self._batch.delete_batch_account(name=self._name, group=self._group._name)
