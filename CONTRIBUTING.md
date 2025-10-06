# Contributing to Environmental Health Platform

Thank you for considering contributing to the Environmental Health Platform! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites
- Python 3.9 or higher
- PostgreSQL 12 or higher
- Redis (optional, for caching)
- Git

### Setting Up Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/pragyakuumarimishra/env-health-platform.git
   cd env-health-platform
   ```

2. **Set up Python virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb env_health_platform
   
   # Copy environment file
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

### Using Docker (Recommended)

```bash
# From project root
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Redis on port 6379
- Backend API on port 8000

## Development Guidelines

### Code Style

- Follow PEP 8 style guide for Python code
- Use type hints where applicable
- Write docstrings for functions and classes
- Keep functions small and focused

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Run tests with: `pytest`

### Commit Messages

Use clear and descriptive commit messages:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests liberally

Example:
```
Add activity recommendation endpoint

- Implement jogging score calculation
- Add support for walking and cycling
- Include tests for different scenarios

Fixes #123
```

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

## Contributing Process

1. **Create an issue** describing the feature or bug fix
2. **Fork the repository** and create a new branch
3. **Make your changes** following the guidelines above
4. **Write or update tests** for your changes
5. **Ensure all tests pass** locally
6. **Submit a pull request** with a clear description of changes

## Pull Request Guidelines

- Link to the relevant issue
- Provide a clear description of changes
- Include screenshots for UI changes
- Ensure CI checks pass
- Request review from maintainers

## Areas for Contribution

### Phase 1 (Current)
- [ ] Improve error handling
- [ ] Add more comprehensive tests
- [ ] Enhance API documentation
- [ ] Add validation for sensor readings
- [ ] Implement caching for external API calls

### Phase 2 (Upcoming)
- [ ] Time series forecasting models
- [ ] Symptom diary functionality
- [ ] Route exposure calculation
- [ ] Chat assistant integration

### Phase 3 (Future)
- [ ] What-if scheduling
- [ ] Exposure budget tracking
- [ ] Pollen data integration
- [ ] Wildfire alert system

## Code Review Process

1. All submissions require review from maintainers
2. Reviewers will check:
   - Code quality and style
   - Test coverage
   - Documentation
   - Performance implications
3. Address review feedback promptly
4. Once approved, maintainers will merge the PR

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about the codebase
- Documentation improvements

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in the project README and release notes.

Thank you for contributing to improving environmental health decision support!
