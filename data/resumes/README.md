# Resume Storage

Upload veteran resumes here for matching.

## Supported Formats

- ✅ PDF (`.pdf`)
- ✅ Microsoft Word (`.docx`)

## Privacy

⚠️ **IMPORTANT:** This directory is excluded from Git tracking (`.gitignore`).
Resumes are kept private and never committed to the repository.

## Usage

1. Upload your resume to this directory
2. Run: `python scripts/live_test.py data/resumes/your_resume.pdf`
3. View results in console and `results/` directory

## Example

```bash
# Upload resume
cp ~/Downloads/free_hall_resume.pdf data/resumes/

# Run live test
python scripts/live_test.py data/resumes/free_hall_resume.pdf
```
