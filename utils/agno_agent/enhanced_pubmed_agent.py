import sys
import os
# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.pubmed import PubmedTools
from utils.key_manager import ApiKeyManager

# Initialize the API key manager
key_manager = ApiKeyManager(required_keys=["GEMINI_API_KEY"])
GEMINI_API_KEY = key_manager.get("GEMINI_API_KEY")

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
       - Use publication_date="2020:2023" for recent research
    
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