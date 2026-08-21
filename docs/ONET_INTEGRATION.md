# O*NET Integration Guide

## Overview

O*NET (Occupational Information Network) provides standardized occupational data.

## Setup

### 1. Register for API Key
Visit: https://services.onetcenter.org/developers

### 2. Configure Databricks Secret
```bash
databricks secrets put --scope fys-apis --key onet-api-key
```

### 3. API Endpoints

**Get Occupation:**
```
GET /ws/online/occupations/{onet_code}
```

**Search Occupations:**
```
GET /ws/online/search?keyword={keyword}
```

**Get Skills:**
```
GET /ws/online/occupations/{onet_code}/skills
```

## Skill Taxonomy

O*NET organizes skills into categories:
- **Basic Skills:** Reading, writing, math
- **Technical Skills:** Programming, CAD, analysis
- **Soft Skills:** Leadership, teamwork, communication

## Crosswalk Example

**Job Title:** "DevOps Engineer"
**O*NET Code:** 15-1252.00
**O*NET Title:** "Software Developers"
**Top Skills:**
- Programming (Importance: 4.5/5)
- Systems Analysis (4.2/5)
- Quality Control (3.8/5)
