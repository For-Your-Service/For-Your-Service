# Frequently Asked Questions

## General

**Q: What is For Your Service?**  
A: An AI-powered platform matching veterans to civilian careers using neural networks.

**Q: Who is it for?**  
A: Transitioning military service members and veterans seeking employment.

**Q: Is it free?**  
A: Yes! The platform uses free-tier cloud services and government APIs.

## Technical

**Q: What APIs do you use?**  
A:
* USAJobs (federal jobs)
* O*NET (occupational data)
* BLS (wage statistics)
* Adzuna (job aggregator)
* CareerOneStop (DOL veteran services)

**Q: How does the matching work?**  
A: We use a Siamese neural network to compute similarity between veteran profiles (MOS, skills, experience) and job requirements, represented as 384-dimensional embeddings.

**Q: What is the MOS mapper?**  
A: Maps military occupational specialties to civilian O*NET occupation codes, translating military experience to civilian job requirements.

## Data

**Q: How often is job data updated?**  
A: Daily for job postings, weekly for occupational data, monthly for wage statistics.

**Q: Where is data stored?**  
A: Databricks Unity Catalog with Bronze (raw), Silver (normalized), and Gold (embeddings) layers.

**Q: Is data secure?**  
A: Yes! We follow enterprise security practices and comply with data privacy regulations.

## For Developers

**Q: How can I contribute?**  
A: See CONTRIBUTING.md for guidelines.

**Q: What tech stack?**  
A: Python 3.11, Databricks, Unity Catalog, Sentence-Transformers, Docker.

**Q: Can I run it locally?**  
A: Yes! See DEPLOYMENT.md for instructions.
