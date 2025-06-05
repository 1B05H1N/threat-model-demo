# Secure Todo API with Automated Threat Modeling

This project demonstrates a secure Todo API built with Flask, featuring automated threat modeling using OWASP PyTM and GitHub Actions. The application implements various security measures and best practices to protect against common web vulnerabilities.

## Quick Start

1. **Clone and Setup**:
   ```bash
   git clone https://github.com/1B05H1N/threat-model-demo.git
   cd threat-model-demo
   make setup
   ```

2. **Configure Environment**:
   ```bash
   cp env.conf.example .env
   # Edit .env with your secure values
   ```

3. **Run the Application**:
   ```bash
   make run
   ```

4. **Generate Threat Model**:
   ```bash
   make model
   ```

## Environment Configuration

1. **Setup Environment Variables**:
   ```bash
   # Copy the example configuration
   cp env.conf.example .env
   
   # Edit the .env file with your secure values
   nano .env  # or use your preferred editor
   ```

2. **Required Variables**:
   - `SECRET_KEY`: A secure random key for session security
   - `ADMIN_USERNAME`: Username for authentication
   - `ADMIN_PASSWORD`: Secure password for authentication

3. **Security Notes**:
   - Never commit the `.env` file to version control
   - Use different values for development and production
   - Rotate secrets regularly in production
   - Consider using a secrets manager in production

4. **Generating a Secure Secret Key**:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

## Features

### API Endpoints
- `GET /`: Landing page with API documentation
- `POST /login`: User authentication
- `POST /logout`: User logout
- `GET /dashboard`: User dashboard with todos
- `GET /todos`: List all todos
- `POST /todos`: Create a todo
- `PUT /todos/<id>`: Update a todo
- `DELETE /todos/<id>`: Delete a todo

### Security Features

1. **Authentication & Authorization**
   - Secure session management
   - Password hashing using Werkzeug
   - Protected routes requiring authentication
   - Environment variable-based credentials

2. **Input Validation & Sanitization**
   - Request payload validation
   - CSRF protection using Flask-WTF
   - Input sanitization for all endpoints

3. **Rate Limiting**
   - Login endpoint: 5 requests per minute
   - Todo endpoints: 10 requests per minute
   - Configurable limits per endpoint

4. **Data Protection**
   - HTTPS for all communications
   - Secure session configuration
   - Environment variable management
   - SQL injection prevention

5. **Threat Modeling**
   - Automated threat analysis using OWASP PyTM
   - Continuous security monitoring via GitHub Actions
   - Comprehensive data flow documentation
   - Security controls validation

## Project Structure

```
threat-model-demo/
├── src/
│   └── app.py              # Flask application
├── threatmodel/
│   └── model.py           # PyTM threat model
├── tests/
│   └── test_app.py        # Test suite
├── .github/
│   └── workflows/
│       └── threat-model.yml  # GitHub Actions workflow
├── requirements.txt       # Python dependencies
├── Makefile             # Build and run commands
├── env.conf.example     # Environment configuration template
└── README.md           # Project documentation
```

## Development

### Prerequisites
- Python 3.8+
- pip
- virtualenv
- make

### Setup Development Environment
```bash
# Create and activate virtual environment
make setup

# Install development dependencies
pip install -r requirements.txt

# Run tests
make test

# Start development server
make run
```

### Running Tests
```bash
# Run all tests
make test

# Run specific test file
python -m pytest tests/test_app.py

# Run with coverage
python -m pytest --cov=src tests/
```

## Deployment

### Production Considerations
1. **Environment**:
   - Set `FLASK_ENV=production`
   - Set `FLASK_DEBUG=0`
   - Use production-grade WSGI server (e.g., Gunicorn)
   - Configure proper logging

2. **Security**:
   - Use HTTPS only
   - Configure secure headers
   - Set up proper CORS policies
   - Implement proper backup strategy

3. **Performance**:
   - Use production-grade database
   - Configure proper caching
   - Set up monitoring
   - Implement rate limiting

### Deployment Steps
1. Set up production environment variables
2. Configure production server
3. Set up SSL/TLS certificates
4. Configure reverse proxy
5. Set up monitoring and logging
6. Implement backup strategy

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**:
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   - Check if `.env` file exists
   - Verify all required variables are set
   - Ensure proper file permissions

3. **Rate Limiting**:
   - Check rate limit configuration
   - Verify storage backend
   - Monitor rate limit headers

4. **Authentication Issues**:
   - Verify credentials in `.env`
   - Check session configuration
   - Ensure proper cookie settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Security

### Reporting Vulnerabilities
If you discover a security vulnerability, please:
1. Do not disclose it publicly
2. Email security@example.com
3. Include detailed information about the vulnerability
4. We will respond within 48 hours

### Security Best Practices
1. Keep dependencies updated
2. Follow secure coding guidelines
3. Regular security audits
4. Monitor security advisories

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OWASP PyTM for threat modeling
- Flask for the web framework
- GitHub Actions for automation

**Author:** [1B05H1N](https://github.com/1B05H1N)

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

For more details, see the `Makefile` and the `threatmodel/model.py` file.
