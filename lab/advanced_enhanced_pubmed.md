# Enhanced PubmedTools Documentation

## Recent Changes to the PubmedTools Class

The `PubmedTools` class has been significantly enhanced with advanced search capabilities, citation analysis, and performance optimizations. These changes transform it from a basic search tool into a comprehensive research assistant for scientific literature exploration.

### 🔄 Key Modifications

| Feature | Description |
|---------|-------------|
| Advanced Search | Added `search_pubmed_advanced()` with multiple filtering options |
| Citation Analysis | New `get_citation_metrics()` and citation search functionality |
| MeSH Term Support | Search using standardized medical subject headings |
| Field-Specific Searching | Target title, abstract, or specific fields |
| Boolean Logic | Enhanced query construction with AND/OR operators |
| Affiliation Filtering | Find research from specific institutions |
| Rate Limiting | Automatic throttling to respect API guidelines |
| Response Caching | Cache results to improve performance |

## 📚 New and Enhanced Functions

### 1. `search_pubmed_advanced()`

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

#### Description
Performs advanced PubMed searches with sophisticated filtering options.

#### Parameters
- `query`: Main search term(s) (optional)
- `author`: Author name in format "Smith JB"
- `journal`: Journal name
- `publication_date`: Date range in format "YYYY:YYYY" or "YYYY/MM/DD:YYYY/MM/DD"
- `publication_type`: Type of publication (e.g., "Review", "Clinical Trial")
- `sort_by`: How to sort results ("relevance", "pub_date", "first_author")
- `filter_free_full_text`: Only return articles with free full text
- `mesh_terms`: MeSH terms separated by semicolons
- `field_restriction`: Restrict search to specific field
- `title_only`: Search only in article titles
- `abstract_only`: Search only in article abstracts
- `boolean_operator`: Operator between terms ("AND", "OR")
- `affiliation`: Filter by author institution
- `cited_by_pmid`: Find articles citing a specific PMID
- `max_results`: Maximum number of results to return

#### Returns
JSON string containing articles matching the criteria

### 2. `get_citation_metrics()`

```python
def get_citation_metrics(pmid: str) -> str
```

#### Description
Analyzes citation metrics for a specific article.

#### Parameters
- `pmid`: PubMed ID of the article to analyze

#### Returns
JSON string containing:
- Article details (title, authors, journal, etc.)
- Citation count
- MeSH terms
- Publication type
- Related articles

### 3. `_make_api_request()`

```python
def _make_api_request(url: str, params: Dict[str, Any]) -> httpx.Response
```

#### Description
Makes API requests with rate limiting and caching.

#### Parameters
- `url`: API endpoint URL
- `params`: API request parameters

#### Returns
Response object from the API

### 4. `_process_citation_search()`

```python
def _process_citation_search(pmid: str, max_results: Optional[int] = None) -> str
```

#### Description
Finds articles that cite a specific paper.

#### Parameters
- `pmid`: PubMed ID to find citations for
- `max_results`: Maximum number of results

#### Returns
JSON string containing the citing articles

## 🧪 Usage Examples with Agno Agents

### Example 1: Systematic Review Agent

```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.pubmed import PubmedTools
from utils.key_manager import ApiKeyManager

# Initialize
key_manager = ApiKeyManager(required_keys=["GEMINI_API_KEY"])
GEMINI_API_KEY = key_manager.get("GEMINI_API_KEY")

# Create systematic review agent
systematic_review_agent = Agent(
    model=Gemini(
        id="gemini-2.0-pro-exp-02-05",
        api_key=GEMINI_API_KEY
    ),
    markdown=True,
    tools=[PubmedTools(
        email="your.email@institution.edu",
        max_results=20,
        results_expanded=True
    )],
    description="""You are a systematic review specialist following PRISMA guidelines.
    For systematic reviews:
    1. Use search_pubmed_advanced with precise search parameters
    2. Use mesh_terms="Term1;Term2" for standardized terminology
    3. Use publication_type="Review" or publication_type="Clinical Trial" as needed
    4. Filter by publication_date to establish time boundaries
    5. Use boolean_operator="AND" for specific intersections of concepts
    6. Screen results for inclusion/exclusion criteria
    7. Extract key data and synthesize findings
    8. Present in PRISMA-compliant format with quality assessment
    """
)

# Example usage
query = """
Conduct a systematic review on SGLT2 inhibitors for heart failure in non-diabetic patients.
Include only clinical trials and reviews from the past 5 years.
"""
systematic_review_agent.print_response(query, markdown=True)
```

