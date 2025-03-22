# Import time for rate limiting
import json
import time
from typing import Any, Dict, List, Optional, Union
from xml.etree import ElementTree

import httpx

from agno.tools import Toolkit
from agno.utils.log import logger


class PubmedTools(Toolkit):
    def __init__(
        self,
        email: str = "your_email@example.com",
        max_results: Optional[int] = None,
        results_expanded: bool = True,
        api_key: Optional[str] = None,  # NCBI API key for higher rate limits
        cache_duration: int = 86400     # Cache results for 24 hours
    ):
        super().__init__(name="pubmed")
        self.max_results: Optional[int] = max_results
        self.email: str = email
        self.results_expanded: bool = results_expanded
        self.api_key = api_key
        self.last_request_time = 0
        self.cache = {}
        self.cache_duration = cache_duration

        # Register functions
        self.register(self.search_pubmed)
        self.register(self.search_pubmed_advanced)
        self.register(self.get_citation_metrics)  # New function

    def fetch_pubmed_ids(self, query: str, max_results: int, email: str) -> List[str]:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        print(f"Max results: {max_results}")
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "email": email,
            "usehistory": "y",
        }
        response = httpx.get(url, params=params)  # type: ignore
        root = ElementTree.fromstring(response.content)
        return [id_elem.text for id_elem in root.findall(".//Id") if id_elem.text is not None]

    def fetch_details(self, pubmed_ids: List[str]) -> ElementTree.Element:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {"db": "pubmed", "id": ",".join(pubmed_ids), "retmode": "xml"}
        response = httpx.get(url, params=params)
        return ElementTree.fromstring(response.content)

    def parse_details(self, xml_root: ElementTree.Element) -> List[Dict[str, Any]]:
        articles = []
        for article in xml_root.findall(".//PubmedArticle"):
            # Get existing fields
            pub_date = article.find(".//PubDate/Year")
            title = article.find(".//ArticleTitle")
            
            # Handle abstract sections with labels (methods, results, etc.)
            abstract_sections = article.findall(".//AbstractText")
            abstract_text = ""
            if abstract_sections:
                for section in abstract_sections:
                    label = section.get("Label", "")
                    if label:
                        abstract_text += f"{label}: {section.text}\n\n"
                    else:
                        abstract_text += f"{section.text}\n\n"
                abstract_text = abstract_text.strip()
            else:
                abstract_text = "No abstract available"
            
            # Get first author
            first_author_elem = article.find(".//AuthorList/Author[1]")
            first_author = "Unknown"
            if first_author_elem is not None:
                last_name = first_author_elem.find("LastName")
                fore_name = first_author_elem.find("ForeName")
                if last_name is not None and fore_name is not None:
                    first_author = f"{last_name.text}, {fore_name.text}"
                elif last_name is not None:
                    first_author = last_name.text
            
            # Get DOI
            doi_elem = article.find(".//ArticleIdList/ArticleId[@IdType='doi']")
            doi = doi_elem.text if doi_elem is not None else "No DOI available"
            
            # Get PMID for URL construction
            pmid_elem = article.find(".//PMID")
            pmid = pmid_elem.text if pmid_elem is not None else ""
            pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "No URL available"
            
            # Check if full text is available via PMC
            pmc_elem = article.find(".//ArticleIdList/ArticleId[@IdType='pmc']")
            full_text_url = "Not available"
            if pmc_elem is not None:
                full_text_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_elem.text}/"
            elif doi_elem is not None:
                full_text_url = f"https://doi.org/{doi}"
            
            # Get keywords
            keywords = []
            for keyword in article.findall(".//KeywordList/Keyword"):
                if keyword.text:
                    keywords.append(keyword.text)
            
            # Get MeSH terms (useful for understanding medical context)
            mesh_terms = []
            for mesh in article.findall(".//MeshHeading/DescriptorName"):
                if mesh.text:
                    mesh_terms.append(mesh.text)
                    
            # Get journal info
            journal_elem = article.find(".//Journal/Title")
            journal = journal_elem.text if journal_elem is not None else "Unknown Journal"
            
            # Publication type (research article, review, etc.)
            pub_types = []
            for pub_type in article.findall(".//PublicationTypeList/PublicationType"):
                if pub_type.text:
                    pub_types.append(pub_type.text)
            
            articles.append({
                "Published": pub_date.text if pub_date is not None else "No date available",
                "Title": title.text if title is not None else "No title available",
                "Summary": abstract_text,
                "First_Author": first_author,
                "DOI": doi,
                "PubMed_URL": pubmed_url,
                "Full_Text_URL": full_text_url,
                "Keywords": ", ".join(keywords) if keywords else "No keywords available",
                "MeSH_Terms": ", ".join(mesh_terms) if mesh_terms else "No MeSH terms available",
                "Journal": journal,
                "Publication_Type": ", ".join(pub_types) if pub_types else "Not specified"
            })
        
        return articles

    def search_pubmed(self, query: str) -> str:
        """Use this function to search PubMed for articles.

        Args:
            query (str): The search query.

        Returns:
            str: A JSON string containing the search results.
        """
        try:
            logger.debug(f"Searching PubMed for: {query}")
            ids = self.fetch_pubmed_ids(query, self.max_results or 10, self.email)
            details_root = self.fetch_details(ids)
            articles = self.parse_details(details_root)
            
            # Create result strings based on configured detail level
            results = []
            for article in articles:
                if self.results_expanded:
                    # Comprehensive format with all metadata
                    article_text = (
                        f"Published: {article.get('Published')}\n"
                        f"Title: {article.get('Title')}\n"
                        f"First Author: {article.get('First_Author')}\n"
                        f"Journal: {article.get('Journal')}\n"
                        f"Publication Type: {article.get('Publication_Type')}\n"
                        f"DOI: {article.get('DOI')}\n"
                        f"PubMed URL: {article.get('PubMed_URL')}\n"
                        f"Full Text URL: {article.get('Full_Text_URL')}\n"
                        f"Keywords: {article.get('Keywords')}\n"
                        f"MeSH Terms: {article.get('MeSH_Terms')}\n"
                        f"Summary:\n{article.get('Summary')}"
                    )
                else:
                    # Concise format with just essential information
                    article_text = (
                        f"Title: {article.get('Title')}\n"
                        f"Published: {article.get('Published')}\n"
                        f"Summary: {article.get('Summary')[:200]}..." if len(article.get('Summary', '')) > 200 
                        else f"Summary: {article.get('Summary')}"
                    )
                results.append(article_text)
            
            return json.dumps(results)
        except Exception as e:
            return f"Could not fetch articles. Error: {e}"

    def search_pubmed_advanced(self, 
                             query: str = None,  # Make query optional
                             author: str = None,
                             journal: str = None,
                             publication_date: str = None,      # Format: YYYY/MM/DD:YYYY/MM/DD
                             publication_type: str = None,      # "Review", "Clinical Trial", etc.
                             sort_by: str = "relevance",        # Options: relevance, pub_date, first_author
                             filter_free_full_text: bool = False,
                             mesh_terms: str = None,  # Changed from Union[str, List[str]]
                             field_restriction: str = None,     # New: restrict to title, abstract, etc.
                             title_only: bool = False,          # New: search only in title
                             abstract_only: bool = False,       # New: search only in abstract
                             boolean_operator: str = "AND",     # New: AND, OR between terms
                             affiliation: str = None,           # New: institution affiliation
                             cited_by_pmid: str = None,         # New: articles citing this PMID
                             max_results: int = None
                             ) -> str:
        """Search PubMed with advanced filtering options.
        
        Args:
            query (str): The main search query.
            author (str, optional): Author name to filter by. Use format: "Smith JB".
            journal (str, optional): Journal name to filter by.
            publication_date (str, optional): Date range in format YYYY/MM/DD:YYYY/MM/DD or YYYY:YYYY.
            publication_type (str, optional): Type of publication (e.g., "Review", "Clinical Trial").
            sort_by (str, optional): How to sort results. Options: relevance, pub_date, first_author.
            filter_free_full_text (bool, optional): Whether to only return articles with free full text.
            mesh_terms (str, optional): Medical Subject Headings to include in search. For multiple terms, 
                                       separate with commas (e.g., "Diabetes Mellitus,Hypertension").
            field_restriction (str, optional): Restrict search to specific field (Title, Abstract, etc).
            title_only (bool, optional): Search only in article titles.
            abstract_only (bool, optional): Search only in article abstracts.
            boolean_operator (str, optional): Operator to use between terms (AND, OR).
            affiliation (str, optional): Filter by author affiliation/institution.
            cited_by_pmid (str, optional): Find articles that cite this PMID.
            max_results (int, optional): Maximum number of results to return. Defaults to self.max_results.
            
        Returns:
            str: A JSON string containing the search results.
        """
        try:
            # Handle citation search separately as it uses a different API
            if cited_by_pmid:
                logger.debug(f"Searching for articles citing PMID: {cited_by_pmid}")
                return self._process_citation_search(cited_by_pmid, max_results)
                
            # Start with the base query
            query_terms = []
            
            # Add main query if provided
            if query:  # Check if query is provided
                # Apply field restrictions to the main query
                if title_only:
                    query_terms.append(f"({query})[Title]")
                elif abstract_only:
                    query_terms.append(f"({query})[Abstract]")
                elif field_restriction:
                    query_terms.append(f"({query})[{field_restriction}]")
                else:
                    query_terms.append(f"({query})")
            
            # Process MeSH terms - improved handling for commas within terms
            if mesh_terms:
                # For multiple MeSH terms, we now expect them to be separated by semicolons
                # This avoids conflicts with commas that appear within MeSH terms themselves
                mesh_term_list = [term.strip() for term in mesh_terms.split(';')]
                for term in mesh_term_list:
                    query_terms.append(f"\"{term}\"[MeSH Terms]")
            
            # Add filters as separate terms for proper Boolean logic
            filters = []
            
            if author:
                filters.append(f"{author}[Author]")
            if journal:
                filters.append(f"\"{journal}\"[Journal]")
            if publication_date:
                filters.append(f"{publication_date}[Date - Publication]")
            if publication_type:
                filters.append(f"\"{publication_type}\"[Publication Type]")
            if filter_free_full_text:
                filters.append("free full text[Filter]")
            if affiliation:
                filters.append(f"\"{affiliation}\"[Affiliation]")
                
            # Combine main query terms with the chosen Boolean operator
            if query_terms:
                main_query = f" {boolean_operator} ".join(query_terms)
            else:
                # If no query terms but only filters, use a broad match
                main_query = "all[sb]"
                
            # Add filters with AND operator
            final_query = main_query
            if filters:
                filter_query = " AND ".join(filters)
                final_query = f"({main_query}) AND ({filter_query})"
                
            logger.debug(f"Advanced PubMed search: {final_query}")
            
            # Determine sorting parameter for the API
            sort_param = "relevance"
            if sort_by == "pub_date":
                sort_param = "date"
            elif sort_by == "first_author":
                sort_param = "first_author"
                
            # Use the API request method for rate limiting and caching
            actual_max_results = max_results or self.max_results or 10
            
            # Get article IDs
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            params = {
                "db": "pubmed",
                "term": final_query,
                "retmax": actual_max_results,
                "email": self.email,
                "usehistory": "y",
                "sort": sort_param,
            }
            response = self._make_api_request(url, params)
            root = ElementTree.fromstring(response.content)
            
            ids = [id_elem.text for id_elem in root.findall(".//Id") if id_elem.text is not None]
            
            # Early return if no results
            if not ids:
                return json.dumps(["No articles found matching your criteria."])
                
            # Get article details
            details_root = self.fetch_details(ids)
            articles = self.parse_details(details_root)
            
            # Format results using the existing logic
            results = []
            for article in articles:
                if self.results_expanded:
                    # Comprehensive format with all metadata
                    article_text = (
                        f"Published: {article.get('Published')}\n"
                        f"Title: {article.get('Title')}\n"
                        f"First Author: {article.get('First_Author')}\n"
                        f"Journal: {article.get('Journal')}\n"
                        f"Publication Type: {article.get('Publication_Type')}\n"
                        f"DOI: {article.get('DOI')}\n"
                        f"PubMed URL: {article.get('PubMed_URL')}\n"
                        f"Full Text URL: {article.get('Full_Text_URL')}\n"
                        f"Keywords: {article.get('Keywords')}\n"
                        f"MeSH Terms: {article.get('MeSH_Terms')}\n"
                        f"Summary:\n{article.get('Summary')}"
                    )
                else:
                    # Concise format with just essential information
                    article_text = (
                        f"Title: {article.get('Title')}\n"
                        f"Published: {article.get('Published')}\n"
                        f"Summary: {article.get('Summary')[:200]}..." if len(article.get('Summary', '')) > 200 
                        else f"Summary: {article.get('Summary')}"
                    )
                results.append(article_text)
            
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error in advanced PubMed search: {e}")
            return f"Could not fetch articles with advanced search. Error: {e}"
    
    # Add new helper method for advanced search with sorting
    def fetch_pubmed_ids_advanced(self, query: str, max_results: int, email: str, sort: str = "relevance") -> List[str]:
        """Fetch PubMed IDs with advanced options like sorting.
        
        Args:
            query (str): The search query.
            max_results (int): Maximum number of results to return.
            email (str): Email address for NCBI records.
            sort (str): Sort order for results. Options: relevance, date, first_author.
            
        Returns:
            List[str]: List of PubMed IDs.
        """
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        print(f"Advanced search - Max results: {max_results}, Sort: {sort}")
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "email": email,
            "usehistory": "y",
            "sort": sort,  # Add sorting parameter
        }
        response = httpx.get(url, params=params)  # type: ignore
        root = ElementTree.fromstring(response.content)
        return [id_elem.text for id_elem in root.findall(".//Id") if id_elem.text is not None]

    def _make_api_request(self, url: str, params: Dict[str, Any]):
        """Make API request with rate limiting and proper headers.
        
        Args:
            url (str): The API endpoint URL.
            params (Dict[str, Any]): Parameters for the API call.
            
        Returns:
            httpx.Response: The API response object.
        """
        # Add required parameters
        params["tool"] = "agno-ai-pubmed-tool"
        params["email"] = self.email
        if self.api_key:
            params["api_key"] = self.api_key
        
        # Cache key for this request
        cache_key = f"{url}:{json.dumps(params, sort_keys=True)}"
        
        # Check if we have a cached result
        if cache_key in self.cache:
            cached_time, cached_response = self.cache[cache_key]
            if time.time() - cached_time < self.cache_duration:
                logger.debug("Using cached PubMed response")
                return cached_response
        
        # Apply rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < 0.34:  # Limit to 3 requests per second
            sleep_time = 0.34 - time_since_last
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        # Make request with proper error handling
        try:
            response = httpx.get(url, params=params)
            self.last_request_time = time.time()
            
            # Cache successful responses
            if response.status_code == 200:
                self.cache[cache_key] = (time.time(), response)
                
            return response
        except Exception as e:
            logger.error(f"Error making PubMed API request: {e}")
            raise
    
    def _process_citation_search(self, pmid: str, max_results: Optional[int] = None) -> str:
        """Find articles that cite a specific PMID.
        
        Args:
            pmid (str): The PubMed ID to find citations for.
            max_results (int, optional): Maximum number of results to return.
            
        Returns:
            str: A JSON string containing the citing articles.
        """
        try:
            # Use elink to find citing articles
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
            params = {
                "dbfrom": "pubmed",
                "db": "pubmed",
                "id": pmid,
                "linkname": "pubmed_pubmed_citedin",
                "retmode": "xml"
            }
            
            response = self._make_api_request(url, params)
            link_root = ElementTree.fromstring(response.content)
            
            # Extract cited-by PMIDs
            citing_ids = []
            for link_set in link_root.findall(".//LinkSet"):
                for cited_id in link_set.findall(".//LinkSetDb/Link/Id"):
                    if cited_id.text:
                        citing_ids.append(cited_id.text)
            
            # Limit results if needed
            actual_max_results = max_results or self.max_results or 10
            citing_ids = citing_ids[:actual_max_results]
            
            # If no citing articles found
            if not citing_ids:
                return json.dumps([f"No articles found citing PMID: {pmid}"])
                
            # Fetch details for the citing articles
            details_root = self.fetch_details(citing_ids)
            articles = self.parse_details(details_root)
            
            # Format results 
            results = []
            for article in articles:
                if self.results_expanded:
                    # Comprehensive format with citation context
                    article_text = (
                        f"Published: {article.get('Published')}\n"
                        f"Title: {article.get('Title')}\n"
                        f"First Author: {article.get('First_Author')}\n"
                        f"Journal: {article.get('Journal')}\n"
                        f"Publication Type: {article.get('Publication_Type')}\n"
                        f"DOI: {article.get('DOI')}\n"
                        f"PubMed URL: {article.get('PubMed_URL')}\n"
                        f"Full Text URL: {article.get('Full_Text_URL')}\n"
                        f"Keywords: {article.get('Keywords')}\n"
                        f"MeSH Terms: {article.get('MeSH_Terms')}\n"
                        f"Cites: PMID {pmid}\n"
                        f"Summary:\n{article.get('Summary')}"
                    )
                else:
                    # Concise format with citation note
                    article_text = (
                        f"Title: {article.get('Title')}\n"
                        f"Published: {article.get('Published')}\n"
                        f"Cites: PMID {pmid}\n"
                        f"Summary: {article.get('Summary')[:200]}..." if len(article.get('Summary', '')) > 200 
                        else f"Summary: {article.get('Summary')}"
                    )
                results.append(article_text)
            
            return json.dumps(results)
            
        except Exception as e:
            logger.error(f"Error in citation search: {e}")
            return f"Could not fetch citing articles. Error: {e}"
    
    def get_citation_metrics(self, pmid: str) -> str:
        """Get citation metrics for an article using PubMed Central and Entrez linking.
        
        Args:
            pmid (str): PubMed ID of the article to analyze.
            
        Returns:
            str: A JSON string containing citation metrics and information.
        """
        try:
            # First get the article details
            details_root = self.fetch_details([pmid])
            articles = self.parse_details(details_root)
            
            if not articles:
                return json.dumps({"error": f"No article found with PMID: {pmid}"})
            
            article = articles[0]
            
            # Use elink to find citing articles
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
            params = {
                "dbfrom": "pubmed",
                "db": "pubmed",
                "id": pmid,
                "linkname": "pubmed_pubmed_citedin",
                "retmode": "xml"
            }
            
            response = self._make_api_request(url, params)
            link_root = ElementTree.fromstring(response.content)
            
            # Extract cited-by PMIDs
            citing_ids = []
            for link_set in link_root.findall(".//LinkSet"):
                for cited_id in link_set.findall(".//LinkSetDb/Link/Id"):
                    if cited_id.text:
                        citing_ids.append(cited_id.text)
            
            # Get related articles
            params = {
                "dbfrom": "pubmed",
                "db": "pubmed",
                "id": pmid,
                "linkname": "pubmed_pubmed",
                "retmode": "xml"
            }
            
            response = self._make_api_request(url, params)
            related_root = ElementTree.fromstring(response.content)
            
            # Extract related PMIDs
            related_ids = []
            for link_set in related_root.findall(".//LinkSet"):
                for link_id in link_set.findall(".//LinkSetDb/Link/Id"):
                    if link_id.text and link_id.text != pmid:  # Exclude self
                        related_ids.append(link_id.text)
            
            # Get up to 5 most relevant related articles
            related_ids = related_ids[:5]
            related_details = []
            
            if related_ids:
                related_root = self.fetch_details(related_ids)
                related_articles = self.parse_details(related_root)
                
                for rel_article in related_articles:
                    related_details.append({
                        "Title": rel_article.get("Title"),
                        "Authors": rel_article.get("First_Author"),
                        "Journal": rel_article.get("Journal"),
                        "Year": rel_article.get("Published"),
                        "URL": rel_article.get("PubMed_URL")
                    })
            
            # Compile metrics
            metrics = {
                "article": {
                    "title": article.get("Title"),
                    "authors": article.get("First_Author"),
                    "journal": article.get("Journal"),
                    "year": article.get("Published"),
                    "doi": article.get("DOI"),
                    "full_text_url": article.get("Full_Text_URL")
                },
                "citation_count": len(citing_ids),
                "mesh_terms": article.get("MeSH_Terms"),
                "publication_type": article.get("Publication_Type"),
                "related_articles": related_details
            }
            
            return json.dumps(metrics)
            
        except Exception as e:
            logger.error(f"Error getting citation metrics: {e}")
            return f"Could not fetch citation metrics. Error: {e}"