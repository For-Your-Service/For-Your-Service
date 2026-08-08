# Root Directory Structure Guide

**For Your Service - 7 Eagle Group**  
*AI-powered veteran job matching platform*

## Purpose of This Document

This guide explains why certain files **must** remain in the project root directory and cannot be moved into subfolders. Understanding this structure is essential for maintaining a professional, functional Python/Docker/Kubernetes project.

---

## 🎯 What is the "Root Directory"?

The **root directory** is the top-level folder of your project - the first thing you see when you open the repository. It contains **project-wide configuration files** that tools expect to find in this exact location.

```
For-Your-Service/          ← ROOT DIRECTORY
├── .dockerignore          ← Root config files
├── Dockerfile             ← Root config files
├── setup.py               ← Root config files
├── README.md              ← Root essential
├── docs/                  ← Subfolder (organized content)
├── src/                   ← Subfolder (organized content)
└── tests/                 ← Subfolder (organized content)
```

---

## 📋 Root Files - Category by Category

### 🐳 Docker Configuration (Container Build)

**Files:**
- `.dockerignore`
- `Dockerfile`
- `docker-compose.yml`

**Why Root?**
- Docker CLI expects `Dockerfile` in the directory where you run `docker build`
- `.dockerignore` must be in root to exclude files during image build
- `docker-compose.yml` defines multi-container orchestration from project root

**What Breaks if Moved:**
```bash
docker build .              # ❌ Fails - can't find Dockerfile
docker-compose up           # ❌ Fails - can't find docker-compose.yml
```

---

### 🐍 Python Package Configuration

**Files:**
- `setup.py` - Package installation & metadata
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Modern Python project config (PEP 518)

**Why Root?**
- `pip install .` expects `setup.py` or `pyproject.toml` in current directory
- `pip install -r requirements.txt` is typically run from project root
- Python packaging tools scan root for package configuration

**What Breaks if Moved:**
```bash
pip install .               # ❌ Fails - can't find setup.py
pip install -r requirements.txt  # ❌ Fails if not in root context
```

---

### 🧪 Testing Configuration

**Files:**
- `pytest.ini` - Pytest test runner configuration
- `.codecov.yml` - Code coverage reporting config

**Why Root?**
- Pytest searches upward from test files until it finds `pytest.ini` in root
- Configuration defines test discovery paths relative to root
- CI/CD systems expect test config at project root

**What Breaks if Moved:**
```bash
pytest                      # ❌ Won't find configuration
pytest tests/               # ❌ May not apply custom markers/options
```

**Example `pytest.ini` content:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

---

### 🔧 Code Quality & Linting

**Files:**
- `.flake8` - Python code style checker config
- `.editorconfig` - Editor formatting rules
- `.pre-commit-config.yaml` - Git pre-commit hooks

**Why Root?**
- Linters scan from root directory
- EditorConfig is automatically detected by IDEs when file is in root
- Pre-commit hooks install from root `.git/` directory

**What Breaks if Moved:**
```bash
flake8 src/                 # ❌ Won't apply custom rules from .flake8
pre-commit install          # ❌ Can't find config
```

---

### 📦 Version Control (Git)

**Files:**
- `.gitignore` - Files/folders Git should ignore
- `.gitattributes` - Git file handling rules (line endings, LFS, diff behavior)

**Why Root?**
- Git reads `.gitignore` from repository root by default
- `.gitattributes` applies rules to all files in the repository
- Essential for consistent behavior across contributors

**What Breaks if Moved:**
```bash
git add .                   # ❌ Won't ignore specified files
git clone                   # ❌ Won't apply LFS or line-ending rules
```

**Example `.gitignore` (partial):**
```
__pycache__/
*.pyc
.env
venv/
```

---

### 🏗️ Build & Infrastructure

**Files:**
- `Makefile` - Build automation commands
- `main.tf` - Terraform infrastructure-as-code

**Why Root?**
- `make` command expects `Makefile` in current directory
- Terraform expects `.tf` files in root (or specified module directory)

**What Breaks if Moved:**
```bash
make test                   # ❌ Fails - can't find Makefile
terraform plan              # ❌ Fails - can't find main.tf
```

**Example `Makefile` commands:**
```makefile
test:
    pytest tests/

build:
    docker build -t for-your-service .
```

---

### 📄 Project Essentials

**Files:**
- `README.md` - Project overview (GitHub displays this on repo homepage)
- `LICENSE` - Legal license for the project

**Why Root?**
- GitHub automatically renders `README.md` from root on repository homepage
- Open-source convention: `LICENSE` in root for easy discovery
- First files contributors look for when evaluating a project

