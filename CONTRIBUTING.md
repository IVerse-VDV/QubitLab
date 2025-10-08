# Contributing to QubitLab

Thank you for your interest in contributing to QubitLab! This project aims to make quantum computing education accessible through interactive visualizations and hands-on experimentation. We welcome contributions from developers, educators, researchers, and quantum computing enthusiasts of all experience levels. Whether you're fixing a bug, adding a feature, improving documentation, or suggesting ideas, your contributions help advance quantum computing education for everyone.

This document provides comprehensive guidelines and instructions for contributing to the QubitLab project. By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md), which ensures a welcoming and inclusive environment for all contributors. We have structured this guide to help you understand not only how to contribute code, but also how the project is organized, what technologies we use, and how to work effectively within our development workflow.


## Getting Started

QubitLab is hosted as an organization repository on GitHub under [IVerse-VDV](https://github.com/IVerse-VDV). Before you begin contributing, you should familiarize yourself with the project structure, existing codebase, and ongoing development efforts. We recommend browsing through existing [issues](https://github.com/IVerse-VDV/QubitLab/issues), [pull requests](https://github.com/IVerse-VDV/QubitLab/pulls), and documentation to understand what areas need attention and where your skills might be most valuable.

### Prerequisites

To contribute effectively to QubitLab, you should have a basic understanding of several key technologies and concepts. First, proficiency in **Python 3.8 or higher** is essential, as the entire application is built using Python. You should be comfortable with object-oriented programming, function definitions, module imports, and Python's standard library. Second, familiarity with **quantum computing fundamentals** is helpful but not strictly required. Understanding concepts like qubits, superposition, entanglement, and quantum gates will help you contribute more effectively, though our community is happy to help guide new learners through these concepts.

Third, basic **Git and GitHub knowledge** is necessary for version control and collaboration. You should understand how to clone repositories, create branches, commit changes, and push to remote repositories. If you're new to Git, we recommend reviewing [GitHub's Git Handbook](https://guides.github.com/introduction/git-handbook/) before contributing. Fourth, experience with **[Streamlit](https://streamlit.io/)** for building interactive web applications is beneficial, though you can learn as you go by examining our existing code. Finally, familiarity with **[Qiskit](https://qiskit.org/)**, IBM's quantum computing framework, will help you understand and extend quantum circuit functionality, particularly if you're working on gate implementations or quantum simulations.

### Repository Information

The QubitLab repository is located within the IVerse-VDV organization on GitHub. Understanding the repository structure and access methods is important for effective contribution:

**GitHub Organization:** [IVerse-VDV](https://github.com/IVerse-VDV)  
**Repository Name:** QubitLab  
**Repository URL:** https://github.com/IVerse-VDV/QubitLab  
**HTTPS Clone URL:** `https://github.com/IVerse-VDV/QubitLab.git`  
**SSH Clone URL:** `git@github.com:IVerse-VDV/QubitLab.git`

You can access and clone the repository using either HTTPS or SSH authentication. HTTPS is simpler for beginners and requires only your GitHub username and password (or personal access token for enhanced security). SSH is recommended for frequent contributors who have [set up SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) with their GitHub account, as it provides passwordless authentication and is more secure for regular use.

## Understanding the Project Structure

QubitLab follows a modular architecture that separates concerns and makes the codebase maintainable and extensible. Understanding how the project is organized will help you navigate the code effectively and determine where to make your contributions. The repository structure is intentionally kept simple to lower the barrier for new contributors while maintaining clear separation between different functional areas.

### Repository Layout

The project consists of several key files, each serving a specific purpose in the application's functionality:

```
QubitLab/
├── app.py                      # Main Streamlit application and UI
├── gates.py                    # Quantum gate definitions and circuit building
├── utils.py                    # Utility functions for simulation and visualization
├── requirements.txt            # Python package dependencies
├── README.md                   # Project documentation and usage guide
├── CONTRIBUTING.md            # This file - contribution guidelines
├── CODE_OF_CONDUCT.md         # Community standards and behavior guidelines
├── .gitignore                 # Git ignore patterns for Python/Streamlit
└── LICENSE                    # Project license (MIT)
```

This flat structure makes it easy to locate specific functionality without navigating through complex directory hierarchies. As the project grows, we may introduce subdirectories for better organization, but the current structure serves our needs while keeping complexity low for new contributors.

### File Purposes Overview

Understanding what each file does is crucial for knowing where to make changes. The **app.py** file serves as the entry point and contains all user interface code built with Streamlit. When you run `streamlit run app.py`, this file initializes the web application, handles user interactions, coordinates between other modules, and renders all visualizations. If you're working on UI improvements, adding new visualization panels, or changing how users interact with the application, this is where you'll make most of your changes.

The **gates.py** module contains all quantum gate implementations and circuit construction logic. Each quantum gate (Hadamard, Pauli-X/Y/Z, CNOT, etc.) has its own function that applies the gate to a Qiskit quantum circuit. The module also defines which gates are available for different numbers of qubits and provides the `create_circuit()` function that builds complete quantum circuits from user-specified gate sequences. If you're adding new quantum gates, modifying gate behavior, or changing how circuits are constructed, you'll work primarily in this file.

The **utils.py** module houses utility functions that dont fit neatly into gates or UI categories. This includes quantum simulation execution using Qiskit Aer, Bloch vector calculations from statevectors and density matrices, partial trace operations for computing reduced density matrices, conversion between little-endian and big-endian qubit ordering, and all visualization generation code for Bloch spheres and state city plots. If you're improving visualization quality, optimizing simulation performance, or adding new analysis capabilities, you'll modify this file.

The **requirements.txt** file lists all Python package dependencies with version constraints. When contributors install dependencies using `pip install -r requirements.txt`, this file ensures everyone uses compatible package versions, preventing "works on my machine" problems. If you add new dependencies to the project, you must update this file with appropriate version specifications.

## Technology Stack and Dependencies

QubitLab leverages several powerful Python libraries to deliver its quantum computing visualization capabilities. Understanding these technologies and how they interact is essential for effective contribution.

### Core Technologies

The foundation of our quantum computing capabilities comes from **[Qiskit](https://qiskit.org/)** version 1.0 or higher. Qiskit, developed by IBM Research, is an open-source framework for working with quantum computers at the level of pulses, circuits, and algorithms. We use Qiskit's circuit construction API to build quantum circuits, the gate library for quantum operations, and the Aer simulator for classical simulation of quantum systems. Importantly, we use Qiskit's **new API** (introduced in version 1.0) rather than deprecated functions, which means we use `backend.run()` instead of the older `execute()` function. You can learn more about Qiskit from the [official documentation](https://qiskit.org/documentation/) and [tutorials](https://qiskit.org/learn/).

Our user interface is powered by **[Streamlit](https://streamlit.io/)** version 1.28 or higher. Streamlit enables building interactive web applications using pure Python without requiring HTML, CSS, or JavaScript knowledge. Its reactive programming model automatically updates the UI when user inputs change, making it perfect for interactive data applications like QubitLab. Streamlit handles our sidebar controls, button interactions, dropdown menus, and layout organization. The [Streamlit documentation](https://docs.streamlit.io/) provides comprehensive guides on creating interactive applications.

For interactive 3D visualizations, particularly the Bloch spheres, we use **[Plotly](https://plotly.com/python/)** version 5.17 or higher. Plotly provides WebGL-accelerated 3D graphics that users can rotate, zoom, and explore interactively in their browsers. We use Plotly's `graph_objects` module to construct custom 3D scatter plots, surfaces, and cone objects that compose our Bloch sphere visualizations. Plotly's [Python graphing library documentation](https://plotly.com/python/) covers all visualization types and customization options.

Mathematical operations throughout the application rely on **[NumPy](https://numpy.org/)** version 1.24 or higher. NumPy provides efficient array operations, complex number arithmetic, matrix multiplications, and linear algebra functions essential for quantum mechanics calculations. When working with statevectors, density matrices, or Bloch vectors, we use NumPy arrays and operations. The [NumPy documentation](https://numpy.org/doc/) is the definitive reference for array manipulation and mathematical functions.

Finally, **[Matplotlib](https://matplotlib.org/)** version 3.7 or higher handles static visualizations, including circuit diagrams and 3D state city plots for three-qubit systems. While Plotly handles interactive graphics, Matplotlib excels at generating publication-quality static figures. The [Matplotlib documentation](https://matplotlib.org/stable/contents.html) covers all plot types and customization options.

### Dependency Management

All project dependences are specified in the `requirements.txt` file with minimum version constraints. When you set up your development environment, running `pip install -r requirements.txt` installs all necessary packages. The version constraints ensure compatibility while allowing bug fixes and minor updates. If you need to add a new dependency, add it to `requirements.txt` with an appropriate version constraint (`package-name>=1.2.0`) and document why its needed in your pull request.

### Understanding Version Constraints

Version constraints in `requirements.txt` use the `>=` operator, which means "install this version or any newer compatible version." For example, `qiskit>=1.0.0` allows Qiskit 1.0.0, 1.0.1, 1.1.0, etc., but not 0.x versions. This approach balances stability with flexibility, allowing contributors to receive bug fixes automatically while preventing breaking changes from major version updates. If a specific version is required due to a bug or incompatibility, we use exact version pinning like `package-name==1.2.3`.

## Working with Qiskit New API

One of the most important aspects of contributing to QubitLab is understanding and using Qiskit New API correctly. Qiskit underwent significant changes in version 1.0, deprecating old patterns and introducing new, more efficient approaches. As a project committed to maintaining new, future-proof code, we strictly use the new API patterns.

### The Deprecated `execute()` Function

In older Qiskit versions (prior to 1.0), the standard way to run quantum circuits was using the `execute()` function. This legacy pattern looked like this:

```python
# OLD DEPRECATED PATTERN - DO NOT USE!!!
from qiskit import execute, Aer

backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1024)
result = job.result()
```

This pattern is now **deprecated** and will be removed in future Qiskit versions. Contributors should never use `execute()` in new code or when modifying existing code. If you encounter `execute()` in our codebase, it should be refactored to use the new API.

### The New `backend.run()` Pattern

The new Qiskit API uses a cleaner, more object oriented approach where you call the `run()` method directly on backend objects. This is the pattern used throughout QubitLab:

```python
# new PATTERN - ALWAYS USE THIS :)
from qiskit_aer import Aer

backend = Aer.get_backend('aer_simulator')
job = backend.run(circuit, shots=1024)
result = job.result()
```

This pattern is more intuitive, more performant, and aligned with Qiskit's long-term architectural vision. When you see `backend.run()` in our code, this is the correct new approach. All new code should follow this pattern exclusively.

### Getting Simulation Results

After running a circuit, extracting results differs slightly depending on what information you need. For statevector simulations (where we want the complete quantum state), we use the `save_statevector()` method on circuits and retrieve it from result data:

```python
# Save statevector in circuit
circuit.save_statevector()

# Run simulation
backend = Aer.get_backend('aer_simulator')
job = backend.run(circuit, shots=1024)
result = job.result()

# Extract statevector from result data
statevector = result.data()['statevector']
```

For measurement simulations where we want classical bit outcomes, we add measurements to the circuit and use `get_counts()`:

```python
# Add measurements
measured_circuit = circuit.copy()
measured_circuit.measure_all()

# Run simulation
backend = Aer.get_backend('aer_simulator')
job = backend.run(measured_circuit, shots=1024)
result = job.result()

# Get measurement counts
counts = result.get_counts()
```

These patterns are used throughout `utils.py` in functions like `run_circuit()` and `get_measurement_counts()`. When adding new simulation functionality, follow these established patterns for consistency.

### Qiskit Circuit Construction

When building quantum circuits, we use Qiskit circuit construction API directly without intermediate wrappers. A typical gate application looks like this:

```python
from qiskit import QuantumCircuit

# Create circuit with specified number of qubits
circuit = QuantumCircuit(num_qubits)

# Apply gates using circuit methods
circuit.h(0)              # Hadamard on qubit 0
circuit.x(1)              # Pauli X on qubit 1
circuit.cx(0, 1)          # CNOT with control=0, target=1
circuit.s(0)              # S gate on qubit 0
circuit.t(1)              # T gate on qubit 1
```

Each gate has a corresponding method on the `QuantumCircuit` object. gate parameters like qubit indices are passed as arguments. Multi qubit gates take multiple qubit indices in the order control(s) then target. This direct use of Qiskit API makes our code transparent and easy to understand for anyone familiar with Qiskit.

### References and Learning Resources

If you are new to qiskit or need to deepen your understanding, IBM provides excellent learning resources. The [Qiskit Textbook](https://qiskit.org/textbook/preface.html) offers comprehensive introductions to quantum computing and Qiskit programming. The [Qiskit Documentation](https://qiskit.org/documentation/) provides detailed API references for all modules and functions. For migration from old to new API patterns, consult the [Qiskit 1.0 Migration Guide](https://qiskit.org/documentation/migration_guides/qiskit_1.0_migration.html), which explains all breaking changes and how to update code accordingly.

## Setting Up Your Development Environment

To contribute to QubitLab, you need to set up a local development environment on your computer. This process involves forking the repository, cloning it locally, installing dependencies, and verifying that the application runs correctly. Follow these detailed steps carefully to ensure a smooth setup process.

### Step 1: Fork the Repository

Navigate to the QubitLab repository at [https://github.com/IVerse-VDV/QubitLab](https://github.com/IVerse-VDV/QubitLab) in your web browser. Click the **Fork** button in the upper right corner of the page. This creates a personal copy of the repository under your GitHub account. All your changes will be made in this forked repository before being submitted back to the main project through pull requests. Forking gives you a personal sandbox where you can experiment freely without affecting the main project.

After forking, GitHub will redirect you to your personal fork, which will be located at `https://github.com/YOUR-USERNAME/QubitLab`. This is your working repository where youll push changes before submitting pull requests to the main project.

### Step 2: Clone Your Fork Locally

After forking the repository, you need to clone your personal copy to your local machine so you can work on the code. Open a terminal or command prompt and navigate to the directory where you want to store the project. Execute one of the following commands based on your preferred authentication method.

If you're using **HTTPS authentication** (recommended for beginners), run:

1.  ```bash
    git clone https://github.com/YOUR-USERNAME/QubitLab.git
    ```
2.  ```bash
    cd QubitLab
    ```

If you're using **SSH authentication** (recommended for regular contributors with SSH keys configured), run:

1.  ```bash
    git clone git@github.com:YOUR-USERNAME/QubitLab.git
    ```
2.  ```bash
    cd QubitLab
    ```

Replace `YOUR-USERNAME` with your actual GitHub username. For example, if your username is `quantumdev`, the HTTPS URL would be `https://github.com/quantumdev/QubitLab.git`. The clone command downloads all project files and git history to your local machine, creating a directory named `QubitLab` containing the complete project.

### Step 3: Configure Upstream Remote

To keep your fork synchronized with the main QubitLab repository, you need to add the original repository as an "upstream" remote. This allows you to pull in the latest changes from the main project and incorporate them into your fork. From within your local `QubitLab` directory, execute:

```bash
git remote add upstream https://github.com/IVerse-VDV/QubitLab.git
```

This command adds a new remote called `upstream` pointing to the main QubitLab repository. Now your local repository knows about two remotes: `origin` (your personal fork) and `upstream` (the main project). You can verify this configuration by running:

```bash
git remote -v
```

You should see output similar to:

```
origin    https://github.com/YOUR-USERNAME/QubitLab.git (fetch)
origin    https://github.com/YOUR-USERNAME/QubitLab.git (push)
upstream  https://github.com/IVerse-VDV/QubitLab.git (fetch)
upstream  https://github.com/IVerse-VDV/QubitLab.git (push)
```

This confirms that both remotes are configured correctly.

### Step 4: Create a Virtual Environment

Python virtual environments isolate project dependencies from your system Python installation, preventing conflicts between different projects that might require different versions of the same packages. Creating a virtual environment is a best practice for all Python development. From your `QubitLab` directory, create and activate a virtual environment using the following commands.

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS or Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

The first command creates a new virtual environment in a directory named `venv` within your project directory. The second command activates the virtual environment. After activation, your terminal prompt should display `(venv)` at the beginning, indicating that the virtual environment is active. All subsequent `pip` commands will install packages into this isolated environment rather than globally on your system.

When you're done working on Qubitlab and want to exit the virtual environment, simply run `deactivate` in your terminal. You'll need to reactivate the environment using `source venv/bin/activate` (or `venv\Scripts\activate` on Windows) each time you return to work on the project.

### Step 5: Install Project Dependencies

With your virtual environment activated, install all required Python packages using the provided requirements file. This ensures you have the exact versions of dependencies that QubitLab requires:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

The first command upgrades pip itself to the latest version, which is good practice to ensure compatibility with new package formats. The second command reads `requirements.txt` and installs all listed packages: Qiskit, Qiskit-Aer, Streamlit, Plotly, NumPy, and Matplotlib. This process may take several minutes depending on your internet connection, as some packages like NumPy and Qiskit are quite large.

If you encounter installation errors, ensure you're using Python 3.8 or higher (`python --version` or `python3 --version`) and that your pip is up to date. On some systems, you might need additional system-level dependencies for packages like NumPy or Matplotlib. Consult the error messages for specific guidance, and dont hesitate to ask for help in [GitHub Discussions](https://github.com/IVerse-VDV/QubitLab/discussions) if you encounter persistent problems.

### Step 6: Verify Your Installation

Test that everything is installed correctly and the application runs properly by starting the Streamlit development server:

```bash
streamlit run app.py
```

Streamlit should launch a local web server (typically at `http://localhost:8501`) and automatically open your default web browser to display the QubitLab application. If the browser doesn't open automatically, check your terminal for the URL and open it manually. If the application loads successfully and you can interact with it, selecting qubits, adding gates, viewing visualizations, your development environment is properly configured and ready for development.

If you encounter errors when running the application, check that all dependencies installed successfully, verify that you're using a compatible Python version, ensure your virtual environment is activated (you should see `(venv)` in your terminal prompt), and review any error messages carefully. Common issues include missing dependencies (re-run `pip install -r requirements.txt`), Python version incompatibility (ensure Python 3.8+), or port conflicts (if port 8501 is in use, Streamlit will try another port automatically).

### Step 7: Create a Development Branch

Before making any changes to the code, create a new Git branch for your work. Never make changes directly on the `main` branch, as this makes it difficult to manage multiple contributions and keep your fork synchronized with upstream changes. Use descriptive branch names that indicate what you're working on:

```bash
git checkout -b feature/rotation-gates
```

or

```bash
git checkout -b fix/bloch-sphere-rendering
```

Use prefixes like `feature/` for new features, `fix/` for bug fixes, `docs/` for documentation changes, `refactor/` for code restructuring without functional changes, or `test/` for adding or modifying tests. This naming convention makes it easier for maintainers to understand the purpose of your pull request at a glance.

For example, if you're adding parametric rotation gates, you might create a branch named `feature/add-rx-ry-rz-gates`. If you're fixing a rendering bug in the Bloch sphere visualization, use `fix/bloch-sphere-axis-labels`. If you're improving README documentation, use `docs/improve-installation-guide`.

## Development Workflow

Understanding the typical development workflow helps you contribute efficiently and avoid common pitfalls. This section describes the standard process for making changes, testing them, and preparing them for submission.

### Syncing with Upstream

Before starting new work, always sync your fork with the latest changes from the main QubitLab repository. This prevents merge conflicts and ensures you're working with the most recent code. From your local repository with your virtual environment activated:

```bash
# Fetch latest changes from upstream
git fetch upstream

# Switch to your main branch
git checkout main

# Merge upstream changes into your main branch
git merge upstream/main

# Push updated main branch to your fork
git push origin main
```

This sequence fetches all changes from the main repository, merges them into your local `main` branch, and updates your fork on GitHub. Perform this sync operation regularly, especially before creating new branches or submitting pull requests.

### Making Changes

Once you've created a development branch and synchronized with upstream, you can begin making your changes. Open the relevant files in your preferred code editor or IDE. We recommend using editors with Python support like [Visual Studio Code](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/), or [Sublime Text](https://www.sublimetext.com/) for the best development experience.

As you work, follow our [coding guidelines](#coding-guidelines-and-standards) and maintain consistency with existing code style. Write clear, descriptive commit messages for each logical unit of work. For example:

```bash
git add gates.py
git commit -m "feat: add Rx, Ry, Rz rotation gates with angle parameters"

git add utils.py
git commit -m "feat: add Bloch vector calculation for rotation gates"

git add app.py
git commit -m "feat: add UI controls for rotation angle selection"
```

Make small, focused commits rather than large commits that change many unrelated things. This makes code review easier and allows reverting specific changes if needed. Use conventional commit message prefixes: `feat:` for features, `fix:` for bug fixes, `docs:` for documentation, `refactor:` for code restructuring, `test:` for tests, and `style:` for formatting changes.

### Testing Locally

Before submitting changes, test them thoroughly in your local development environment. Run the Streamlit application and verify that your changes work as expected:

```bash
streamlit run app.py
```

Test with different configurations: try 1, 2, and 3 qubit circuits, apply various gate combinations, verify visualizations render correctly, check that existing functionality still works (regression testing), and test edge cases and error conditions. If you're adding new features, test them comprehensively with different inputs. If you're fixing bugs, verify that the bug is actually fixed and hasn't been replaced with a new issue.

Pay special attention to the quantum mechanics correctness of any changes involving gate implementations or calculations. Compare your results with known quantum states or use Qiskit's built-in verification tools to ensure mathematical accuracy. Incorrect quantum mechanics calculations can silently produce wrong results without obvious errors.

## Code Architecture and File Functions

Understanding how QubitLab's code is organized and what each file does is essential for effective contribution. This section provides detailed explanations of each file's purpose and internal structure.

### app.py - Main Application File

- `app.py` file is the entry point for the QubitLab application and contains all Streamlit UI code. When you run `streamlit run app.py`, this file executes and creates the interactive web interface. Understanding its structure helps you modify UI elements or add new visualizations.

- file begins with imports of all necessary libraries and our custom modules (`gates` and `utils`). It then calls `st.set_page_config()` to configure the Streamlit page with a title, icon, and layout preferences. The `main()` function contains all application logic and is called when the script runs. This function is organized into several sections that handle different aspects of the UI.

- **sidebar section** creates the left sidebar with controls for selecting the number of qubits, choosing gates, specifying gate parameters (like target qubits or control/target pairs), and adding gates to the circuit sequence. It uses Streamlit's `st.sidebar` context manager to place all these controls in the sidebar. Session state (`st.session_state`) maintains the current gate sequence across page refreshes, as Streamlit re-runs the entire script on every interaction.

- **circuit building section** uses the gate sequence from session state to call `create_circuit()` from `gates.py`, generating a Qiskit `QuantumCircuit` object. It then displays circuit statistics using `st.metric()` widgets showing qubit count, depth, gate count, and operation types. The circuit diagram is rendered using Qiskit's `circuit_drawer()` function with matplotlib output, displayed via `st.pyplot()`.

- **visualization section** adapts based on the number of qubits. For 1 qubit, it calls `statevector_to_bloch_vector()` and `plot_bloch_sphere_plotly()` from `utils.py` to create an interactive Bloch sphere. For 2 qubits, it computes reduced density matrices via `get_single_qubit_density_matrices()` and displays two Bloch spheres side by side. For 3 qubits, it uses `plot_state_city_big_endian()` to show amplitude bar charts.

- **results section** displays the statevector, probability distribution, and measurement histogram. It calls `run_circuit()` to execute the simulation, `calculate_probabilities()` to compute measurement probabilities, `format_statevector()` to prepare amplitudes for display, and `get_measurement_counts()` to simulate measurements. Results are presented in columns using `st.columns()` for side-by-side layouts.

- The **footer section** displays attribution and project information at the bottom of the page. If you're adding new UI elements, you'll work primarily in this file, integrating your visualization code with the existing Streamlit layout.

**Summary `app.py`** (Main Application)
- Implements the Streamlit user interface
- Handles user interactions and input validation
- Orchestrates circuit building and simulation
- Renders all visualizations
- Manages session state for circuit persistence
- Coordinates between gates.py and utils.py modules


### gates.py - Quantum Gate Definitions
- `gates.py` module encapsulates all quantum gate operations and circuit construction logic. It provides a clean abstraction over Qiskit's circuit API, making it easier to add gates programmatically based on user selections. Understanding this file is crucial if you're implementing new quantum gates or modifying how circuits are constructed.

- file defines individual functions for each quantum gate. For example, `apply_hadamard(circuit, qubit)` applies a Hadamard gate to the specified qubit on the given circuit object. Similarly, `apply_pauli_x(circuit, qubit)`, `apply_cnot(circuit, control, target)`, and other functions encapsulate specific gate operations. Each function is documented with a docstring explaining its parameters and behavior.

- `AVAILABLE_GATES` dictionary maps qubit counts to lists of available gates. For 1 qubit, only single-qubit gates like H, X, Y, Z, S, and T are available. For 2 qubits, multi-qubit gates like CNOT and SWAP are added. For 3 qubits, the Toffoli gate becomes available. This dictionary is used by `app.py` to populate the gate selection dropdown dynamically based on the chosen number of qubits.

- `create_circuit(num_qubits, gate_sequence)` function is the core circuit builder. It takes the number of qubits and a list of gate specifications, creates a `QuantumCircuit` object, iterates through the gate sequence, and applies each gate by calling the appropriate gate function. Finally, it calls `circuit.save_statevector()` to ensure the statevector is saved during simulation. This function bridges user selections from the UI with Qiskit circuit construction.

- `get_gate_description(gate_name)` function returns human-readable descriptions of each gate for display in the UI. These descriptions help users understand what each gate does without requiring deep quantum mechanics knowledge.

- When adding new gates, you'll add a new gate application function, update `AVAILABLE_GATES` to include the new gate for appropriate qubit counts, add a case in `create_circuit()` to handle the new gate, and add a description in `get_gate_description()`. For example, to add an Rx rotation gate, you would define `apply_rx(circuit, qubit, angle)`, add 'Rx' to the available gates lists, handle 'Rx' in the create_circuit switch statement, and provide a description explaining the X-axis rotation.

**Summary `gates.py`** (Quantum Gates Module)
- Defines individual gate application functions
- Implements `create_circuit()` for building complete circuits
- Exports `AVAILABLE_GATES` dictionary mapping qubit counts to valid gates
- Provides `get_gate_description()` for user-friendly gate explanations
- Handles gate parameter validation

### utils.py - Utility Functions

- `utils.py` module contains all the "behind the scenes" functionality that supports the main application without directly interacting with users. This includes quantum simulation, mathematical calculations, data transformations, and visualization generation. Understanding this file is essential for improving simulation accuracy, optimizing performance, or enhancing visualizations.

- file is organized into several functional areas. **Simulation functions** handle running quantum circuits and extracting results. The `run_circuit(circuit, shots)` function takes a Qiskit circuit, gets the Aer simulator backend, runs the circuit using the new `backend.run()` API, and returns the statevector and result object. This is where we interface with Qiskit's simulation engine, so any simulation-related improvements would modify this function.

- **Endianness conversion functions** handle the translation between Qiskit's little-endian notation and our user-friendly big-endian notation. The `reverse_bitstring(bitstring)` function simply reverses a string of bits. The `convert_counts_to_big_endian(counts)` and `convert_probs_to_big_endian(probabilities)` functions convert dictionaries with bitstring keys from little-endian to big-endian. These functions are called throughout the codebase to ensure all outputs use consistent big-endian notation.

- **Probability calculation functions** compute measurement probabilities from statevectors. The `calculate_probabilities(statevector)` function iterates through the statevector, converts indices to binary strings (and reverses them for big-endian), computes probability as |amplitude|², and returns a dictionary mapping basis states to probabilities. The `format_statevector(statevector, threshold)` function similarly processes statevectors but returns formatted tuples of (basis_state, amplitude, probability) for display, filtering out near-zero amplitudes below a threshold to reduce clutter.

- **Bloch vector calculation functions** convert quantum states to geometric Bloch sphere coordinates. The `statevector_to_bloch_vector(statevector)` function handles single-qubit states directly, extracting amplitudes α and β, and computing x, y, z coordinates using the formulas x = 2·Re(α*β), y = 2·Im(α*β), and z = |α|² - |β|². The `density_matrix_to_bloch_vector(density_matrix)` function handles general 2×2 density matrices (including mixed states from entanglement) by computing traces with Pauli matrices: x = Tr(ρσₓ), y = Tr(ρσᵧ), z = Tr(ρσᵤ).

- **Density matrix functions** support multi-qubit entanglement visualization. The `statevector_to_density_matrix(statevector)` function converts a statevector |ψ⟩ to its density matrix representation ρ = |ψ⟩⟨ψ|. The `partial_trace(density_matrix, keep_qubit, num_qubits)` function is mathematically complex but crucial, it computes the reduced density matrix for a single qubit by tracing out all other qubits, enabling individual qubit visualization even in entangled multi-qubit states. The `get_single_qubit_density_matrices(statevector, num_qubits)` function orchestrates this process, converting the full statevector to a density matrix and then computing partial traces for each qubit.

- **Visualization functions** generate all the visual outputs. The `plot_bloch_sphere_plotly(bloch_vector, title)` function creates interactive 3D Bloch spheres using Plotly's graph objects API. It constructs the sphere surface using parametric equations, adds meridians and equator as guide lines, draws X/Y/Z axes with appropriate colors and labels, places the Bloch vector as a 3D arrow with a cone arrowhead, adds state labels for common basis states, and configures camera angles and interactivity settings. This function returns a Plotly figure object that Streamlit renders with `st.plotly_chart()`.

- The `plot_state_city_big_endian(statevector, num_qubits, title)` function handles 3-qubit visualization. It first reorders the statevector from little-endian to big-endian using `reorder_statevector_to_big_endian()`, then creates a 3D bar chart using Matplotlib's `bar3d` method. Real components are plotted as red bars, imaginary components as blue bars, and basis states are labeled along the X-axis in big-endian order. This ensures the visualization matches user expectations for qubit ordering.

- **Helper functions** provide various utility capabilities. The `format_complex_number(complex_num)` function converts complex numbers to readable strings, handling pure real, pure imaginary, and mixed cases appropriately. The `get_measurement_counts(circuit, shots)` function simulates actual measurements by adding `measure_all()` to a circuit copy, running it, extracting counts, and converting them to big-endian. The `get_circuit_stats(circuit)` function extracts metadata like qubit count, depth, size, and gate counts for display in the UI.

- When working in `utils.py`, pay careful attention to mathematical correctness, especially in Bloch vector calculations and partial traces. These functions implement quantum mechanics formulas that must be exact. Test thoroughly with known quantum states to verify accuracy. For example, |0⟩ should yield Bloch vector (0, 0, 1), |+⟩ should yield (1, 0, 0), and |+i⟩ should yield (0, 1, 0).

**Summary `utils.py`** (Utilities Module)
- `run_circuit()`: Executes circuits using Qiskit Aer simulator
- `calculate_probabilities()`: Computes measurement probabilities from statevectors
- `format_statevector()`: Formats complex [amplitudes](https://en.wikipedia.org/wiki/Probability_amplitude) for display
- `get_measurement_counts()`: Simulates measurements and returns counts
- `statevector_to_bloch_vector()`: Converts single qubit states to Bloch coordinates
- `density_matrix_to_bloch_vector()`: Converts density matrices to Bloch vectors
- `partial_trace()`: Computes reduced density matrices for individual qubits
- `plot_bloch_sphere_plotly()`: Creates interactive 3D Bloch sphere visualizations
- `plot_state_city_big_endian()`: Generates 3D amplitude bar charts
- `reorder_statevector_to_big_endian()`: Converts Qiskit [Little-endian](https://en.wikipedia.org/wiki/Endianness) to [Big-endian](https://en.wikipedia.org/wiki/Endianness)
- Helper functions for formatting and data conversion

### requirements.txt - Dependency Specification

- `requirements.txt` file lists all Python packages required to run QubitLab along with version constraints. This file follows the standard pip requirements format where each line specifies a package and optional version constraint. Understanding this file helps you manage dependencies when adding new functionality.

Current dependencies are specified as follows:

```
qiskit>=1.0.0
qiskit-aer>=0.13.0
streamlit>=1.28.0
plotly>=5.17.0
matplotlib>=3.7.0
numpy>=1.24.0
```

The `>=` operator means "install this version or any newer compatible version." This approach balances stability (we know these versions work) with flexibility (contributors get bug fixes automatically). When adding new dependencies, use `>=` with the minimum version you've tested. Avoid overly restrictive constraints like `==` (exact version) unless absolutely necessary for compatibility.

If you need to add a dependency, add it to `requirements.txt` with an appropriate version constraint, document why it's needed in your pull request description, and verify that it doesn't conflict with existing dependencies by testing in a clean virtual environment. For example, if you're adding support for quantum error correction and need the `qiskit-ignis` package, you would add `qiskit-ignis>=0.7.0` and explain in your PR that it provides quantum error correction circuit building utilities.

Consider dependency size and installation complexity when adding new requirements. Prefer lightweight packages over heavy ones when alternatives exist. Ensure added packages are actively maintained and have permissive licenses compatible with our MIT license. Check that packages work on all major platforms (Windows, macOS, Linux).

## Coding Guidelines and Standards

Maintaining consistent code quality and style is essential for collaborative software development. These guidelines ensure that all contributors write code that is readable, maintainable, and consistent with the existing codebase. Following these standards makes code review faster and reduces the likelihood of bugs.

### Python Style Guide

QubitLab follows [PEP 8](https://pep.python.org/pep-0008/), the official Python style guide. PEP 8 covers naming conventions, code layout, whitespace usage, and commenting practices. Key PEP 8 principles relevant to QubitLab include using 4 spaces for indentation (never tabs), limiting lines to 79 characters for code and 72 for comments/docstrings (we allow up to 100 for code if it improves readability), using blank lines to separate functions and classes (2 blank lines before top-level definitions, 1 before methods), and surrounding operators with single spaces (`x = 1` not `x=1`).

For naming conventions, use `snake_case` for functions and variables (`calculate_bloch_vector`, `statevector_data`), `PascalCase` for class names (`QuantumVisualizer`, `BlochSphere`), `UPPER_CASE` for constants (`MAX_QUBITS`, `DEFAULT_SHOTS`), and descriptive names that clearly indicate purpose. Avoid single-letter variable names except for common mathematical variables (i, j for indices, x, y, z for coordinates).

### Code Organization

Structure your code logically within files. Group related functions together, place helper functions near the functions that use them, and order functions from high-level to low level (main logic first, helpers below). Add section comments to delineate functional areas within large files. For example, in `utils.py`, comments like `# Simulation functions`, `# Bloch vector calculations`, and `# Visualization functions` help navigate the file.

Keep functions focused and short. Each function should do one thing well. If a function exceeds 50 lines, consider breaking it into smaller helper functions. Single Responsibility Principle applies: each function, class, or module should have one clear purpose. When you find yourself using "and" to describe what a function does, it probably should be split.

### Documentation Standards

Every function, class, and module must have a docstring explaining its purpose, parameters, return values, and any exceptions it might raise. QubitLab uses [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for consistency. A well-documented function looks like this:

```python
def calculate_probabilities(statevector):
    """
    Calculate measurement probabilities from quantum statevector.
    
    Converts a quantum statevector to a dictionary mapping basis states
    (in big-endian notation) to measurement probabilities. Probability
    for each state is computed as |amplitude|².
    
    Args:
        statevector: NumPy array representing quantum state amplitudes.
                    Length must be 2^n for n qubits.
    
    Returns:
        dict: Dictionary mapping basis state strings ('01', '10')
              to float probabilities. All probabilities sum to 1.0.
    
    Raises:
        ValueError: If statevector length is not a power of 2.
    
    Example:
        >>> sv = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
        >>> probs = calculate_probabilities(sv)
        >>> probs
        {'0': 0.5, '1': 0.5}
    """
    # Implementation here :)
```

Include a brief one line summary, a more detailed explanation if needed, comprehensive parameter documentation with types and descriptions, return value documentation including type and meaning, exceptions that might be raised with conditions, and optional usage examples for complex functions.

Add inline comments to explain complex logic, mathematical formulas, or non-obvious implementation decisions. Comments should explain *why* code does something, not *what* it does (the code itself shows what). Good comment: `# Use partial trace to compute reduced density matrix for entangled qubits`. Bad comment: `# Loop through indices` (obvious from code).

### Type Hints

Use Python type hints to document expected types for function parameters and return values. Type hints improve code readability, enable better IDE autocomplete and error checking, and serve as inline documentation. Here an example with type hints:

```python
from typing import List, Tuple, Dict
import numpy as np

def format_statevector(
    statevector: np.ndarray,
    threshold: float = 1e-10
) -> List[Tuple[str, complex, float]]:
    """
    Format statevector for display, filtering near-zero amplitudes.
    
    Args:
        statevector: Quantum statevector as NumPy array
        threshold: Minimum amplitude magnitude to include
    
    Returns:
        List of tuples containing (basis_state, amplitude, probability)
    """
    # Implementation here
```

Use built-in types (`str`, `int`, `float`, `bool`, `list`, `dict`) when possible. Import complex types from the `typing` module (`List`, `Dict`, `Tuple`, `Optional`, `Union`). For NumPy arrays, use `np.ndarray`. For Qiskit objects, use their full type names like `qiskit.QuantumCircuit`.

### Quantum Computing Specifics

When implementing quantum gates or algorithms, ensure mathematical correctness by comparing against Qiskit documentation, quantum computing textbooks (like Nielsen & Chuangs "Quantum Computation and Quantum Information"), or research papers. Include references in docstrings when implementing algorithms from papers. For example:

```python
def apply_grover_diffusion(circuit: QuantumCircuit, qubits: List[int]) -> None:
    """
    Apply Grover diffusion operator to specified qubits.
    
    Implements the diffusion operator D = 2|s⟩⟨s| - I where |s⟩ is the
    equal superposition state. This operator amplifies amplitude of marked
    states in Grover's search algorithm.
    
    Reference:
        Grover, L.K. (1996). A fast quantum mechanical algorithm for
        database search. Proceedings of STOC 1996, 212-219.
    
    Args:
        circuit: Quantum circuit to modify
        qubits: List of qubit indices to apply diffusion to
    """
    # Implementation
```

Maintain the big-endian convention consistently. When converting between Qiskit's little-endian and our big-endian, use the conversion functions in `utils.py`. Never hardcode bit reversals, use `reverse_bitstring()` and related functions. Test edge cases like all |0⟩ states, all |1⟩ states, maximally entangled states, and states with complex phases to ensure correctness across diverse quantum states.

### Testing Best Practices

While QubitLab doesnt currently have a comprehensive automated test suite, we encourage contributors to write tests for new functionality. When adding features, create test functions that verify correct behavior, include tests for edge cases and error conditions, and document expected behavior in test docstrings. Use descriptive test function names like `test_hadamard_creates_superposition()` or `test_cnot_generates_bell_state()`.

For quantum functionality, verify against known results. For example, test that applying Hadamard to |0⟩ produces |+⟩ with correct amplitudes, CNOT on |+⟩|0⟩ produces Bell state |Φ+⟩, and Pauli-X flips |0⟩ to |1⟩ exactly. Use `np.allclose()` for floating-point comparisons to handle numerical precision issues:

```python
import numpy as np

def test_hadamard_superposition():
    """Verify Hadamard gate creates equal superposition."""
    circuit = QuantumCircuit(1)
    circuit.h(0)
    circuit.save_statevector()
    
    result = run_simulation(circuit)
    statevector = result['statevector']
    
    expected = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    assert np.allclose(statevector, expected), \
        f"Expected {expected}, got {statevector}"
```

## Testing Your Changes

Thorough testing is crucial before submitting contributions. This section describes how to test your changes effectively to ensure they work correctly and dont break existing functionality.

### Manual Testing Checklist

Before submitting a pull request, run through this manual testing checklist. Start the application with `streamlit run app.py` and systematically test functionality:

**Basic Functionality:**
- Test with 1, 2, and 3 qubits separately
- Add various gates and verify circuit diagram updates correctly
- Verify gate sequence displays accurately in sidebar
- Test deleting individual gates and clearing all gates
- Change measurement shots and verify simulation re-runs

**Visualization Verification:**
- For 1 qubit: Verify Bloch sphere renders, can be rotated with mouse, shows correct state vector direction, and displays accurate X/Y/Z components
- For 2 qubits: Verify both Bloch spheres render side by side, each can be rotated independently, entanglement indicator works (vector length < 1 for entangled states), and individual qubit states are labeled correctly
- For 3 qubits: Verify state city renders with 8 basis states, bars show real (red) and imaginary (blue) components separately, basis states are labeled in big-endian order, and all non-zero amplitudes are visible

**Results Accuracy:**
- Verify statevector displays with correct complex numbers
- Check probability distribution sums to 1.0
- Confirm measurement histogram matches theoretical probabilities (within statistical variation)
- Test that big endian notation is consistent across all outputs

**Known Quantum States:**
- Test |0⟩ state (initial state, no gates): Expect Bloch vector at +Z (north pole), 100% probability for |0⟩
- Test Hadamard on |0⟩: Expect Bloch vector at +X, 50/50 probability for |0⟩ and |1⟩
- Test Pauli-X on |0⟩: Expect Bloch vector at -Z (south pole), 100% probability for |1⟩
- Test Bell state (H on q0, CNOT(0→1)): Expect both Bloch spheres showing mixed states, only |00⟩ and |11⟩ with 50% each

### Regression Testing

Regression testing ensures your changes dont break existing functionality. After making changes, test workflows that worked before to verify they still work. Run through common use cases like creating superposition, generating entanglement, and applying multiple gates in sequence. If you modified a specific file, pay extra attention to functionality in that area (if you changed `gates.py`, thoroughly test all gate operations).

### CrossP latform Testing

If possible, test on different platforms. QubitLab should work on Windows, macOS, and Linux. While we dont require contributors to test on all platforms, being aware of platform specific issues helps. Common platform differences include file path separators (use `os.path.join()` instead of hardcoding `/` or `\`), line endings (CRLF vs LF, let Git handle this with `.gitattributes`), and font rendering (text might appear differently on different OS).

### Browser Testing

Since QubitLab runs in web browsers, test in at least your primary browser. The application should work in Chrome, Firefox, Safari, and Edge. Plotly visualizations are WebGL-based and should work across new browsers. If you notice visualization issues in specific browsers, note them in your pull request description.

## Submitting Pull Requests

When your changes are ready and thoroughly tested, its time to submit a pull request to merge your work into the main QubitLab repository. Following this process ensures smooth code review and integration.

### Pre Submission Checklist

Before submitting your pull request, verify you've completed these steps:

- [ ] All changes are committed with clear, descriptive commit messages
- [ ] Code follows PEP 8 style guidelines and QubitLab conventions
- [ ] All new functions have comprehensive docstrings
- [ ] Type hints are included for function signatures
- [ ] Manual testing completed successfully across different qubit counts
- [ ] No console errors or warnings when running the application
- [ ] Big-endian convention maintained throughout
- [ ] Qiskit new API (`backend.run()`) used, not deprecated `execute()`
- [ ] Documentation updated if adding features or changing behavior
- [ ] No unnecessary files committed (check `.gitignore`)

### Syncing with Upstream

Before submitting, sync yur branch with the latest upstream changes to avoid merge conflicts from your feature branch:

```bash
# Fetch latest upstream changes
git fetch upstream

# Rebase your branch onto upstream/main
git rebase upstream/main

# If conflicts occur, resolve them, then continue rebase
git add <resolved-files>
git rebase --continue

# Force push to your fork (rebase rewrites history)
git push origin your-feature-branch --force
```

Rebasing replays your commits on top of the lateest main branch, creating a clean, linear history. If you encounter conflicts during rebase, Git will pause and show which files conflict. Edit those files to resolve conflicts (look for `<<<<<<<`, `=======`, `>>>>>>>` markers), remove the conflict markers, add the resolved files, and continue the rebase. If the rebase becomes too complex, you can abort with `git rebase --abort` and ask for help in GitHub Discussions.

### Pushing Your Branch

Push your branch to your fork on GitHub:

```bash
git push origin your-feature-branch
```

If you previously pushed this branch and then rebased, you all need to force push (as shown in the sync section above). Force pushing is safe for feature branches in your own fork, but never force push to shared branches or the main repository.

### Creating the Pull Request

navigate to the main QubitLab repository at [https://github.com/IVerse-VDV/QubitLab](https://github.com/IVerse-VDV/QubitLab). GitHub will usually show a banner suggesting you create a pull request from your recently pushed branch. Click "Compare & pull request." If you dont see this banner, click "Pull requests" then "New pull request", select "compare across forks", choose your fork and branch as the source, and the main repositorys `main` branch as the target.

**Pull Request Title:** Use a clear, descriptive title following conventional commit format. Examples include "feat: Add Rx, Ry, Rz rotation gates with angle parameters", "fix: Correct Bloch vector Y axis calculation for phase states", "docs: Improve installation instructions in README", or "refactor: Simplify density matrix partial trace computation". The title should be concise but informative enough that someone can understand what the PR does without reading the description.

**Pull Request Description:** Provide a comprehensive description using this template:

```markdown
## Description
Brief summary of what this PR does and why.

## Changes Made
- Detailed list of changes
- Include modified files and their purposes
- Explain design decisions

## Testing Performed
- Describe how you tested these changes
- List specific test cases or scenarios
- Include screenshots for UI changes

## Related Issues
Fixes #123 (if applicable)
Closes #456 (if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tested with 1, 2, and 3 qubits
- [ ] Big-endian convention maintained
- [ ] new Qiskit API used
```

For UI changes or new visualizations, include screenshots or short screen recordings showing the new functionality. GitHub supports drag-and-drop for images and GIF animations. Visual demonstrations help reviewers understand your changes quickly and provide better feedback.

If your PR addresses an existing issue, reference it using `Fixes #123` or `Closes #123`. GitHub automatically links the PR to the issue and closes the issue when the PR is merged. Use "Fixes" for bug fixes and "Closes" for feature implementations or other resolutions.

### The Review Process

After submitting your pull request, maintainers will review your code. This process typically involves examining code quality, verifying quantum mechanics correctness, checking consistency with project architecture, evaluating documentation completeness, and assessing adherence to coding guidelines. Reviews may take several days depending on maintainer availability and PR complexity. Be patient and responsive.

Maintainers may request changes or ask questions. When they do, engage constructively by responding promptly to review comments, making requested changes in new commits (dont force push during review), and asking for clarification if feedback is unclear. Push additional commits to your branch to address feedback:

```bash
# Make requested changes in your code
git add <modified-files>
git commit -m "refactor: simplify Bloch vector calculation per review"
git push origin your-feature-branch
```

GitHub automatically updates the pull request with new commits. Once reviewers approve your changes, a maintainer will merge your PR into the main repository. Congratulations! Your contribution is now part of QubitLab. After your PR is merged, you can delete your feature branch locally and on your fork:

```bash
# Delete local branch
git branch -d your-feature-branch

# Delete remote branch on your fork
git push origin --delete your-feature-branch
```

Then sync your fork's main branch with upstream and start a new branch for your next contribution.

## Reporting Issues

If you encounter bugs, have feature requests, or find documentation problems, please report them using [GitHub Issues](https://github.com/IVerse-VDV/QubitLab/issues). Well-written issue reports help maintainers understand and address problems efficiently.

### Before Creating an Issue

Before opening a new issue, search existing issues to see if someone already reported the same problem or suggested the same feature. If you find an existing issue, add a comment with additional information or a "+1" to indicate you're also affected. Avoid creating duplicate issues, as they fragment discussion and make tracking difficult.

### Creating a Bug Report

Navigate to the issues page and click "New Issue." Select "Bug Report" if a template is available, or create a descriptive title and fill in the following information:

**Title:** Clear, concise description of the problem. Good example: "Bloch sphere renders incorrectly for |+i⟩ state". Bad example: "Visualization bug" (too vague).

**Description:** Explain what's wrong and what you expected to happen. Be specific about the discrepancy between expected and actual behavior.

**Reproduction Steps:** Provide a numbered, detailed list of exact steps to reproduce the bug:
1. Open QubitLab application
2. Select 1 qubit
3. Add Hadamard gate to q0
4. Add S gate to q0
5. Observe Bloch sphere shows vector at (0.5, 0.5, 0) instead of (0, 1, 0)

**Environment Information:**
- Operating System: (Windows 11, macOS 13.0, Ubuntu 22.04)
- Python Version: (run `python --version`)
- Browser and Version: (Chrome 119, Firefox 120)
- Qiskit Version: (run `pip show qiskit`)
- Running locally or deployed: (local development server)

**Screenshots/Videos:** If applicable, include screenshots showing the problem, error messages, or unexpected behavior. For complex UI issues, a short screen recording can be very helpful.

**Error Messages:** If you see error messages in the terminal or browser console, copy and paste them exactly as they appear. Include the full stack trace if available.

### Creating a Feature Request

For feature requests, provide the following information:

**Use Case:** Describe the problem or need that motivates the feature request. Explain what you're trying to accomplish and why current functionality doesn't meet your needs. Good feature requests solve real problems.

**Proposed Solution:** Explain how you envision the feature working. Be as specific as possible about UI changes, new functions, or behavior modifications. If you have mockups or examples from other tools, include them.

**Alternatives Considered:** Discuss any alternative approaches you've considered and why they're insufficient. This shows you've thought through the problem and helps maintainers understand your reasoning.

**Additional Context:** Provide any other relevant information, such as related research papers, similar features in other quantum computing tools, or technical considerations for implementation.

### Issue Etiquette

When creating or commenting on issues, be respectful and constructive, provide complete information to help others understand the problem, stay on topic (use separate issues for separate problems), and update issues if you find new information or solve the problem yourself. If you submit an issue and later figure out a solution, post the solution and close the issue, this helps future users who encounter the same problem.

## Documentation Standards

Good documentation is as important as good code. QubitLab documentation helps users understand how to use the application and helps contributors understand how to extend it. When contributing, ensure documentation stays current and comprehensive.

### README.md Updates

The [README.md](README.md) file is the primary documentation for QubitLab. When adding features, update the README to include usage instructions, examples demonstrating the new feature, and explanations of any new concepts. When changing behavior, update relevant sections to reflect the changes. Keep the README well-organized with clear headings, and use examples to illustrate complex concepts.

### Code Documentation

As discussed in [Coding Guidelines](#coding-guidelines-and-standards), all functions, classes, and modules must have comprehensive docstrings. Beyond docstrings, add inline comments for complex logic, non-obvious optimizations, mathematical formulas, or subtle quantum mechanics considerations. Comments should explain *why*, not *what*. For example:

```python
# Apply partial trace to compute reduced density matrix for individual
# qubit visualization in entangled systems. This is mathematically equivalent
# to measuring and discarding the other qubits.
reduced_dm = partial_trace(full_dm, keep_qubit, num_qubits)
```

### Tutorial and Example Content

When adding complex features, consider creating tutorial content or examples. This might include example circuits demonstrating the feature, step by step guides for common use cases, or explanations of underlying quantum mechanics concepts. Tutorial content can be added to the README or as separate markdown files in a `docs/` directory if it becomes extensive.

## Communication Channels

The QubitLab community uses several channels for different types of communication. Choosing the right channel ensures your message reaches the appropriate audience and gets timely responses.

### GitHub Issues

Use [GitHub Issues](https://github.com/IVerse-VDV/QubitLab/issues) for bug reports, feature requests, tracking specific tasks or enhancements, and discussing implementation details of proposed changes. Issues are best for concrete, actionable items that need to be tracked and resolved.

### GitHub Discussions

Use [GitHub Discussions](https://github.com/IVerse-VDV/QubitLab/discussions) for general questions about quantum computing or Qiskit, ideas and brainstorming that aren't yet concrete proposals, showing off projects built with QubitLab, and community conversations that dont fit as issues. Discussions are more informal and conversational than issues.

### Pull Request Comments

Pull request comment threads are for discussions about specific code changes, implementation approaches and design decisions, requesting clarification on review feedback, and collaborating on solutions to review concerns. Keep PR discussions focused on the changes in that PR.

### Communication Guidelines

Across all channels, be respectful, patient, and constructive. Remember that everyone is volunteering their time. Respond to others as you'd want to be treated. Provide context when asking questions, link to relevant code, explain what you've tried, and describe what you are trying to accomplish. Search before asking, many questions have been answered before. Use clear, descriptive titles for issues and discussions so others can find them easily.

## Recognition and Community

We deeply value all contributions to QubitLab, whether large or small. Every bug fix, feature addition, documentation improvement, and thoughtful code review makes the project better and helps advance quantum computing education worldwide.

### Contributor Recognition

Contributors who submit accepted pull requests will be acknowledged in our project documentation. We maintain a `CONTRIBUTORS.md file (or section in `README.md`) listing everyone who has contributed code, documentation, or other significant improvements. Significant or regular contributors may be invited to join the maintainer team with expanded responsibilities and privileges.

We believe in recognizing not just code contributions but all forms of participation. Helping others in discussions, improving documentation, reporting detailed bug reports, and providing thoughtful code reviews are all valuable contributions deserving recognition.

### Building Community

QubitLab depends on a welcoming, inclusive community where everyone feels comfortable contributing regardless of background or experience level. We encourage mentoring new contributors, celebrating successes and milestones, collaborating across disciplines (physicists, computer scientists, educators), and maintaining a positive, supportive atmosphere.

If you're new to open source, to quantum computing, or to Python development, dont hesitate to ask questions or request guidance. Our community members remember being beginners and are happy to help you learn and grow. Everyone has unique perspectives and skills to contribute, beginners often spot confusing documentation or UI issues that experts overlook.

## Questions and Support

If you have questions about contributing that arent answered in this comprehensive guide, several resources are available to help you:

**GitHub Discussions:** Post questions in our [Discussions forum](https://github.com/IVerse-VDV/QubitLab/discussions). Community members and maintainers monitor discussions and provide assistance.

**Issue Comments:** If you're working on a specific issue, ask questions in that issue's comment thread. Maintainers and other contributors can provide context and guidance.

**Documentation:** Review our [README.md](README.md) for usage instructions and project overview, check Qiskit's [official documentation](https://qiskit.org/documentation/) for quantum computing questions, consult Streamlit's [documentation](https://docs.streamlit.io/) for UI-related questions, and reference Plotly [graphing library docs](https://plotly.com/python/) for visualization questions.

We're committed to making contributing to QubitLab as smooth and welcoming as possible. Your questions help us improve this guide and our onboarding process, so dont hesitate to ask.

## Conclusion

Thank you for taking the time to read this comprehensive contributing guide. Your interest in contributing to QubitLab is greatly appreciated, and your efforts, whether fixing a typo, adding a feature, or improving visualizations, make a real difference in advancing quantum computing education.

QubitLab aims to demystify quantum computing through interactive visualization and hands on experimentation. By contributing, you're not just writing code, you're helping students understand superposition, enabling researchers to prototype algorithms quickly, inspiring educators with new teaching tools, and making quantum mechanics accessible to curious minds worldwide.

We look forward to your contributions and to collaborating with you in building the future of quantum computing education. Welcome to the QubitLab community!

---

**QubitLab** - Making quantum computing visual, interactive, and accessible.  
**Organization:** [IVerse-VDV](https://github.com/IVerse-VDV)  
**Repository:** [QubitLab](https://github.com/IVerse-VDV/QubitLab)  
**Documentation:** [README.md](README.md)  
**Code of Conduct:** [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

*Last Updated: 2025*
