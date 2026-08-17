#!/usr/bin/env python3
"""
Script to help register for all API keys
"""

print("=" * 70)
print("API Registration Guide")
print("=" * 70)

apis = [
    {
        "name": "USAJobs",
        "url": "https://developer.usajobs.gov/",
        "cost": "FREE (unlimited)",
        "notes": "Instant approval",
    },
    {
        "name": "BLS",
        "url": "https://data.bls.gov/registrationEngine/",
        "cost": "FREE (500/day)",
        "notes": "Receive key via email",
    },
    {
        "name": "Adzuna",
        "url": "https://developer.adzuna.com/signup",
        "cost": "FREE (1,000/month)",
        "notes": "Create app after signup",
    },
    {
        "name": "O*NET",
        "url": "https://services.onetcenter.org/reference/",
        "cost": "FREE (unlimited)",
        "notes": "Use your email as username",
    },
    {
        "name": "CareerOneStop",
        "url": "https://www.careeronestop.org/Developers/WebAPI/registration.aspx",
        "cost": "FREE (unlimited)",
        "notes": "Instant approval",
    },
]

for api in apis:
    print(f"\n{api['name']}")
    print(f"  URL: {api['url']}")
    print(f"  Cost: {api['cost']}")
    print(f"  Notes: {api['notes']}")

print("\n" + "=" * 70)
print("After registration, add keys to .env file")
print("=" * 70)
