# Basic Bulk Import
Demonstrates bulk import using the `pulumi import -f` option.
This includes **IMPORTING INTO A COMPONENT RESOURCE**. See below for details.

## Set up
* Go to `source-project` 
  * `python3 -m venv venv; source ./venv/bin/activate; pip install -r requirements.txt`
  * `pulumi stack init` if needed
  * `pulumi up`
  * `pulumi stack -i`
    * This will output the resource types and IDs to use for import below.
* Go to `imported-project`
  * Modify `import.json` with the IDs from above. 

## Demo
### Prep
* Go to `imported-project`
* `python3 -m venv venv; source ./venv/bin/activate; pip install -r requirements.txt`
* `pulumi stack init` if no stack currently exists.

### Demo Flow
* Show `import.json` to show the json file.
  * Explain there are ways to build this file programmatically.
* `pulumi import -f import.json -o __main__.py`
  * **CURRENTLY FAILS ON CODEGEN**
    * State import works as expected. The resources are in state as children of the component.
    * But codegen then fails:
      * ERROR: `error: could not find latest version for provider mycomponent: 404 HTTP error fetching plugin from https://api.github.com/repos/pulumi/pulumi-mycomponent/releases/latest. If this is a private GitHub repository, try providing a token via the GITHUB_TOKEN environment variable. See: https://github.com/settings/tokens`
* Show the generated code in `__main__.py` 
* `pulumi stack` to show the resources that are now managed in this stack.

### Clean up
* When done, `pulumi stack rm --force -y` to force deleting the state. The `source-project` can be used to clean up the resources.

### Import into a component resource
The premise is as follows:
* I have a [component resource](https://www.pulumi.com/docs/iac/concepts/resources/components/) named `mycomponent:az:StorageComponent` which is an abstraction to create storage accounts and blob containers together.
  * The component can be found in `imported-project/az_storage.py`
* I want to import a storage account and blob container and have it placed under the component resource.
  * A "standard" import would put the resources under the stack. But by specifying the `import.json` using the component and parent properties, `pulumi import` will place the resources under the component.