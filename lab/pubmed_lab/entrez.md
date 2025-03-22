---
title: "E-utilities Quick Start - Entrez Programming Utilities Help - NCBI Bookshelf"
source: "https://www.ncbi.nlm.nih.gov/books/NBK25500/"
author:
published:
created: 2025-03-22
description: "Please see our Release Notes for details on recent changes and updates."
tags:
  - "clippings"
---
## Release Notes

Please see our [Release Notes](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter4/#chapter4.Release_Notes) for details on recent changes and updates.

## Announcement

On December 1, 2018, NCBI will begin enforcing the use of new API keys for E-utility calls. Please see [Chapter 2](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter2/) for more details about this important change.

## Introduction

This chapter provides a brief overview of basic E-utility functions along with examples of URL calls. Please see [Chapter 2](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter2/) for a general introduction to these utilities and [Chapter 4](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter4/) for a detailed discussion of syntax and parameters.

*Examples* include live URLs that provide sample outputs.

All E-utility calls share the same base URL:

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

## Searching a Database

### Associating Search Results with Existing Search Results

```
esearch.fcgi?db=<database>&term=<query1>&usehistory=y# esearch produces WebEnv value ($web1) and QueryKey value ($key1) esearch.fcgi?db=<database>&term=<query2>&usehistory=y&WebEnv=$web1# esearch produces WebEnv value ($web2) that contains the results 
of both searches ($key1 and $key2)
```

Input: Any Entrez text query (&term); Entrez database (&db); &usehistory=y; Existing web environment (&WebEnv) from a prior E-utility call

Output: Web environment (&WebEnv) and query key (&query\_key) parameters specifying the location on the Entrez history server of the list of UIDs matching the Entrez query

### For More Information

Please see [ESearch In-Depth](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter4/#chapter4.ESearch) for a full description of ESearch.

### Sample ESearch Output

```
<?xml version="1.0" ?>
<!DOCTYPE eSearchResult PUBLIC "-//NLM//DTD eSearchResult, 11 May 2002//EN"
 "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/eSearch_020511.dtd">
<eSearchResult>
<Count>255147</Count>   # total number of records matching query
<RetMax>20</RetMax># number of UIDs returned in this XML; default=20
<RetStart>0</RetStart># index of first record returned; default=0
<QueryKey>1</QueryKey># QueryKey, only present if &usehistory=y
<WebEnv>0l93yIkBjmM60UBXuvBvPfBIq8-9nIsldXuMP0hhuMH-
8GjCz7F_Dz1XL6z@397033B29A81FB01_0038SID</WebEnv> 
                  # WebEnv; only present if &usehistory=y
      <IdList>
<Id>229486465</Id>    # list of UIDs returned
<Id>229486321</Id>
<Id>229485738</Id>
<Id>229470359</Id>
<Id>229463047</Id>
<Id>229463037</Id>
<Id>229463022</Id>
<Id>229463019</Id>
<Id>229463007</Id>
<Id>229463002</Id>
<Id>229463000</Id>
<Id>229462974</Id>
<Id>229462961</Id>
<Id>229462956</Id>
<Id>229462921</Id>
<Id>229462905</Id>
<Id>229462899</Id>
<Id>229462873</Id>
<Id>229462863</Id>
<Id>229462862</Id>
</IdList>
<TranslationSet>        # details of how Entrez translated the query
    <Translation>
     <From>mouse[orgn]</From>
     <To>"Mus musculus"[Organism]</To>
    </Translation>
</TranslationSet>
<TranslationStack>
   <TermSet>
    <Term>"Mus musculus"[Organism]</Term>
    <Field>Organism</Field>
    <Count>255147</Count>
    <Explode>Y</Explode>
   </TermSet>
   <OP>GROUP</OP>
</TranslationStack>
<QueryTranslation>"Mus musculus"[Organism]</QueryTranslation>
</eSearchResult>
```

## Uploading UIDs to Entrez

### Associating a Set of UIDs with Previously Posted Sets

```
epost.fcgi?db=<database1>&id=<uid_list1># epost produces WebEnv value ($web1) and QueryKey value ($key1)epost.fcgi?db=<database2>&id=<uid_list2>&WebEnv=$web1# epost produces WebEnv value ($web2) that contains the results of both 
posts ($key1 and $key2)
```

Input: List of UIDs (&id); Entrez database (&db); Existing web environment (&WebEnv)

Output: Web environment (&WebEnv) and query key (&query\_key) parameters specifying the location on the Entrez history server of the list of uploaded UIDs

### For More Information

Please see [EPost In-Depth](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter4/#chapter4.EPost) for a full description of EPost.

### Sample EPost Output

```
<?xml version="1.0"?>
<!DOCTYPE ePostResult PUBLIC "-//NLM//DTD ePostResult, 11 May 2002//EN"
 "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/ePost_020511.dtd">
<ePostResult>
<QueryKey>1</QueryKey>
<WebEnv>NCID_01_268116914_130.14.18.47_9001_1241798628</WebEnv>
</ePostResult>
```

## Downloading Document Summaries

### Basic Downloading

```
esummary.fcgi?db=<database>&id=<uid_list>
```

Input: List of UIDs (&id); Entrez database (&db)

Output: XML DocSums

*Example: Download DocSums for these protein GIs: 6678417,9507199,28558982,28558984,28558988,28558990*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=protein&id=6678417,9507199,28558982,28558984,28558988,28558990](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=protein&id=6678417,9507199,28558982,28558984,28558988,28558990)

### Downloading Data From a Previous Search

```
esearch.fcgi?db=<database>&term=<query>&usehistory=y# esearch produces WebEnv value ($web1) and QueryKey value ($key1)esummary.fcgi?db=<database>&query_key=$key1&WebEnv=$web1
```

Input: Web environment (&WebEnv) and query key (&query\_key) representing a set of Entrez UIDs on the Entrez history server

Output: XML DocSums

### Sample ESummary Output

The output of ESummary is a series of XML “DocSums” (Document Summaries), the format of which depends on the database. Below is an example DocSum for Entrez Protein.

```
<?xml version="1.0"?>
<!DOCTYPE eSummaryResult PUBLIC "-//NLM//DTD eSummaryResult, 29 October
 2004//EN" "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/eSummary_
041029.dtd">
<eSummaryResult>
<DocSum>
<Id>15718680</Id>
<Item Name="Caption" Type="String">NP_005537</Item>
<Item Name="Title" Type="String">IL2-inducible T-cell kinase [Homo
 sapiens]</Item>
<Item Name="Extra" 
Type="String">gi|15718680|ref|NP_005537.3|[15718680]</Item>
<Item Name="Gi" Type="Integer">15718680</Item>
<Item Name="CreateDate" Type="String">1999/06/09</Item>
<Item Name="UpdateDate" Type="String">2009/04/05</Item>
<Item Name="Flags" Type="Integer">512</Item>
<Item Name="TaxId" Type="Integer">9606</Item>
<Item Name="Length" Type="Integer">620</Item>
<Item Name="Status" Type="String">live</Item>
<Item Name="ReplacedBy" Type="String"></Item>
<Item Name="Comment" Type="String"><![CDATA[  ]]></Item>
</DocSum>
</eSummaryResult>
```

### Sample ESummary version 2.0 Output

Version 2.0 of ESummary is an alternate XML presentation of Entrez DocSums. To retrieve version 2.0 DocSums, the URL should contain the &version parameter with an assigned value of ‘2.0’. Each Entrez database provides its own unique DTD for version 2.0 DocSums, and a link to the relevant DTD is provided in the header of the version 2.0 XML.

```
esummary.fcgi?db=<database>&id=<uid_list>&version=2.0
```

Below is an example version 2.0 DocSum from Entrez Protein (the same record as shown above in the default DocSum XML).

```
<?xml version="1.0"?>
<!DOCTYPE eSummaryResult PUBLIC "-//NLM//DTD eSummaryResult//EN" "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/eSummaryDTD/eSummary_protein.dtd">
<eSummaryResult>
    <DocumentSummarySet status="OK">
        <DocumentSummary uid="15718680">
            <Caption>NP_005537</Caption>
            <Title>tyrosine-protein kinase ITK/TSK [Homo sapiens]</Title>
            <Extra>gi|15718680|ref|NP_005537.3|</Extra>
            <Gi>15718680</Gi>            <CreateDate>1999/06/09</CreateDate>
            <UpdateDate>2011/10/09</UpdateDate>
            <Flags>512</Flags>
            <TaxId>9606</TaxId>
            <Slen>620</Slen>            <Biomol/>            <MolType>aa</MolType>
            <Topology>linear</Topology>
            <SourceDb>refseq</SourceDb>
            <SegSetSize>0</SegSetSize>
            <ProjectId>0</ProjectId>
            <Genome>genomic</Genome>            <SubType>chromosome|map</SubType>
            <SubName>5|5q31-q32</SubName>
            <AssemblyGi>399658</AssemblyGi>
            <AssemblyAcc>D13720.1</AssemblyAcc>
            <Tech/>
            <Completeness/>
            <GeneticCode>1</GeneticCode>            <Strand/>
            <Organism>Homo sapiens</Organism>
            <Statistics>
                <Stat type="all" count="8"/>
                <Stat type="blob_size" count="16154"/>
                <Stat type="cdregion" count="1"/>
                <Stat type="cdregion" subtype="CDS" count="1"/>
                <Stat type="gene" count="1"/>
                <Stat type="gene" subtype="Gene" count="1"/>
                <Stat type="org" count="1"/>
                <Stat type="prot" count="1"/>
                <Stat type="prot" subtype="Prot" count="1"/>
                <Stat type="pub" count="14"/>
                <Stat type="pub" subtype="PubMed" count="10"/>
                <Stat type="pub" subtype="PubMed/Gene-rif" count="4"/>
                <Stat type="site" count="4"/>
                <Stat type="site" subtype="Site" count="4"/>
                <Stat source="CDD" type="all" count="15"/>
                <Stat source="CDD" type="region" count="6"/>
                <Stat source="CDD" type="region" subtype="Region" count="6"/>
                <Stat source="CDD" type="site" count="9"/>
                <Stat source="CDD" type="site" subtype="Site" count="9"/>
                <Stat source="HPRD" type="all" count="3"/>
                <Stat source="HPRD" type="site" count="3"/>
                <Stat source="HPRD" type="site" subtype="Site" count="3"/>
                <Stat source="SNP" type="all" count="31"/>
                <Stat source="SNP" type="imp" count="31"/>
                <Stat source="SNP" type="imp" subtype="variation" count="31"/>
                <Stat source="all" type="all" count="57"/>
                <Stat source="all" type="blob_size" count="16154"/>
                <Stat source="all" type="cdregion" count="1"/>
                <Stat source="all" type="gene" count="1"/>
                <Stat source="all" type="imp" count="31"/>
                <Stat source="all" type="org" count="1"/>
                <Stat source="all" type="prot" count="1"/>
                <Stat source="all" type="pub" count="14"/>
                <Stat source="all" type="region" count="6"/>
                <Stat source="all" type="site" count="16"/>
            </Statistics>
            <AccessionVersion>NP_005537.3</AccessionVersion>
            <Properties aa="2">2</Properties>
            <Comment/>
            <OSLT indexed="yes">NP_005537.3</OSLT>
            <IdGiClass mol="3" repr="2" gi_state="10" sat="4" sat_key="58760802" owner="20"
                sat_name="NCBI" owner_name="NCBI-Genomes" defdiv="GNM" length="620" extfeatmask="41"
            />
        </DocumentSummary>    </DocumentSummarySet>
</eSummaryResult>
```

## Downloading Full Records

### Downloading Data From a Previous Search

```
esearch.fcgi?db=<database>&term=<query>&usehistory=y# esearch produces WebEnv value ($web1) and QueryKey value ($key1)efetch.fcgi?db=<database>&query_key=$key1&WebEnv=$web1&rettype=
<retrieval_type>&retmode=<retrieval_mode>
```

Input: Entrez database (&db); Web environment (&WebEnv) and query key (&query\_key) representing a set of Entrez UIDs on the Entrez history server; Retrieval type (&rettype); Retrieval mode (&retmode)

Output: Formatted data records as specified

### Downloading a Large Set of Records

Please see [Application 3](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter3/#chapter3.Application_3_Retrieving_large) in Chapter 3

Input: Entrez database (&db); Web environment (&WebEnv) and query key (&query\_key) representing a set of Entrez UIDs on the Entrez history server; Retrieval start (&retstart), the first record of the set to retrieve; Retrieval maximum (&retmax), maximum number of records to retrieve

Output: Formatted data records as specified

### For More Information

Please see [EFetch In-Depth](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter4/#chapter4.EFetch) for a full description of EFetch.

## Getting Database Statistics and Search Fields

```
einfo.fcgi?db=<database>
```

Input: Entrez database (&db)

Output: XML containing database statistics

*Note: If no database parameter is supplied, einfo will return a list of all valid Entrez databases.*

*Example: Find database statistics for Entrez Protein.*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=protein](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=protein)

### For More Information

Please see [EInfo In-Depth](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter4/#chapter4.EInfo) for a full description of EInfo.

### Sample EInfo Output

```
<?xml version="1.0"?>
<!DOCTYPE eInfoResult PUBLIC "-//NLM//DTD eInfoResult, 11 May 2002//EN" 
"https://www.ncbi.nlm.nih.gov/entrez/query/DTD/eInfo_020511.dtd">
<eInfoResult>
<DbInfo>
<DbName>protein</DbName>
<MenuName>Protein</MenuName>
<Description>Protein sequence record</Description>
<Count>26715092</Count>
<LastUpdate>2009/05/12 04:39</LastUpdate>
<FieldList>
<Field>
<Name>ALL</Name>
<FullName>All Fields</FullName>
<Description>All terms from all searchable fields</Description>
<TermCount>133639432</TermCount>
<IsDate>N</IsDate>
<IsNumerical>N</IsNumerical>
<SingleToken>N</SingleToken>
<Hierarchy>N</Hierarchy>
<IsHidden>N</IsHidden>
</Field>
...
<Field>
<Name>PORG</Name>
<FullName>Primary Organism</FullName>
<Description>Scientific and common names 
of primary organism, and all higher levels of taxonomy</Description>
<TermCount>673555</TermCount>
<IsDate>N</IsDate>
<IsNumerical>N</IsNumerical>
<SingleToken>Y</SingleToken>
<Hierarchy>Y</Hierarchy>
<IsHidden>N</IsHidden>
</Field>
</FieldList>
<LinkList>
<Link>
<Name>protein_biosystems</Name>
<Menu>BioSystem Links</Menu>
<Description>BioSystems</Description>
<DbTo>biosystems</DbTo>
</Link>
...
<Link>
<Name>protein_unigene</Name>
<Menu>UniGene Links</Menu>
<Description>Related UniGene records</Description>
<DbTo>unigene</DbTo>
</Link>
</LinkList>
</DbInfo>
</eInfoResult>
```

## Performing a Global Entrez Search

```
egquery.fcgi?term=<query>
```

Input: Entrez text query (&term)

Output: XML containing the number of hits in each database.

*Example: Determine the number of records for mouse in Entrez.*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi?term=mouse\[orgn\]](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi?term=mouse%5borgn%5d)

### For More Information

Please see [EGQuery In-Depth](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter4/#chapter4.EGQuery) for a full description of EGQuery.

### Sample EGQuery Output

```
<?xml version="1.0"?>
<!DOCTYPE Result PUBLIC "-//NLM//DTD eSearchResult, January 2004//EN"
 "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/egquery.dtd">
<!--
        $Id: egquery_template.xml 106311 2007-06-26 14:46:31Z osipov $
-->
<!-- ================================================================= -->
<Result>
        <Term>mouse[orgn]</Term>
        <eGQueryResult>
             <ResultItem>
                  <DbName>pubmed</DbName>
                  <MenuName>PubMed</MenuName>
                  <Count>0</Count>
                  <Status>Term or Database is not found</Status>
             </ResultItem>
             <ResultItem>
                  <DbName>pmc</DbName>
                  <MenuName>PMC</MenuName>
                  <Count>3823</Count>
                  <Status>Ok</Status>
             </ResultItem>
...
             <ResultItem>
                  <DbName>nuccore</DbName>
                  <MenuName>Nucleotide</MenuName>
                  <Count>1739903</Count>
                  <Status>Ok</Status>
             </ResultItem>
             <ResultItem>
                  <DbName>nucgss</DbName>
                  <MenuName>GSS</MenuName>
                  <Count>2264567</Count>
                  <Status>Ok</Status>
             </ResultItem>
             <ResultItem>
                  <DbName>nucest</DbName>
                  <MenuName>EST</MenuName>
                  <Count>4852140</Count>
                  <Status>Ok</Status>
             </ResultItem>
             <ResultItem>
                  <DbName>protein</DbName>
                  <MenuName>Protein</MenuName>
                  <Count>255212</Count>
                  <Status>Ok</Status>
             </ResultItem>
...
             <ResultItem>
                  <DbName>proteinclusters</DbName>
                  <MenuName>Protein Clusters</MenuName>
                  <Count>13</Count>
                  <Status>Ok</Status>
             </ResultItem>
        </eGQueryResult>
</Result>
```

## Retrieving Spelling Suggestions

```
espell.fcgi?term=<query>&db=<database>
```

Input: Entrez text query (&term); Entrez database (&db)

Output: XML containing the original query and spelling suggestions.

*Example: Find spelling suggestions for the PubMed Central query ‘fiberblast cell grwth’.*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi?term=fiberblast+cell+grwth&db=pmc](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi?term=fiberblast+cell+grwth&db=pmc)

### For More Information

Please see [ESpell In-Depth](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter4/#chapter4.ESpell) for a full description of EGQuery.

### Sample ESpell Output

```
<?xml version="1.0"?>
<!DOCTYPE eSpellResult PUBLIC "-//NLM//DTD eSpellResult, 23 November 
2004//EN" "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/eSpell.dtd">
<eSpellResult>
<Database>pmc</Database>
<Query>fiberblast cell grwth</Query>
<CorrectedQuery>fibroblast cell growth</CorrectedQuery>
<SpelledQuery>
 <Replaced>fibroblast</Replaced>
 <Original> cell </Original>
 <Replaced>growth</Replaced>
</SpelledQuery>
<ERROR/>
</eSpellResult>
```

## Demonstration Programs

### EBot

[EBot](https://www.ncbi.nlm.nih.gov/Class/PowerTools/eutils/ebot/ebot.cgi) is an interactive web tool that first allows users to construct an arbitrary E-utility analysis pipeline and then generates a Perl script to execute the pipeline. The Perl script can be downloaded and executed on any computer with a Perl installation. For more details, see the EBot page linked above.

### Sample Perl Scripts

The two sample Perl scripts below demonstrate basic E-utility functions. Both scripts should be copied and saved as plain text files and can be executed on any computer with a Perl installation.

ESearch-EFetch demonstrates basic search and retrieval functions.

```
#!/usr/local/bin/perl -w
# =======================================================================
#
#                            PUBLIC DOMAIN NOTICE
#               National Center for Biotechnology Information
#
#  This software/database is a "United States Government Work" under the
#  terms of the United States Copyright Act.  It was written as part of
#  the author's official duties as a United States Government employee and
#  thus cannot be copyrighted.  This software/database is freely available
#  to the public for use. The National Library of Medicine and the U.S.
#  Government have not placed any restriction on its use or reproduction.
#
#  Although all reasonable efforts have been taken to ensure the accuracy
#  and reliability of the software and data, the NLM and the U.S.
#  Government do not and cannot warrant the performance or results that
#  may be obtained by using this software or data. The NLM and the U.S.
#  Government disclaim all warranties, express or implied, including
#  warranties of performance, merchantability or fitness for any particular
#  purpose.
#
#  Please cite the author in any work or product based on this material.
#
# =======================================================================
#
# Author:  Oleg Khovayko
#
# File Description: eSearch/eFetch calling example
#  
# ---------------------------------------------------------------------
# Subroutine to prompt user for variables in the next sectionsub ask_user {
  print "$_[0] [$_[1]]: ";
  my $rc = <>;
  chomp $rc;
  if($rc eq "") { $rc = $_[1]; }
  return $rc;
}# ---------------------------------------------------------------------
# Define library for the 'get' function used in the next section.
# $utils contains route for the utilities.
# $db, $query, and $report may be supplied by the user when prompted; 
# if not answered, default values, will be assigned as shown below.use LWP::Simple;my $utils = "https://www.ncbi.nlm.nih.gov/entrez/eutils";my $db     = ask_user("Database", "Pubmed");
my $query  = ask_user("Query",    "zanzibar");
my $report = ask_user("Report",   "abstract");# ---------------------------------------------------------------------
# $esearch cont?ins the PATH & parameters for the ESearch call
# $esearch_result containts the result of the ESearch call
# the results are displayed ?nd parsed into variables 
# $Count, $QueryKey, and $WebEnv for later use and then displayed.my $esearch = "$utils/esearch.fcgi?" .
              "db=$db&retmax=1&usehistory=y&term=";my $esearch_result = get($esearch . $query);print "\nESEARCH RESULT: $esearch_result\n";$esearch_result =~ 
  m|<Count>(\d+)</Count>.*<QueryKey>(\d+)</QueryKey>.*<WebEnv>(\S+)</WebEnv>|s;my $Count    = $1;
my $QueryKey = $2;
my $WebEnv   = $3;print "Count = $Count; QueryKey = $QueryKey; WebEnv = $WebEnv\n";# ---------------------------------------------------------------------
# this area defines a loop which will display $retmax citation results from 
# Efetch each time the the Enter Key is pressed, after a prompt.my $retstart;
my $retmax=3;for($retstart = 0; $retstart < $Count; $retstart += $retmax) {
  my $efetch = "$utils/efetch.fcgi?" .
               "rettype=$report&retmode=text&retstart=$retstart&retmax=$retmax&" .
               "db=$db&query_key=$QueryKey&WebEnv=$WebEnv";	  print "\nEF_QUERY=$efetch\n";       my $efetch_result = get($efetch);    print "---------\nEFETCH RESULT(". 
         ($retstart + 1) . ".." . ($retstart + $retmax) . "): ".
        "[$efetch_result]\n-----PRESS ENTER!!!-------\n";
  <>;
}
```

EPost-ESummary demonstrates basic uploading and document summary retrieval.

```
#!/usr/local/bin/perl -w
# =======================================================================
#
#                            PUBLIC DOMAIN NOTICE
#               National Center for Biotechnology Information
#
#  This software/database is a "United States Government Work" under the
#  terms of the United States Copyright Act.  It was written as part of
#  the author's official duties as a United States Government employee and
#  thus cannot be copyrighted.  This software/database is freely available
#  to the public for use. The National Library of Medicine and the U.S.
#  Government have not placed any restriction on its use or reproduction.
#
#  Although all reasonable efforts have been taken to ensure the accuracy
#  and reliability of the software and data, the NLM and the U.S.
#  Government do not and cannot warrant the performance or results that
#  may be obtained by using this software or data. The NLM and the U.S.
#  Government disclaim all warranties, express or implied, including
#  warranties of performance, merchantability or fitness for any particular
#  purpose.
#
#  Please cite the author in any work or product based on this material.
#
# =======================================================================
#
# Author:  Oleg Khovayko
#
# File Description: ePost/eSummary calling example
#  # ---------------------------------------------------------------------
my $eutils_root  = "https://www.ncbi.nlm.nih.gov/entrez/eutils";
my $ePost_url    = "$eutils_root/epost.fcgi";
my $eSummary_url = "$eutils_root/esummary.fcgi";my $db_name = "PubMed";# ---------------------------------------------------------------------
use strict;use LWP::UserAgent;
use LWP::Simple;
use HTTP::Request;
use HTTP::Headers;
use CGI;# ---------------------------------------------------------------------
# Read input file into variable $file
# File name - forst argument $ARGV[0]undef $/;  #for load whole fileopen IF, $ARGV[0] || die "Can't open for read: $!\n";
my $file = <IF>;
close IF;
print "Loaded file: [$file]\n";# Prepare file - substitute all separators to comma$file =~ s/\s+/,/gs;
print "Prepared file: [$file]\n";#Create CGI param linemy $form_data = "db=$db_name&id=$file";# ---------------------------------------------------------------------
# Create HTTP requestmy $headers = new HTTP::Headers(
	Accept		=> "text/html, text/plain",
	Content_Type	=> "application/x-www-form-urlencoded"
);my $request = new HTTP::Request("POST", $ePost_url, $headers );$request->content($form_data);# Create the user agent objectmy $ua = new LWP::UserAgent;
$ua->agent("ePost/example");# ---------------------------------------------------------------------
# send file to ePost by HTTPmy $response = $ua->request($request);# ---------------------------------------------------------------------print "Responce status message: [" . $response->message . "]\n";
print "Responce content: [" .        $response->content . "]\n";# ---------------------------------------------------------------------
# Parse response->content and extract QueryKey & WebEnv
$response->content =~ 
  m|<QueryKey>(\d+)</QueryKey>.*<WebEnv>(\S+)</WebEnv>|s;my $QueryKey = $1;
my $WebEnv   = $2;print "\nEXTRACTED:\nQueryKey = $QueryKey;\nWebEnv = $WebEnv\n\n";# ---------------------------------------------------------------------
# Retrieve DocSum from eSummary by simple::get method and print it
#
print "eSummary result: [" . 
  get("$eSummary_url?db=$db_name&query_key=$QueryKey&WebEnv=$WebEnv") . 
  "]\n";
```

## For More Information

### Announcement Mailing List

NCBI posts general announcements regarding the E-utilities to the [utilities-announce announcement mailing list](https://www.ncbi.nlm.nih.gov/mailman/listinfo/utilities-announce/). This mailing list is an announcement list only; individual subscribers may **not** send mail to the list. Also, the list of subscribers is private and is not shared or used in any other way except for providing announcements to list members. The list receives about one posting per month. Please subscribe at the above link.

### Getting Help

Please refer to the [PubMed](https://www.ncbi.nlm.nih.gov/books/n/helppubmed/pubmedhelp/) and [Entrez](https://www.ncbi.nlm.nih.gov/books/n/helpentrez/EntrezHelp/) help documents for more information about search queries, database indexing, field limitations and database content.

Suggestions, comments, and questions specifically relating to the EUtility programs may be sent to [vog.hin.mln.ibcn@seitilitue](https://www.ncbi.nlm.nih.gov/books/NBK25500/).

---
title: "A General Introduction to the E-utilities - Entrez Programming Utilities Help - NCBI Bookshelf"
source: "https://www.ncbi.nlm.nih.gov/books/NBK25497/"
author:
published:
created: 2025-03-22
description: "The Entrez Programming Utilities (E-utilities) are a set of nine server-side programs that provide a stable interface into the Entrez query and database system at the National Center for Biotechnology Information (NCBI). The E-utilities use a fixed URL syntax that translates a standard set of input parameters into the values necessary for various NCBI software components to search for and retrieve the requested data. The E-utilities are therefore the structured interface to the Entrez system, which currently includes 38 databases covering a variety of biomedical data, including nucleotide and protein sequences, gene records, three-dimensional molecular structures, and the biomedical literature."
tags:
  - "clippings"
---
## Introduction

The Entrez Programming Utilities (E-utilities) are a set of nine server-side programs that provide a stable interface into the Entrez query and database system at the National Center for Biotechnology Information (NCBI). The E-utilities use a fixed URL syntax that translates a standard set of input parameters into the values necessary for various NCBI software components to search for and retrieve the requested data. The E-utilities are therefore the structured interface to the Entrez system, which currently includes 38 databases covering a variety of biomedical data, including nucleotide and protein sequences, gene records, three-dimensional molecular structures, and the biomedical literature.

To access these data, a piece of software first posts an E-utility URL to NCBI, then retrieves the results of this posting, after which it processes the data as required. The software can thus use any computer language that can send a URL to the E-utilities server and interpret the XML response; examples of such languages are Perl, Python, Java, and C++. Combining E-utilities components to form customized data pipelines within these applications is a powerful approach to data manipulation.

This chapter first describes the general function and use of the eight E-utilities, followed by basic usage guidelines and requirements, and concludes with a discussion of how the E-utilities function within the Entrez system.

## Usage Guidelines and Requirements

### Use the E-utility URL

All E-utility requests should be made to URLs beginning with the following string:

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/)

These URLs direct requests to servers that are used only by the E-utilities and that are optimized to give users the best performance.

### Frequency, Timing and Registration of E-utility URL Requests

In order not to overload the E-utility servers, NCBI recommends that users post no more than three URL requests per second and limit large jobs to either weekends or between 9:00 PM and 5:00 AM Eastern time during weekdays. Failure to comply with this policy may result in an IP address being blocked from accessing NCBI. If NCBI blocks an IP address, service will not be restored unless the developers of the software accessing the E-utilities register values of the **tool** and **email** parameters with NCBI. The value of **tool** should be a string with no internal spaces that uniquely identifies the software producing the request. The value of **email** should be a complete and valid e-mail address of the software developer and not that of a third-party end user. The value of **email** will be used only to contact developers if NCBI observes requests that violate our policies, and we will attempt such contact prior to blocking access. In addition, developers may request that the value of **email** be added to the E-utility mailing list that provides announcements of software updates, known bugs and other policy changes affecting the E-utilities. To register **tool** and **email** values, simply send an e-mail to [vog.hin.mln.ibcn@seitilitue](https://www.ncbi.nlm.nih.gov/books/NBK25497/) including the desired values along with the name of either a developer or the organization creating the software. Once NCBI establishes communication with a developer, receives values for **tool** and **email** and validates the e-mail address in **email**, the block will be lifted. Once **tool** and **email** values are registered, all subsequent E-utility requests from that software package should contain both values. Please be aware that merely providing values for **tool** and **email** in requests is not sufficient to comply with this policy; these values must be registered with NCBI. Requests from any IP that lack registered values for **tool** and **email** and that violate the above usage policies may be blocked. Software developers may register values of **tool** and **email** at any time, and are encouraged to do so.

### API Keys

Since December 1, 2018, NCBI has provided API keys that offer enhanced levels of supported access to the E-utilities. Without an API key, any site (IP address) posting more than 3 requests per second to the E-utilities will receive an error message. By including an API key, a site can post up to 10 requests per second by default. Higher rates are available by request ([vog.hin.mln.ibcn@seitilitue](https://www.ncbi.nlm.nih.gov/books/NBK25497/)). Users can obtain an API key now from the Settings page of their NCBI account (to create an account, visit [http://www.ncbi.nlm.nih.gov/account/](https://www.ncbi.nlm.nih.gov/account/)). After creating the key, users should include it in each E-utility request by assigning it to the *api\_key* parameter.

```
Example request including an API key:
esummary.fcgi?db=pubmed&id=123456&api_key=ABCDE12345Example error message if rates are exceeded:
{"error":"API rate limit exceeded","count":"11"}
```

Only one API key is allowed per NCBI account; however, a user may request a new key at any time. Such a request will invalidate any existing API key associated with that NCBI account.

### Minimizing the Number of Requests

If a task requires searching for and/or downloading a large number of records, it is much more efficient to use the Entrez History to upload and/or retrieve these records in batches rather than using separate requests for each record. Please refer to [Application 3 in Chapter 3](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter3/#chapter3.Application_3_Retrieving_large) for an example. Many thousands of IDs can be uploaded using a single EPost request, and several hundred records can be downloaded using one EFetch request.

### Disclaimer and Copyright Issues

If you use the E-utilities within software, NCBI's Disclaimer and Copyright notice ([https://www.ncbi.nlm.nih.gov/About/disclaimer.html](https://www.ncbi.nlm.nih.gov/About/disclaimer.html)) must be evident to users of your product. Please note that abstracts in PubMed may incorporate material that may be protected by U.S. and foreign copyright laws. All persons reproducing, redistributing, or making commercial use of this information are expected to adhere to the terms and conditions asserted by the copyright holder. Transmission or reproduction of protected items beyond that allowed by fair use (PDF) as defined in the copyright laws requires the written permission of the copyright owners. NLM provides no legal advice concerning distribution of copyrighted materials. Please consult your legal counsel. If you wish to do a large data mining project on PubMed data, you can download a local copy of the database at [https://www.nlm.nih.gov/databases/download/pubmed\_medline.html](https://www.nlm.nih.gov/databases/download/pubmed_medline.html).

### Handling Special Characters Within URLs

When constructing URLs for the E-utilities, please use lowercase characters for all parameters except &WebEnv. There is no required order for the URL parameters in an E-utility URL, and null values or inappropriate parameters are generally ignored. Avoid placing spaces in the URLs, particularly in queries. If a space is required, use a plus sign (+) instead of a space:

```
Incorrect: &id=352, 25125, 234
Correct:   &id=352,25125,234Incorrect: &term=biomol mrna[properties] AND mouse[organism]
Correct:   &term=biomol+mrna[properties]+AND+mouse[organism]
```

Other special characters, such as quotation marks (“) or the # symbol used in referring to a query key on the History server, should be represented by their URL encodings (%22 for “; %23 for #).

```
Incorrect: &term=#2+AND+"gene in genomic"[properties]
Correct:   &term=%232+AND+%22gene+in+genomic%22[properties]
```

## The Nine E-utilities in Brief

### EInfo (database statistics)

*eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi*

Provides the number of records indexed in each field of a given database, the date of the last update of the database, and the available links from the database to other Entrez databases.

### ESearch (text searches)

*eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi*

Responds to a text query with the list of matching UIDs in a given database (for later use in ESummary, EFetch or ELink), along with the term translations of the query.

### EPost (UID uploads)

*eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi*

Accepts a list of UIDs from a given database, stores the set on the History Server, and responds with a query key and web environment for the uploaded dataset.

### ESummary (document summary downloads)

*eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi*

Responds to a list of UIDs from a given database with the corresponding document summaries.

### EFetch (data record downloads)

*eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi*

Responds to a list of UIDs in a given database with the corresponding data records in a specified format.

### ELink (Entrez links)

*eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi*

Responds to a list of UIDs in a given database with either a list of related UIDs (and relevancy scores) in the same database or a list of linked UIDs in another Entrez database; checks for the existence of a specified link from a list of one or more UIDs; creates a hyperlink to the primary LinkOut provider for a specific UID and database, or lists LinkOut URLs and attributes for multiple UIDs.

### EGQuery (global query)

*eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi*

Responds to a text query with the number of records matching the query in each Entrez database.

### ESpell (spelling suggestions)

*eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi*

Retrieves spelling suggestions for a text query in a given database.

### ECitMatch (batch citation searching in PubMed)

*eutils.ncbi.nlm.nih.gov/entrez/eutils/ecitmatch.cgi*

Retrieves PubMed IDs (PMIDs) corresponding to a set of input citation strings.

## Understanding the E-utilities Within Entrez

### The E-utilities Access Entrez Databases

The E-utilities access the core search and retrieval engine of the Entrez system and, therefore, are only capable of retrieving data that are already in Entrez. Although the majority of data at NCBI are in Entrez, there are several datasets that exist outside of the Entrez system. Before beginning a project with the E-utilities, check that the desired data can be found within an Entrez database.

### The Entrez System Identifies Database Records Using UIDs

Each Entrez database refers to the data records within it by an integer ID called a UID (unique identifier). Examples of UIDs are GI numbers for Nucleotide and Protein, PMIDs for PubMed, or MMDB-IDs for Structure. The E-utilities use UIDs for both data input and output, and thus it is often critical, especially for advanced data pipelines, to know how to find the UIDs associated with the desired data before beginning a project with the E-utilities.

See [Table 1](https://www.ncbi.nlm.nih.gov/books/NBK25497/table/chapter2.T._entrez_unique_identifiers_ui/?report=objectonly) for a complete list of UIDs in Entrez.

[![Table Icon](https://www.ncbi.nlm.nih.gov/corehtml/pmc/css/bookshelf/2.26/img/table-icon.gif)](https://www.ncbi.nlm.nih.gov/books/NBK25497/table/chapter2.T._entrez_unique_identifiers_ui/?report=objectonly "Table 1 ")

#### [Table 1](https://www.ncbi.nlm.nih.gov/books/NBK25497/table/chapter2.T._entrez_unique_identifiers_ui/?report=objectonly)

– Entrez Unique Identifiers (UIDs) for selected databases

### Accessing Sequence Records Using Accession.Version Identifiers

NCBI now uses the accession.version identifier rather that the GI number (UID) as the primary identifier for nucleotide and protein sequence records (records in the nuccore, nucest, nucgss, popset, and protein databases). Even so, the E-utilities continue to provide access to these records using either GI numbers or accession.version identifiers. Those E-utilities that accept UIDs as input will also accept accession.version identifiers (for the sequence databases listed above). Those E-utilities that output UIDs can output accession.version identifiers instead by setting the &idtype parameter to “acc”. Finally, EFetch can retrieve *any* sequence record by its accession.version identifier, including sequences that do not have GI numbers. Please see [Chapter 4](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter4/) for more details about how each E-utility handles accession.version identifers.

### The Entrez Core Engine: EGQuery, ESearch, and ESummary

The core of Entrez is an engine that performs two basic tasks for any Entrez database: 1) assemble a list of UIDs that match a text query, and 2) retrieve a brief summary record called a Document Summary (DocSum) for each UID. These two basic tasks of the Entrez engine are performed by ESearch and ESummary. ESearch returns a list of UIDs that match a text query in a given Entrez database, and ESummary returns DocSums that match a list of input UIDs. A text search in web Entrez is equivalent to ESearch-ESummary. EGQuery is a global version of ESearch that searches all Entrez databases simultaneously. Because these three E-utilities perform the two core Entrez functions, they function for all Entrez databases.

```
egquery.fcgi?term=query
esearch.fcgi?db=database&term=query
esummary.fcgi?db=database&id=uid1,uid2,uid3,...
```

### Syntax and Initial Parsing of Entrez Queries

Text search strings entered into the Entrez system are converted into Entrez queries with the following format:

term1\[field1\] **Op** term2\[field2\] **Op** term3\[field3\] **Op** ...

where the terms are search terms, each limited to a particular Entrez field in square brackets, combined using one of three Boolean operators: Op = AND, OR, or NOT. These Boolean operators must be typed in all capital letters.

Example: human\[organism\] AND topoisomerase\[protein name\]

Entrez initially splits the query into a series of items that were originally separated by spaces in the query; therefore it is critical that spaces separate each term and Boolean operator. If the query consists *only* of a list of UID numbers (unique identifiers) or accession numbers, the Entrez system simply returns the corresponding records and no further parsing is performed. If the query contains any Boolean operators (AND, OR, or NOT), the query is split into the terms separated by these operators, and then each term is parsed independently. The results of these searches are then combined according to the Boolean operators.

A full account of how to search Entrez can be found in the [Entrez Help Document](https://www.ncbi.nlm.nih.gov/books/n/helpentrez/EntrezHelp/). Additional information is available from [Entrez Help](https://www.ncbi.nlm.nih.gov/books/n/helpentrez/).

### Entrez Databases: EInfo, EFetch, and ELink

The NCBI Entrez system currently contains 38 databases. EInfo provides detailed information about each database, including lists of the indexing fields in the database and the available links to other Entrez databases.

```
einfo.fcgi?db=database
```

Each Entrez database includes two primary enhancements to the raw data records: 1) software for producing a variety of display formats appropriate to the given database, and 2) links to records in other Entrez databases manifested as lists of associated UIDs. The display format function is performed by EFetch, which generates formatted output for a list of input UIDs. For example, EFetch can produce abstracts from Entrez PubMed or FASTA format from Entrez Protein. EFetch does not yet support all Entrez databases; please see the [EFetch documentation](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter4/#chapter4.EFetch) for details.

```
efetch.fcgi?db=database&id=uid1,uid2,uid3&rettype=report_type&retmode=
data_mode
```

The linking function is performed by ELink, which generates a list of UIDs in a specified Entrez database that are linked to a set of input UIDs in either the same or another database. For example, ELink can find Entrez SNP records linked to records in Entrez Nucleotide, or Entrez Domain records linked to records in Entrez Protein.

```
elink.fcgi?dbfrom=initial_databasedb=target_database&id=uid1,uid2,uid3
```

### Using the Entrez History Server

A powerful feature of the Entrez system is that it can store retrieved sets of UIDs temporarily on the servers so that they can be subsequently combined or provided as input for other E-utility calls. The Entrez History server provides this service and is accessed on the Web using either the Preview/Index or History tabs on Entrez search pages. Each of the E-utilities can also use the History server, which assigns each set of UIDs an integer label called a query key (&query\_key) and an encoded cookie string called a Web environment (&WebEnv). EPost allows any list of UIDs to be uploaded to the History Server and returns the query key and Web environment. ESearch can also post its output set of UIDs to the History Server, but only if the &usehistory parameter is set to “y”. ELink also can post its output to the History server if &cmd is set to "neighbor\_history". The resulting query key and Web environment from either EPost or ESearch can then be used in place of a UID list in ESummary, EFetch, and ELink.

In Entrez, a set of UIDs is represented on the History by three parameters:

```
&db = database; &query_key = query key; &WebEnv = web environment
```

Upload steps that generate a web environment and query key

```
esearch.fcgi?db=database&term=query&usehistory=yepost.fcgi?db=database&id=uid1,uid2,uid3,...elink.fcgi?dbfrom=source_db&db=destination_db&cmd=neighbor_history&id=
uid1,uid2,...
```

Download steps that use a web environment and query key

```
esummary.fcgi?db=database&WebEnv=webenv&query_key=keyefetch.fcgi?db=database&WebEnv=webenv&query_key=key&rettype=
report_type&retmode=data_mode
```

Link step that uses a web environment and query key

```
elink.fcgi?dbfrom=initial_databasedb=target_database&WebEnv=
webenv&query_key=key
```

Search step that uses a web environment and a query key in the &term parameter (preceded by #, encoded as %23)

```
esearch.fcgi?db=database&term=%23key+AND+query&WebEnv=webenv&usehistory=y
```

### Generating Multiple Data Sets on the History Server

Each web environment on the History Server can be associated with any number of query keys. This allows different data sets to be combined with the Boolean operators AND, OR, and NOT, or with another Entrez query. It is important to remember that for two data sets (query keys) to be combined, they must be associated with the same web environment. By default, successive E-utility calls produce query keys that are *not* associated with the same web environment, and so to overcome this, each E-utility call after the initial call must set the &WebEnv parameter to the value of the pre-existing web environment.

Default behavior: These two URLs…

```
URL 1: epost.fcgi?db=database&id=uid1,uid2,uid3
URL 2: esearch.fcgi?db=database&term=query&usehistory=y
```

will produce two History sets associated with different web environments:

```
URL   WebEnv     query_key        UIDs
1      web1          1        uid1,uid2,uid3
2      web2          1        uids matching query
```

Desired behavior: These two URLs…

```
URL 1: epost.fcgi?db=database&id=uid1,uid2,uid3
(extract web1 from the output of URL 1)
URL 2: esearch.fcgi?db=database&term=query&usehistory=y&WebEnv=web1
```

will produce two sets associated with the same (new) web environment:

```
URL   WebEnv      query_key        UIDs
1      web2          1        uid1,uid2,uid3
2      web2          2        uids matching query
```

## Combining E-utility Calls to Create Entrez Applications

The E-utilities are useful when used by themselves in single URLs; however, their full potential is realized when successive E-utility URLs are combined to create a data pipeline. When used within such pipelines, the Entrez History server simplifies complex retrieval tasks by allowing easy data transfer between successive E-utility calls. Listed below are several examples of pipelines produced by combining E-utilities, with the arrows representing the passing of db, WebEnv and query\_key values from one E-utility to another. These and related pipelines are discussed in detail in Chapter 3.

### Basic Pipelines

### Advanced Pipelines

## Demonstration Programs

Please see [Chapter 1](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter1/#chapter1.Demonstration_Programs) for sample Perl scripts.

## For More Information

Please see [Chapter 1](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter1/#chapter1.For_More_Information_8) for getting additional information about the E-utilities.

---
title: "The E-utilities In-Depth: Parameters, Syntax and More - Entrez Programming Utilities Help - NCBI Bookshelf"
source: "https://www.ncbi.nlm.nih.gov/books/NBK25499/"
author:
published:
created: 2025-03-22
description: "This chapter serves as a reference for all supported parameters for the E-utilities, along with accepted values and usage guidelines. This information is provided for each E-utility in sections below, and parameters and/or values specific to particular databases are discussed within each section. Most E-utilities have a set of parameters that are required for any call, in addition to several additional optional parameters that extend the tool's functionality. These two sets of parameters are discussed separately in each section."
tags:
  - "clippings"
---
## Introduction

This chapter serves as a reference for all supported parameters for the E-utilities, along with accepted values and usage guidelines. This information is provided for each E-utility in sections below, and parameters and/or values specific to particular databases are discussed within each section. Most E-utilities have a set of parameters that are required for any call, in addition to several additional optional parameters that extend the tool's functionality. These two sets of parameters are discussed separately in each section.

## General Usage Guidelines

Please see [Chapter 2](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter2/) for a detailed discussion of E-utility usage policy. The following two parameters should be included in all E-utility requests.

### email

E-mail address of the E-utility user. Value must be a string with no internal spaces, and should be a valid e-mail address.

If you expect to post more than 3 E-utility requests per second from a single IP address, consider including the following parameter:

### **api\_key**

Value of the API key for sites that post more than 3 requests per second. Please see [Chapter 2](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter2/) for a full discussion of this policy.

## E-utilities DTDs

With the exception of EFetch, the E-utilities each generate a single XML output format that conforms to a DTD specific for that utility. Links to these DTDs are provided in the XML headers of the E-utility returns.

ESummary version 2.0 produces unique XML DocSums for each Entrez database, and as such each Entrez database has a unique DTD for version 2.0 DocSums. Links to these DTDs are provided in the version 2.0 XML.

EFetch produces output in a variety of formats, some of which are XML. Most of these XML formats also conform to DTDs or schema specific to the relevant Entrez database. Please follow the appropriate link below for the PubMed DTD:

## EInfo

### Base URL

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi

### Functions

- Provides a list of the names of all valid Entrez databases
- Provides statistics for a single database, including lists of indexing fields and available link names

### Required Parameters

None. If no **db** parameter is provided, einfo will return a list of the names of all valid Entrez databases.

### Optional Parameters

#### version

Used to specify version 2.0 EInfo XML. The only supported value is ‘2.0’. When present, EInfo will return XML that includes two new fields: <IsTruncatable> and <IsRangeable>. Fields that are truncatable allow the wildcard character ‘\*’ in terms. The wildcard character will expand to match any set of characters up to a limit of 600 unique expansions. Fields that are rangeable allow the range operator ‘:’ to be placed between a lower and upper limit for the desired range (e.g. 2008:2010\[pdat\]).

#### retmode

Retrieval type. Determines the format of the returned output. The default value is ‘xml’ for EInfo XML, but ‘json’ is also supported to return output in JSON format.

## ESearch

### Base URL

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi

### Functions

- Provides a list of UIDs matching a text query
- Posts the results of a search on the History server
- Downloads all UIDs from a dataset stored on the History server
- Combines or limits UID datasets stored on the History server
- Sorts sets of UIDs

API users should be aware that some NCBI products contain search tools that generate content from searches on the web interface that are not available to ESearch. For example, the PubMed web interface (pubmed.ncbi.nlm.nih.gov) contains citation matching and spelling correction tools that are only available through that interface. Please see ECitMatch and ESpell below for API equivalents.

### Required Parameters

#### term

Entrez text query. All special characters must be URL encoded. Spaces may be replaced by '+' signs. For very long queries (more than several hundred characters long), consider using an HTTP POST call. See the [PubMed](https://pubmed.ncbi.nlm.nih.gov/help/) or [Entrez](https://www.ncbi.nlm.nih.gov/books/n/helpentrez/EntrezHelp/) help for information about search field descriptions and tags. Search fields and tags are database specific.

```
esearch.fcgi?db=pubmed&term=asthma
```

PubMed also offers “[proximity searching](https://pubmed.ncbi.nlm.nih.gov/help/#proximity-searching)” for multiple terms appearing in any order within a specified number of words from one another in the \[Title\] or \[Title/Abstract\] fields.

```
esearch.fcgi?db=pubmed&term=”asthma treatment”[Title:~3]
```

### Optional Parameters – History Server

#### usehistory

When **usehistory** is set to 'y', ESearch will post the UIDs resulting from the search operation onto the History server so that they can be used directly in a subsequent E-utility call. Also, **usehistory** must be set to 'y' for ESearch to interpret query key values included in **term** or to accept a **WebEnv** as input.

#### WebEnv

Web environment string returned from a previous ESearch, EPost or ELink call. When provided, ESearch will post the results of the search operation to this pre-existing WebEnv, thereby appending the results to the existing environment. In addition, providing **WebEnv** allows query keys to be used in **term** so that previous search sets can be combined or limited. As described above, if **WebEnv** is used, **usehistory** must be set to 'y'.

```
esearch.fcgi?db=pubmed&term=asthma&WebEnv=<webenv string>&usehistory=y
```

#### query\_key

Integer query key returned by a previous ESearch, EPost or ELink call. When provided, ESearch will find the intersection of the set specified by **query\_key** and the set retrieved by the query in **term** (i.e. joins the two with AND). For **query\_key** to function, **WebEnv** must be assigned an existing WebEnv string and **usehistory** must be set to 'y'.

Values for query keys may also be provided in **term** if they are preceeded by a '#' (%23 in the URL). While only one **query\_key** parameter can be provided to ESearch, any number of query keys can be combined in **term**. Also, if query keys are provided in **term**, they can be combined with OR or NOT in addition to AND.

```
The following two URLs are functionally equivalent:esearch.fcgi?db=pubmed&term=asthma&query_key=1&WebEnv=
<webenv string>&usehistory=yesearch.fcgi?db=pubmed&term=%231+AND+asthma&WebEnv=
<webenv string>&usehistory=y
```

### Optional Parameters – Retrieval

#### retstart

Sequential index of the first UID in the retrieved set to be shown in the XML output (default=0, corresponding to the first record of the entire set). This parameter can be used in conjunction with **retmax** to download an arbitrary subset of UIDs retrieved from a search.

#### retmax

Total number of UIDs from the retrieved set to be shown in the XML output (default=20). By default, ESearch only includes the first 20 UIDs retrieved in the XML output. If **usehistory** is set to 'y', the remainder of the retrieved set will be stored on the History server; otherwise these UIDs are lost. Increasing **retmax** allows more of the retrieved UIDs to be included in the XML output, up to a maximum of 10,000 records.

To retrieve more than 10,000 UIDs from databases other than PubMed, submit multiple esearch requests while incrementing the value of **retstart** (see Application 3). For PubMed, ESearch can only retrieve the first 10,000 records matching the query. To obtain more than 10,000 PubMed records, consider using <EDirect> that contains additional logic to batch PubMed search results automatically so that an arbitrary number can be retrieved.

#### rettype

Retrieval type. There are two allowed values for ESearch: 'uilist' (default), which displays the standard XML output, and 'count', which displays only the <Count> tag.

#### retmode

Retrieval type. Determines the format of the returned output. The default value is ‘xml’ for ESearch XML, but ‘json’ is also supported to return output in JSON format.

#### sort

Specifies the method used to sort UIDs in the ESearch output. The available values vary by database (**db**) and may be found in the Display Settings menu on an Entrez search results page. If **usehistory** is set to ‘y’, the UIDs are loaded onto the History Server in the specified sort order and will be retrieved in that order by ESummary or EFetch. Example values are ‘relevance’ and ‘name’ for Gene. Users should be aware that the default value of **sort** varies from one database to another, and that the default value used by ESearch for a given database may differ from that used on NCBI web search pages.

Values of **sort** for PubMed are as follows:

- *pub\_date* – descending sort by publication date
- *Author* – ascending sort by first author
- *JournalName* – ascending sort by journal name
- *relevance* – default sort order, (“Best Match”) on web PubMed

#### field

Search field. If used, the entire search term will be limited to the specified Entrez field. The following two URLs are equivalent:

```
esearch.fcgi?db=pubmed&term=asthma&field=titleesearch.fcgi?db=pubmed&term=asthma[title]
```

#### idtype

Specifies the type of identifier to return for sequence databases (nuccore, popset, protein). By default, ESearch returns GI numbers in its output. If **idtype** is set to ‘acc’, ESearch will return accession.version identifiers rather than GI numbers.

### Optional Parameters – Dates

#### datetype

Type of date used to limit a search. The allowed values vary between Entrez databases, but common values are 'mdat' (modification date), 'pdat' (publication date) and 'edat' (Entrez date). Generally an Entrez database will have only two allowed values for **datetype**.

#### reldate

When **reldate** is set to an integer *n*, the search returns only those items that have a date specified by **datetype** within the last *n* days.

#### mindate, maxdate

Date range used to limit a search result by the date specified by **datetype**. These two parameters (**mindate, maxdate**) must be used together to specify an arbitrary date range. The general date format is YYYY/MM/DD, and these variants are also allowed: YYYY, YYYY/MM.

## EPost

### Base URL

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi

### Functions

- Uploads a list of UIDs to the Entrez History server
- Appends a list of UIDs to an existing set of UID lists attached to a Web Environment

### Required Parameters

#### db

Database containing the UIDs in the input list. The value must be a valid [Entrez database name](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter2/#chapter2.chapter2_table1) (default = pubmed).

#### id

UID list. Either a single UID or a comma-delimited list of UIDs may be provided. All of the UIDs must be from the database specified by **db**. For PubMed, no more than 10,000 UIDs can be included in a single URL request. For other databases there is no set maximum for the number of UIDs that can be passed to epost, but if more than about 200 UIDs are to be posted, the request should be made using the HTTP POST method.

For sequence databases (nuccore, popset, protein), the UID list may be a mixed list of GI numbers and accession.version identifiers. **Note:** When using accession.version identifiers, there is a conversion step that takes place that causes large lists of identifiers to time out, even when using POST. Therefore, we recommend batching these types of requests in sizes of about 500 UIDs or less, to avoid retrieving only a partial amount of records from your original POST input list.

```
epost.fcgi?db=pubmed&id=19393038,30242208,29453458
epost.fcgi?db=protein&id=15718680,NP_001098858.1,119703751
```

### Optional Parameter

#### WebEnv

Web Environment. If provided, this parameter specifies the Web Environment that will receive the UID list sent by post. EPost will create a new query key associated with that Web Environment. Usually this WebEnv value is obtained from the output of a previous ESearch, EPost or ELink call. If no **WebEnv** parameter is provided, EPost will create a new Web Environment and post the UID list to **query\_key** 1.

```
epost.fcgi?db=protein&id=15718680,157427902,119703751&WebEnv=
<webenv string>
```

## ESummary

### Base URL

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi

### Functions

- Returns document summaries (DocSums) for a list of input UIDs
- Returns DocSums for a set of UIDs stored on the Entrez History server

### Required Parameter

#### db

Database from which to retrieve DocSums. The value must be a valid [Entrez database name](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter2/#chapter2.chapter2_table1) (default = pubmed).

### Required Parameter – Used only when input is from a UID list

#### id

UID list. Either a single UID or a comma-delimited list of UIDs may be provided. All of the UIDs must be from the database specified by **db**. There is no set maximum for the number of UIDs that can be passed to ESummary, but if more than about 200 UIDs are to be provided, the request should be made using the HTTP POST method.

For sequence databases (nuccore, popset, protein), the UID list may be a mixed list of GI numbers and accession.version identifiers.

```
esummary.fcgi?db=pubmed&id=19393038,30242208,29453458
esummary.fcgi?db=protein&id=15718680,NP_001098858.1,119703751
```

### Required Parameters – Used only when input is from the Entrez History server

#### query\_key

Query key. This integer specifies which of the UID lists attached to the given Web Environment will be used as input to ESummary. Query keys are obtained from the output of previous ESearch, EPost or ELink calls. The **query\_key** parameter must be used in conjunction with **WebEnv**.

#### WebEnv

Web Environment. This parameter specifies the Web Environment that contains the UID list to be provided as input to ESummary. Usually this WebEnv value is obtained from the output of a previous ESearch, EPost or ELink call. The **WebEnv** parameter must be used in conjunction with **query\_key**.

```
esummary.fcgi?db=protein&query_key=<key>&WebEnv=<webenv string>
```

### Optional Parameters – Retrieval

#### retstart

Sequential index of the first DocSum to be retrieved (default=1, corresponding to the first record of the entire set). This parameter can be used in conjunction with **retmax** to download an arbitrary subset of DocSums from the input set.

#### retmax

Total number of DocSums from the input set to be retrieved, up to a maximum of 10,000. If the total set is larger than this maximum, the value of **retstart** can be iterated while holding **retmax** constant, thereby downloading the entire set in batches of size **retmax**.

#### retmode

Retrieval type. Determines the format of the returned output. The default value is ‘xml’ for ESummary XML, but ‘json’ is also supported to return output in JSON format.

#### version

Used to specify version 2.0 ESummary XML. The only supported value is ‘2.0’. When present, ESummary will return version 2.0 DocSum XML that is unique to each Entrez database and that often contains more data than the default DocSum XML.

## EFetch

### Base URL

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi

### Functions

- Returns formatted data records for a list of input UIDs
- Returns formatted data records for a set of UIDs stored on the Entrez History server

### Required Parameters

#### db

Database from which to retrieve records. The value must be a valid [Entrez database name](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter2/#chapter2.chapter2_table1) (default = pubmed). Currently EFetch does not support all Entrez databases. Please see [Table 1](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter2/#chapter2.T._entrez_unique_identifiers_ui) in Chapter 2 for a list of available databases.

### Required Parameter – Used only when input is from a UID list

#### id

UID list. Either a single UID or a comma-delimited list of UIDs may be provided. All of the UIDs must be from the database specified by **db**. There is no set maximum for the number of UIDs that can be passed to EFetch, but if more than about 200 UIDs are to be provided, the request should be made using the HTTP POST method.

For sequence databases (nuccore, popset, protein), the UID list may be a mixed list of GI numbers and accession.version identifiers.

```
efetch.fcgi?db=pubmed&id=19393038,30242208,29453458
efetch.fcgi?db=protein&id=15718680,NP_001098858.1,119703751
```

*Special note for sequence databases.*

NCBI is no longer assigning GI numbers to a growing number of new sequence records. As such, these records are not indexed in Entrez, and so cannot be retrieved using ESearch or ESummary, and have no Entrez links accessible by ELink. EFetch *can* retrieve these records by including their accession.version identifier in the **id** parameter.

### Required Parameters – Used only when input is from the Entrez History server

#### query\_key

Query key. This integer specifies which of the UID lists attached to the given Web Environment will be used as input to EFetch. Query keys are obtained from the output of previous ESearch, EPost or ELInk calls. The **query\_key** parameter must be used in conjunction with **WebEnv**.

#### WebEnv

Web Environment. This parameter specifies the Web Environment that contains the UID list to be provided as input to EFetch. Usually this WebEnv value is obtained from the output of a previous ESearch, EPost or ELink call. The **WebEnv** parameter must be used in conjunction with **query\_key**.

```
efetch.fcgi?db=protein&query_key=<key>&WebEnv=<webenv string>
```

### Optional Parameters – Retrieval

#### retmode

Retrieval mode. This parameter specifies the data format of the records returned, such as plain text, HMTL or XML. See [Table 1](https://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.T._valid_values_of__retmode_and/?report=objectonly) for a full list of allowed values for each database.

[![Table Icon](https://www.ncbi.nlm.nih.gov/corehtml/pmc/css/bookshelf/2.26/img/table-icon.gif)](https://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.T._valid_values_of__retmode_and/?report=objectonly "Table 1 ")

#### [Table 1](https://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.T._valid_values_of__retmode_and/?report=objectonly)

– Valid values of &retmode and &rettype for EFetch (null = empty string)

#### rettype

Retrieval type. This parameter specifies the record view returned, such as Abstract or MEDLINE from PubMed, or GenPept or FASTA from protein. Please see [Table 1](https://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.T._valid_values_of__retmode_and/?report=objectonly) for a full list of allowed values for each database.

#### retstart

Sequential index of the first record to be retrieved (default=0, corresponding to the first record of the entire set). This parameter can be used in conjunction with **retmax** to download an arbitrary subset of records from the input set.

#### retmax

Total number of records from the input set to be retrieved, up to a maximum of 10,000. Optionally, for a large set the value of **retstart** can be iterated while holding **retmax** constant, thereby downloading the entire set in batches of size **retmax**.

### Optional Parameters – Sequence Databases

#### strand

Strand of DNA to retrieve. Available values are "1" for the plus strand and "2" for the minus strand.

#### seq\_start

First sequence base to retrieve. The value should be the integer coordinate of the first desired base, with "1" representing the first base of the seqence.

#### seq\_stop

Last sequence base to retrieve. The value should be the integer coordinate of the last desired base, with "1" representing the first base of the seqence.

#### complexity

Data content to return. Many sequence records are part of a larger data structure or "blob", and the **complexity** parameter determines how much of that blob to return. For example, an mRNA may be stored together with its protein product. The available values are as follows:

[View in own window](https://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.Tc/?report=objectonly)

<table><thead><tr><th scope="col" rowspan="1" colspan="1">Value of complexity</th><th scope="col" rowspan="1" colspan="1">Data returned for each requested GI</th></tr></thead><tbody><tr><td headers="hd_h_chapter4.Tc_1_1_1_1" scope="row" rowspan="1" colspan="1"><p>0</p></td><td headers="hd_h_chapter4.Tc_1_1_1_2" rowspan="1" colspan="1"><p>entire blob</p></td></tr><tr><td headers="hd_h_chapter4.Tc_1_1_1_1" scope="row" rowspan="1" colspan="1"><p>1</p></td><td headers="hd_h_chapter4.Tc_1_1_1_2" rowspan="1" colspan="1"><p>bioseq</p></td></tr><tr><td headers="hd_h_chapter4.Tc_1_1_1_1" scope="row" rowspan="1" colspan="1"><p>2</p></td><td headers="hd_h_chapter4.Tc_1_1_1_2" rowspan="1" colspan="1"><p>minimal bioseq-set</p></td></tr><tr><td headers="hd_h_chapter4.Tc_1_1_1_1" scope="row" rowspan="1" colspan="1"><p>3</p></td><td headers="hd_h_chapter4.Tc_1_1_1_2" rowspan="1" colspan="1"><p>minimal nuc-prot</p></td></tr><tr><td headers="hd_h_chapter4.Tc_1_1_1_1" scope="row" rowspan="1" colspan="1"><p>4</p></td><td headers="hd_h_chapter4.Tc_1_1_1_2" rowspan="1" colspan="1"><p>minimal pub-set</p></td></tr></tbody></table>

## ELink

### Base URL

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi

### Functions

- Returns UIDs linked to an input set of UIDs in either the same or a different Entrez database
- Returns UIDs linked to other UIDs in the same Entrez database that match an Entrez query
- Checks for the existence of Entrez links for a set of UIDs within the same database
- Lists the available links for a UID
- Lists LinkOut URLs and attributes for a set of UIDs
- Lists hyperlinks to primary LinkOut providers for a set of UIDs
- Creates hyperlinks to the primary LinkOut provider for a single UID

### Required Parameters

#### db

Database from which to retrieve UIDs. The value must be a valid [Entrez database name](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter2/#chapter2.chapter2_table1) (default = pubmed). This is the destination database for the link operation.

#### dbfrom

Database containing the input UIDs. The value must be a valid [Entrez database name](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter2/#chapter2.chapter2_table1) (default = pubmed). This is the origin database of the link operation. If **db** and **dbfrom** are set to the same database value, then ELink will return computational neighbors within that database. Please see the [full list of Entrez links](https://eutils.ncbi.nlm.nih.gov/entrez/query/static/entrezlinks.html) for available computational neighbors. Computational neighbors have linknames that begin with *dbname\_dbname* (examples: protein\_protein, pcassay\_pcassay\_activityneighbor).

#### cmd

ELink command mode. The command mode specified which function ELink will perform. Some optional parameters only function for certain values of &cmd (see below).

**cmd=neighbor (default)**

ELink returns a set of UIDs in **db** linked to the input UIDs in **dbfrom.**

*Example: Link from protein to gene*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&db=gene&id=15718680,157427902](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&db=gene&id=15718680,157427902)

**cmd=neighbor\_score**

ELink returns a set of UIDs within the same database as the input UIDs along with computed similarity scores**.**

*Example: Find related articles to PMID 20210808*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&id=20210808&cmd=neighbor\_score](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&id=20210808&cmd=neighbor_score)

**cmd=neighbor\_history**

ELink posts the output UIDs to the Entrez History server and returns a **query\_key** and **WebEnv** corresponding to the location of the output set.

*Example: Link from protein to gene and post the results on the Entrez History*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&db=gene&id=15718680,157427902&cmd=neighbor\_history](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&db=gene&id=15718680,157427902&cmd=neighbor_history)

**cmd=acheck**

ELink lists all links available for a set of UIDs.

*Example: List all possible links from two protein GIs*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&id=15718680,157427902&cmd=acheck](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&id=15718680,157427902&cmd=acheck)

*Example: List all possible links from two protein GIs to PubMed*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&db=pubmed&id=15718680,157427902&cmd=acheck](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&db=pubmed&id=15718680,157427902&cmd=acheck)

**cmd=ncheck**

ELink checks for the existence of links *within the same database* for a set of UIDs. These links are equivalent to setting **db** and **dbfrom** to the same value.

*Example: Check whether two nuccore sequences have "related sequences" links.*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=nuccore&id=21614549,219152114&cmd=ncheck](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=nuccore&id=21614549,219152114&cmd=ncheck)

**cmd=lcheck**

Elink checks for the existence of external links (LinkOuts) for a set of UIDs.

*Example: Check whether two protein sequences have any LinkOut providers.*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&id=15718680,157427902&cmd=lcheck](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&id=15718680,157427902&cmd=lcheck)

**cmd=llinks**

For each input UID, ELink lists the URLs and attributes for the LinkOut providers that are not libraries.

*Example: List the LinkOut URLs for non-library providers for two pubmed abstracts.*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=19880848,19822630&cmd=llinks](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=19880848,19822630&cmd=llinks)

**cmd=llinkslib**

For each input UID, ELink lists the URLs and attributes for *all* LinkOut providers including libraries.

*Example: List all LinkOut URLs for two PubMed abstracts.*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=19880848,19822630&cmd=llinkslib](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=19880848,19822630&cmd=llinkslib)

**cmd=prlinks**

ELink lists the primary LinkOut provider for each input UID, or links directly to the LinkOut provider's web site for a single UID if **retmode** is set to *ref*.

*Example: Find links to full text providers for two PubMed abstracts.*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=19880848,19822630&cmd=prlinks](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=19880848,19822630&cmd=prlinks)

*Example: Link directly to the full text for a PubMed abstract at the provider's web site.*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=19880848&cmd=prlinks&retmode=ref](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=19880848&cmd=prlinks&retmode=ref)

### Required Parameter – Used only when input is from a UID list

### Required Parameters – Used only when input is from the Entrez History server

#### query\_key

Query key. This integer specifies which of the UID lists attached to the given Web Environment will be used as input to ELink. Query keys are obtained from the output of previous ESearch, EPost or ELInk calls. The **query\_key** parameter must be used in conjunction with **WebEnv**.

#### WebEnv

Web Environment. This parameter specifies the Web Environment that contains the UID list to be provided as input to ELink. Usually this WebEnv value is obtained from the output of a previous ESearch, EPost or ELink call. The **WebEnv** parameter must be used in conjunction with **query\_key**.

```
Link from protein to gene:
elink.fcgi?dbfrom=protein&db=gene&query_key=<key>&WebEnv=<webenv string>Find related sequences (link from protein to protein):
elink.fcgi?dbfrom=protein&db=protein&query_key=<key>&WebEnv=
<webenv string>
```

### Optional Parameter – Retrieval

#### retmode

Retrieval type. Determines the format of the returned output. The default value is ‘xml’ for ELink XML, but ‘json’ is also supported to return output in JSON format.

#### idtype

Specifies the type of identifier to return for sequence databases (nuccore, popset, protein). By default, ELink returns GI numbers in its output. If **idtype** is set to ‘acc’, ELink will return accession.version identifiers rather than GI numbers.

### Optional Parameters – Limiting the Output Set of Links

### Optional Parameters – Dates

These parameters only function when **cmd** is set to *neighbor* or *neighbor\_history* and **dbfrom** is *pubmed*.

#### datetype

Type of date used to limit a link operation. The allowed values vary between Entrez databases, but common values are 'mdat' (modification date), 'pdat' (publication date) and 'edat' (Entrez date). Generally an Entrez database will have only two allowed values for **datetype**.

#### reldate

When **reldate** is set to an integer *n*, ELink returns only those items that have a date specified by **datetype** within the last *n* days.

#### mindate, maxdate

Date range used to limit a link operation by the date specified by **datetype**. These two parameters (**mindate, maxdate**) must be used together to specify an arbitrary date range. The general date format is YYYY/MM/DD, and these variants are also allowed: YYYY, YYYY/MM.

## EGQuery

### Base URL

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi

### Function

Provides the number of records retrieved in all Entrez databases by a single text query.

### Required Parameter

## ESpell

### Base URL

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi

### Function

Provides spelling suggestions for terms within a single text query in a given database.

### Required Parameters

## ECitMatch

### Base URL

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ecitmatch.cgi

### Function

Retrieves PubMed IDs (PMIDs) that correspond to a set of input citation strings.

### Required Parameters

#### db

Database to search. The only supported value is ‘pubmed’.

#### rettype

Retrieval type. The only supported value is ‘xml’.

## Release Notes

### EFetch; ELink JSON ouput: June 24, 2015

- EFetch now supports ClinVar and GTR
- ELink now provides output in JSON format

### ESearch &sort; JSON output format: February 14, 2014

- ESearch now provides a supported **sort** parameter
- EInfo, ESearch and ESummary now provide output data in JSON format

### ECitMatch, EInfo Version 2.0, EFetch: August 9, 2013

- EInfo has an updated XML output that includes two new fields: <IsTruncatable> and <IsRangeable>
- EFetch now supports the BioProject database.

### EFetch Version 2.0. Target release date: February 15, 2012

- EFetch now supports the following databases: biosample, biosystems and sra
- EFetch now has defined default values for &retmode and &rettype for all supported databases (please see [Table 1](https://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.T._valid_values_of__retmode_and/?report=objectonly) for all supported values of these parameters)
- EFetch no longer supports &retmode=html; requests containing &retmode=html will return data using the default &retmode value for the specified database (&db)
- EFetch requests including &rettype=docsum return XML data equivalent to ESummary output

### Release of new Genome database: November 9, 2011

- Entrez Genome has been completely redesigned, and database records now correspond to a species rather than an individual chromosome sequence. Please see full details of the change at [https://www.ncbi.nlm.nih.gov/About/news/17Nov2011.html](https://www.ncbi.nlm.nih.gov/About/news/17Nov2011.html)

- EFetch no longer supports retrievals from Genome (db=genome).
- The ESummary XML for Genome has been recast to reflect the new data model.

### ESummary Version 2.0. November 4, 2011

- ESummary now supports a new, alternative XML presentation for Entrez document summaries (DocSums). The new XML is unique to each Entrez database and generally contains more extensive data about the record than the original DocSum XML.
- There are no plans at present to discontinue the original DocSum XML, so developers can continue to use this presentation, which will remain the default.
- Version 2.0 XML is returned when &version=2.0 is included in the ESummary URL.

## Demonstration Programs

Please see [Chapter 1](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter1/#chapter1.Demonstration_Programs) for sample Perl scripts.

## For More Information

Please see [Chapter 1](https://www.ncbi.nlm.nih.gov/books/n/helpeutils/chapter1/#chapter1.For_More_Information_8) for getting additional information about the E-utilities.