### Example 2: Citation Analysis Agent

```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.pubmed import PubmedTools

# Create citation analysis agent
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

# Example usage
query = "Analyze the citation impact of the DAPA-HF trial (PMID: 31535829)"
citation_agent.print_response(query, markdown=True)
```

### Example 3: Research Exploration Agent

```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.pubmed import PubmedTools

# Create research exploration agent
exploration_agent = Agent(
    model=Gemini(id="gemini-2.0-pro-exp-02-05", api_key=GEMINI_API_KEY),
    markdown=True,
    tools=[PubmedTools(email="your.email@institution.edu", max_results=15)],
    description="""You are a research exploration assistant.
    When exploring new research areas:
    1. Use search_pubmed_advanced with broad queries
    2. Use boolean_operator="OR" to cast a wide net
    3. Use mesh_terms to identify established subfields
    4. Find seminal papers using citation metrics
    5. Identify emerging research trends
    6. Map connections between different concepts
    7. Note methodological innovations
    8. Suggest potential research directions based on gaps
    """
)

# Example usage
query = """
I'm interested in exploring the intersection of artificial intelligence and drug discovery.
What are the key research directions, methods, and unsolved problems?
"""
exploration_agent.print_response(query, markdown=True)
```

### Example 4: Clinical Evidence Agent

```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.pubmed import PubmedTools

# Create clinical evidence agent
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

# Example usage
query = """
What's the current evidence for using DOACs vs. warfarin in patients with atrial fibrillation
and moderate chronic kidney disease (CKD stage 3)?
"""
clinical_agent.print_response(query, markdown=True)
```

### Example 5: Research Methodology Agent

```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.pubmed import PubmedTools

# Create methodology agent
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

# Example usage
query = """
What are the current best practices for single-cell RNA sequencing experiments 
with spatial resolution? What are the key methodological challenges?
"""
methodology_agent.print_response(query, markdown=True)
```

### example 6 AI-powered medical research assistant that can intelligently search and analyze medical literature from PubMed based on user queries, following evidence-based medicine principles.

```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.pubmed import PubmedTools


# Create a comprehensive research agent using enhanced PubmedTools
research_agent = Agent(
    model=Gemini(
        id="gemini-2.0-pro-exp-02-05",
        api_key=GEMINI_API_KEY
    ),
    markdown=True,
    tools=[PubmedTools(
        email="your.email@example.com", 
        max_results=5,
        results_expanded=True
    )],
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



## 📖 Advanced Usage Examples

### Example: Finding Papers from Top Institutions

```python
results = pubmed_tool.search_pubmed_advanced(
    query="CRISPR gene editing",
    affiliation="Harvard",
    publication_date="2020:2023",
    sort_by="pub_date"
)
```

### Example: Finding Clinical Practice Guidelines

```python
results = pubmed_tool.search_pubmed_advanced(
    mesh_terms="Practice Guidelines as Topic",
    query="diabetes management",
    publication_type="Guideline",
    filter_free_full_text=True
)
```

### Example: Finding Papers Citing a Landmark Study

```python
results = pubmed_tool.search_pubmed_advanced(
    cited_by_pmid="28445112",  # Example PMID of a landmark paper
    publication_date="2021:2023",
    journal="Nature Medicine"
)
```

### Example: Comprehensive MeSH-Based Search

```python
results = pubmed_tool.search_pubmed_advanced(
    mesh_terms="Alzheimer Disease;Amyloid beta-Peptides;tau Proteins",
    publication_type="Review",
    boolean_operator="AND"
)
```

These enhancements make the PubmedTools class significantly more powerful for researchers, supporting sophisticated literature search strategies, citation analysis, and evidence synthesis workflows.

