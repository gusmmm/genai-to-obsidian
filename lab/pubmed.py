import json
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree
import httpx
import os
import datetime
from agno.tools import Toolkit
from agno.utils.log import logger


class PubmedTools(Toolkit):
    def __init__(
        self,
        email: str = "your_email@example.com",
        max_results: Optional[int] = None,
    ):
        super().__init__(name="pubmed")
        self.max_results: Optional[int] = max_results
        self.email: str = email

        self.register(self.search_pubmed)

    def fetch_pubmed_ids(self, query: str, max_results: int, email: str) -> List[str]:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
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

    def search_pubmed(self, query: str, max_results: int = 10) -> str:
        """Use this function to search PubMed for articles.

        Args:
            query (str): The search query.
            max_results (int): The maximum number of results to return.

        Returns:
            str: A JSON string containing the search results.
        """
        try:
            logger.debug(f"Searching PubMed for: {query}")
            ids = self.fetch_pubmed_ids(query, self.max_results or max_results, self.email)
            details_root = self.fetch_details(ids)
            articles = self.parse_details(details_root)
            results = [
                f"Published: {article.get('Published')}\nTitle: {article.get('Title')}\nSummary:\n{article.get('Summary')}"
                for article in articles
            ]
            return json.dumps(results)
        except Exception as e:
            return f"Cound not fetch articles. Error: {e}"
        

# test the class
if __name__ == "__main__":
    pubmed_tool = PubmedTools(email="jgustavomartins@gmail.com", max_results=15)
    query = "Is there any correlation between parasitemia levels in malaria patients and the mortality?"
    print(f"\n🔍 Searching PubMed for: \"{query}\"\n")
    
    # Get the raw XML data and save it to a file
    print("⬇️ Fetching PubMed IDs...")
    ids = pubmed_tool.fetch_pubmed_ids(query, pubmed_tool.max_results or 3, pubmed_tool.email)
    print(f"✅ Found {len(ids)} article IDs")
    
    print("⬇️ Fetching article details...")
    details_root = pubmed_tool.fetch_details(ids)
    
    # Save the XML to a file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pubmed_results_{timestamp}.xml"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    # Convert ElementTree to string and write to file
    xml_string = ElementTree.tostring(details_root, encoding='utf-8', method='xml')
    with open(filepath, "wb") as file:
        file.write(xml_string)
    print(f"💾 Saved raw XML data to: {filepath}")
    
    # Get the detailed articles directly using parse_details
    detailed_articles = pubmed_tool.parse_details(details_root)
    
    # Print each article with all fields in a readable format
    for i, article in enumerate(detailed_articles, 1):
        print(f"\n📄 Article {i} " + "="*40)
        print(f"📅 Published: {article['Published']}")
        print(f"📌 Title: {article['Title']}")
        print(f"👤 First Author: {article['First_Author']}")
        print(f"📊 Journal: {article['Journal']}")
        print(f"🏷️ Publication Type: {article['Publication_Type']}")
        print(f"🔍 DOI: {article['DOI']}")
        print(f"🌐 PubMed URL: {article['PubMed_URL']}")
        print(f"📑 Full Text URL: {article['Full_Text_URL']}")
        print(f"🔑 Keywords: {article['Keywords']}")
        print(f"🏥 MeSH Terms: {article['MeSH_Terms']}")
        
        print(f"📝 Summary:")
        for summary_line in article['Summary'].split('\n'):
            print(f"   {summary_line}")
        print("=" * 50)
    
    print(f"✅ Found {len(detailed_articles)} articles related to the query.\n")