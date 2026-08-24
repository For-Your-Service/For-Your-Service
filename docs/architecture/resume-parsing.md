# Resume Parsing Architecture

## Overview
Converts unstructured PDF/DOCX resumes into normalized, structured data.

## Components
- Text Extraction (PDF/DOCX → plain text)
- NER Extraction (text → structured entities)
- Skill Normalization (variants → canonical names)

## Flow
```
Resume (PDF) → TextExtractor → SkillExtractor → ParsedResume
```
