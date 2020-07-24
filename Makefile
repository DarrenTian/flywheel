clean:
	@echo "--> Cleaning pyc files..."
	find . -name "*.pyc" -delete

init: clean
	pipenv sync
	test ! -f || rm requirements.txt
	pipenv run pip freeze > requirements.txt

build: init
	@echo "--> Building image..."
	docker build --rm -t flywheel:latest .

docker-run:
	docker-compose up -d
