import pytest
import json
from scripts import update_snippets
from capdb.models import Snippet

@pytest.mark.django_db
def test_map_numbers(ingest_case_xml):
    update_snippets.update_map_numbers()
    snippet = Snippet.objects.get(label="map_numbers")
    parsed = json.loads(snippet.contents)
    assert len(parsed) == 2
    assert 'US-WA' in parsed
    assert parsed['US-IL']['case_count'] == 2
    assert parsed['US-IL']['volume_count'] == 2
    assert parsed['US-IL']['page_count'] == 8

@pytest.mark.django_db
def test_cases_by_decision_date(ingest_case_xml):
    update_snippets.cases_by_decision_date_tsv()
    cases_by_decision_date = Snippet.objects.get(label='cases_by_decision_date')
    assert '1819-12-01' in cases_by_decision_date.contents
    assert '2017-07-11' in cases_by_decision_date.contents

@pytest.mark.django_db
def test_cases_by_jurisdiction(ingest_case_xml):
    update_snippets.cases_by_jurisdiction_tsv()
    cases_by_jurisdiction = Snippet.objects.get(label='cases_by_jurisdiction')
    rows = cases_by_jurisdiction.contents.split("\r\n")[:-1]
    assert len(rows) == 2
    assert 'Washington' in cases_by_jurisdiction.contents
    assert rows[0].split("\t")[1] == '"Illinois"'
    assert rows[0].split("\t")[2] == '2'

@pytest.mark.django_db
def test_cases_by_reporter(ingest_case_xml):
    update_snippets.cases_by_reporter_tsv()
    cases_by_reporter = Snippet.objects.get(label='cases_by_reporter')
    rows = cases_by_reporter.contents.split("\r\n")[:-1]
    assert len(rows) == 3
    assert 'Washington' in cases_by_reporter.contents
    assert rows[0].split("\t")[2] == '1'
    assert rows[0].split("\t")[1] == '"Illinois Appellate Court Reports"'

@pytest.mark.django_db
def test_search_jurisdiction_list(ingest_case_xml):
    update_snippets.search_jurisdiction_list()
    jurisdictions = Snippet.objects.get(label='search_jurisdiction_list')
    parsed = json.loads(jurisdictions.contents)
    assert parsed['wash'] == 'Washington'
    assert parsed['ill'] == 'Illinois'

@pytest.mark.django_db
def test_search_court_list(ingest_case_xml):
    update_snippets.search_court_list()
    courts = Snippet.objects.get(label='search_court_list')
    parsed = json.loads(courts.contents)
    assert parsed['wash-ct-app'] == 'Washington: Washington Court of Appeals'
    assert parsed['ill-app-ct'] == 'Illinois: Illinois Appellate Court'
    assert parsed['ill'] == 'Illinois: Illinois Supreme Court'

@pytest.mark.django_db
def test_search_reporter_list(ingest_case_xml):
    update_snippets.search_reporter_list()
    reporters = Snippet.objects.get(label='search_reporter_list')
    parsed = json.loads(reporters.contents)
    assert parsed['477'] == 'Wash. App.- Washington Appellate Reports'
    assert parsed['1058'] == 'Ill. (Breese)- Illinois Reports'
    assert parsed['892'] == 'N.W. 2d- North Western Reporter 2d'
    assert parsed['315'] == 'Ill. App.- Illinois Appellate Court Reports'
