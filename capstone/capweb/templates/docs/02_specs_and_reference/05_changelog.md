{% load static %}
{% load pipeline %}
{% load api_url %}
title: Changelog
page_image: img/og_image/docs.png
meta_description: CAP Data/Feature Change Log
explainer: If our data or user-facing research features change in significant ways&mdash;beyond bug fixes and minor changes&mdash;we'll record those changes here.
top_section_style: bg-black
row_style: bg-tan

# August 28 2020 {: class="changelog-head"  }

**API:**
{: class="changelog-subhead"  }

* Cases Endpoint:
    * Allow `ordering` by analysis fields.

# August 2020 {: class="changelog-head"  }

**API:**
{: class="changelog-subhead"  }

* Cases Endpoint:
{: add_list_class="changelog-list" }
    * Added `last_updated` field and filters to get cases changed since date.
    * Added `analysis` field and filters to list extracted facts about case, such as word count.
    * Added `frontend_pdf_url` field.
    * Added `?format=pdf` query parameter for single-case endpoint.
* Volumes Endpoint:
    * Added `frontend_url` field.
* Reporters Endpoint:
    * Added `frontend_url` field.
    
**Website:**
{: class="changelog-subhead"  }

* Non-API URLs such as Downloads now accept `Authorization: Token` header. 
{: add_list_class="changelog-list" }
    
# June 2020 {: class="changelog-head"  }

**Website:**
{: class="changelog-subhead"  }

* Moved bulk data releases from an API endpoint to the /download/ section.
{: add_list_class="changelog-list" }

**Data:**
{: class="changelog-subhead"  }

