# Contributing to For Your Service

Thank you for your interest in contributing! This project helps military veterans find civilian tech jobs using AI-powered matching.

## Partner Organization

**7 Eagle Group** - Veteran placement organization  
**Project Lead:** William Free Hall <whall4.wh@gmail.com>

## How to Contribute

### 1. Code Contributions

**Areas needing help:**
- Job scraper APIs (Indeed, LinkedIn, USAJobs)
- ML model improvements (better embeddings, feature engineering)
- UI/UX enhancements (Streamlit interface)
- Data validation and cleaning
- Test coverage

**Setup:**
```bash
# Clone repo
git clone https://github.com/For-Your-Service/For-Your-Service.git
cd For-Your-Service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

**Branch naming:**
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring

**Commit messages:**
```
feat: Add LinkedIn job scraper
fix: Correct salary parsing bug
docs: Update API authentication guide
refactor: Extract embedding logic to utils
```

### 2. Data Contributions

**We need:**
- Real veteran resumes (with permission)
- Job posting samples
- Skills taxonomy data
- MOS-to-civilian role mappings

**Data privacy:**
- Remove PII before contributing
- Get explicit consent for any veteran data
- Anonymize all personal information

### 3. Documentation

**Docs needed:**
- API integration guides
- Deployment tutorials
- User guides for veterans
- Admin/operator manuals

### 4. Testing

**Test categories:**
- Unit tests (pytest)
- Integration tests (API mocking)
- End-to-end tests (full pipeline)
- Performance benchmarks

**Run tests:**
```bash
# All tests
pytest

# With coverage
pytest --cov=.

# Specific module
pytest tests/unit/test_matching.py
```

### 5. Issue Reporting

**Bug reports should include:**
1. Description of the bug
2. Steps to reproduce
3. Expected vs actual behavior
4. Environment (OS, Python version, etc.)
5. Logs/screenshots if applicable

**Feature requests should include:**
1. Problem statement
2. Proposed solution
3. Alternative approaches considered
4. Impact on veterans/users

## Code Style

**Python:**
- Follow PEP 8
- Use Black for formatting
- Type hints encouraged
- Docstrings required for public APIs

**SQL:**
- Uppercase keywords (SELECT, FROM, WHERE)
- Lowercase table/column names
- 2-space indentation
- Comments for complex queries

**Format code:**
```bash
# Format Python
black .

# Sort imports
isort .

# Lint
flake8 .
```

## Pull Request Process

1. **Fork the repo** and create your branch
2. **Make changes** with clear commit messages
3. **Add tests** for new functionality
4. **Update docs** if needed
5. **Run all tests** and ensure they pass
6. **Submit PR** with description of changes

**PR checklist:**
- [ ] Tests pass
- [ ] Code formatted (black, isort)
- [ ] Documentation updated
- [ ] No PII in commits
- [ ] Signed commits (if required)

## Review Process

- PRs reviewed within 48 hours
- At least 1 approval required
- CI/CD must pass
- No merge conflicts

## Code of Conduct

- Be respectful and inclusive
- Focus on helping veterans
- Constructive feedback only
- Zero tolerance for discrimination

## Questions?

- **Email:** whall4.wh@gmail.com
- **GitHub Issues:** Use for technical questions
- **Discussions:** Use for general questions

## License

By contributing, you agree your contributions will be licensed under the project's MIT License.

---

**Thank you for helping veterans transition to civilian tech careers!**
