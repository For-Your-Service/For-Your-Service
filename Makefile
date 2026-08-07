install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src/ --cov-report=html

lint:
	black src/ tests/
	flake8 src/ tests/
	mypy src/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache htmlcov

docker-build:
	docker build -t fys-job-pipeline .

docker-run:
	docker run -it --env-file .env fys-job-pipeline

.PHONY: install test test-cov lint clean docker-build docker-run
