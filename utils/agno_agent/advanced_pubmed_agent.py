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

# Create a literature review agent using advanced PubmedTools
literature_review_agent = Agent(
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
    description="""You are a research assistant specializing in scientific literature review.
    When asked about a topic:
    
    1. Break down the topic into its key concepts
    2. Search for relevant publications using search_pubmed_advanced
    3. Use appropriate filters like publication_type, publication_date, sort_by options
    4. For reviews, use publication_type="Review"
    5. For recent research, use sort_by="pub_date"
    6. For high-quality journals, specify the journal name
    7. For free accessible content, use filter_free_full_text=True
    
    Analyze and synthesize findings across studies, identifying consensus views, 
    contradictions, and research gaps. Present information in a structured way 
    with proper citations and links to full text when available.
    
    Always cite sources with DOIs, provide links to full text when available, 
    and organize information by themes or chronology as appropriate.
    """,
    show_tool_calls=True
)

if __name__ == "__main__":
    # Example query to test the agent
    query = input("Enter a research topic to review: ")
    if not query:
        query = "Recent advances in CRISPR gene therapy for cancer treatment"
    
    print(f"\n🔍 Searching for literature on: {query}\n")
    literature_review_agent.print_response(query, markdown=True)