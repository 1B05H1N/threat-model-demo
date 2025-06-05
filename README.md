# Secure Todo API with Threat Modeling

A secure Todo API built with Flask, featuring comprehensive security measures and automated threat modeling using OWASP PyTM.

## Features

### Security Features
- **Authentication**: Secure login/logout with session management
- **CSRF Protection**: Built-in CSRF token validation
- **Rate Limiting**: Protection against brute force attacks
- **Input Validation**: Form validation using Flask-WTF
- **Secure Headers**: Implementation of security headers
- **Environment Configuration**: Secure handling of sensitive data

### API Endpoints
- `GET /`: Landing page with API documentation
- `POST /login`: User authentication
- `POST /logout`: Session termination
- `GET /dashboard`: User dashboard
- `GET /todos`: List all todos
- `POST /todos`: Create a new todo
- `PUT /todos/<id>`: Update a todo
- `DELETE /todos/<id>`: Delete a todo

## Quick Start

1. Clone the repository:
   ```sh
   git clone https://github.com/1B05H1N/threat-model-demo.git
   cd threat-model-demo
   ```

2. Set up the virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```sh
   cp env.conf.example .env
   # Edit .env with your configuration
   ```

5. Run the application:
   ```sh
   make run
   ```

## Threat Model Diagrams

This project uses [OWASP PyTM](https://owasp.org/www-project-threat-model-automation/) to automatically generate threat model diagrams for the application.

### Data Flow Diagram (DFD)
- **File:** `dfd.png`
- **Purpose:** Visualizes the flow of data between different components and boundaries (e.g., User, API, Database) in the system. It helps identify trust boundaries and potential attack surfaces.

### Sequence Diagram
- **File:** `sequence.png`
- **Purpose:** Shows the sequence of interactions between actors and system components for various operations (such as login, todo management). This helps in understanding the order of operations and where security controls are applied.

### How to Regenerate the Diagrams
To regenerate the diagrams after making changes to the threat model:

```sh
make diagrams
```
This will:
- Run the threat model and output PlantUML and Graphviz code
- Generate `sequence.png` (sequence diagram)
- Generate `dfd.png` (data flow diagram)

### Why These Diagrams Matter
- **DFD**: Helps you and your team visualize trust boundaries, data stores, and the flow of sensitive information, which is essential for identifying and mitigating security risks.
- **Sequence Diagram**: Clarifies the order of operations and the involvement of security controls (like authentication, CSRF protection, and rate limiting) in each user interaction.

## Automated Threat Modeling

The project includes a GitHub Actions workflow that automatically generates and updates the threat model diagrams whenever changes are pushed to the repository.

### Workflow Features
- Runs on push to master and manual trigger
- Installs all required dependencies
- Generates sequence and data flow diagrams
- Automatically commits and pushes updated diagrams
- Uses GitHub's built-in token for secure authentication

### Manual Trigger
You can manually trigger the workflow from the GitHub Actions tab in your repository.

## Development

### Prerequisites
- Python 3.11+
- Graphviz
- PlantUML

### Testing
Run the test suite:
```sh
make test
```

### Code Style
The project follows PEP 8 guidelines. Use `make lint` to check code style.

## Security

### Environment Variables
Required environment variables:
- `SECRET_KEY`: Flask application secret key
- `ADMIN_USERNAME`: Admin user username
- `ADMIN_PASSWORD`: Admin user password

### Security Best Practices
1. Never commit `.env` file
2. Use strong, unique passwords
3. Keep dependencies updated
4. Review threat model regularly
5. Monitor security headers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OWASP PyTM](https://owasp.org/www-project-threat-model-automation/) for threat modeling automation
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Flask-WTF](https://flask-wtf.readthedocs.io/) for form validation
- [Flask-Limiter](https://flask-limiter.readthedocs.io/) for rate limiting

## Author

**1B05H1N** - [GitHub Profile](https://github.com/1B05H1N)
