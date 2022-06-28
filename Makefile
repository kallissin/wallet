build:
	@echo "--> Build Docker Base Image"
	docker build -t wallet-app .
	@echo "--> rebuilding docker-compose"
	docker-compose build

build-no-cache:
	@echo "--> Build Docker Base Image"
	docker build -t wallet-app . --no-cache
	@echo "--> rebuilding docker-compose"
	docker-compose build

bash:
	docker-compose run app bash

run: 
	docker-compose up

run-debug:
	docker-compose run --service-ports app

create-revisions:
	docker-compose run app bash -c "flask db upgrade"
