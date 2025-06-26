# Makefile

TERRAFORM_DIR := terraform

.PHONY: install clean run init plan apply destroy

install:
	pip install -r requirements.txt

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +

run:
	python3 cli.py

init:
	cd $(TERRAFORM_DIR) && terraform init

plan:
	cd $(TERRAFORM_DIR) && terraform plan

apply:
	cd $(TERRAFORM_DIR) && terraform apply -auto-approve

destroy:
	cd $(TERRAFORM_DIR) && terraform destroy -auto-approve
