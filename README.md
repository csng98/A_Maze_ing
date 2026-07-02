*This project has been created as part of the 42 curriculum by ripaparo and csekakul.*

# A-Maze-ing

An interactive, procedural maze generator and interactive game written in Python. It utilizes a custom object-oriented framework alongside a Python wrapper for the classic C graphics library **MiniLibX (MLX)** to handle low-level, memory-mapped pixel rendering. 

---

## Description

The core objective of **A-Maze-ing** is to procedurally generate a "perfect maze"—a maze containing no isolated loops, no unreachable cells, and exactly one unique solution path between any two coordinates. 

Beyond strict generation, the project writes the finalized spatial map to an encoded text file and presents a fully interactive visual window where a player can navigate the maze in real time.

### Key Features
* **Procedural Perfection:** Tunnels are dynamically carved to guarantee a fully compliant, solvable layout every time.
* **The "42" Centerpiece:** On maps large enough to accommodate it ($> 8 \times 6$), the generation engine leaves a solid, impenetrable block matrix in the center forming the shape of the 42 logo.
* **Low-Level Blitting:** Renders graphics by modifying individual byte offsets in a volatile shared memory buffer before flashing the completed image to the screen.
* **Interactive Control Deck:**
  * `W`, `A`, `S`, `D` for player movement.
  * Real-time automated path solver visualization.
  * Instant map regeneration matrices.
  * Dynamic wall color theme shifting.

---

## Configuration File Format

The program parses an external plain-text configuration file (`config.txt`) to establish map constants. The layout must match the following format explicitly:

```text
# Dimension parameters (Integers)
WIDTH=20
HEIGHT=15

# Coordinate matrices formatted as Column,Row (0-indexed)
ENTRY=0,0
EXIT=19,14

# Output target file
OUTPUT_FILE=maze.txt

# Structural constraint
PERFECT=True

# Optional seed
SEED=42
```

### Constraints & Validations Enforced
* `WIDTH` and `HEIGHT` must be positive integers.
* `ENTRY` and `EXIT` must fall within the bounds of the coordinate grid and cannot point to the exact same cell.
* `PERFECT` must be explicitly declared as a boolean token (`True` or `False`).
* `SEED` is optional. When provided, it must be a valid integer and ensures the same maze is generated every time the same configuration is used.
* Any lines initiated by `#` or containing empty spaces are discarded by the engine.

---

## Instructions

### Prerequisites
* A Linux/Unix environment configured with X11 window server development headers.
* Python 3.8+ installed.
* The native compiled C binary dependency `libmlx.so` present in the environment path.

### Compilation and Execution

The project is entirely managed using a `Makefile`.

```bash
# Install dependencies and set up the Python virtual environment sandbox
make install

# Launch the interactive game using the default configuration file
make run
```

### Administrative Rules Matrix

| Command | Action |
| :--- | :--- |
| `make all` | Default target. Prints project banner and triggers environment installation. |
| `make install` | Provisions a localized `venv` wrapper and silently installs requirements. |
| `make clean` | Purges internal python caching footprints (`__pycache__`, `.pyc`). |
| `make fclean` | Executes `clean`, wipes out the virtual environment, and deletes generated text maps. |
| `make re` | Triggers a hard rebuild from scratch (`fclean` followed by `all`). |
| `make lint` | Validates code standards using basic typing and syntax checks. |
| `make lint-strict` | Executes a strict linting compilation checklist to prevent style deviations. |
| `make debug` | Compiles code with explicit trace logs activated for performance testing. |

---

## Maze Generation Algorithm

### Chosen Framework: Randomized Depth-First Search (DFS)
The project builds its grids using an iterative **Randomized Depth-First Search / Recursive Backtracking** algorithm.

### Why We Chose This Algorithm
* **Guaranteed Perfection:** By tracking visited states and breaking walls down sequentially, DFS inherently creates a spanning tree over the grid graph. This mathematically ensures there are no broken loops or disconnected spaces.
* **Memory Safety (Anti-Recursion Crash):** Python places strict boundaries on execution call stacks. Implementing the algorithm iteratively via an explicit array history stack (`stack: List[Tuple[int, int]]`) avoids recursion depth limits completely, allowing for massive maze sizes.
* **Distinct Structural Aesthetics:** DFS generation creates highly winding, long, corridor paths with fewer scattered dead-ends compared to Prim's or Kruskal's algorithms, making it visually engaging to solve.

