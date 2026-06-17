.DEFAULT_GOAL := help

UV := uv
APP := multi-ai-agent
PROJECT ?= ./output
WORKERS ?= 4
ARGS ?=

.PHONY: help sync init-env run run-quiet run-reset run-container stop-container clean-container build-wheel clean

help:
	@printf "Available targets:\n"
	@printf "  make sync                       Install project dependencies with uv\n"
	@printf "  make init-env                   Copy .env.example to .env if missing\n"
	@printf "  make run TASK='...'             Run the application\n"
	@printf "  make run-quiet TASK='...'       Run without intermediate tool logs\n"
	@printf "  make run-reset TASK='...'       Run after clearing shared memory and messages\n"
	@printf "  make run-container              Run app + MongoDB via Docker Compose\n"
	@printf "  make stop-container             Stop Docker Compose services\n"
	@printf "  make clean-container            Stop services and remove MongoDB volume\n"
	@printf "  make build-wheel                Build the wheel distribution\n"
	@printf "  make clean                      Remove generated build artifacts\n"

sync:
	$(UV) sync

init-env:
	@test -f .env || cp .env.example .env

run:
	@test -n "$(TASK)" || (echo "TASK is required. Usage: make run TASK='build a RAG chatbot'" && exit 1)
	$(UV) run $(APP) --task "$(TASK)" --project "$(PROJECT)" --workers "$(WORKERS)" $(ARGS)

run-quiet:
	@test -n "$(TASK)" || (echo "TASK is required. Usage: make run-quiet TASK='build a data pipeline'" && exit 1)
	$(UV) run $(APP) --task "$(TASK)" --project "$(PROJECT)" --workers "$(WORKERS)" --quiet $(ARGS)

run-reset:
	@test -n "$(TASK)" || (echo "TASK is required. Usage: make run-reset TASK='redesign the recommendation engine'" && exit 1)
	$(UV) run $(APP) --task "$(TASK)" --project "$(PROJECT)" --workers "$(WORKERS)" --reset-memory $(ARGS)

run-container:
	@set -a; \
	if [ -f .env ]; then . ./.env; fi; \
	set +a; \
	if [ -z "$$ANTHROPIC_API_KEY" ] || [ "$$ANTHROPIC_API_KEY" = "your_anthropic_api_key_here" ]; then \
		echo "ANTHROPIC_API_KEY is missing or still using the placeholder value. Update .env or export the key before running make run-container."; \
		exit 1; \
	fi; \
	docker compose -f container/docker-compose.yml up --build

stop-container:
	docker compose -f container/docker-compose.yml down

clean-container:
	docker compose -f container/docker-compose.yml down -v

build-wheel:
	$(UV) build --wheel

clean:
	rm -rf build dist src/*.egg-info
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	find . -name '.DS_Store' -type f -delete