**What Breaks if Moved:**
- ❌ GitHub won't display README on repository landing page
- ❌ License scanners won't detect project license
- ❌ Reduced project discoverability and professionalism

---

## 🎨 Best Practice: Organized vs. Root

### ✅ Keep in Root (Configuration)
**Rule:** If a tool expects it in root, it stays in root

- Build configs (Docker, Python, Terraform)
- Test configs (pytest, coverage)
- Linting configs (flake8, editorconfig)
- Git configs (.gitignore, .gitattributes)
- Project essentials (README, LICENSE)

### ✅ Move to Subfolders (Content)

**Rule:** If it's organized content (code, docs, data), it goes in a folder

- `src/` - Application source code
- `tests/` - Test files
- `docs/` - Documentation (guides, API docs, notes)
- `notebooks/` - Jupyter/Databricks notebooks
- `results/` - Output data
- `scripts/` - Utility scripts

---

## 🧹 Repository Organization Principles

### 1. **Root = Project-Wide Settings**
Files that apply to the ENTIRE project and are used by external tools.

### 2. **Subfolders = Organized Content**
Related files grouped logically for easy navigation.

### 3. **Industry Standards Matter**
Following conventions makes it easier for contributors to onboard.

---

## 📊 For Your Service Structure

Our repository follows these principles:

```
For-Your-Service/
├── 📋 Root Config Files (20 files)    ← Tools look here
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── setup.py
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── pytest.ini
│   ├── .flake8
│   ├── .editorconfig
│   ├── .pre-commit-config.yaml
│   ├── .codecov.yml
│   ├── .gitignore
│   ├── .gitattributes
│   ├── Makefile
│   ├── main.tf
│   ├── README.md
│   └── LICENSE
│
├── 📁 Organized Content (Subfolders)  ← Humans navigate here
│   ├── docs/           ← Documentation
│   ├── src/            ← Application code
│   ├── tests/          ← Test files
│   ├── notebooks/      ← Analysis notebooks
│   ├── scripts/        ← Utility scripts
│   ├── results/        ← Output data
│   ├── config/         ← Application configs
│   ├── databricks/     ← Databricks workflows
│   └── cloud-functions/ ← Serverless functions
```

**Result:** Clean, professional, industry-standard structure

---

## ❓ Common Questions

### "Why can't I move pytest.ini into tests/?"

Pytest needs to know WHERE to find tests. If `pytest.ini` is inside `tests/`, pytest can't find it until it already knows to look in `tests/` - a circular dependency.

### "Can I move requirements.txt into a config/ folder?"

You could, but it breaks convention. Every Python developer expects:
```bash
pip install -r requirements.txt
```
Not:
```bash
pip install -r config/requirements.txt
```

### "This seems messy - why so many root files?"

Each file serves a specific tool:
- Docker needs 3 files
- Python needs 3 files  
- Testing needs 2 files
- Linting needs 3 files
- Git needs 2 files
- Build needs 2 files
- Docs need 2 files

**Total: ~17-20 files is standard** for a modern Python/Docker project.

### "What about other projects with fewer root files?"

Simpler projects have fewer tools:
- No Docker → No `Dockerfile`
- No Terraform → No `main.tf`
- No pre-commit hooks → No `.pre-commit-config.yaml`

For Your Service is a **production-ready platform** with:
- Containerization (Docker)
- Infrastructure-as-code (Terraform)
- CI/CD (pytest, pre-commit, codecov)
- Multiple deployment targets (Kubernetes, Hugging Face)

**More capabilities = More root config files** ✅

---

## 🎓 Learning Resources

### Understanding Project Structure
- [Python Packaging Guide](https://packaging.python.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [pytest Configuration](https://docs.pytest.org/en/stable/reference/customize.html)

### Repository Organization
- [GitHub's Repository Guide](https://docs.github.com/en/repositories)
- [EditorConfig Specification](https://editorconfig.org/)

---

## 📝 Summary for Contributors

**If you're new to the For Your Service repository:**

1. ✅ **Don't move root config files** - They're in the right place
2. ✅ **Add new documentation to `docs/`** - Keep docs organized
3. ✅ **Add new code to `src/`** - Keep source organized
4. ✅ **Add new tests to `tests/`** - Keep tests organized
5. ✅ **Follow the existing structure** - It's industry-standard

**Questions?** Ask in GitHub Discussions or contact Free Hall (whall4.wh@gmail.com)

---

**Maintained by:** Free Hall for 7 Eagle Group  
**Last Updated:** December 2026  
**Project:** For Your Service - AI-powered veteran job matching platform  
**GitHub:** https://github.com/For-Your-Service/For-Your-Service
