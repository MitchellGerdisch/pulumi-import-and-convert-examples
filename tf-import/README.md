# Pulumi Import from Terraform State Demo
Shows how you can do a Pulumi import from TF state

## Launch TF Project
* `cd source-tf-project`
* `terrform init -upgrade`
* `terraform apply --auto-approve`

## Set up import project
* `cd imported-tf-project`

If importing to python, `cd import-to-python` folder:
* `python3 -m venv venv; source ./venv/bin/activate; pip install -r requirements.txt`
* `pulumi stack init dev`
* `pulumi import --from terraform ../../source-tf-project/terraform.tfstate --out __main__.py`
  * This assumes you don't have anything in `__main__.py` you want to save.

If importing to typescript, `cd import-to-typescript` folder:
* `npm i`
* `pulumi stack init dev`
* `pulumi import --from terraform ../../source-tf-project/terraform.tfstate --out index.ts`
  * This assumes you don't have anything in `index.ts` you want to save.

## Clean Up
* Remove the code from `__main__.py` or `index.ts` as applicable, so it is ready for the next demo.
* `pulumi stack rm --force -y`
  * This clears out the state for the stack.
* `cd source-tf-project`
* `terraform destroy --auto-approve`