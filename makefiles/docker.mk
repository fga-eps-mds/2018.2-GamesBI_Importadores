# DOCKER DEPLOY ------------------------------------------------
file := "docker-compose.yml"

up:
	# Create and start containers
	sudo docker-compose up

build:
	# Rebuild the docker compose
	sudo docker-compose build

restart:
	# Restart services
	sudo docker-compose restart

logs:
	# View output from containers
	sudo docker-compose logs

start:
	# Start services
	sudo docker-compose start

stop:
	# Stop services
	sudo docker-compose stop

ps:
	# List all running containers
	sudo docker-compose ps

down:
	# Stop and Remove all containers
	sudo docker-compose down

