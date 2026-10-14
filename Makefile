.PHONY: setup data test run docker-run clean
setup:
	pip install -r requirements.txt
data:
	mkdir -p data/cache results
test:
	PYTHONPATH=src pytest -q
run:
	mkdir -p data/cache results
	PYTHONPATH=src python3 src/run_all.py
docker-run:
	docker compose up --build
clean:
	rm -rf results/*.json results/SUMMARY.md data/cache/*.csv __pycache__ src/__pycache__
