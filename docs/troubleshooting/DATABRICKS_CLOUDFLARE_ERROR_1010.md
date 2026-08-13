# Databricks Cloudflare Error 1010 - Troubleshooting Guide

**Organization:** 7 Eagle Group  
**Project:** For Your Service  
**Issue:** Cloudflare Browser Integrity Check blocking Databricks UI  
**Error Code:** 1010

---

## What is Error 1010?

Cloudflare Error 1010 occurs when the Browser Integrity Check flags your session as automated or non-standard. This is a false positive that commonly affects legitimate Databricks users.

**Symptoms:**
- Cannot access Databricks workspace UI
- WebSocket connections fail
- "Access Denied" or "Browser Integrity Check" page
- REST API calls blocked

---

## Why Databricks Triggers This Error

Databricks UI relies heavily on:
- Background WebSocket connections
- Continuous REST API calls
- Session tokens and OAuth flows
- Analytics/telemetry requests

Cloudflare's WAF (Web Application Firewall) monitors these connections and may flag legitimate activity.

---

## Common Triggers

### 1. Adblocker / Privacy Extensions

**Extensions that cause issues:**
- uBlock Origin
- Brave Shields
- Privacy Badger
- Ghostery
- NoScript

**Why it happens:**
- These extensions block Databricks background telemetry/analytics requests
- Cloudflare sees missing HTTP headers
- Connection appears non-standard and gets dropped

### 2. VPN / Proxy Session Mismatches

**VPN-related triggers:**
- IP address rotates mid-session
- IP range is on a shared threat list
- Exit nodes flagged as suspicious
- Shared VPN IP with automated traffic

**Proxy issues:**
- Local proxy intercepting requests
- Modified HTTP headers
- Certificate chain validation failures

### 3. Stale Session Tokens

**Session expiration triggers:**
- Leaving Databricks tab open for extended periods
- OAuth/CSRF token expiration (typically 8-24 hours)
- Malformed API calls from expired tokens
- WAF interprets as bot behavior

### 4. Custom CLI / Automation Scripts

**Script-related triggers:**
- Missing standard browser User-Agent headers
- Rapid API requests without delays
- Concurrent requests from same IP
- Missing referrer headers

---

## How to Fix Immediately

### Fix 1: Disable Extensions on Databricks

**Recommended Approach:**

1. **Whitelist Databricks Domain:**
   - Add `*.cloud.databricks.com` (or your custom domain) to extension whitelist
   - For uBlock Origin: Dashboard → Whitelist → Add domain
   - For Brave: Settings → Shields → Site Settings → Add exception

2. **Or Disable Temporarily:**
   - Click extension icon → Toggle off for Databricks
   - Refresh the page

### Fix 2: Hard Refresh / Clear Workspace Cookies

**Windows:**
```
Ctrl + F5
```

**macOS:**
```
Cmd + Shift + R
```

**Manual Cookie Clearing:**
1. Open browser DevTools (F12)
2. Application tab → Storage → Cookies
3. Delete all cookies for `*.cloud.databricks.com`
4. Refresh page

**Chrome/Edge:**
```
Settings → Privacy → Site Settings → View permissions and data → 
Search for "databricks" → Clear data
```

**Firefox:**
```
Options → Privacy → Cookies and Site Data → Manage Data → 
Search for "databricks" → Remove Selected
```

### Fix 3: Bypass / Toggle VPN

**If using VPN:**
1. Disconnect from VPN temporarily
2. Access Databricks workspace
3. Once loaded, reconnect VPN (if needed)

**If VPN is required:**
1. Switch to different VPN location
2. Choose exit node in same region as Databricks workspace
3. Avoid shared/free VPN services (high abuse scores)

**Recommended VPN Settings:**
- Split tunneling: Exclude Databricks domains
- Dedicated IP (if available)
- Business VPN tiers (lower abuse scores)

### Fix 4: Try Incognito / Private Mode

**Why this works:**
- Disables all extensions by default
- Fresh session with no cached tokens
- Clean cookie state

