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