# Pulumi Convert from Terraform Program (including Modules)
A demo of how to convert a Terraform program that uses modules.

This demo not only translates the TF code to a Pulumi program but also creates the Pulumi "Component Resources" based on the Terrform modules.

## Overview
The `pulumi convert` command is run on the `terraform-source` folder and the `pulumi-convert` folder is populated with Pulumi code in the chosen language.

### References
* https://www.pulumi.com/docs/iac/cli/commands/pulumi_convert/ 

## Steps
* `cd terraform-source`
* Run `pulumi convert --from terraform --language python --out ../pulumi-convert`
  * You can specify any Pulumi-supported language (i.e. python, typescript, go, csharp, java)
  * You can specify any folder for the `--out` parameter. 
* Review the generated code and note:
  * The TF code is converted to Pulumi code in the chosen language.
  * The TF module has been converted into a component resource.
  * The main Pulumi program uses the component resource.
