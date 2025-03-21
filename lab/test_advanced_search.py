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
                    else:
                        print(f"   {line}")
            print()
    except json.JSONDecodeError:
        print("Error parsing results:")
        print(results)

def test_basic_search():
    """Test the basic search functionality as a reference"""
    print("Testing basic PubMed search...")
    pubmed_tool = PubmedTools(email="your.email@example.com", max_results=3)
    
    query = "CRISPR gene editing cancer therapy"
    print(f"Query: {query}")
    
    results = pubmed_tool.search_pubmed(query)
    display_results(results, "Basic Search Results")

def test_advanced_search():
    """Test the advanced search functionality with various filters"""
    print("\nTesting advanced PubMed search...")
    pubmed_tool = PubmedTools(email="your.email@example.com", max_results=5)
    
    # Test 1: Filter by publication type
    query = "Alzheimer's disease"
    publication_type = "Review"
    print(f"Query: {query}, Publication Type: {publication_type}")
    
    results = pubmed_tool.search_pubmed_advanced(
        query=query,
        publication_type=publication_type,
        max_results=3
    )
    display_results(results, "Advanced Search - Reviews Only")
    
    # Test 2: Filter by date and sort by recency
    query = "COVID-19 vaccine efficacy"
    publication_date = "2022:2023"  # Only articles from 2022-2023
    print(f"\nQuery: {query}, Date Range: {publication_date}, Sort by: Most Recent")
    
    results = pubmed_tool.search_pubmed_advanced(
        query=query,
        publication_date=publication_date,
        sort_by="pub_date",
        max_results=3
    )
    display_results(results, "Advanced Search - Recent Articles Sorted by Date")
    
    # Test 3: Filter by author and journal
    query = "cancer immunotherapy"
    author = "Sharma P"  # Example author
    journal = "Nature Medicine"
    print(f"\nQuery: {query}, Author: {author}, Journal: {journal}")
    
    results = pubmed_tool.search_pubmed_advanced(
        query=query,
        author=author,
        journal=journal,
        max_results=3
    )
    display_results(results, "Advanced Search - Specific Author and Journal")
    
    # Test 4: Free full text filter
    query = "machine learning radiology"
    print(f"\nQuery: {query}, Filter: Free Full Text Only")
    
    results = pubmed_tool.search_pubmed_advanced(
        query=query,
        filter_free_full_text=True,
        max_results=3
    )
    display_results(results, "Advanced Search - Free Full Text Only")

if __name__ == "__main__":
    # Test basic search first as reference
    test_basic_search()
    
    # Test advanced search with various filters
    test_advanced_search()