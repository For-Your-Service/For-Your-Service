"""
Job Matcher

Vector-based job matching using Siamese neural network embeddings.
Finds best job matches for candidate profiles.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class JobMatch:
    """Individual job match result"""

    job_id: str
    job_title: str
    company: str
    location: str
    similarity_score: float  # 0.0-1.0
    matching_skills: List[str]
    salary_range: Optional[str] = None
    remote_option: bool = False
    veteran_friendly: bool = False


@dataclass
class MatchResult:
    """Complete matching results"""

    candidate_id: str
    matches: List[JobMatch]
    total_jobs_searched: int
    avg_similarity: float
    best_match: Optional[JobMatch] = None


class JobMatcher:
    """Matches candidates to jobs using vector embeddings"""

    def __init__(self, similarity_threshold: float = 0.6):
        """
        Initialize job matcher

        Args:
            similarity_threshold: Minimum similarity score for match (0-1)
        """
        self.similarity_threshold = similarity_threshold

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors

        Args:
            vec1: First embedding vector
            vec2: Second embedding vector

        Returns:
            Similarity score 0.0-1.0
        """
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            return 0.0

        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        # Normalize to 0-1 range
        return float((similarity + 1) / 2)

    def find_matches(
        self,
        candidate_embedding: np.ndarray,
        job_embeddings: List[Tuple[str, np.ndarray, Dict]],
        top_k: int = 10,
        location_filter: Optional[str] = None,
        salary_min: Optional[int] = None,
        candidate_input: Optional[Dict] = None,
    ) -> MatchResult:
        """
        Find best job matches for candidate dynamically driven by candidate location input.

        Args:
            candidate_embedding: Candidate's skill vector
            job_embeddings: List of (job_id, embedding, metadata) tuples
            top_k: Number of top matches to return
            location_filter: Optional location filter (e.g., "Greenville, SC" or "Dallas, TX")
            salary_min: Optional minimum salary requirement
            candidate_input: Optional candidate input payload with target_city, target_state, commute_radius_miles

        Returns:
            MatchResult with ranked job matches
        """
        matches = []

        # Extract dynamic location criteria directly from candidate input payload
        if candidate_input:
            target_city = candidate_input.get("target_city")
            target_state = candidate_input.get("target_state")
            remote_ok = candidate_input.get("remote_ok", True)
        elif location_filter:
            parts = [p.strip() for p in location_filter.split(",") if p.strip()]
            target_city = parts[0] if len(parts) > 0 else None
            target_state = parts[1] if len(parts) > 1 else None
            remote_ok = True
        else:
            target_city = None
            target_state = None
            remote_ok = True

        for job_id, job_embedding, metadata in job_embeddings:
            # Dynamic Location Filter: completely agnostic and adaptable to any region
            if target_city or target_state or location_filter:
                job_loc = str(metadata.get("location", ""))
                job_city = str(metadata.get("city", ""))
                job_state = str(metadata.get("state", ""))
                is_remote = metadata.get("remote_option", False) or "remote" in job_loc.lower() or "remote" in job_city.lower()

                if is_remote and remote_ok:
                    loc_matched = True
                elif target_city and target_state:
                    loc_matched = (
                        (job_city and job_city.lower() == target_city.strip().lower() and job_state and job_state.upper() == target_state.strip().upper())
                        or (target_city.strip().lower() in job_loc.lower() and target_state.strip().upper() in job_loc.upper())
                        or (location_filter and location_filter.strip().lower() == job_loc.strip().lower())
                    )
                elif location_filter:
                    loc_matched = location_filter.strip().lower() == job_loc.strip().lower() or location_filter.strip().lower() in job_loc.lower()
                else:
                    loc_matched = True

                if not loc_matched:
                    continue

            if salary_min:
                job_salary = self._extract_min_salary(metadata.get("salary_range"))
                if job_salary and job_salary < salary_min:
                    continue

            # Calculate similarity
            similarity = self.cosine_similarity(candidate_embedding, job_embedding)

            if similarity >= self.similarity_threshold:
                match = JobMatch(
                    job_id=job_id,
                    job_title=metadata.get("title", "Unknown"),
                    company=metadata.get("company", "Unknown"),
                    location=metadata.get("location", "Unknown"),
                    similarity_score=similarity,
                    matching_skills=metadata.get("skills", []),
                    salary_range=metadata.get("salary_range"),
                    remote_option=metadata.get("remote_option", False),
                    veteran_friendly=metadata.get("veteran_friendly", False),
                )
                matches.append(match)

        # Sort by similarity (descending)
        matches.sort(key=lambda m: m.similarity_score, reverse=True)

        # Take top K
        top_matches = matches[:top_k]

        # Calculate statistics
        avg_sim = np.mean([m.similarity_score for m in top_matches]) if top_matches else 0.0
        best = top_matches[0] if top_matches else None

        return MatchResult(
            candidate_id="",  # Set by caller
            matches=top_matches,
            total_jobs_searched=len(job_embeddings),
            avg_similarity=float(avg_sim),
            best_match=best,
        )

    def batch_match(
        self,
        candidate_embeddings: List[Tuple[str, np.ndarray]],
        job_embeddings: List[Tuple[str, np.ndarray, Dict]],
        top_k: int = 10,
    ) -> Dict[str, MatchResult]:
        """
        Match multiple candidates to jobs

        Args:
            candidate_embeddings: List of (candidate_id, embedding) tuples
            job_embeddings: List of (job_id, embedding, metadata) tuples
            top_k: Number of matches per candidate

        Returns:
            Dict mapping candidate_id to MatchResult
        """
        results = {}

        for candidate_id, candidate_emb in candidate_embeddings:
            match_result = self.find_matches(candidate_emb, job_embeddings, top_k=top_k)
            match_result.candidate_id = candidate_id
            results[candidate_id] = match_result

        return results

    def _extract_min_salary(self, salary_range: Optional[str]) -> Optional[int]:
        """
        Extract minimum salary from range string

        Args:
            salary_range: String like "$120K-$180K" or "$150,000"

        Returns:
            Minimum salary as integer or None
        """
        if not salary_range:
            return None

        # Remove currency symbols and commas
        cleaned = salary_range.replace("$", "").replace(",", "")

        # Handle ranges
        if "-" in cleaned:
            min_str = cleaned.split("-")[0].strip()
        else:
            min_str = cleaned.strip()

        # Convert K to thousands
        if "K" in min_str.upper():
            min_str = min_str.upper().replace("K", "000")

        try:
            return int(min_str)
        except ValueError:
            return None

    def rank_by_veteran_preference(self, matches: List[JobMatch]) -> List[JobMatch]:
        """
        Re-rank matches to prioritize veteran-friendly employers

        Args:
            matches: List of job matches

        Returns:
            Re-ranked list with veteran-friendly jobs boosted
        """
        # Boost veteran-friendly scores by 10%
        for match in matches:
            if match.veteran_friendly:
                match.similarity_score = min(1.0, match.similarity_score * 1.1)

        # Re-sort
        matches.sort(key=lambda m: m.similarity_score, reverse=True)
        return matches

    def filter_by_security_clearance(
        self, matches: List[JobMatch], has_clearance: bool
    ) -> List[JobMatch]:
        """
        Filter jobs based on security clearance requirement

        Args:
            matches: List of job matches
            has_clearance: Whether candidate has active clearance

        Returns:
            Filtered matches
        """
        if has_clearance:
            # Show all jobs (clearance is an advantage)
            return matches
        else:
            # Filter out clearance-required jobs
            return [m for m in matches if not m.job_title.lower().endswith("(clearance required)")]
