rung: # run generate_proforma command
	venv/Scripts/python src/main.py gen data/contract_data.json 3

runm:	# run display milestones command
	venv/Scripts/python src/main.py mile data/contract_data.json

setup: requirements.txt
	./venv/Scripts/pip install -r requirements.txt

a-venv: requirements.txt
	python -m venv venv
	./venv/Scripts/pip install -r requirements.txt


