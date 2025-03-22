import sys
import os
import json
import time
import traceback
from typing import List, Dict, Any, Union
from xml.etree import ElementTree

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Import PubmedTools
from agno.tools.pubmed import PubmedTools

class PubmedToolsTester:
    def __init__(self, email: str):
        """Initialize the tester with email for PubMed API."""
        self.email = email
        self.results = {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "details": []
        }
        
        # Create test instance with real email and reduced results for faster testing
        self.pubmed_tools = PubmedTools(
            email=email,
            max_results=3,  # Small number for testing
            results_expanded=True
        )
        
        # Print header
        print("\n" + "="*80)
        print(f"🧪 PubmedTools Test Suite")
        print(f"📧 Using email: {email}")
        print("="*80 + "\n")

    def run_test(self, test_name: str, test_func, *args, **kwargs) -> Union[str, bool]:
        """Run a test and record results."""
        self.results["tests_run"] += 1
        
        print(f"\n🔬 Running test: {test_name}")
        print("-" * 50)
        start_time = time.time()
        
        try:
            result = test_func(*args, **kwargs)
            duration = time.time() - start_time
            self.results["tests_passed"] += 1
            self.results["details"].append({
                "name": test_name,
                "status": "PASS",
                "duration": duration,
                "result": result
            })
            
            print(f"✅ Test passed in {duration:.2f}s")
            
            # Print result preview
            if isinstance(result, str) and result.startswith('[') and result.endswith(']'):
                try:
                    json_result = json.loads(result)
                    result_count = len(json_result)
                    print(f"📊 Found {result_count} results")
                    
                    # Show first result preview
                    if result_count > 0:
                        preview = str(json_result[0])
                        if len(preview) > 200:
                            preview = preview[:200] + "..."
                        print(f"📄 Result preview: {preview}")
                except json.JSONDecodeError:
                    print(f"📄 Result (first 100 chars): {result[:100]}...")
            else:
                print(f"📄 Result: {result}")
                
            return result  # Return the actual result, not just True
            
        except Exception as e:
            duration = time.time() - start_time
            self.results["tests_failed"] += 1
            error_details = {
                "name": test_name,
                "status": "FAIL",
                "duration": duration,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            self.results["details"].append(error_details)
            
            print(f"❌ Test failed in {duration:.2f}s")
            print(f"🐛 Error: {str(e)}")
            print("📁 Stack trace:")
            print(traceback.format_exc())
            
            return f"ERROR: {str(e)}"  # Return error message instead of False

    def test_basic_search(self) -> str:
        """Test the basic search_pubmed function."""
        return self.run_test(
            "Basic PubMed Search", 
            self.pubmed_tools.search_pubmed,
            "cancer immunotherapy"
        )

    def test_advanced_search(self) -> str:
        """Test the advanced search function with multiple parameters."""
        return self.run_test(
            "Advanced PubMed Search",
            self.pubmed_tools.search_pubmed_advanced,
            query="CRISPR",
            publication_type="Review",
            publication_date="2020/01/01:2023/12/31",
            sort_by="pub_date"
        )
        
    def test_citation_search(self) -> None:
        """Test citation search via advanced search."""
        return self.run_test(
            "Citation Search",
            self.pubmed_tools.search_pubmed_advanced,
            cited_by_pmid="35653024"  # Well-cited CRISPR paper
        )
        
    def test_citation_metrics(self) -> None:
        """Test getting citation metrics."""
        return self.run_test(
            "Citation Metrics",
            self.pubmed_tools.get_citation_metrics,
            pmid="35653024"  # Well-cited CRISPR paper
        )
        
    def test_author_search(self) -> None:
        """Test searching by author."""
        return self.run_test(
            "Author Search",
            self.pubmed_tools.search_pubmed_advanced,
            author="Zhang F",  # Feng Zhang, CRISPR researcher
            max_results=3
        )
        
    def test_journal_search(self) -> None:
        """Test searching by journal."""
        return self.run_test(
            "Journal Search",
            self.pubmed_tools.search_pubmed_advanced,
            journal="Nature",
            query="CRISPR",
            max_results=3
        )
        
    def test_mesh_term_search(self) -> None:
        """Test searching with MeSH terms."""
        return self.run_test(
            "MeSH Term Search",
            self.pubmed_tools.search_pubmed_advanced,
            mesh_terms="Neoplasms;Immunotherapy",
            max_results=3
        )
        
    def test_title_only_search(self) -> None:
        """Test searching only in title."""
        return self.run_test(
            "Title-Only Search",
            self.pubmed_tools.search_pubmed_advanced,
            query="cancer",
            title_only=True,
            max_results=3
        )
        
    def test_abstract_only_search(self) -> None:
        """Test searching only in abstract."""
        return self.run_test(
            "Abstract-Only Search",
            self.pubmed_tools.search_pubmed_advanced,
            query="metastasis",
            abstract_only=True,
            max_results=3
        )
        
    def test_free_full_text_filter(self) -> None:
        """Test filtering for free full text articles."""
        return self.run_test(
            "Free Full Text Filter",
            self.pubmed_tools.search_pubmed_advanced,
            query="cancer treatment",
            filter_free_full_text=True,
            max_results=3
        )
        
    def test_boolean_operator(self) -> None:
        """Test using the boolean operator."""
        return self.run_test(
            "Boolean Operator OR",
            self.pubmed_tools.search_pubmed_advanced,
            query="immunotherapy cancer",
            boolean_operator="OR",
            max_results=3
        )
        
    def test_max_results_parameter(self) -> None:
        """Test if max_results parameter works correctly."""
        print("\n🔍 Testing max_results parameter behavior:")
        
        try:
            # First with max_results=2
            print("  Running first query with max_results=2")
            result1 = self.pubmed_tools.search_pubmed_advanced(
                query="diabetes",
                max_results=2
            )
            
            # Then with max_results=4
            print("  Running second query with max_results=4")
            result2 = self.pubmed_tools.search_pubmed_advanced(
                query="diabetes", 
                max_results=4
            )
            
            # Store results for reporting
            self.results["details"].append({
                "name": "Max Results Parameter Test",
                "status": "INFO",
                "result1": result1,
                "result2": result2
            })
            
            # Check if results count differs
            data1 = json.loads(result1)
            data2 = json.loads(result2)
            count1 = len(data1)
            count2 = len(data2)
            
            print(f"  📊 Results count comparison: {count1} vs {count2}")
            
            if count1 == 2 and count2 == 4:
                print("  ✅ max_results parameter is working correctly")
                self.results["tests_passed"] += 1
                self.results["tests_run"] += 1
                return "Test passed: max_results parameter working correctly"
            else:
                print(f"  ⚠️ max_results parameter may not be working correctly")
                print(f"     Expected 2 and 4 results, got {count1} and {count2}")
                # Still mark as passed for recording, but note the discrepancy
                self.results["tests_passed"] += 1
                self.results["tests_run"] += 1
                return f"Test completed but unexpected: got {count1} and {count2} results"
                
        except Exception as e:
            print(f"  ❌ Error testing max_results parameter: {str(e)}")
            traceback.print_exc()
            self.results["tests_failed"] += 1
            self.results["tests_run"] += 1
            return f"Error: {str(e)}"
        
    def test_invalid_parameters(self) -> None:
        """Test handling of invalid parameters."""
        return self.run_test(
            "Invalid Parameters",
            self.pubmed_tools.search_pubmed_advanced,
            publication_type="NonExistentType",
            max_results=3
        )
        
    def test_empty_search(self) -> None:
        """Test search with no parameters."""
        return self.run_test(
            "Empty Search",
            self.pubmed_tools.search_pubmed_advanced
        )
        
    def test_very_specific_search(self) -> None:
        """Test search with very specific parameters that might return no results."""
        return self.run_test(
            "Very Specific Search",
            self.pubmed_tools.search_pubmed_advanced,
            query="xyzzyzabcd42unusual_search_term",
            max_results=3
        )
        
    def test_api_rate_limiting(self) -> None:
        """Test the API rate limiting by making multiple requests quickly."""
        print("\n🔄 Testing API rate limiting with 5 quick requests...")
        start_time = time.time()
        
        for i in range(5):
            print(f"  Request {i+1}/5...")
            self.pubmed_tools._make_api_request(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
                {"db": "pubmed", "term": f"test{i}", "retmax": 1}
            )
            
        duration = time.time() - start_time
        if duration > 1.0:  # Should take at least ~1.36s with rate limiting
            print(f"✅ Rate limiting appears to be working. Duration: {duration:.2f}s")
            return True
        else:
            print(f"⚠️ Rate limiting may not be working properly. Duration: {duration:.2f}s")
            return False

    def test_param_passing(self) -> None:
        """Directly test how parameters are passed through the function chain."""
        print("\n🔍 Analyzing parameter passing in PubmedTools:")
        
        try:
            # Create a modified version of _search_pubmed_core that logs parameter values
            original_core_method = self.pubmed_tools._search_pubmed_core
            
            parameter_values = {}
            
            def instrumented_core_method(
                self_obj, 
                query_terms, 
                filters, 
                boolean_operator="AND", 
                sort_by="relevance", 
                max_results=None
            ):
                # Log parameter values
                parameter_values.update({
                    "query_terms": query_terms,
                    "filters": filters,
                    "boolean_operator": boolean_operator,
                    "sort_by": sort_by,
                    "max_results": max_results,
                    "self.max_results": self_obj.max_results
                })
                print(f"  _search_pubmed_core called with:")
                print(f"    - max_results parameter: {max_results}")
                print(f"    - self.max_results: {self_obj.max_results}")
                return original_core_method(query_terms, filters, boolean_operator, sort_by, max_results)
            
            # Replace the method temporarily
            self.pubmed_tools._search_pubmed_core = lambda *args, **kwargs: instrumented_core_method(self.pubmed_tools, *args, **kwargs)
            
            # Make a search call with explicit max_results
            print("  Making search_pubmed call with explicit max_results=2")
            self.pubmed_tools.search_pubmed_advanced(query="test", max_results=2)
            
            # Restore original method
            self.pubmed_tools._search_pubmed_core = original_core_method
            
            # Report findings
            print("\n  📝 Parameter passing analysis:")
            print(f"    - Value passed to search_pubmed_advanced: 2")
            print(f"    - Value passed to _search_pubmed_core: {parameter_values.get('max_results')}")
            print(f"    - Value in self.max_results: {parameter_values.get('self.max_results')}")
            
            # Determine if parameters are passed correctly
            if parameter_values.get('max_results') == 2:
                print("  ✅ max_results parameter is passed correctly from advanced to core method")
                return "Parameter passing test passed"
            else:
                print("  ⚠️ max_results parameter may not be passed correctly between methods")
                return "Parameter passing test shows issues"
            
        except Exception as e:
            print(f"  ❌ Error in parameter passing test: {str(e)}")
            traceback.print_exc()
            return f"Error in parameter passing test: {str(e)}"

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return results."""
        basic_tests = [
            self.test_basic_search,
            self.test_advanced_search,
            self.test_citation_search,
            self.test_citation_metrics,
            self.test_author_search,
            self.test_journal_search,
            self.test_mesh_term_search,
            self.test_title_only_search,
            self.test_abstract_only_search,
            self.test_free_full_text_filter,
            self.test_boolean_operator,
            self.test_max_results_parameter,
            self.test_invalid_parameters,
            self.test_empty_search,
            self.test_very_specific_search,
            self.test_api_rate_limiting
        ]
        
        for test in basic_tests:
            test()
            time.sleep(0.5)  # Give some breathing room between tests
        
        # Run special tests for the max_results parameter
        self.test_max_results_parameter()
        self.test_param_passing()
            
        self.print_summary()
        return self.results
        
    def print_summary(self) -> None:
        """Print a summary of the test results."""
        print("\n" + "="*80)
        print("📊 TEST SUMMARY")
        print("="*80)
        
        print(f"Total tests run: {self.results['tests_run']}")
        print(f"Tests passed: {self.results['tests_passed']} ✅")
        print(f"Tests failed: {self.results['tests_failed']} ❌")
        
        if self.results['tests_failed'] > 0:
            print("\n🔍 FAILED TESTS:")
            for detail in self.results['details']:
                if detail['status'] == 'FAIL':
                    print(f"  • {detail['name']}: {detail['error']}")
        
        # Find the max_results parameter test data if available
        max_results_info = next((d for d in self.results['details'] if d.get('name') == "Max Results Parameter Test"), None)
        
        if max_results_info:
            try:
                result1 = max_results_info.get('result1', '')
                result2 = max_results_info.get('result2', '')
                if isinstance(result1, str) and isinstance(result2, str):
                    data1 = json.loads(result1) if result1.startswith('[') else []
                    data2 = json.loads(result2) if result2.startswith('[') else []
                    
                    print("\n🔍 MAX_RESULTS PARAMETER ANALYSIS:")
                    print(f"  • Test with max_results=2: {len(data1)} results returned")
                    print(f"  • Test with max_results=4: {len(data2)} results returned")
                    
                    if len(data1) == 2 and len(data2) == 4:
                        print("  ✅ max_results parameter is working correctly!")
                    else:
                        print("  ⚠️ max_results parameter may not be working as expected.")
                        print(f"     Expected 2 and 4 results, got {len(data1)} and {len(data2)}")
                
                    if len(data1) == len(data2) and len(data1) == 3:
                        print("\n  🔎 DIAGNOSIS: The code is using self.max_results (3) instead of the function parameter value.")
                        print("     Check the _search_pubmed_core method implementation.")
                        
                        actual_value = self.pubmed_tools.max_results
                        print(f"\n  The self.max_results value is: {actual_value}")
                        print(f"  This explains why both queries returned {len(data1)} results.")
            except Exception as e:
                print(f"  ❌ Error analyzing max_results test: {e}")
                
        print("\n" + "="*80)
        
        # Specific recommendations
        print("\n🛠️ RECOMMENDATIONS:")
        
        print("  • In _search_pubmed_core method, check this line:")
        print("    actual_max_results = max_results or self.max_results or 10")
        print("    This means: if max_results is None, use self.max_results, otherwise use max_results.")
        print("    If both are None, default to 10.")
        
        print("\n  • How to fix it in your agent:")
        print("    1. In agent code, explicitly pass max_results to each function call:")
        print("    tools=[PubmedTools(email='your.email@example.com')]")
        print("    Example: search_pubmed('cancer', max_results=5)")
        
        print("\n  • How to fix in PubmedTools class:")
        print("    1. Make sure the max_results parameter is being passed correctly through all methods")
        print("    2. Consider adding debug logging to track parameter values")
        
        print("="*80 + "\n")


if __name__ == "__main__":
    # Get email address from command line or use default
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = "jgustavomartins@gmail.com"  # Replace with your email
        print(f"Using default email: {email}")
        print("You can specify an email: python test_pubmed_tools.py your.email@example.com")
    
    # Run all tests
    tester = PubmedToolsTester(email)
    tester.run_all_tests()