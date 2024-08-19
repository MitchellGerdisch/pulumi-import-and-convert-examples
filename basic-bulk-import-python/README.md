# Basic Bulk Import
Demonstrates bulk import using the `pulumi import -f` option

## Set up
* Go to `source-project` 
  * `pulumi up`
  * `pulumi stack -i`
    * This will output the resource types and IDs to use for import below.
* Go to `imported-project`
  * Modify `import.json` with the IDs from above. 
  

## Demo
* Go to `imported-project`
* Show `import.json` to show the json file.
  * Explain there are ways to build this file programmatically.
* `pulumi import -f import.json -o __main__.py`
* Show the generated code in `__main__.py` 
* `pulumi stack` to show the resources that are now managed in this stack.

