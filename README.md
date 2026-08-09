# For Your Service
## AI-Powered Veteran Job Matching Platform

**Organization:** 7 Eagle Group  
**Developer:** Free Hall <whall4.wh@gmail.com>  
**Mission:** Connect veterans with meaningful employment through intelligent job matching

---

## 🎯 Project Overview

For Your Service is an AI-powered job matching platform designed specifically for military veterans. Using neural network technology and semantic analysis, we match veterans with civilian job opportunities based on their military experience, skills, and career goals.

**Partner:** [7 Eagle Group](https://7eaglegroup.org) - Veteran placement and support organization

---

## 📊 Key Features

* **Intelligent Matching:** Siamese twin tower neural network architecture for semantic job-veteran matching
* **Resume Optimization:** Gap analysis showing veterans how to improve match scores
* **Cost-Effective:** $5-10/month total infrastructure cost (95% savings vs. traditional cloud)
* **Scalable:** Built on Databricks lakehouse for enterprise-grade data processing
* **FREE API:** Hosted on Hugging Face Spaces (zero hosting costs)

---

## 🏗️ Architecture

For Your Service uses a **three-tier hybrid architecture**:

```
Base44 Frontend → Hugging Face API (FREE) → Databricks Lakehouse ($5-10/month)
```

**Key Innovation:** Separates API hosting (FREE tier) from data processing (serverless pay-per-query)

📖 **Read the full story:**
* [Architecture Overview](docs/ARCHITECTURE.md) - Technical deep-dive
* [Deployment Strategy](docs/DEPLOYMENT_STRATEGY.md) - Cost optimization and design decisions

---

## 💰 Cost Breakdown

| Component | Service | Cost |
|-----------|---------|------|
| Frontend | Base44 | $0/month |
| API Hosting | Hugging Face Spaces | **$0/month (FREE)** |
| Data Storage | Databricks Unity Catalog | ~$2-3/month |
| Compute | Databricks Serverless SQL | ~$3-7/month |
| **Total** | | **~$5-10/month** |

**Traditional Cloud (GCP/AWS):** $95-600/month  
**Savings:** 95-98% cost reduction

---

## 🚀 Quick Start

### For Developers

1. **Clone the repository**
   ```bash
   git clone https://github.com/For-Your-Service/For-Your-Service.git
   cd For-Your-Service
   ```

2. **Set up Unity Catalog tables**
   ```bash
   # Run in Databricks notebook
   python setup/01_Unity_Catalog_Setup.py
   ```

3. **Deploy to Hugging Face Spaces**
   * Create Space: https://huggingface.co/spaces
   * Upload files from `huggingface/` directory
   * Configure secrets (see [huggingface/README.md](huggingface/README.md))

4. **Test the API**
   ```bash
   python setup/03_Test_API.py
   ```

📖 **Full deployment guide:** [DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)

---

## 📁 Repository Structure

```
For-Your-Service/
├── docs/
│   ├── ARCHITECTURE.md              # System architecture deep-dive
│   ├── DEPLOYMENT_STRATEGY.md       # Cost optimization rationale
│   └── daily-notes/                 # Development progress notes
├── huggingface/
│   ├── Dockerfile                   # HF Spaces deployment
│   ├── app.py                       # FastAPI backend (262 lines)
│   ├── requirements.txt             # Python dependencies
│   └── README.md                    # Deployment instructions
├── notebooks/
│   ├── 06_Enhanced_Job_Matching_Engine.py   # Neural network matching
│   └── 08_Base44_API_Backend.py             # API development notebook
├── setup/
│   ├── 01_Unity_Catalog_Setup.py            # Automated table creation
│   ├── 02_Generate_Databricks_Token.md      # Token generation guide
│   └── 03_Test_API.py                       # API testing suite
├── DEPLOYMENT_STATUS.md             # Current deployment checklist
└── README.md                        # This file
```

---

## 🔧 Technology Stack

### Frontend
* Base44 (No-code form builder)

### API Layer
* FastAPI 0.104.1
* Python 3.11
* Databricks SQL Connector 3.0.0
* Deployed on Hugging Face Spaces (Docker)

### Data & Compute
* Databricks Lakehouse Platform
* Unity Catalog (Delta Lake storage)
* Serverless SQL Warehouse
* PySpark for data processing

### Machine Learning
* Siamese Twin Tower Neural Network
* 384-dimensional semantic embeddings
* Cosine similarity matching

---

## 📈 Current Status

**Development Phase:** MVP Complete  
**Deployment:** Ready for Hugging Face Spaces  
**Data:** 90+ Houston job postings, 1 test veteran profile  
**Next Steps:** Deploy to production, integrate neural network

### Recent Updates (2026-08-09)

* ✅ Hugging Face Spaces deployment files created
* ✅ Unity Catalog tables created and populated
* ✅ Resume optimization pipeline added (458 lines)
* ✅ API testing suite completed (6 automated tests)
* ✅ Architecture documentation finalized
* 🔄 Awaiting manual HF Space deployment

📖 **Full history:** See [DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)

---

## 🎓 How It Works

### For Veterans

1. **Complete Intake Form** (Base44 frontend)
   * Personal information
   * Military background and skills
   * Target roles and salary expectations
   * Preferred job locations

2. **Get Matched** (Neural network processing)
   * 384-dimensional semantic analysis
   * Military-to-civilian skill translation
   * Top 10 ranked job opportunities

3. **Optimize Resume** (Gap analysis)
   * Identify missing keywords
   * Show probability lift for improvements
   * Before/After match score simulation

### For Employers

1. **Job Posting Aggregation**
   * Scraped from Indeed, USAJobs, Adzuna
   * Standardized schema (location, salary, requirements)
   * Daily updates

2. **Veteran Matching**
   * AI-powered candidate ranking
   * Skills gap identification
   * Cultural fit scoring (military values alignment)

---

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info and health |
| `/health` | GET | Database connectivity check |
| `/api/v1/veteran/register` | POST | Register new veteran profile |
| `/api/v1/veteran/{id}` | GET | Retrieve veteran profile |
| `/api/v1/match` | POST | Get AI-powered job matches |
| `/api/v1/jobs` | GET | Search job postings |

**Interactive Docs:** `https://YOUR-HF-SPACE.hf.space/docs` (after deployment)

---

## 🔒 Security & Privacy

* **PII Protection:** Unity Catalog governance tags applied
* **Credential Management:** Databricks tokens stored as HF Spaces secrets
* **HTTPS Only:** All communications encrypted
* **CORS Restrictions:** API limited to Base44 frontend domain
* **Access Control:** Row-level security for veteran profiles

---

## 🚦 Roadmap

### Phase 1: MVP (Current)
- [x] Databricks data pipeline
- [x] FastAPI backend
- [x] Neural network matching algorithm
- [x] Hugging Face deployment prep
- [ ] Production deployment
- [ ] Base44 frontend integration

### Phase 2: Enhancement (Q3 2026)
- [ ] Multi-city job coverage (Greenville, SC + nationwide)
- [ ] Resume optimization UI
- [ ] Email notifications for new matches
- [ ] Veteran login and saved searches

### Phase 3: Scale (Q4 2026+)
- [ ] Mobile app (iOS/Android)
- [ ] Employer portal for direct job posting
- [ ] Success metrics and outcomes tracking
- [ ] Integration with VA benefits

---

## 🤝 Contributing

This is a nonprofit project supporting veterans. Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is developed for 7 Eagle Group, a 501(c)(3) nonprofit organization dedicated to veteran support.

---

## 📞 Contact

**Developer:** Free Hall  
**Email:** whall4.wh@gmail.com  
**Organization:** 7 Eagle Group  
**GitHub:** https://github.com/For-Your-Service/For-Your-Service

---

## 🙏 Acknowledgments

* **7 Eagle Group** - Mission, partnership, and veteran advocacy
* **Databricks Community Edition** - Lakehouse platform
* **Hugging Face** - FREE API hosting
* **All veterans** - Your service inspires this work

---

**Built with ❤️ for those who served**

*"No veteran left behind in the civilian job market"*
