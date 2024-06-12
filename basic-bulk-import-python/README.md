# Basic Bulk Import
Demonstrates bulk import using the `pulumi import -f` option

## Set up
* Go to `source-project` 
  * `pulumi up`
  * `pulumi stack -i`
    * This will output the resource types and IDs to use for import below.
* Go to `imported-project`
  * Modify `import.json` with the IDs from above. 
  * `pulumi import -f import.json`
  * Copy the computed code and use https://www.pulumi.com/ai/ to "rewrite this without explicit references"
    * This will rewrite the code to use property references.
    * Paste this into the imported-project program and do a `pulumi up` to show nothing has changed.