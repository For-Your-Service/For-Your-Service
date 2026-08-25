# Istio Egress Gateway & External Data Source Auditing

## 1. Architecture
Direct outbound connections from application containers are blocked. All egress traffic targeting external federal and job board APIs must pass through the dedicated `istio-egressgateway`.

```
[ Application Pod ] ---> [ Sidecar Proxy ] ---> [ Istio Egress Gateway ] ---> [ External API ]
                                                                                (USAJOBS, RapidAPI)
```

## 2. Approved ServiceEntries
- `data.usajobs.gov` (USAJOBS Federal API)
- `jsearch.p.rapidapi.com` (JSearch Live Job Search API)
- `api.adzuna.com` (Adzuna Employment Aggregator)
- `*.databricks.com` & `*.aws.databricksapps.com` (Databricks Serverless Compute)
