import json
import sys
import os
import datetime
# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from utils.key_manager import ApiKeyManager
from agno.tools.pubmed import PubmedTools

def display_results(results, title):
    """Helper function to display search results nicely formatted"""
    print(f"\n{'='*20} {title} {'='*20}")
    try:
        articles = json.loads(results)
        print(f"Found {len(articles)} articles\n")
        
        for i, article in enumerate(articles, 1):
            print(f"Article {i} {'-'*40}")
            # Initialize the in_summary variable before using it
            in_summary = False
            
            # Print each line with appropriate formatting
            for line in article.split('\n'):
                if line.startswith("Summary:"):
                    print("\n📝 Summary:")
                    in_summary = True
                elif in_summary and line.strip():
                    print(f"   {line}")
                elif line.strip():
                    if line.startswith("Title:"):
                        print(f"📌 {line}")
                    elif line.startswith("Published:"):
                        print(f"📅 {line}")
                    elif line.startswith("First Author:"):
                        print(f"👤 {line}")
                    elif line.startswith("Journal:"):
                        print(f"📊 {line}")
                    elif line.startswith("MeSH Terms:"):
                        print(f"🏷️ {line}")
                    elif line.startswith("Cites:"):
                        print(f"🔗 {line}")
                    else:
                        print(f"   {line}")
            print()
    except json.JSONDecodeError:
        print("Error parsing results:")
        print(results)

def test_mesh_terms():
    """Test searching with MeSH terms"""
    print("\nTesting MeSH term searching...")
    pubmed_tool = PubmedTools(email="your.email@example.com", max_results=3)
    
    # Test with single MeSH term
    mesh_term = "Diabetes Mellitus, Type 2"
    print(f"Query with MeSH Term: {mesh_term}")
    
    results = pubmed_tool.search_pubmed_advanced(
        query="treatment",
        mesh_terms=mesh_term,
        max_results=3
    )
    display_results(results, "MeSH Term Search - Single Term")
    
    # Test with multiple MeSH terms
    mesh_terms = "Hypertension;Treatment Outcome"  # Now using semicolons
    print(f"\nQuery with Multiple MeSH Terms: {mesh_terms.replace(';', ', ')}")  # For display
    
    results = pubmed_tool.search_pubmed_advanced(
        mesh_terms=mesh_terms,  # Using string format instead of list
        boolean_operator="AND",
        max_results=3
    )
    display_results(results, "MeSH Term Search - Multiple Terms")

def test_field_restrictions():
    """Test field-specific searching"""
    print("\nTesting field-specific searching...")
    pubmed_tool = PubmedTools(email="your.email@example.com", max_results=3)
    
    # Test title-only search
    query = "artificial intelligence ethics"
    print(f"Title-Only Search: {query}")
    
    results = pubmed_tool.search_pubmed_advanced(
        query=query,
        title_only=True,
        max_results=3
    )
    display_results(results, "Title-Only Search")
    
    # Test abstract-only search
    print(f"\nAbstract-Only Search: {query}")
    
    results = pubmed_tool.search_pubmed_advanced(
        query=query,
        abstract_only=True,
        max_results=3
    )
    display_results(results, "Abstract-Only Search")
    
    # Test custom field restriction
    print(f"\nCustom Field (Affiliation) Search: 'Harvard'")
    
    results = pubmed_tool.search_pubmed_advanced(
        affiliation="Harvard",
        query="gene therapy",
        max_results=3
    )
    display_results(results, "Affiliation Search")

def test_boolean_logic():
    """Test complex boolean logic"""
    print("\nTesting boolean logic...")
    pubmed_tool = PubmedTools(email="your.email@example.com", max_results=3)
    
    # Test OR boolean operator
    print("Testing OR operator with multiple search terms")
    
    results = pubmed_tool.search_pubmed_advanced(
        query="machine learning",
        mesh_terms="Artificial Intelligence;Neural Networks, Computer",  # Changed to semicolon-separated string
        boolean_operator="OR",
        max_results=3
    )
    display_results(results, "Boolean OR Search")
    
    # Rest of function remains unchanged
    print("\nTesting complex filtering with multiple criteria")
    
    results = pubmed_tool.search_pubmed_advanced(
        query="vaccine efficacy",
        publication_date="2022:2023",
        publication_type="Clinical Trial",
        journal="Lancet",
        max_results=3
    )
    display_results(results, "Complex Filtering")

def test_citation_search():
    """Test citation-based searching"""
    print("\nTesting citation-based searching...")
    pubmed_tool = PubmedTools(email="your.email@example.com", max_results=5)
    
    # Use a well-cited PMID (this is an example - you may want to use a different one)
    # This PMID is for a paper on COVID-19
    cited_pmid = "32203977"
    print(f"Finding articles that cite PMID: {cited_pmid}")
    
    results = pubmed_tool.search_pubmed_advanced(
        cited_by_pmid=cited_pmid,
        max_results=3
    )
    display_results(results, "Citation Search")
    
def test_citation_metrics():
    """Test citation metrics function"""
    print("\nTesting citation metrics...")
    pubmed_tool = PubmedTools(email="your.email@example.com")
    
    # Use a well-cited PMID (this is an example - you may want to use a different one)
    pmid = "32203977"
    print(f"Getting citation metrics for PMID: {pmid}")
    
    results = pubmed_tool.get_citation_metrics(pmid)
    
    try:
        metrics = json.loads(results)
        print("\n📊 Citation Metrics")
        print(f"📌 Title: {metrics['article']['title']}")
        print(f"👤 Authors: {metrics['article']['authors']}")
        print(f"📅 Year: {metrics['article']['year']}")
        print(f"📚 Journal: {metrics['article']['journal']}")
        print(f"📝 DOI: {metrics['article']['doi']}")
        print(f"🔢 Citation Count: {metrics['citation_count']}")
        
        if metrics['related_articles']:
            print("\n🔍 Related Articles:")
            for i, article in enumerate(metrics['related_articles'], 1):
                print(f"  {i}. {article['Title']} ({article['Year']})")
                
        print(f"\n🏷️ MeSH Terms: {metrics['mesh_terms']}")
        print(f"📋 Publication Type: {metrics['publication_type']}")
        
    except json.JSONDecodeError:
        print("Error parsing metrics:")
        print(results)

if __name__ == "__main__":
    print("🧪 Testing Enhanced PubMed Tools")
    
    # Test each feature set separately
    test_mesh_terms()
    test_field_restrictions()
    test_boolean_logic()
    test_citation_search()
    test_citation_metrics()
    
    print("\n✅ All tests completed!")