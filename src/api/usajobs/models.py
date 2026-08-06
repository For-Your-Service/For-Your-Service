"""
USAJobs API Data Models
Pydantic models for type-safe API responses
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class PositionRemuneration(BaseModel):
    """Salary information for a federal position"""
    minimum_range: str = Field(alias="MinimumRange")
    maximum_range: str = Field(alias="MaximumRange")
    rate_interval_code: str = Field(alias="RateIntervalCode")  # PA = Per Annum
    
    class Config:
        populate_by_name = True


class PositionLocation(BaseModel):
    """Geographic location of a position"""
    location_name: str = Field(alias="LocationName")
    city_name: Optional[str] = Field(None, alias="CityName")
    state_code: Optional[str] = Field(None, alias="StateCode")
    country_code: str = Field(alias="CountryCode")
    latitude: Optional[float] = Field(None, alias="Latitude")
    longitude: Optional[float] = Field(None, alias="Longitude")
    
    class Config:
        populate_by_name = True


class VeteranPreference(BaseModel):
    """Veteran preference information"""
    hiring_path: List[str] = Field(default_factory=list, alias="HiringPath")
    total_openings: Optional[int] = Field(None, alias="TotalOpenings")
    
    class Config:
        populate_by_name = True


class JobPosting(BaseModel):
    """Complete USAJobs job posting"""
    position_id: str = Field(alias="PositionID")
    position_title: str = Field(alias="PositionTitle")
    position_uri: str = Field(alias="PositionURI")
    organization_name: str = Field(alias="OrganizationName")
    department_name: Optional[str] = Field(None, alias="DepartmentName")
    
    position_remuneration: List[PositionRemuneration] = Field(
        default_factory=list, 
        alias="PositionRemuneration"
    )
    position_location: List[PositionLocation] = Field(
        default_factory=list,
        alias="PositionLocation"
    )
    
    position_start_date: str = Field(alias="PositionStartDate")
    position_end_date: str = Field(alias="PositionEndDate")
    publication_start_date: str = Field(alias="PublicationStartDate")
    application_close_date: str = Field(alias="ApplicationCloseDate")
    
    position_schedule: List[Dict[str, Any]] = Field(
        default_factory=list,
        alias="PositionSchedule"
    )
    
    position_offering_type: List[Dict[str, Any]] = Field(
        default_factory=list,
        alias="PositionOfferingType"
    )
    
    qualifications_required: Optional[str] = Field(None, alias="QualificationsRequired")
    job_category: List[Dict[str, Any]] = Field(default_factory=list, alias="JobCategory")
    
    security_clearance: Optional[str] = Field(None, alias="SecurityClearance")
    supervisory_status: Optional[bool] = Field(None, alias="SupervisoryStatus")
    
    user_area: Optional[VeteranPreference] = Field(None, alias="UserArea")
    
    class Config:
        populate_by_name = True


class SearchResult(BaseModel):
    """USAJobs search result wrapper"""
    matched_object_id: str = Field(alias="MatchedObjectId")
    matched_object_descriptor: JobPosting = Field(alias="MatchedObjectDescriptor")
    relevance: float = Field(alias="Relevance")
    
    class Config:
        populate_by_name = True


class SearchResponse(BaseModel):
    """Complete search response from USAJobs API"""
    search_result: Dict[str, Any] = Field(alias="SearchResult")
    language_code: str = Field(alias="LanguageCode")
    
    @property
    def total_jobs(self) -> int:
        """Get total number of jobs found"""
        return int(self.search_result.get("SearchResultCount", 0))
    
    @property
    def jobs(self) -> List[JobPosting]:
        """Extract job postings from search result"""
        items = self.search_result.get("SearchResultItems", [])
        return [
            item["MatchedObjectDescriptor"] 
            for item in items 
            if "MatchedObjectDescriptor" in item
        ]
    
    class Config:
        populate_by_name = True
