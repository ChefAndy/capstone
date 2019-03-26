from lxml import etree
import re

from .helpers import left_strip_text

tag_map = {"author": "p", "opinion": "article", "casebody": "section",
           "citation": "p", "correction": "aside", "court": "p",
           "decisiondate": "p", "disposition": "p", "docketnumber": "p",
           "headnotes": "p", "history": "p", "otherdate": "p",
           "parties": "h4", "seealso": "aside", "summary": "p",
           "syllabus": "p", "footnote": "aside", "attorneys": "p",
           "judges": "p", "bracketnum": "a", "footnotemark": "a",
           "page-number": "a"}

# these will pull out the headnotes number and corresponding bracketnum
bracketnum_number = re.compile(r'\d')
headnotes_number = re.compile(r'^(\d+).*')


def generate_html(casebody, tag_map=tag_map, abbreviated=False):
    """
        Converts case xml to html. casebody should be a pyquery element extracted from case XML.
    """
    casebody_tree = casebody[0]

    # all elements before the first opinion go into a <section class="head-matter"> container
    first_opinion = casebody("casebody|opinion").eq(0)
    head_matter_els = first_opinion.prev_all()
    head_matter_el = etree.Element("section", {"class": "head-matter"})
    casebody(head_matter_el).append(head_matter_els)
    casebody.prepend(head_matter_el)

    # traverse the casebody tree and convert elements
    for element in casebody_tree.iter():

        # skip any anchor tags we generated
        if 'class' in element.attrib:
            if element.attrib['class'] == 'footnote_anchor' or element.attrib['class'] == 'headnote_anchor':
                continue

        # skip new section tag
        if element.tag == "section":
            continue

        # remove the namespace from the tag name
        tag = element.tag.split('}')[-1]

        if abbreviated:
            if tag == "parties" or tag == "decisiondate" or tag == "docketnumber":
                element.getparent().remove(element)
                continue

        element_text_copy = element.text

        if element_text_copy is None and tag != 'page-number':
            element_text_copy = element.getchildren()[0].text

        # for every attribute except id, turn it into an accepted data-* attribute
        # use list(element.attrib) so we can safely mutate dictionary during iteration
        for attribute in list(element.attrib):
            if attribute == 'id' \
                or attribute == 'href' \
                or attribute.startswith('data-'):
                continue
            element.attrib['data-' + attribute] = element.attrib[attribute]
            element.attrib.pop(attribute)

        # rename the tag based on the tag map, and set the class to the original tag name
        # e.g. <author> becomes <p class="author">
        if tag in tag_map:
            element.attrib['class'] = tag
            element.tag = tag_map[tag]

        # create internal links
        if tag == "footnote":
            label = element.attrib.get('data-label')
            if label:
                # strip footnote label from start of footnote text
                left_strip_text(element[0], label)

                # element id allows the footnotemark to link to the footnote
                element.attrib["id"] = "footnote_" + label

                # add link to show footnote label and jump back up to text
                anchor = etree.Element("a", href="#ref_" + label)
                anchor.text = label
                element.insert(0, anchor)
        elif tag == "headnotes":
            # this anchor allows the bracketnum to link to the proper headnote, if it exists
            number_match = headnotes_number.match(element_text_copy)
            if number_match:
                number = number_match.groups(1)[0]
                anchor = etree.Element("a")
                anchor.attrib["id"] = "headnote_" + number
                anchor.attrib['class'] = "headnote_anchor"
                anchor.text = " "
                element.append(anchor)
        elif tag == "footnotemark":
            # point to the anchor in the footnote
            element.tag = "a"
            element.attrib['href'] = "#footnote_" + element_text_copy
            element.attrib['id'] = "ref_" + element_text_copy
        elif tag == "bracketnum":
            # point to the anchor in the headnote.
            # Hack-> If it can't find the headnote, maybe because it's an imporperly tagged bracketnum,
            # just make it a span
            if bracketnum_number.search(element_text_copy):
                element.tag = "a"
                element.attrib['href'] = "#headnote_" + bracketnum_number.search(element_text_copy).group(0)
            else:
                element.tag = "span"

        elif tag == "page-number":
            # point to the anchor in the headnote
            element.attrib['style'] = "page-break-before: always"

    # get casebody as string with namespaces stripped
    casebody_str = re.sub(r' xmlns(:xlink)?="http://[^"]+"', '', str(casebody))

    return casebody_str
