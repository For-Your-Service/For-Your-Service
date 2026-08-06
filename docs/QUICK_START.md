# Quick Start Guide

Get up and running with For Your Service in 5 minutes!

## 1. Clone Repository
```bash
git clone https://github.com/For-Your-Service/For-Your-Service.git
cd For-Your-Service
```

## 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## 3. Configure API Keys
```bash
cp .env.example .env
# Edit .env with your API keys
```

## 4. Register for API Keys
Run the helper script:
```bash
python scripts/register_apis.py
```

## 5. Run Tests
```bash
pytest tests/ -v
```

## 6. Initialize Database (Databricks)
```bash
python scripts/init_db.py
```

## 7. Start Data Collection
```bash
python -m src.ingestion.scheduler
```

## Next Steps
* Read ARCHITECTURE.md for system overview
* Check API.md for endpoint documentation
* Review DEPLOYMENT.md for production setup
