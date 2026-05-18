rung: # run generate_proforma command
	.venv/Scripts/python src/proforma_generator/main.py gen contract_data 3
rung2: # run generate_proforma command
	.venv/Scripts/python src/proforma_generator/main.py gen contract_data 2 3

runm:	# run display milestones command
	.venv/Scripts/python src/proforma_generator/main.py mile contract_data

runu: # run update contract command
	.venv/Scripts/python src/proforma_generator/main.py update contract_data 2

setup: requirements.txt
	./.venv/Scripts/pip install -r requirements.txt

a-venv: requirements.txt
	python -m venv venv
	./venv/Scripts/pip install -r requirements.txt

build: pyproject.toml
	uv tool install --reinstall .