* Removed a number of duplicate volumes (see bug [#1322](https://github.com/harvard-lil/capstone/issues/1322)).
{: add_list_class="changelog-list" }
* Corrected a number of citations containing strange characters (see bug [#960](https://github.com/harvard-lil/capstone/issues/960)).
* 20200604 bulk data release including citation fixed, duplicate volume fixes, and cites_to field. 

# April 2020 {: class="changelog-head"  }

**Website:**
{: class="changelog-subhead"  }

* Linked citations in cases to cited case.
{: add_list_class="changelog-list" }

**API:**
{: class="changelog-subhead"  }

* Cases Endpoint:
{: add_list_class="changelog-list" }
    * Added `cites_to` field to list cases cited.
    * Added `cites_to` filter to find cases citing to a case.

**Data:**
{: class="changelog-subhead"  }

* Added `/download/citation_graph/` folder.
{: add_list_class="changelog-list" }

# March 2020 {: class="changelog-head"  }

**API:**
{: class="changelog-subhead"  }

* Cases Endpoint:
{: add_list_class="changelog-list" }
    * Raise max results per request to 10,000.

**Data:**
{: class="changelog-subhead"  }

* Merged duplicate New York reporters (see bug [#1420](https://github.com/harvard-lil/capstone/issues/1420)).
{: add_list_class="changelog-list" }

# February 2020 {: class="changelog-head"  }

**Website:**
{: class="changelog-subhead"  }

* Added /download/ section to download files.
{: add_list_class="changelog-list" }
* Added opt-in ability for user to track their previously-viewed cases.
* Cases now link to per-case PDFs.

**Data:**
{: class="changelog-subhead"  }

* Added to Downloads section:
{: add_list_class="changelog-list" }
    * `scdb/` folder with SCDB to CAP matchups.
    * `PDFs/` folder with full volume scans.
    * `illustrations/` folder with extracted figures and illustrations from cases. 

**API:**
{: class="changelog-subhead"  }

* Cases Endpoint:
{: add_list_class="changelog-list" }
    * Removed the `format=html` and `format=xml` parameters, which previously caused the case detail endpoint to return
      either HTML or XML instead of JSON. API will always return JSON, with case body format still
      controllable via `body_format`. Requests for `format=html` will redirect to the frontend case browser, which
      shows identical contents to what `format=html` used to return.
* Volumes Endpoint:
    * Added pdf_url field to volumes endpoint.
* User History Endpoint:
    * Added opt-in ability for user to retrieve their previously-viewed cases via API.

# January 24, 2020 {: class="changelog-head"  }

**API:**
{: class="changelog-subhead"  }

* Cases Endpoint
{: add_list_class="changelog-list" }
    * Default sort for full-text search is now relevance, rather than decision date.
* Search
    * Default sort for full-text search is now relevance, rather than decision date.
    * Added Sorting field to case endpoint searches. You can now sort by decision date, and relevance.

# January 19, 2020 {: class="changelog-head"  }

**Security:**
{: class="changelog-subhead"  }

* Added a dmarc record for the case.law domain. Thanks to Kashif Shoukat for the suggestion!

# January 16, 2020 {: class="changelog-head"  }

**Data:**
{: class="changelog-subhead"  }

* 99% of US Supreme Court cases have been matched to [SCDB](http://scdb.wustl.edu/), and now have SCDB citations like 
  "SCDB 1970-131" as well as parallel citations drawn from SCDB. Add a new "vendor" category of citations, used for
  citations to other vendors' databases.
{: add_list_class="changelog-list" }
* Include `<img>` tags in case XML output, identical to existing `<img>` tags in HTML output.

**Website:**
{: class="changelog-subhead"  }

* Case HTML pages now include a link to the case in the API.
{: add_list_class="changelog-list" }

# January 9, 2020 {: class="changelog-head"  }

**API**
{: class="changelog-subhead"  }

* Cases Endpoint
{: add_list_class="changelog-list" }
    * Reverted to using a `decision_date` format that reflects the granularity of the original data. In the original 
    data, some of the decision dates specify only a year and month, but not a day. To make these findable in a 
    standardized date index, we set those to the first of the month. When we switched over to elasticsearch, we served
    the full date with the possibly inaccurate first-of-the-month date field in `decision_date.` We've reverted to using
    the original date without the day.
    * New `preview` field. If you use the full-text search feature, you'll now get an array of matches in-context. The
    actual word or phrase match is surrounded in html emphasis tags. For example, if you performed a full-text 
    search for the word `judge`, the preview field in one of your hits would look like this:
    
    
    [ "DEWEY, District <em class='search_highlight'>Judge</em>.", 
    "<em class='search_highlight'>Judge</em> Reeves of Kansas City, Mo., in 1938, in a bankruptcy proceeding entitled “In the Matter of Irving"
    ]
{: class="code-block" }

**Website:**
{: class="changelog-subhead"  }

* Search Documentation
{: add_list_class="changelog-list" }
    * Added search section documenting new features in our Elasticsearch-backed cases endpoint:
        * Phrase Searching
        * Search Exclusion

# December 6, 2019 {: class="changelog-head"  }

**Website:**
{: class="changelog-subhead"  }

* API Documentation
{: add_list_class="changelog-list" }
    * Added search section documenting new features in our Elasticsearch-backed cases endpoint:
        * Phrase Searching
        * Search Exclusion
        * Sorting

# October 1, 2019 {: class="changelog-head"  }

**API:**
{: class="changelog-subhead"  }

* Elasticsearch
{: add_list_class="changelog-list" }
	* We've switched the back end of the cases endpoint to Elasticsearch. We tried to maintain the same API interface and output that older Postgres back end had, but please let us know if anything is broken. 
	This update will:
		* increase performance
		* pave the way for lots of new features and functionality
		* increase the length of cursor strings
		* invalidate old Postgres cursor strings
* New IDs
	* We've started including some new IDs in our API's case output. Volumes now include a unique 'barcode' value which (usually) corresponds to the barcode in our library's cataloging system. Reporter entries now include the reporter ID. These values were previously only available as part of the URL value. Thanks to [Mike Lissner](https://michaeljaylissner.com/) for pointing this one out.
		
**Data:**
{: class="changelog-subhead"  }

* Nominative Reporters
{: add_list_class="changelog-list" }
	* We've cleaned up the nominative entries in our reporters table! This affects not only the reporters table but also corrects citations and volume metadata. 


**Website:**
{: class="changelog-subhead"  }

* New Gallery Entries
{: add_list_class="changelog-list" }
    * We've been adding some new entries to our [Gallery Page]({% url "contact" %}) so head on over and check 'em out.

# July 31, 2019 {: class="changelog-head"  }

**Website:**
{: class="changelog-subhead"  }

* Improved case display at cite.case.law:
{: add_list_class="changelog-list" }
    * Cases include images for non-textual regions (figures and illustrations)
        ([example](https://cite.case.law/f2d/537/531/))
    * Case text includes italics, where detected by OCR
    * Case text includes pin cites, i.e. page breaks that can be linked to 
        ([example](https://cite.case.law/f2d/537/531/#p533))
        
**API:**
{: class="changelog-subhead"  }

* Removed from `/cases/` endpoint:
{: add_list_class="changelog-list" }
    * In full case responses with JSON format, `["casebody"]["data"]["parties"]` is no longer included.
      The `["name"]` attribute provides the same information in a cleaner format.
    * Queries for CaseXML documents (`/cases/<id>/?full_case=true&format=xml`) will return only `<casebody>`, 
      and not the entire CaseXML file. The outer wrapper had no useful information other than to estimate the 
      location of page breaks, which are now precisely marked by `<page-number>` elements.
          
**Data format:**
{: class="changelog-subhead"  }

* Added to case HTML and XML:
{: add_list_class="changelog-list" }
    * `<img>` tags to show images for non-textual regions (figures and illustrations)
    * `<em>` tags to show italics detected by OCR
    * `<page-number>` (in xml) or `<a class="page-number">` (in html) tags to mark page breaks
* Removed from case XML:
{: add_list_class="changelog-list" }
    * The `pgmap` attribute was removed. It was confusing, because it referred to the page-side index in the 
        physical volume rather than to the printed page label, and it did not allow for precise placement of
        page breaks within a paragraph. The replacement is to use `<page-number>` elements to infer the correct
        page number for each element.
          
# June 19, 2019 {: class="changelog-head"  }

**Website:**
{: class="changelog-subhead"  }

* Started recording this public changelog.
{: add_list_class="changelog-list" }
* Added the [historic trends]({% url 'trends' %}) tool.

**API:**
{: class="changelog-subhead"  }

* Added the [ngrams]({% api_url "ngrams-list" %}) endpoint. Here are the [docs]({% url 'api' %}#endpoint-ngrams).
{: add_list_class="changelog-list" }
