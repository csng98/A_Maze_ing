CYAN = \\033[1;36m
RESET = \\033[0;0m
RED = \\033[0;31m
GREEN = \\033[0;32m

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

MAIN = src/a_maze_ing.py
CONFIG = config.txt

all: banner install

banner:
	@echo   " $(CYAN)    ___        __  ___                     _             $(RESET)  "
	@echo   " $(CYAN)   /   |      /  |/  /___ _____  ___      ( )____  _____ $(RESET)  "
	@echo   " $(CYAN)  / /| |     / /|_/ / __ '/_  / / _ \     / / __ \/ __ '/ $(RESET)  "
	@echo   " $(CYAN) / ___ |    / /  / / /_/ / / /_/  __/    / / / / / /_/ /  $(RESET)  "
	@echo   " $(CYAN)/_/  |_|___/_/  /_/\__,_/ /___/\___/____/_/_/ /_/\__, /   $(RESET)  "
	@echo   " $(CYAN)       /_____/                    /_____/       /____/    \n$(RESET)  "

install: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	@echo "$(CYAN)Creating virtual sandbox and installing dependencies...$(RESET)"
	@python3 -m venv $(VENV) > /dev/null 2>&1 && \
	$(PIP) install --upgrade pip > /dev/null 2>&1 && \
	$(PIP) install -r requirements.txt > /dev/null 2>&1 & \
	pid=$$!; \
	printf "$(CYAN)[$(RESET)"; \
	while kill -0 $$pid 2>/dev/null; do \
		printf "$(CYAN)▮$(RESET)"; \
		sleep 0.199; \
	done; \
	printf "$(CYAN)]$(RESET)\n"
	@touch $(VENV)/bin/activate
	@echo "$(GREEN)Environment successfully provisioned!!$(RESET)"

run: install
	@echo "$(CYAN)Starting the interactive maze...$(RESET)"
	@$(PYTHON) $(MAIN) $(CONFIG)

debug: install
	@echo "$(CYAN)Launching program in debug mode via pdb...$(RESET)"
	@$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint: install
	@echo "$(CYAN)Running standard linting checks (flake8 + mypy)...$(RESET)"
	@$(PYTHON) -m flake8 . --exclude=venv,src/mlx,maze_analyzer.py
	@$(PYTHON) -m mypy . --exclude="venv|mlx|maze_analyzer.py" --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	@echo "$(CYAN)Running strict compliance checks (flake8 + mypy --strict)...$(RESET)"
	@$(PYTHON) -m flake8 . --exclude=venv,src/mlx,maze_analyzer.py
	@$(PYTHON) -m mypy . --exclude="venv|mlx|maze_analyzer.py" --strict

clean:
	@echo "$(RED)Purging internal cache files and runtime footprints...(__pycache__, etc.)...$(RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf .mypy_cache .pytest_cache

fclean: clean
	@echo "$(RED)Dismantling virtual environment and clearing exported maze files...$(RESET)"
	@rm -rf $(VENV)
	@rm -f maze.txt

re: fclean all

.PHONY: all banner install run debug lint lint-strict clean fclean re