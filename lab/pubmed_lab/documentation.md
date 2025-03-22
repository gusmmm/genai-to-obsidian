# PubmedTools Documentation

This document provides comprehensive documentation for the `PubmedTools` class in the Agno toolkit, designed for medical literature search and analysis through the PubMed database.

## Table of Contents

- [Technical Details](#technical-details)
  - [Class Overview](#class-overview)
  - [Constructor](#constructor)
  - [Methods](#methods)
- [Integration with Agno Agents](#integration-with-agno-agents)
- [Use Cases](#use-cases)
  - [Biomedical Researcher Workflows](#biomedical-researcher-workflows)
  - [Medical Doctor Workflows](#medical-doctor-workflows)
- [Implementation Examples](#implementation-examples)

## Technical Details

### Class Overview

`PubmedTools` is a toolkit class that enables Agno agents to search, retrieve, and analyze medical literature from PubMed, the comprehensive database of biomedical literature maintained by the National Center for Biotechnology Information (NCBI).

The class provides:
- Simple and advanced PubMed searching
- Citation analysis
- Article metadata extraction
- Rate limiting and caching for efficient API usage

### Constructor

```python
def __init__(
    email: str = "your_email@example.com",
    max_results: Optional[int] = None,
    results_expanded: bool = True,
    api_key: Optional[str] = None,
    cache_duration: int = 86400
)
```

**Parameters:**

- `email` (str): Email address required by NCBI for API usage tracking
- `max_results` (int, optional): Default maximum number of results to return (if not specified in method calls)
- `results_expanded` (bool): Whether to return detailed article information (True) or condensed format (False)
- `api_key` (str, optional): NCBI API key for higher rate limits (recommended for production use)
- `cache_duration` (int): How long to cache results in seconds (default: 24 hours)

### Methods

#### 1. `search_pubmed`

```python
def search_pubmed(self, query: str) -> str
```

**Description:** Basic PubMed search functionality with a simple query string.

**Parameters:**
- `query` (str): Search terms for PubMed

**Returns:**
- JSON string containing formatted article results based on the `results_expanded` setting.

**Example usage:**
```python
results = pubmed_tools.search_pubmed("diabetes mellitus type 2")
```

#### 2. `search_pubmed_advanced`

```python
def search_pubmed_advanced(
    query: str = None,
    author: str = None,
    journal: str = None,
    publication_date: str = None,
    publication_type: str = None,
    sort_by: str = "relevance",
    filter_free_full_text: bool = False,
    mesh_terms: str = None,
    field_restriction: str = None,
    title_only: bool = False,
    abstract_only: bool = False,
    boolean_operator: str = "AND",
    affiliation: str = None,
    cited_by_pmid: str = None,
    max_results: int = None
) -> str
```

**Description:** Comprehensive PubMed search with multiple filtering options and field-specific searching capabilities.

**Parameters:**
- `query` (str, optional): Main search query (can be None if other parameters are used)
- `author` (str, optional): Author name to filter by (format: "Smith JB")
- `journal` (str, optional): Journal name to filter results by
- `publication_date` (str, optional): Date range in format "YYYY:YYYY" or "YYYY/MM/DD:YYYY/MM/DD"
- `publication_type` (str, optional): Type of publication (e.g., "Review", "Clinical Trial")
- `sort_by` (str): How to sort results - options: "relevance", "pub_date", "first_author"
- `filter_free_full_text` (bool): Only return articles with free full text access
- `mesh_terms` (str, optional): Medical Subject Headings to include (use semicolons between terms)
- `field_restriction` (str, optional): Restrict search to a specific field
- `title_only` (bool): Search only in article titles
- `abstract_only` (bool): Search only in abstracts
- `boolean_operator` (str): Operator between terms ("AND", "OR")
- `affiliation` (str, optional): Filter by author institution
- `cited_by_pmid` (str, optional): Find articles that cite a specific PMID
- `max_results` (int, optional): Maximum number of results to return

**Returns:**
- JSON string containing formatted article results based on the `results_expanded` setting.

**Example usage:**
```python
results = pubmed_tools.search_pubmed_advanced(
    query="SGLT2 inhibitors",
    publication_date="2020:2023",
    publication_type="Clinical Trial",
    mesh_terms="Heart Failure;Diabetes Mellitus, Type 2",
    filter_free_full_text=True
)
```

#### 3. `get_citation_metrics`

```python
def get_citation_metrics(self, pmid: str) -> str
```

**Description:** Analyzes citation data and related metrics for a specific article identified by its PubMed ID.

**Parameters:**
- `pmid` (str): PubMed ID of the article to analyze

**Returns:**
- JSON string containing:
  - Article details (title, authors, journal, year, etc.)
  - Citation count
  - MeSH terms
  - Publication type
  - List of related articles

**Example usage:**
```python
metrics = pubmed_tools.get_citation_metrics("31535829")  # PMID for the DAPA-HF trial
```

#### 4. Helper Methods (Internal Use)

The class also includes several internal helper methods:

- `_make_api_request`: Handles API requests with rate limiting and caching
- `_process_citation_search`: Finds articles citing a specific PMID
- `fetch_pubmed_ids`: Retrieves PubMed IDs matching a query
- `fetch_details`: Gets detailed article information for given PMIDs
- `parse_details`: Parses XML responses into structured article data

These methods are used internally by the public methods and typically don't need to be called directly.

## Integration with Agno Agents

To use `PubmedTools` with an Agno agent, you need to:

1. Import the necessary classes
2. Initialize the PubmedTools instance
3. Register it with an Agno agent
4. Provide appropriate system instructions to guide the agent's use of the tools

Basic integration example:

```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.pubmed import PubmedTools
from utils.key_manager import ApiKeyManager

# Initialize
key_manager = ApiKeyManager(required_keys=["GEMINI_API_KEY"])
GEMINI_API_KEY = key_manager.get("GEMINI_API_KEY")

# Create agent with PubmedTools
agent = Agent(
    model=Gemini(
        id="gemini-2.0-pro-exp-02-05",
        api_key=GEMINI_API_KEY
    ),
    markdown=True,
    tools=[PubmedTools(
        email="your.email@institution.edu",
        max_results=10,
        results_expanded=True
    )],
    description="""You are a medical research assistant that helps users find
    relevant medical literature from PubMed."""
)
```

## Use Cases

### Biomedical Researcher Workflows

#### 1. Systematic Review Agent

**Purpose**: Assist with systematic literature reviews following PRISMA guidelines.

**Agent Instructions**:

```python
systematic_review_agent = Agent(
    model=Gemini(id="gemini-2.0-pro-exp-02-05", api_key=GEMINI_API_KEY),
    markdown=True,
    tools=[PubmedTools(email="your.email@institution.edu", max_results=20, results_expanded=True)],
    description="""You are a systematic review specialist following PRISMA guidelines.
    For systematic reviews:
    1. Use search_pubmed_advanced with precise search parameters
    2. Use mesh_terms for standardized terminology (separate terms with semicolons)
    3. Use publication_type="Review" or publication_type="Clinical Trial" as appropriate
    4. Filter by publication_date to establish time boundaries
    5. Use boolean_operator="AND" for specific intersections of concepts
    6. Screen results for inclusion/exclusion criteria
    7. Extract key data and synthesize findings
    8. Present in PRISMA-compliant format with quality assessment
    """
)
```

**Example Implementation**:

```python
# Query for systematic review
query = """
Conduct a systematic review on SGLT2 inhibitors for heart failure in non-diabetic patients.
Include only clinical trials and reviews from the past 5 years.
"""
systematic_review_agent.print_response(query, markdown=True)
```

#### 2. Research Methodology Agent

**Purpose**: Help researchers identify and implement appropriate research methods.

**Agent Instructions**:

```python
methodology_agent = Agent(
    model=Gemini(id="gemini-2.0-pro-exp-02-05", api_key=GEMINI_API_KEY),
    markdown=True,
    tools=[PubmedTools(email="your.email@institution.edu", max_results=10)],
    description="""You are a research methodology specialist.
    When advising on research methods:
    1. Use search_pubmed_advanced with method-specific terms
    2. Use field_restriction to focus on methods sections
    3. Identify established protocols and best practices
    4. Note methodological limitations in existing studies
    5. Compare different approaches to similar research questions
    6. Find validation studies for methods of interest
    7. Identify relevant statistical approaches
    8. Consider ethical implications of different methods
    """
)
```

**Example Implementation**:

```python
# Query about methodology
query = """
What are the current best practices for single-cell RNA sequencing experiments 
with spatial resolution? What are the key methodological challenges?
"""
methodology_agent.print_response(query, markdown=True)
```

#### 3. Citation Analysis Agent

**Purpose**: Analyze the impact and relationships between research papers.

**Agent Instructions**:

```python
citation_agent = Agent(
    model=Gemini(id="gemini-2.0-pro-exp-02-05", api_key=GEMINI_API_KEY),
    markdown=True,
    tools=[PubmedTools(email="your.email@institution.edu", results_expanded=True)],
    description="""You are a citation analysis specialist.
    When analyzing research impact:
    1. Use get_citation_metrics(pmid) to analyze an article's citation profile
    2. Use search_pubmed_advanced(cited_by_pmid="PMID") to find citing articles
    3. Identify citation patterns across time
    4. Note which fields and journals cite the work
    5. Analyze the context in which the article is cited
    6. Identify the most influential related works
    7. Determine if the article has influenced clinical practice guidelines
    8. Create a citation network visualization description
    """
)
```

**Example Implementation**:

```python
# Citation analysis query
query = "Analyze the citation impact of the DAPA-HF trial (PMID: 31535829)"
citation_agent.print_response(query, markdown=True)
```

### Medical Doctor Workflows

#### 1. Clinical Evidence Agent

**Purpose**: Provide evidence-based answers for clinical decision-making.

**Agent Instructions**:

```python
clinical_agent = Agent(
    model=Gemini(id="gemini-2.0-pro-exp-02-05", api_key=GEMINI_API_KEY),
    markdown=True,
    tools=[PubmedTools(email="your.email@institution.edu", results_expanded=True)],
    description="""You are a clinical evidence specialist.
    When supporting clinical decision-making:
    1. Use search_pubmed_advanced with highly specific queries
    2. Prioritize evidence in this order: meta-analyses, RCTs, cohort studies
    3. Use publication_type to filter for highest-quality evidence
    4. Use mesh_terms for precise medical terminology
    5. Focus on patient-relevant outcomes
    6. Note statistical significance and clinical relevance
    7. Extract adverse events and safety data
    8. Consider applicability to different patient populations
    """
)
```

**Example Implementation**:

```python
# Clinical question
query = """
What's the current evidence for using DOACs vs. warfarin in patients with atrial fibrillation
and moderate chronic kidney disease (CKD stage 3)?
"""
clinical_agent.print_response(query, markdown=True)
```

#### 2. Comprehensive Medical Research Assistant

**Purpose**: AI-powered medical research assistant for physicians during clinical practice.

**Agent Instructions**:

```python
research_agent = Agent(
    model=Gemini(id="gemini-2.0-pro-exp-02-05", api_key=GEMINI_API_KEY),
    markdown=True,
    tools=[PubmedTools(email="your.email@example.com", max_results=5, results_expanded=True)],
    description="""You are a specialized medical research assistant with deep expertise in evidence-based medicine.
    
    When handling research questions:
    
    1. ANALYZE the research question to determine the most appropriate search approach
    2. For systematic reviews, use MeSH terms with search_pubmed_advanced
       - Use mesh_terms="Term1;Term2" for standardized medical terminology (separated by semicolons)
       - Note: Use semicolons between MeSH terms, not commas, as MeSH terms often contain commas
    
    3. For precise searching:
       - Use title_only=True when looking for specific concepts
       - Use abstract_only=True for more comprehensive but focused results
       - Use journal="Journal Name" for high-quality source filtering
       - Use publication_type="Review" for overview articles
       - Use publication_type="Clinical Trial" for empirical evidence
       - Use publication_date="2020:2025" for recent research
    
    4. For citation analysis:
       - Use cited_by_pmid="PMID" to find papers citing an important work
       - Use get_citation_metrics(pmid) to analyze influence
    
    5. For institutional research:
       - Use affiliation="Institution Name" to find research from specific organizations
    
    6. ALWAYS prioritize:
       - Highest quality evidence (meta-analyses, RCTs, systematic reviews)
       - Most recent research
       - Articles with most citations when appropriate
       - Full text availability for the researcher
    
    7. SYNTHESIZE information by:
       - Organizing findings by themes
       - Highlighting consensus and contradictions
       - Noting methodological strengths and limitations
       - Explaining relevance to the original question
    
    Maintain scientific rigor and communicate findings using appropriate medical terminology.
    Always provide citation details and links to full text when available.
    """
)
```

**Example Implementation**:

```python
# Complete script for the medical research assistant
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.pubmed import PubmedTools
from utils.key_manager import ApiKeyManager

# Initialize
key_manager = ApiKeyManager(required_keys=["GEMINI_API_KEY"])
GEMINI_API_KEY = key_manager.get("GEMINI_API_KEY")

# Create comprehensive research agent
research_agent = Agent(
    model=Gemini(id="gemini-2.0-pro-exp-02-05", api_key=GEMINI_API_KEY),
    markdown=True,
    tools=[PubmedTools(email="your.email@example.com", max_results=5, results_expanded=True)],
    description="""You are a specialized medical research assistant with deep expertise in evidence-based medicine.
    
    When handling research questions:
    
    1. ANALYZE the research question to determine the most appropriate search approach
    2. For systematic reviews, use MeSH terms with search_pubmed_advanced
       - Use mesh_terms="Term1;Term2" for standardized medical terminology (separated by semicolons)
       - Note: Use semicolons between MeSH terms, not commas, as MeSH terms often contain commas
    
    3. For precise searching:
       - Use title_only=True when looking for specific concepts
       - Use abstract_only=True for more comprehensive but focused results
       - Use journal="Journal Name" for high-quality source filtering
       - Use publication_type="Review" for overview articles
       - Use publication_type="Clinical Trial" for empirical evidence
       - Use publication_date="2020:2025" for recent research
    
    4. For citation analysis:
       - Use cited_by_pmid="PMID" to find papers citing an important work
       - Use get_citation_metrics(pmid) to analyze influence
    
    5. For institutional research:
       - Use affiliation="Institution Name" to find research from specific organizations
    
    6. ALWAYS prioritize:
       - Highest quality evidence (meta-analyses, RCTs, systematic reviews)
       - Most recent research
       - Articles with most citations when appropriate
       - Full text availability for the researcher
    
    7. SYNTHESIZE information by:
       - Organizing findings by themes
       - Highlighting consensus and contradictions
       - Noting methodological strengths and limitations
       - Explaining relevance to the original question
    
    Maintain scientific rigor and communicate findings using appropriate medical terminology.
    Always provide citation details and links to full text when available.""",
    show_tool_calls=True
)

if __name__ == "__main__":
    print("🔬 Enhanced Medical Research Assistant")
    print("Ask a medical research question, or try one of these examples:")
    print("1. 'What are the most recent systematic reviews on SGLT2 inhibitors for heart failure?'")
    print("2. 'Find papers that cite the original study on remdesivir for COVID-19'")
    print("3. 'What's the evidence for cognitive behavioral therapy in treatment-resistant depression?'")
    print("4. 'Compare the methodologies used in recent gene therapy clinical trials for hemophilia'")
    
    query = input("\nEnter your research question: ")
    if not query:
        query = "What are the latest advances in CAR-T cell therapy for solid tumors? Focus on clinical trials from the past 3 years."
    
    print(f"\n🔍 Researching: {query}\n")
    research_agent.print_response(query, markdown=True)
```

#### 3. Practice Guidelines Finder

**Purpose**: Quickly identify current clinical practice guidelines for medical conditions.

**Agent Instructions**:

```python
guidelines_agent = Agent(
    model=Gemini(id="gemini-2.0-pro-exp-02-05", api_key=GEMINI_API_KEY),
    markdown=True,
    tools=[PubmedTools(email="your.email@institution.edu", max_results=10)],
    description="""You are a clinical practice guidelines specialist.
    When finding guidelines:
    1. Use search_pubmed_advanced with condition-specific terms
    2. Use mesh_terms="Practice Guidelines as Topic" with the clinical condition
    3. Use publication_type="Guideline" or publication_type="Practice Guideline"
    4. Filter for most recent guidelines (past 1-5 years)
    5. Identify professional society and organization sources
    6. Note geographic regions where guidelines apply
    7. Summarize key recommendations by evidence level
    8. Highlight differences between competing guidelines when present
    """
)
```

**Example Implementation**:

```python
# Guidelines query
query = """
Find the most recent clinical practice guidelines for managing diabetic foot ulcers,
focusing on infection control and prevention of amputation.
"""
guidelines_agent.print_response(query, markdown=True)
```

#### 4. Adverse Event Monitoring Agent

**Purpose**: Identify safety concerns and adverse events related to medical interventions.

**Agent Instructions**:

```python
adverse_events_agent = Agent(
    model=Gemini(id="gemini-2.0-pro-exp-02-05", api_key=GEMINI_API_KEY),
    markdown=True,
    tools=[PubmedTools(email="your.email@institution.edu", max_results=15)],
    description="""You are an adverse event monitoring specialist.
    When analyzing medication or treatment safety:
    1. Use search_pubmed_advanced with drug/treatment name plus "adverse events" or "safety"
    2. Use mesh_terms like "Drug-Related Side Effects and Adverse Reactions"
    3. Filter for post-marketing surveillance studies and case reports
    4. Look for meta-analyses of safety outcomes
    5. Note frequency and severity of reported events
    6. Identify risk factors for adverse events
    7. Highlight any black box warnings or regulatory actions
    8. Compare safety profiles across similar interventions
    """
)
```

**Example Implementation**:

```python
# Adverse events query
query = """
What are the reported adverse events associated with JAK inhibitors
for rheumatoid arthritis? Are there differences in safety profiles
between different JAK inhibitors?
"""
adverse_events_agent.print_response(query, markdown=True)
```

## Implementation Examples

### Example 1: Finding Papers from Top Institutions

```python
results = pubmed_tool.search_pubmed_advanced(
    query="CRISPR gene editing",
    affiliation="Harvard",
    publication_date="2020:2023",
    sort_by="pub_date"
)
```

### Example 2: Finding Clinical Practice Guidelines

```python
results = pubmed_tool.search_pubmed_advanced(
    mesh_terms="Practice Guidelines as Topic",
    query="diabetes management",
    publication_type="Guideline",
    filter_free_full_text=True
)
```

### Example 3: Finding Papers Citing a Landmark Study

```python
results = pubmed_tool.search_pubmed_advanced(
    cited_by_pmid="28445112",  # Example PMID of a landmark paper
    publication_date="2021:2023",
    journal="Nature Medicine"
)
```

### Example 4: Comprehensive MeSH-Based Search

```python
results = pubmed_tool.search_pubmed_advanced(
    mesh_terms="Alzheimer Disease;Amyloid beta-Peptides;tau Proteins", 
    publication_type="Review",
    boolean_operator="AND"
)
```

### Example 5: Full-Scale Research Assistant Implementation 

```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.pubmed import PubmedTools

def create_research_assistant(api_key):
    """Create and return a comprehensive medical research assistant"""
    return Agent(
        model=Gemini(
            id="gemini-2.0-pro-exp-02-05",
            api_key=api_key
        ),
        markdown=True,
        tools=[PubmedTools(
            email="your.email@institution.edu", 
            max_results=10,
            results_expanded=True,
            api_key=None,  # Add your NCBI API key here for higher rate limits
            cache_duration=86400  # 24-hour cache
        )],
        description="""You are a specialized medical research assistant.
        [Insert detailed instructions from examples above]
        """
    )

if __name__ == "__main__":
    from utils.key_manager import ApiKeyManager
    
    key_manager = ApiKeyManager(required_keys=["GEMINI_API_KEY"])
    api_key = key_manager.get("GEMINI_API_KEY")
    
    assistant = create_research_assistant(api_key)
    
    # Interactive mode
    while True:
        query = input("\nEnter your research question (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
            
        print("\nResearching...\n")
        assistant.print_response(query, markdown=True)
```

This documentation provides a comprehensive overview of the `PubmedTools` class and demonstrates how to integrate it with Agno agents for various medical research applications. The code examples and workflows are designed to address the needs of both biomedical researchers and practicing clinicians.
