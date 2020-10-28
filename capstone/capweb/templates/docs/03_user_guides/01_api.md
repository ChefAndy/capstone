{% load static %}
{% load pipeline %}
{% load api_url %}
title: API User Guide
page_image: img/og_image/docs.png
meta_description: Caselaw Access Project API Docs
explainer: The Caselaw Access Project API, also known as CAPAPI, serves all official US court cases published in books from 1658 to 2018. The collection includes over six million cases scanned from the Harvard Law School Library shelves. <a href="{% url "about" }>Learn more about the project</a>.


{# ==============> GETTING STARTED <============== #}
# Getting Started {: class="subtitle" data-toc-label='Getting Started' }

If you're an RESTful API Pro, you may just need our API reference
[API Reference]({% url 'docs' 'specs_and_reference/api_reference' %}).

If you're an absolute beginner and haven't used APIs before, but want to get up to speed, check out our 
[Beginner's Introduction to APIs]({% url 'docs' 'tutorials/intro_to_APIs' %}).

If you need a more detailed, step-by-step walkthrough of our API, check out our 
[CAP API Tutorial]({% url 'docs' 'tutorials/api' %}).

## Making Basic Queries

This is a restful API, and it's primary return format is in JSON. For details on the data returned by the API, head over
to our [API Reference]({% url 'docs' 'specs_and_reference/api_reference' %})

CAPAPI includes an in-browser API viewer, but is primarily intended for software developers to access caselaw 
programmatically, whether to run your own analysis or build tools for other users. API results are in JSON format with 
case text available as structured XML, presentation HTML, or plain text. If you just want to read cases, we do have
a [Search Tool]({% url 'search'%}).

To get started with the API, you can [explore it in your browser]({% api_url "api-root" %}), or reach it from the 
command line. For example, here is a curl command to request 
[a single case from Illinois]({% api_url "cases-list" %}?jurisdiction=ill&page_size=1):

    curl "{% api_url "cases-list" %}?jurisdiction=ill&page_size=1"

## Filtering
To filter your queries, just add more parameters. For example, if we wanted to request 
[a single case from illinois decided before 1850]({% api_url "cases-list" %}?jurisdiction=ill&page_size=1&decision_date__gte=1832):

    curl "{% api_url "cases-list" %}?jurisdiction=ill&page_size=1&decision_date__gte=1832"
    
Now let's search for all cases in the jurisdiction of Rhode Island that contain the word "spork":

    curl "{% api_url "cases-list" %}?search=spork&jurisdiction=ri"


{# ====> Searching and Filtering <==== #}
## Searching and Filtering Cases {: class="subtitle" data-toc-label='Search' }

Our [cases endpoint](#endpoint-cases) is indexed by Elasticsearch, and supports a range of searching, filtering, and
sorting options.

Options in this section work only with the cases endpoint.
{: class="highlighted" }

### Full-text Search
{: #case-fts class="topic-header" }

Full-text search uses the `search` parameter. For example, if you'd
like to search for all cases that contain the word 'baronetcy', use the following query:

    {% api_url "cases-list" %}?search=baronetcy

The `search` field supports Elasticsearch [Simple Query String Syntax](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/query-dsl-simple-query-string-query.html#_simple_query_string_syntax)
For example, you can use `"quotes"` to search by phrase and `-negation` to exclude cases with matching terms.

The `search` parameter searches the case, jurisdiction, and court names, docket number, and case text.
You can also use the `name`, `name_abbreviation`, or `docket_number` parameters to perform full-text search
just on those fields.



### Filtering by Groups or Ranges
{: #case-filtering class="topic-header" }

Many of the parameters on the cases endpoint can be filtered by appending a suffix to the query parameter key.

To match to a list, append `__in` to the query parameter. For example, to fetch cases matching ID `12`, `34`, or `56`:

    curl "{% api_url "cases-list" %}?id__in=12__34__56"

To filter by less than or greater than, append `__gt` (greater than), `__gte` (greater than or equal to), 
`__lt` (less than), or `__lte` (less than or equal to). For example, to fetch cases of 2,000 to 3,000 words:

    curl "{% api_url "cases-list" %}?analysis.word_count__gte=2000&analysis.word_count__lte=3000"

To filter by prefix, append `__prefix`. For example, to find cases from February of 1800:

    curl "{% api_url "cases-list" %}?decision_date__prefix=1800-02"
    
## Sorting
{: class="topic-header" }
  
You can sort your search in the cases endpoint using the `ordering` argument. To order your results in ascending order, 
supply the ordering argument with the field on which you'd like to sort your results. For example, if you'd like to 
search for the term 'baronetcy' with the oldest cases appearing first, supply the following query: 

    {% api_url "cases-list" %}?search=baronetcy&ordering=decision_date

You can also sort in descending order by adding a minus sign before the field on which you'd like to sort. To perform 
the same search sorted in descending order, that is, seeing the newest cases first, then use this query:

    {% api_url "cases-list" %}?search=baronetcy&ordering=-decision_date
    

## Types of Data You Can Query

We make data available through several API Endpoints, the most popular being our cases endpoint. It's the only endpoint
through which we distribute full case text, and the only endpoint for which you may need authentication. We also serve 
up citations, ngrams, court metadata, reporter series metadata, volume metadata, and jurisdiction metadata. They all
work about the same way, and are all based off of the same data set. That means that an ID in the reporters endpoint 
will correspond to a reporter object's ID listed in a case. 

Check out our [API Reference]({% url 'docs' 'specs_and_references/api_reference' %}) for a complete list of specs and arguments.

# Getting Full Case Text

You can request the get full case text for cases anywhere in the cases endpoint, whether you're viewing an individual
case, or a query with many cases. to do so, you must include the `full_case=true` argument in your query url, like so:

[{% api_url "cases-list" %}jurisdiction=ill&page_size=1&full_case=true]({% api_url "cases-list" %}jurisdiction=ill&page_size=1&full_case=true)

Without that option, you'll just get the case metadata:

[{% api_url "cases-list" %}jurisdiction=wash&page_size=1]({% api_url "cases-list" %}jurisdiction=wash&page_size=1)

For most cases, you'll need to be authenticate using an API key to get the case test. There are several jurisdictions
for which we do not require authenticating, which we call 
[whitelisted]({% url 'docs' 'user_guides/documentation_glossary' %}#def-whitelisted) jurisdictions. To see 
a complete list of whitelisted jurisdictions, check out our 
[access limits documentation]({% url 'docs' 'specs_and_references/access_limits' %}).

For non-whitelisted jurisdictions, if you try to get case text without authenticating, you'll run into this:

[{% api_url "cases-list" %}jurisdiction=wash&page_size=1&full_case=true]({% api_url "cases-list" %}jurisdiction=wash&page_size=1&full_case=true)

          "casebody": {
            "data": null,
            "status": "error_auth_required"
          }

{# ==============> AUTHENTICATION <============== #}
# Authentication {: class="subtitle" }

Once you've read the [access limits documentation]({% url 'docs' 'specs_and_references/access_limits' %}) to confirm
you need to authenticate, and [registered your account]({% url "docs" "user_guides/registration"%}), you're ready to 
authenticate your requests.

## Find your API Key {: class="subtitle" }

First, log in to your account using the [LOG IN]({% url "login" %}) link at the top of the screen. After you've signed 
in, the [LOG IN]({% url "login" %}) link at the top of the screen now reads [ACCOUNT]({% url "user-details" %}). Click 
that link. In the API key field, you should see a 40 
[character]({% url 'docs' 'user_guides/documentation_glossary' %}#def-character) long 
[string]({% url 'docs' 'user_guides/documentation_glossary' %}#def-string). That is your API key.

## Modify Your Headers {: class="subtitle" }
You must submit the API key in the request headers. The headers are a group of metadata fields automatically included in the background of each request. Your browser (or equivalent like `curl`, or a requests library) uses headers to describe each request to the server, and the server to describe its response. For example, your web browser will include a header field called `User-Agent`, which tells the web server what version of what browser you're using, on what operating system. Among the various headers in its response, the server will include a `Content-Type` field, which says if it's HTML text, an image, etc.
Our service requires you to include the header labeled `Authorization`, containing the string `Token [your API key]`. So, if your API key were `1234thisisntarealapikeysodontusethisone1`, your header would look like this: `Authorization: Token 1234thisisntarealapikeysodontusethisone1`. 

In practice, that looks like this:
### curl {: class="subtitle" }
	curl -H "Authorization: Token 1234thisisntarealapikeysodontusethisone1" "https://api.case.law/v1/cases/435800/?full_case=true"

### python requests library {: class="subtitle" }
	response = requests.get(
    'https://api.case.law/v1/cases/435800/?full_case=true',
    headers={'Authorization': 'Token 1234thisisntarealapikeysodontusethisone1'})

### Other Environments {: class="subtitle" }

Other environments work much the same way— consult your documentation to see how to modify the headers of your request. 
As long as a header labelled `Authorization` has a value of `Token [your API key]`, that should do the trick. 

## Doesn't work?

There are a few common errors that trip up API users.

### error_auth_required

If you request full case text from from non-whitelisted jurisdictions without authenticating, this is what you'll see
in the casebody section of each case:

      "casebody": {
        "data": null,
        "status": "error_auth_required"
      }
      
In this example the response included a case from a non-whitelisted jurisdiction, and `casebody.data` for the case is 
therefore blank, while `casebody.status` is "error_auth_required". To resolve this, simply include a valid API key in
your request.

### error_limit_exceeded

You've likely exceeded your limit of 500 per day limit of non-whitelisted case texts. See the 
[access limits documentation]({% url 'docs' 'specs_and_references/access_limits' %}) for more info.


{# ==============> DATA FORMATS <============== #}
# Case Text Formats {: class="subtitle" data-toc-label='Data Formats' }

All non-browser API responses are in JSON format.

    {
        "count": (integer),
        "next": (url),
        "previous": (url),
        "results": [list of objects]
    }

Each endpoint has its own object format. For a complete breakdown, check out 
[data specs]({% url 'docs' 'specs_and_references/data_specs' %})

This is what a case object looks like:

    {
        "id": (int),
        "url": (API url to this case),
        "name": (string),
        "name_abbreviation": (string),
        "decision_date": (string),
        "docket_number": (string),
        "first_page": (string),
        "last_page": (string),
        "citations": [array of citation objects],
        "volume": {Volume Object},
        "reporter": {Reporter Object},
        "court": {Court Object},
        "jurisdiction": {Jurisdiction Object},
        "cites_to": [array of cases this case cites to],
        "frontend_url": (url of case on our website),
        "frontend_pdf_url": (url of case pdf),
        "preview": [array of snippets that contain search term],
        "analysis": {
            "cardinality": (int),
            "char_count": (int),
            "ocr_confidence": (float),
            "sha256": (str),
            "simhash": (str),
            "word_count": (int)
        },
        "last_updated": (datetime),
        "casebody": {
            "status": ok/(error)"
            "data": (null if status is not ok) {
                "judges": [array of strings that contain judges names],
                "parties": [array of strings containing party names],
                "opinions": [
                    {
                        "text": (case text),
                        "type": (string),
                        "author": (string)
                    }
                ],
                "attorneys": [array of strings that contain attorneys names],
                "corrections": (string. May include formatting notes.),
                "head_matter": (elements before the case text)
            }
        }
    }


By default, when you include `full_case=true` in your request url, the cases endpoint returns structured plain text. 
Structured text is most useful for natural language processing. By changing the `body_format` query parameter, it can 
also return the casebody in XML (`body_format=xml`), or HTML (`body_format=html`). 


## Structured Casebody Text

[{% api_url "cases-list" %}?jurisdiction=ill&full_case=true]({% api_url "cases-list" %}?jurisdiction=ill&full_case=true)
{: class="example-link mt-0" }

Example response data:

    "data": {
          "head_matter": "Fifth District\n(No. 70-17;\nThe People of the State of Illinois ...",
          "opinions": [
              {
                  "author": "Mr. PRESIDING JUSTICE EBERSPACHER",
                  "text": "Mr. PRESIDING JUSTICE EBERSPACHER\ndelivered the opinion of the court: ...",
                  "type": "majority"
              }
          ],
          "judges": [],
          "attorneys": [
              "John D. Shulleriberger, Morton Zwick, ...",
              "Robert H. Rice, State’s Attorney, of Belleville, for the Peop ..."
          ]
      }
    }

In this example, `"head_matter"` is a string representing all text printed in the volume before the text prepared by 
judges. `"opinions"` is an array containing a dictionary for each opinion in the case. `"judges"`, and 
`"attorneys"` are particular substrings from `"head_matter"` that we believe to refer to entities involved with the 
case.


{# ====> Analysis Fields <==== #}
# Analysis Fields

Check out the writeup in the [API Reference]({% url 'docs' 'specs_and_reference/api_reference' %}) for more info
on the analysis fields.

# Other Endpoints

The other endpoints function in a very similar way to the case endpoint, though the parameters and return values are 
obvioulsy different. Check out our [API Reference]({% url 'docs' 'specs_and_reference/api_reference' %}) for a complete 
list of endpoints and values. Check out our [data specs]({% url 'docs' 'specs_and_references/data_specs' %}) for a 
complete rundown of data formats.