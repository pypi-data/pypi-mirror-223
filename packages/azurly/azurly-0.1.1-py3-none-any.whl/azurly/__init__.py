from os import path, mkdir
from shutil import rmtree
from json import dumps

from azurly.api import AzureGroupAPI


class _AzureResource:

    def __init__(self, name: str, group: 'AzureGroup'):
        self._name = name
        self._group = group
        self._template = None
        self._group._resources.append(self)

    # General methods used in all child classes (except AzureBlob!).
    def _build(self) -> True:
        # Convert dictionary to JSON format and save.
        template = dumps(obj=self._build_template(), indent=2)
        template_path = f'./build/{self._group._name}/{self._name}.json'

        with open(template_path, 'w') as file:
            file.write(template)

        # Set the template attribute to the template path for the deploy method.
        self._template = f'./build/{self._group._name}/{self._name}.json'
        return True

    def _deploy(self):
        # Check if the template is build.
        if self._template is not None:
            created = self._deploy_api()

            if not created and self._group.overwrite:
                self._destroy_api()
                self._deploy_api()
                return True
            elif not created and not self._group.overwrite:
                return False
            else:
                return True

        else:
            return False

    def _destroy(self) -> bool:
        # This method will be defined per child class.
        return self._destroy_api()

    # Unique methods for each child class.
    def _build_template(self):
        return True

    def _deploy_api(self):
        return True

    def _destroy_api(self):
        return True


class _AzureGroup(_AzureResource):

    def __init__(self, name: str, group: 'AzureGroup'):
        super().__init__(name=name, group=group)

        self._main = AzureGroupAPI()

    def _build_template(self) -> dict:
        template = {
                      "location": self._group._region
                    }
        return template

    def _deploy_api(self) -> bool:
        return self._main.create_resource_group(name=self._name, template=self._template)

    def _destroy_api(self) -> bool:
        return self._main.delete_resource_group(name=self._name)


class AzureGroup:
    """
    Main class to deploy all resources under a single resource group.
    """
    def __init__(self, name: str, region: str, overwrite: bool = False, rollback: bool = True):
        """
        Parameters
        ----------
        name: str
            Name of the resource group.
        region: str
            Region of the resource group (see Azure documentation for valid regions).
        overwrite: bool
            Delete the resource group if it already exists.
        rollback: bool
            Delete the resource group if an error is raised during deployment.
        """
        self.overwrite = overwrite
        self.rollback = rollback

        self._name = name
        self._region = region
        self._log = f'./logs/{name}.log'
        self._main = AzureGroupAPI(logfile=self._log)
        self._resources = []
        self._group = _AzureGroup(name=self._name, group=self)

    def build(self) -> bool:
        """
        Build the templates for all the specified resources.

        Returns
        -------
        bool:
            True, all resource templates are created successfully.
            False, creating a resource template failed.
        """
        if not path.exists(path='./build/'):
            mkdir(path=f'./build/')
        elif path.exists(path=f'./build/{self._name}'):
            rmtree(path=f'./build/{self._name}')

        mkdir(path=f'./build/{self._name}')

        for resource in self._resources:
            if not resource._build():
                self._main._logger.warning(f'Building resource template for {resource._name} failed!')
                return False

        self._main._logger.info(f'Building resource templates for {self._name} succeeded.\n')
        return True

    def deploy(self) -> bool:
        """
        Deploy the resource group (including its specified resources).

        Returns
        -------
        bool:
            True, all the resources have been deployed successfully.
            False, deploying a resource failed.
        """
        try:
            for resource in self._resources:
                if not resource._deploy():
                    self._main._logger.warning(f'Deploying {resource._name} failed, because it already exists.')
                    return False

            self._main._logger.info(f'Deploying resources for {self._name} succeeded.\n')
            return True

        except Exception as e:
            if self.rollback:
                self._main.delete_resource_group(name=self._name)

            self._main._logger.error(f'An error was raised during deployment:\n\n{str(e)}')
            raise e

    def destroy(self) -> bool:
        """
        Destroy the resource group.

        Returns
        -------
        bool:
            True, the resource group has been deleted successfully.
            False, the resource group has not been deleted, because it does not exist.
        """
        return self._group._destroy()
