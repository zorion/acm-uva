# -*- coding: utf-8 -*-
"""This package contains these methods:

        jsonml_xml.to_XML(jsonml_list)
            Converts JsonML-list to XML nodes.

        jsonml_xml.to_XML_text(jsonml_list)
            Converts JsonML-list to XML text.

        jsonml_xml.from_XML(node)
            Converts XML nodes to JsonML-list.

        jsonml_xml.from_XML_text(xml_text)
            Converts XML text to JsonML-list.
"""
from xmlhelper import etree


def from_XML_text(xml_text):
    """From an xml_text get the equivalent JsonML-list.

    >>> test = from_XML_text('<a />')
    >>> True if test == ['a'] else test
    True
    >>> test = from_XML_text('<a></a>')
    >>> True if test == ['a'] else test
    True
    >>> test = from_XML_text('<a t="a"><b>foo</b></a>')
    >>> True if test == ['a', {'t': 'a'}, ['b', 'foo']] else test
    True
    """
    return from_XML(etree.XML(xml_text))


def from_XML(node):
    """From an xml node get the equivalent JsonML-list."""
    result, tail = _from_XML_with_tail(node)
    return result


def to_XML_text(jsonml_list):
    """From JsonML-list to XML text representation.

    >>> test = to_XML_text(['a'])
    >>> True if test in ['<a />', '<a></a>', '<a/>'] else test
    True
    >>> test = to_XML_text(['a', ['b', 'hey']])
    >>> True if test == '<a><b>hey</b></a>' else test
    True
    >>> test = to_XML_text(['a', {'b': 'c'}, 'd'])
    >>> True if test == '<a b="c">d</a>' else test
    True
    >>> test = to_XML_text(['a', 't1', ['b', 't2'], 't3', ['b', 't4'], 't5'])
    >>> True if test == '<a>t1<b>t2</b>t3<b>t4</b>t5</a>' else test
    True
    """
    return etree.tostring(to_XML(jsonml_list))


def to_XML(jsonml_list):
    """From JsonML-list to XML."""
    tag = jsonml_list[0]
    root = etree.Element(tag)
    list_length = len(jsonml_list)
    next_item = 1
    if list_length == 1:
        return root

    if isinstance(jsonml_list[1], dict):
        # Attributes
        next_item = 2
        for key, value in jsonml_list[1].items():
            root.set(key, value)

    last_node = None
    for i in range(next_item, list_length):
        element = jsonml_list[i]
        if isinstance(element, basestring):
            if last_node is None:
                root.text = element
            else:
                last_node.tail = element
        else:
            node = to_XML(element)
            last_node = node
            root.append(node)

    return root


def _from_XML_with_tail(node):
    element = []

    # Get the node name
    tag = node.tag
    element.append(tag)

    # Get the attributes
    atts = dict([item for item in node.items()])
    if atts:
        element.append(atts)

    # Get the text
    if node.text:
        text = _cleanup_text(node.text)
        if text:
            element.append(text)

    # Get the children
    for child in node.getchildren():
        if isinstance(child, basestring):
            # For text ignore whitespace
            text = _cleanup_text(child)
            if text:
                element.append(text)
        else:
            assert etree.iselement(child)
            child_el, tail = _from_XML_with_tail(child)
            element.append(child_el)
            if tail:
                element.append(tail)

    # Get the tail
    tail = None
    if node.tail:
        tail = _cleanup_text(node.tail)
    return element, tail


def _cleanup_text(raw_text, strip_chars=(' ', '\t', '\n')):
    return raw_text.strip(''.join(strip_chars))


def test_from_xml_text():
    """Test some samples."""
    text = """<ul>
         <li style="color:red">First Item</li>
         <li title="Some hover text." style="color:green"> Second Item </li>
         <li><span class="code-example-third">Third</span>
         Item<br />Foo<br />Bar</li>
         </ul>"""
    expected = ['ul',
                ['li', {'style': 'color:red'}, 'First Item'],
                ['li', {'style': 'color:green',
                        'title': 'Some hover text.'}, 'Second Item'],
                ['li',
                    ['span', {'class': 'code-example-third'}, 'Third'],
                    # Notice the three "tails" are properly collected.
                    'Item', ['br'], 'Foo', ['br'], 'Bar']]
    assert from_XML_text(text) == expected
    assert from_XML_text('<xml />') == ['xml']

    complex_text = """
    <table class="MyTable" style="background-color:yellow">
      <tr>
        <td class="MyTD" style="border:1px solid black">
        #5D28D1</td>
        <td class="MyTD" style="background-color:red">
        Example text here</td>
      </tr>
      <tr>
        <td class="MyTD" style="border:1px solid black">
        #AF44EF</td>
        <td class="MyTD" style="background-color:green">
        127310656</td>
      </tr>
      <tr>
        <td class="MyTD" style="border:1px solid black">
        #AAD034</td>
        <td class="MyTD" style="background-color:blue">
        &nbsp;
        <span style="background-color:maroon">&copy;</span>
        &nbsp;
          </td>
      </tr>
    </table>
    """
    complex_expected = """["html", ["body", [
        "table", {
            "class": "MyTable",
            "style": "background-color:yellow"
        },
        [
            "tr",
            ["td", {
                "class": "MyTD",
                "style": "border:1px solid black"
            },
                "#5D28D1"
            ],
            ["td", {
                "class": "MyTD",
                "style": "background-color:red"
            },
                "Example text here"
            ]
        ],
        [
            "tr",
            ["td", {
                "class": "MyTD",
                "style": "border:1px solid black"
            },
                "#AF44EF"
            ],
            ["td", {
                "class": "MyTD",
                "style": "background-color:green"
            },
                "127310656"
            ]
        ],
        [
            "tr",
            ["td", {
                "class": "MyTD",
                "style": "border:1px solid black"
            },
                "#AAD034"
            ],
            ["td", {
                "class": "MyTD",
                "style": "background-color:blue"
            },
                "\u00A0",
                ["span", {"style": "background-color:maroon"},
                 "\u00A9"
                 ],
                "\u00A0"
            ]
        ]
    ]
    ]]"""
    # etree.HTML exists in lxml, check that we are using something compatible.
    assert 'HTML' in dir(etree), etree.__file__
    result = from_XML(etree.HTML(complex_text))
    import json
    assert result == json.loads(complex_expected), result
