"""
TODO
"""
from lxml import etree
import argparse
import random, string

from pyparlaclarin.refine import format_texts

TEI_NAMESPACE ="{http://www.tei-c.org/ns/1.0}"
ALTO_NAMESPACE = "{http://www.loc.gov/standards/alto/ns-v3#}"
XML_NAMESPACE = "{http://www.w3.org/XML/1998/namespace}"

XML_PARSER = etree.XMLParser(remove_blank_text=True)

def load_xml(path):
    with open(path) as f:
        root = etree.parse(f, XML_PARSER).getroot()
    return root

def populate_parlaclarin(parlaclarin, alto, alto_path):
    # Remove example elements
    body = parlaclarin.findall(f".//{TEI_NAMESPACE}body")[0]
    div = body.findall(f".//{TEI_NAMESPACE}div")[0]
    for elem in div:
        elem.getparent().remove(elem)

    # Add link to file
    pb = etree.SubElement(div, f"{TEI_NAMESPACE}pb")
    pb.attrib["facs"] = alto_path

    # TODO: add paragraphs from alto
    for TextBlock in alto.findall(f".//{ALTO_NAMESPACE}TextBlock"):
        paragraph_words = []
        for String in TextBlock.findall(f".//{ALTO_NAMESPACE}String"):
            word = String.attrib["CONTENT"]
            paragraph_words.append(word)

        paragraph_text = " ".join(paragraph_words)
        print(paragraph_text)
        note = etree.SubElement(div, f"{TEI_NAMESPACE}note")
        note.text = paragraph_text
        note.attrib[f"{XML_NAMESPACE}id"] = "".join(random.choices(string.ascii_letters, k=8))

    return parlaclarin

def main(args):
    parlaclarin = load_xml(args.template_path)
    alto = load_xml(args.altopath)

    parlaclarin = populate_parlaclarin(parlaclarin, alto, args.altopath)
    parlaclarin = format_texts(parlaclarin, padding=10)
    b = etree.tostring(
        parlaclarin, pretty_print=True, encoding="utf-8", xml_declaration=True
    )
    with open(args.outpath, "wb") as f:
        f.write(b)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--altopath", type=str, required=True)
    parser.add_argument("--template_path", type=str, default="data/template.xml")
    parser.add_argument("--outpath", type=str, required=True)
    args = parser.parse_args()
    main(args)
