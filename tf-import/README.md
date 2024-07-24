# Pulumi Import from Terraform State Demo
Shows how you can do a Pulumi import from TF state

## Launch TF Project
* `cd source-tf-project`
* `terrform init -upgrade`
* `terraform apply`

## Set up import project
* `cd imported-tf-project`
* `python3 -m venv venv; source ./venv/bin/activate; pip install -r requirements.txt`
* `pulumi import --from terraform ../source-tf-project/terraform.tfstate --out __main__.py`
  * This assumes you don't have anything in `__main__.py` you want to save.
* Don't ask pulumi ai to rewrite without explicity references since it will think it's azure-native instead of azure-classic (which is what is used for import since it's based on the TF provider) and the settings won't be write.
* Don't bother with a pulumi preview - just show the generated code.
  * `pulumi preview` will throw an error about the container's storage encryption scope - just delete it and it'll be fine.
  * But this affects the flow of the demo.