up:
	docker-compose up -d

build:
	docker-compose up -d --build

migrate:
	docker-compose exec pollution.service ./manage.py migrate

index:
	docker-compose exec pollution.service ./manage.py search_index --rebuild
