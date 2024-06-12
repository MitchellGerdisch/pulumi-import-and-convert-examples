# Pulumi Import from Terraform State Demo
Shows how you can do a Pulumi import from TF state

## Launch TF Project
* `cd tf-project`
* `terrform init -upgrade`
* `terraform apply`

## Set up import project
* `cd imported-project`
* `python3 -m venv venv; source ./venv/bin/activate; pip install -r requirements.txt`
* `pulumi import --from terraform --file ../tf-project/terraform.tfstate`
* Don't ask pulumi ai to rewrite without explicity references since it will think it's azure-native instead of azure-classic (which is what is used for import since it's based on the TF provider) and the settings won't be write.