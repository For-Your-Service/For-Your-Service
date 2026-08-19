# For Your Service — Platform Guardrails & Development Rules ????

## 1. Core Mission & Scope Boundaries
* **Strict Input-Driven Matching:** The application must strictly filter, display, and evaluate jobs matching the exact parameters requested by the user (Target Role/Title, Career Track, Verified Resume Skills, MOS/Branch, Security Clearance, Salary Range, and Commute Radius).
* **Zero Bias & Equal Career Opportunity:** The platform must never favor or default to any single branch, specialty, or industry (e.g. IT/Cloud vs. Logistics vs. Construction vs. Operations). All fields are treated with equal weight unless the veteran specifies otherwise.
* **No Speculative or Hallucinated Data:** Never inject unverified skills or phantom certifications (e.g., PMP, CISSP, AWS) unless explicitly present in the candidate's resume text.

---

## 2. Deterministic Matching & Priority Hierarchy
When matching jobs to a candidate profile, the ranking comparator strictly enforces the following order:

1. **Requested Job Title Match (Priority 1):** Exact or substring matches to the user's entered `Specific Desired Job Title(s)` receive top priority (`+60 pts`, `?? Requested Title Match` badge).
2. **Requested Keyword Match (Priority 2):** Word-token matches in the job title receive second priority (`+48 pts`, `?? Requested Keyword Match` badge).
3. **Requested Role Specialty (Priority 3):** Match in job description or category receives third priority (`+38 pts`, `?? Requested Role Specialty` badge).
4. **Target Career Track (Priority 4):** Positions in the candidate's selected industry track receive fourth priority (`+30 pts` if specific roles given, `+45 pts` if general).
5. **Clearance Eligibility:** Eligible candidates rank before clearance-ineligible candidates. Ineligible candidates receive a `-40 pt` penalty and `? INELIGIBLE` badge.
6. **Highest Compatibility Score:** Overall match score computed from verified skills, MOS crosswalk, salary alignment, and commute distance.

---

## 3. Individual Key Match Factors & Projected Success Breakdown
* **Individual Scorecard per Job:** Every job listing displays an individual **"?? Key Match Factors & Projected Success Breakdown"** container.
* **5 Evaluation Pillars:**
  1. **?? Role & Track Alignment:** Direct match for requested title or track.
  2. **??? Security Clearance:** Satisfies defense clearance requirements vs. direct civilian entry vs. ineligible.
  3. **?? Skills Coverage:** Count and list of matched vs. missing core competencies.
  4. **?? Compensation Fit:** Exact salary range comparison against target.
  5. **?? Location & Travel Distance:** True point-to-point mileage from city center and commute radius compliance (10, 20, 50, 100 miles).
* **?? Projected Success with Self-Improvement:**
  - Current Compatibility Score
  - Projected Compatibility with Skill Bridge (`+X% Uplift`)
  - Estimated Annual Compensation Gain (`+$X/yr`)
  - Direct 100% Free Veteran Funding Links in Tab 2

---

## 4. Geographic Engine & Commute Radius
* Commute distances are calculated via Haversine distance from the center of the candidate's chosen target city.
* Commute radii supported: `10 miles`, `20 miles`, `50 miles`, `100 miles`, and `Any Distance / Nationwide`.
* Remote and flexible positions are always treated as universal matches.