---

## Reusable Code

The architecture separates concerns cleanly to maximize code reusability:

* **`Mlx` C-Bridge (`mlx.py`):** The comprehensive `ctypes` wrapper wraps low-level graphics pointers into a native Python object model. This wrapper can be dropped unchanged into any separate Python project requiring high-performance pixel drawing without raw C dependency overhead.
* **`parse_config` Engine (`config_parser.py`):** A bulletproof configuration file reader equipped with defensive bounds-checking and string separation logic that can handle initialization parameters for any grid-based system.
* **`Cell` Matrix Architecture:** The coordinate-based structural nodes present inside `mazegen.py` utilize an isolated direction mapping scheme that can serve as the foundational backbone for alternative pathfinding grids or puzzle games.
* **Reusable package:** The project can be packaged and installed as a standard Python module.

	1. `pip install build`
	2. `python3 -m build`

	The build process uses the `pyproject.toml` file located at the root of the repository to generate both the `.tar.gz` (source distribution) and `.whl` (wheel distribution) files.

	The `pyproject.toml` file defines the package metadata and build configuration:

	* **`[build-system]`** – Specifies the build tool (`setuptools`) and the backend used to create the package.
	* **`[project]`** – Contains the package metadata, including its name, version, description, authors, README, and the minimum supported Python version.
	* **`[tool.setuptools]`** – Configures how `setuptools` discovers the package, indicating that the source code is located in the `src` directory and that `mazegen.py` is the module to package.


---

## Team and Project Management

### Roles and Contributions

* **`ripaparo`**
  * Core Project Architect.
  * Designed and built the procedural generation structures and pathfinding solving logic.
  * Integrated the initial `Mlx` C-library binding hooks and constructed the functional pixel blitting mechanics.
  * Build Management and Optimization Engineer.
* **`csekakul`**
  * Translated the lifecycle tracking system (`Makefile`).
  * Extended pipeline tooling by implementing code standardization routines (`lint`, `lint-strict`, `debug`).
  * Authored the comprehensive documentation framework (`README.md`).

### Project Planning and Evolution
* **Phase 1 (Anticipated):** Create a baseline text generator, outputting hexadecimal matrices to terminal outputs.
* **Phase 2 (Evolution):** Shifted directly into dynamic integration once the `Mlx` wrapper was functional. The team expanded goals to support advanced operational features like active palette shifting and automated solver line tracing.
* **Phase 3 (Polishing):** Code cleanups and English translation steps were implemented to guarantee seamless pipeline deployments across platforms.

### Retrospective
* **What Worked Well:** The separation of the graphical rendering plane from generation mathematics allowed both developers to debug modules concurrently without merge conflicts.
* **What Could Be Improved:** The path solver utilizes a Depth-First Search strategy tracking path instances within lists. Utilizing a true Breadth-First Search queue would optimize runtime execution speed and ensure the absolute shortest path on imperfect layouts.

### Specific Tools Used
* **Python 3 / venv Wrapper:** For platform-independent sandbox isolation.
* **MiniLibX C Library:** For direct operating system window server rendering hooks.
* **GNU Make:** For uniform compilation and automated deployment execution.

---

## Resources

* **MiniLibX Documentation:** Standard reference for graphical window configurations and hook handling.
* **Think Labyrinth (Maze Generation Algorithms):** Classic analysis on the procedural characteristics of recursive backtracking systems.
* **Python `ctypes` Reference:** Core documentation utilized to pipe byte structures accurately into shared C memory arrays.

### Artificial Intelligence Integration Statement
AI tools were utilized during the development lifecycle for specific optimization tasks:
* **Algorithmic Structure Validation:** Employed to cross-examine binary wall masks and check validation ranges during manual string manipulation phases.
* **Exploratory Architecture Breakdown:** Used to inspect byte allocation formulas within the custom shared image data wrapper arrays.
* **Documentation Structuring:** Leveraged to organize raw source code requirements into a standardized, professional markdown presentation.
