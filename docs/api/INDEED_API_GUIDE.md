# 🔵 Indeed API Registration Guide

**Status:** Indeed has MULTIPLE API programs - we want the Publisher Program (FREE)

---

## ⚠️ IMPORTANT: Indeed API Options

Indeed has 3 different API offerings:

### 1. Indeed Publisher Program (FREE) ⭐ RECOMMENDED
- **Purpose:** Display Indeed jobs on your site
- **Cost:** FREE
- **Volume:** Unlimited job access
- **Registration:** https://www.indeed.com/publisher
- **Use case:** Educational, non-commercial job matching

### 2. Indeed Hiring Platform API (PAID)
- **Purpose:** Post jobs TO Indeed
- **Cost:** $$$ (employers pay to post)
- **Not what we need**

### 3. Indeed Apply API (PAID)
- **Purpose:** Integrate Indeed Apply button
- **Cost:** $$$
- **Not what we need**

---

## ✅ STEP-BY-STEP: Indeed Publisher Program

### Step 1: Go to Publisher Homepage
**URL:** https://www.indeed.com/publisher

**Or search Google for:** "Indeed Publisher Program"

---

### Step 2: Click "Sign Up Now" or "Join"

Fill out:
```
Email:           whall4.wh@gmail.com
Name:            Free Hall
Organization:    7 Eagle Group
Website:         https://github.com/For-Your-Service/For-Your-Service
Description:     Veteran job matching platform using AI
```

---

### Step 3: Agree to Terms

- ✅ Non-commercial use
- ✅ Educational/research purpose
- ✅ Properly attribute Indeed

---

### Step 4: Get Your Publisher ID

You'll receive:
```
Publisher ID: 123456789012345
```

This is your API key!

---

### Step 5: API Access

**Endpoint:**
```
https://api.indeed.com/ads/apisearch
```

**Required params:**
- `publisher` (your publisher ID)
- `q` (search query)
- `l` (location)
- `format=json`

---

## 📝 Sample Request

```python
import requests

PUBLISHER_ID = "YOUR_PUBLISHER_ID"

params = {
    "publisher": PUBLISHER_ID,
    "q": "cybersecurity",
    "l": "San Diego, CA",
    "format": "json",
    "v": "2",
    "limit": 25,
    "radius": 25,
    "fromage": 7  # Jobs from last 7 days
}

response = requests.get(
    "https://api.indeed.com/ads/apisearch",
    params=params
)

if response.status_code == 200:
    data = response.json()

    results = data.get("results", [])
    print(f"Found {len(results)} jobs")

    for job in results[:5]:
        print(f"\nTitle: {job['jobtitle']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['formattedLocation']}")
        print(f"Snippet: {job['snippet']}")
        print(f"URL: {job['url']}")
```

---

## 🎯 What You'll Get

**Volume:** 30M+ jobs (100x more than current!)

**Data per job:**
- Job title
- Company name
- Location (city, state, country)
- Job snippet/summary
- Posted date
- Indeed URL
- Source (company website, job board, etc.)
- Job key (unique ID)

**Advanced search:**
- Keywords
- Location + radius
- Date posted (last 1, 3, 7, 15, 30 days)
- Job type (full-time, part-time, contract)
- Experience level
- Salary estimate (when available)

---

## 💰 Cost & Limits

**Publisher Program:**
- ✅ FREE for non-commercial/educational use
- ✅ Unlimited API calls
- ✅ Must properly attribute Indeed
- ✅ Cannot scrape job details (use provided snippets)

**Terms:**
- Display "jobs by Indeed" logo
- Link back to Indeed for applications
- Don't remove Indeed tracking params
- For non-commercial/research use

---

## 🚨 Alternative: Indeed Advanced Job Search (No API Key)

If Publisher Program requires review, you can use:

**URL:** https://www.indeed.com/jobs

**Scrape parameters from URL:**
```
https://www.indeed.com/jobs?q=cybersecurity&l=San%20Diego%2C%20CA
```

**NOT RECOMMENDED** (violates TOS, rate limits, blocking)

---

## 🎯 Recommendation

1. **Try Publisher Program first** (FREE, legal, best option)
2. **If that's slow**, we can build Bronze layer with current data (335 jobs)
3. **Add Indeed later** once approved

---

## 📊 Impact on Your Tensors

### Current Data:
- 335 jobs (240 Adzuna + 95 USAJobs)
- Good starting point

### With Indeed:
- **10,000+ jobs per scrape**
- Better salary distribution
- More companies (1000s)
- Better geographic coverage
- Rare job titles (edge cases)
- **Much better probability distributions!**

---

## ✅ Next Steps

1. **Go to:** https://www.indeed.com/publisher
2. **Sign up** with 7 Eagle Group info
3. **Get Publisher ID**
4. **Tell me:** "I have the Indeed Publisher ID: [paste it]"
5. **I'll integrate it** into your scraper!

**OR**

If the Publisher Program requires review/approval:
- **Build Bronze layer NOW** with 335 jobs
- **Add Indeed later** (once approved)
- **Don't let API approval block your progress!**
