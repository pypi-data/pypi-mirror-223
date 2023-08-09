# Developer Guide for Meeting Roles Manager

This guide provides information for developers who want to contribute to, extend, or modify the Meeting Roles Manager project. Here you will find details on the project structure, how to set up your development environment, coding standards, testing, and more.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Development Environment](#development-environment)
4. [Coding Standards](#coding-standards)
5. [Testing](#testing)
6. [Contributing](#contributing)
7. [License](#license)

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/meeting-roles-manager.git
    ```

2. Navigate to the project directory:

    ```bash
    cd meeting-roles-manager
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Project Structure

The project is structured as follows:

- `meeting_roles/`: Main package containing the application code.
  - `static/`: Static assets like CSS and JavaScript files.
  - `templates/`: HTML templates for rendering views.
- `tests/`: Unit tests for the application.
- `run.py`: Entry point script to start the application.

## Development Environment

- **Python Version**: The project uses Python 3.8 or higher.
- **Virtual Environment**: It is recommended to use a virtual environment like `venv` to isolate the project dependencies.

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) as the style guide for Python code.
- Write clear and meaningful variable, function, and class names.
- Include comments and documentation where necessary.
- Keep functions and methods concise, aiming for a single responsibility.

## Testing

- Use `pytest` for writing and running tests.
- Aim for good test coverage across modules.
- Write tests for any new functionality or bug fixes.

To run tests, execute the following command:

```bash
pytest tests/
```

## Contributing

- Fork the repository and create a new branch for your feature, enhancement, or bug fix.
- Follow the coding standards and write tests for your changes.
- Submit a pull request with a detailed description of your changes.

## License

The project is licensed under the AGPL. Please refer to the [LICENSE](LICENSE) file for more information.

---

This guide provides the basic information needed to get started with development on the Meeting Roles Manager project. Feel free to reach out to the maintainers or consult the existing documentation and codebase for more specific details. Happy coding!
