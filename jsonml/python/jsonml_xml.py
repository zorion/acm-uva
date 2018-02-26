# -*- coding: utf-8 -*-
"""This file creates a global JsonML object containing these methods:

        jsonml_xml.to_XML(string|array)
            Converts JsonML to XML nodes

        jsonml_xml.to_XML_text(JsonML)
            Converts JsonML to XML text

        jsonml_xml.from_XML(node)
            Converts XML nodes to JsonML

        jsonml_xml.from_XML_text(xmlText)
            Converts XML text to JsonML
"""
from xmlhelper import etree


def from_XML_text(xml_text):
    """From an xml_text get the equivalent object."""
    return from_XML(etree.XML(xml_text))


def from_XML(node):
    """From an xml node get the equivalent object."""
    result, tail = _from_XML_with_tail(node)
    return result


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
        text = node.text.strip()
        if text:
            element.append(text)

    # Get the children
    for child in node.getchildren():
        if isinstance(child, basestring):
            # For text ignore whitespace
            text = child.strip()
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
        tail = node.tail.strip()
    return element, tail


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
    assert 'HTML' in dir(etree), etree.__file__
    result = from_XML(etree.HTML(complex_text))
    import json
    assert result == json.loads(complex_expected), result
