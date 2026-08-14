# FYS-E011 — Security & Privacy

## Problem Statement
Veteran contact and career data can contain sensitive PII, while matching and analytics need only a minimized projection. Current serving configuration includes permissive cross-origin access with credentials, write operations lack a defined authentication boundary, and API configuration contains live-looking credential defaults. These conditions make it unsafe to scale the Veteran and Match surfaces.

## Solution
Create a privacy-preserving operating model: isolate operational Veteran PII from anonymized analytics and Match inputs; use secrets-only configuration; restrict browser origins; require authenticated authorization for writes and partner access; and align retention behavior with documented policy. The public Match surface may return only authorized, minimized information and must not turn analytics tables into a raw PII write path.

## User Stories
1. As a Veteran, I want my email and contact details kept separate from matching analytics, so that job recommendations do not expose my identity unnecessarily.
2. As a counselor, I want to retrieve a Veteran profile only through an authorized operational path, so that I can assist the Veteran without broad access to unrelated PII.
3. As a matching service, I want an anonymized Veteran projection for scoring, so that Match computation uses only the attributes it needs.
4. As a platform engineer, I want PII classification at ingestion and transformation boundaries, so that bronze, silver, and gold data use appropriate handling rules.
5. As a security engineer, I want all provider credentials loaded from secret scopes or environment injection, so that tracked configuration never contains usable secrets.
6. As a source-integrations owner, I want startup validation to fail clearly when required production credentials are absent, so that a source does not silently operate with defaults.
7. As a frontend maintainer, I want an explicit CORS allowlist, so that only approved web clients can call credentialed Veteran and Match APIs.
8. As a Veteran, I want profile registration and updates authenticated, so that another person cannot create or modify my career data.
9. As a Partner administrator, I want partner routes authorized by scoped identity, so that cohort access is limited to the appropriate organization.
10. As a compliance owner, I want retention and deletion behavior applied consistently to operational Veteran data and derived analytics, so that records are not retained longer than policy permits.
11. As an auditor, I want logs and status output to avoid secret values and unnecessary PII, so that operational diagnostics do not become an exposure channel.
12. As a Match consumer, I want explanations grounded in authorized, minimized factors, so that privacy controls do not weaken trust in the recommendation.

## Implementation Decisions
- FYS-100: Separate the operational Veteran record from an `AnonymizedCandidate` projection. The projection uses a non-reversible or controlled pseudonymous identifier and contains only approved matching features, never direct contact fields.
- FYS-100: Keep operations and analytics logically separate across bronze, silver, and gold. Raw source and operational access remain restricted; silver and gold matching relations receive only the fields required by JobPosting enrichment and Match computation.
- FYS-101 and FYS-105: Read credentials only from runtime secret injection or managed secret scopes. Configuration declares names, validation state, and required/optional status, never production-looking fallback credentials.
- FYS-101 and FYS-105: Establish environment-specific validation: production fails fast for missing required source and warehouse credentials; development can use explicitly marked non-secret fixtures.
- FYS-102: Configure exact approved origins, methods, headers, and credential behavior. Wildcard origins must never be combined with credentialed access.
- FYS-103: Require authentication before Veteran create, update, or sensitive read operations. Authorization must bind the caller to their Veteran record or an approved counselor/Partner role; partner cohort access is scoped by `partner_id`.
- FYS-104: Define retention classes for raw source payloads, operational Veteran PII, anonymized Match features, Match outputs, and security logs. Deletion and retention jobs must propagate to derived records according to policy and legal requirements.
- Preserve the Match serving boundary: Match requests and Veteran retrieval operate over the code-canonical workspace spine. Security controls must wrap that boundary, not introduce an alternate data store.
- The `ready_for_matching` completeness rule is an E005 dependency. Authentication must protect the field, but this epic does not define the profile-gate requirements.

## Testing Decisions
- Verify that anonymization removes direct identifiers and that Match inputs cannot resolve a Veteran identity without authorized operational access.
- Scan tracked configuration and documentation samples for credential patterns; fail when a usable secret or live-looking default is present.
- Test missing required production secrets cause explicit startup or readiness failure without leaking configuration values.
- Test CORS preflight and credentialed requests from approved and rejected origins; assert rejected origins receive no credentialed access.
- Test authorization for Veteran self-service, counselor access, cross-Veteran denial, Partner cohort isolation, and unauthenticated write denial.
- Test retention classification and deletion propagation using fixture Veteran, JobPosting, and Match records.
- Assert logs, health, and error payloads omit secrets and direct PII.

## Out of Scope
- Full identity-provider selection, UI design, and onboarding flow.
- A complete E005 profile implementation or `ready_for_matching` specification.
- Encryption-key rotation program, SOC certification, or legal policy authoring beyond implementing the approved retention policy.
- Partner campaign and placement workflow features.

## Further Notes
- Code-canonical spine: `workspace.fys_bronze.job_postings` → `workspace.fys_silver.veteran_profiles` → `workspace.fys_gold.*`; secure the existing serving path rather than documenting a parallel one.
- GitHub parent epic: E011 = #38. Child FYS IDs: FYS-100, FYS-101, FYS-102, FYS-103, FYS-104, FYS-105.
- Slice 1 relevance: PII projection, secrets-only configuration, and CORS lockdown are required before the real Veteran-to-Match serving flow can be considered safe for early users.
