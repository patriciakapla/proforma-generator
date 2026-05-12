rung: # run generate_proforma command
	venv/Scripts/python src/proforma_generator/main.py gen src/proforma_generator/data/contract_data.json 3
rung2: # run generate_proforma command
	venv/Scripts/python src/proforma_generator/main.py gen src/proforma_generator/data/contract_data.json 2 3

runm:	# run display milestones command
	venv/Scripts/python src/proforma_generator/main.py mile src/proforma_generator/data/contract_data.json

runu: # run update contract command
	venv/Scripts/python src/proforma_generator/main.py update src/proforma_generator/data/contract_data.json 2

setup: requirements.txt
	./venv/Scripts/pip install -r requirements.txt

a-venv: requirements.txt
	python -m venv venv
	./venv/Scripts/pip install -r requirements.txt

build: pyproject.toml
	uv tool install --reinstall .