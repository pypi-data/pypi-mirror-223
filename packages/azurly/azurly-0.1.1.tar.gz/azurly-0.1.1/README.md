# Azurly

## Project Description

With this package it is possible to send API requests or deploy infrastructure-as-code to Azure in an intuitive way.
Authorisation is easy to set up and the classes are highly standardised, making the package easy to use.

## Installation

The package interacts with Azure through a Service Principal (SP). The SP can be created via the following steps:

1. Install the latest version of Azure CLI (https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
2. Open the applicable terminal (e.g. Windows PowerShell) and execute the following commands:
   1. az login
   2. az account set --subscription "YOUR SUBSCRIPTION ID"
   3. az ad sp create-for-rbac --name "YOUR SP NAME"
3. Save the generated 'client_id', 'client_secret' and 'tenant_id' from the previous command in a secure location.
4. Go to the Azure portal and navigate to IAM in the applicable subscription.
5. Add the applicable role assignments, 'Contributor' and 'Storage Blob Data Contributor' are commonly used, but more 
restrictive roles are recommended.

## Usage

### Azurly

1. The group is initiated with AzureGroup class containing everything required to deploy all the resources. The 
credentials for the SP are taken by default from the environment, but can also be given as arguments. The resource 
group is automatically generated and does not need to be added manually. 
2. Other resources can be added by simply initiating the respective class (e.g. AzureStorage for a storage account). 
The arguments ensure deployment in the correct order and all dependencies are present (e.g. a container cannot be 
deployed before the storage account parent is created). 
3. Once the desired resources are added, the app can be deployed by first running <YOUR GROUP>.build() and 
<YOUR GROUP>.deploy() afterwards. The build function creates all the templates required to define the request to Azure, 
the deploy function sends the requests using the AzurlyAPI package.

Common errors include:

1. AuthenticationError, the SP is incorrectly configured, or does not have the required authorisation.
2. AzureError, the request contains invalid parameters. This can occur due to a variety of reasons, but the main 
reason being identical resource names.

### Azurly API

1. Create the template used for deployment (not applicable if the resource is to be deleted obviously). These can be 
copied via the Azure portal from similar deployed resources, or the Azurly package can be used to generate them via 
the build method in the AzureApp class.
2. Import the respective class (e.g. AzureStorageAPI for everything related to Microsoft Storage) and call the 
applicable methods (e.g. create_storage_account).

Common errors include:

1. AuthenticationError, the SP is incorrectly configured, or does not have the required authorisation.
2. AzureError, the request contains invalid parameters. Dependencies on other resources and the templates are not 
checked, which is the most likely reason for this error. For example, deploying a container in a non-existing storage 
account will cause this error.

## Features

### Azurly

The following resources can be deployed with the Azurly package (per service provider):

- Microsoft Management:
  - Resource groups.

- Microsoft Storage:
  - Blob storage accounts.
  - Containers.
  - Blobs.

### Azurly API

The following resource requests can be executed with the AzurlyAPI package (per service provider):

- Microsoft Management:
  - Create / delete resource groups.

- Microsoft Storage:
  - Create / delete storage accounts.
  - Create / delete containers.
  - Upload / download / delete blobs.

### Documentation

Each class and function provides docstrings which can be consulted. Simply use the build-in help() function to see 
them after import. 

### Changelog

- 0.1.1:
  - Build method updated from setup.py to pyproject.toml.

- 0.1.0:
  - Azurly:
    - AzureGroup class added.
    - AzureStorage class added.
    - AzureContainer class added.
    - AzureBlob class added.
  - AzurlyAPI:
    - AzureGroupAPI class added.
    - AzureStorageAPI class added.
