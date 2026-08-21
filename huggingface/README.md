# For Your Service - API Backend

AI-powered veteran job matching platform by 7 Eagle Group

## 🚀 Deployed on Hugging Face Spaces (FREE Tier)

This FastAPI backend connects the Base44 frontend to Databricks Unity Catalog.

---

## 📋 Deployment Instructions

### Step 1: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in:
   - **Space name:** `for-your-service-api`
   - **SDK:** Select **Docker**
   - **Hardware:** CPU basic (FREE)
4. Click **Create Space**

### Step 2: Upload Files

Upload these 3 files to your Space:
- `app.py`
- `requirements.txt`
- `README.md`

### Step 3: Configure Databricks Credentials

In your Space → **Settings** → **Variables and secrets**, add:

| Secret Name | Value | Where to Find |
|------------|-------|---------------|
| `DATABRICKS_SERVER_HOSTNAME` | `dbc-xxx.cloud.databricks.com` | Workspace URL (no `https://`) |
| `DATABRICKS_HTTP_PATH` | `/sql/1.0/warehouses/xxxxx` | SQL Warehouse → Connection details |
| `DATABRICKS_TOKEN` | `dapi...` | User Settings → Developer → Access tokens |

### Step 4: Test Your API

Once deployed (~2 min):

**Health Check:**
```bash
curl https://YOUR_USERNAME-for-your-service-api.hf.space/health
```

**Interactive Docs:**
Visit: `https://YOUR_USERNAME-for-your-service-api.hf.space/docs`

---

## 🔌 Connect Base44 Frontend

In your Base44 app, add:

```javascript
const API_BASE_URL = "https://YOUR_USERNAME-for-your-service-api.hf.space";

async function registerVeteran(formData) {
  const response = await fetch(`${API_BASE_URL}/api/v1/veteran/register`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(formData)
  });
  return response.json();
}

async function getJobMatches(veteranId) {
  const response = await fetch(`${API_BASE_URL}/api/v1/match`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({veteran_id: veteranId, top_n: 10})
  });
  return response.json();
}
```

---

## 💰 Cost: $5-10/month

* **Hugging Face Spaces:** FREE (CPU basic)
* **Databricks:** ~$5-10/month (serverless SQL)

---

## 👨‍💻 Developer

**Free Hall**
Email: whall4.wh@gmail.com
Organization: 7 Eagle Group
