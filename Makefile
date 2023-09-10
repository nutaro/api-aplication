.PHONY: build
build:
	docker-compose build

.PHONY: up
up:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down

.PHONY: tests
tests:
	docker exec -i api bash -c "pip install coverage pytest"
	docker exec -i api bash -c "coverage run -m pytest"
	docker exec -i api bash -c "coverage report -m"

.PHONY: migrations
migrations:
	docker exec -i api bash -c "alembic upgrade head"