**Steps:**
1. Open new Incognito/Private window
2. Navigate to Databricks workspace
3. If it loads successfully, the issue is extension-related
4. Return to regular browser and disable problematic extensions

---

## Prevention / Long-Term Solutions

### 1. Whitelist Databricks Permanently

Add these domains to all extension whitelists:
- `*.cloud.databricks.com`
- `*.databricks.com`
- `*.databricksusercontent.com`

### 2. Use Dedicated Databricks Browser Profile

**Chrome/Edge:**
```
Settings → Profiles → Add Profile → "Databricks Work"
- Install minimal extensions
- No ad blockers or privacy tools
```

**Firefox:**
```
about:profiles → Create New Profile → "Databricks Work"
```

### 3. Configure VPN Split Tunneling

**Example (for WireGuard/OpenVPN):**
```
# Exclude Databricks from VPN tunnel
route_nopull
route 0.0.0.0 0.0.0.0 vpn_gateway
route 52.40.0.0 14 net_gateway  # AWS us-west-2 range for Databricks
```

### 4. Set Reasonable Session Timeouts

**Team Guidelines:**
- Close Databricks tabs after work sessions
- Refresh workspace daily to get new tokens
- Don't leave notebooks running overnight

---

## For Your Service Team: Specific Recommendations

### Development Environment
- **Browser:** Chrome or Firefox (latest stable)
- **Extensions:** Disable all except:
  - Password manager (1Password, LastPass)
  - GitHub-related tools
- **VPN:** If required, use split tunneling

### Production Environment
- **Browser:** Clean profile with zero extensions
- **Network:** Direct connection (no VPN)
- **Monitoring:** If automation is needed, use Databricks CLI with proper auth

### CI/CD Pipelines
- **Never** use browser automation (Selenium/Puppeteer) against Databricks UI
- Use Databricks REST API or CLI instead
- Set proper User-Agent headers in API requests:
  ```bash
  curl -H "User-Agent: ForYourService/1.0 (Team: 7EagleGroup)" \
       -H "Authorization: Bearer $DATABRICKS_TOKEN" \
       https://your-workspace.cloud.databricks.com/api/2.0/...
  ```

---

## Verification After Fix

Once you've applied a fix, verify with these steps:

1. **Navigate to Workspace:**
   ```
   https://your-workspace.cloud.databricks.com
   ```

2. **Open Browser Console (F12):**
   - Check for WebSocket connections (should show `ws://` or `wss://`)
   - Look for 200/101 status codes (not 403/1010)

3. **Test API Access:**
   ```python
   # In Databricks notebook
   import requests
   response = requests.get("https://www.databricks.com")
   print(response.status_code)  # Should be 200
   ```

4. **Verify Session Persistence:**
   - Leave tab open for 5 minutes
   - Execute a notebook cell
   - Should work without re-authentication

---

## Still Having Issues?

### Contact Databricks Support

If fixes above don't work, contact Databricks support with:

1. **Error Details:**
   - Exact error message
   - Timestamp of occurrence
   - Your public IP address (visit https://whatismyip.com)

2. **Browser Information:**
   ```
   navigator.userAgent  (paste from browser console)
   ```

3. **Network Details:**
   - VPN provider (if applicable)
   - Corporate firewall settings
   - Proxy configuration

4. **Screenshot:**
   - Full Cloudflare error page
   - Browser console (F12 → Console tab)

### Escalation Path

1. **Workspace Admin** (your organization)
2. **Databricks Account Team** (account@databricks.com)
3. **Cloudflare WAF Rules** (if you control Databricks deployment)

---

## Related Documentation

- [Databricks Network Connectivity](https://docs.databricks.com/administration-guide/cloud-configurations/aws/customer-managed-vpc.html)
- [Cloudflare Error 1010](https://support.cloudflare.com/hc/en-us/articles/360029779472-Troubleshooting-Cloudflare-1XXX-errors)
- [Browser Extensions Security](https://docs.databricks.com/security/privacy/index.html)

---

**Last Updated:** 2026-08-13  
**Maintained By:** Free Hall <whall4.wh@gmail.com>  
**Organization:** 7 Eagle Group  
**Project:** For Your Service
