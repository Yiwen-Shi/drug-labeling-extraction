from lxml import etree
from datetime import datetime
from orderedset import OrderedSet

namespaces = {"v": "urn:hl7-org:v3"}


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def printbold(string):
    print(''.join(style.BOLD + '\n' + string + style.END))


class SPL:
    def __init__(self, xmlString):
        p = etree.XMLParser(huge_tree=True)
        self.xml = etree.fromstring(xmlString, p)

    @property
    def Drug_Name(self):
        try:
            name = self.xml.xpath("//v:manufacturedProduct/v:manufacturedProduct/v:name"
                                  "| //v:manufacturedProduct/v:manufacturedMedicine/v:name", namespaces=namespaces)

            return name[0].text.replace("\t", "").replace("\n", "")
        except:
            return ""

    @property
    def NDCs(self):
        try:
            ndcs = self.xml.xpath("//v:manufacturedProduct/v:manufacturedProduct/v:code/@code"
                                  "| //v:manufacturedProduct/v:manufacturedMedicine/v:code/@code",
                                  namespaces=namespaces)
            return ndcs
        except:
            return ""

    @property
    def Effective_Date(self):
        try:
            date = self.xml.xpath("//v:effectiveTime/@value", namespaces=namespaces)
            date[0] = date[0][0:8]
            date = datetime.strptime(date[0], '%Y%m%d')
            return date
        except:
            return ""

    @property
    def Box_Warning(self):  # "ENTRESTO":box_warning repeated!!!
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34066-1']/..//v:title"
                                                      "| //v:code[@code='34066-1']/..//v:paragraph"
                                                      "| //v:code[@code='34066-1']/..//v:item",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    @property
    def Box_Warning_OLD(self):  # Working, TODO: subtitle in BOLD

        note_section_titles = (self.xml.xpath("//v:code[@code='34066-1']""/..//v:title",
                                              namespaces=namespaces))
        subtitle = note_section_titles[0].xpath(".//text()")

        note_section_paragraphs = (self.xml.xpath("//v:code[@code='34066-1']""/..//v:paragraph",
                                                  namespaces=namespaces))

        # text = list()
        text = subtitle
        for paragraph in note_section_paragraphs:
            text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

        return '\n\n'.join(OrderedSet(text))

    # 	INDICATIONS & USAGE SECTION - 34067-9

    @property
    def Indication(self):  # TODO: much to do for short summary
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34067-9']/..//v:title" 
                                                      " | //v:code[@code='34067-9']""/..//v:paragraph"
                                                      " | //v:code[@code='34067-9']/..//v:item",
                                                      namespaces=namespaces))
            excerpt_section_paragraphs = (self.xml.xpath("//v:code[@code='34067-9']/..//v:excerpt//v:title" 
                                                         " | //v:code[@code='34067-9']/..//v:excerpt//v:paragraph"
                                                         " | //v:code[@code='34067-9']/..//v:excerpt//v:item",
                                                         namespaces=namespaces))
            note_section_paragraphs = filter(lambda x: x not in excerpt_section_paragraphs, note_section_paragraphs)

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # INFORMATION FOR PATIENTS SECTION - 34076-0
    @property
    def Information_for_Patients(self):  # why 'Route of Administration'?
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34076-0']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            """ for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))
            """

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # Dosage and Administration with Dosing Regimen
    ## DOSAGE & ADMINISTRATION SECTION

    @property
    def Dosage_Administration(self):  # TODO: subtitles in BOLD

        """
        note_section_paragraphs = (self.xml.xpath("//v:code[@code='34068-7']" "/following-sibling::v:paragraph[1]",
            namespaces=namespaces))
        """
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34068-7']/..//v:title"
                                                      "| //v:code[@code='34068-7']/..//v:paragraph"
                                                      "| //v:code[@code='34068-7']/..//v:item",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # MECHANISM OF ACTION SECTION  - 43679-0
    @property
    def Mechanism_of_Action(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='43679-0']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # PHARMACODYNAMICS SECTION - 43681-6
    @property
    def Pharmacodynamics(self):  # Why also called "Mechanism of Action"?
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='43681-6']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # DRUG PRODUCT & SAFETY INFORMATION
    # PREGNANCY SECTION - 42228-7

    @property
    def Pregnancy(self):  # It's called "Pregnancy"
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='42228-7']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    @property
    def Teratogenic_Effects(self):  # NEED "Animal Findings"?
        try:
            note_section_paragraphs = (
                self.xml.xpath("//v:code[@code='34077-8']/..//v:paragraph | //v:code[@code='34077-8']/..//v:item",
                               namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    @property
    def Nonteratogenic_Effects(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34078-6']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    @property
    def Lactation(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='77290-5']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # How about LACTATION SECTION (77290-5)?
    @property
    def Nursing_Mothers(self):  # NURSING MOTHERS SECTION
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34080-2']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            # OrderedSet library is used to remove any duplicate selected text while maintaining text order.
            # This may be able to be replaced by just using a standard dict. With something like
            # ' '.join(list(dict.fromkeys(text)))
            # but this has not been tested.

            return ' '.join(OrderedSet(text))
        except:
            return ""

    # FEMALES & MALES OF REPRODUCTIVE POTENTIAL SECTION 77291 - 3
    @property
    def Females_Males_of_Reproductive_Potential(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='77291-3']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    # PHARMACOKINETICS SECTION - 43682-4
    @property
    def Pharmacokinetics(self):  # TODO: how to assign each paragraph?
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='43682-4']/..//v:title"
                                                      "| //v:code[@code='43682-4']/..//v:paragraph"
                                                      "| //v:code[@code='43682-4']/..//v:item",
                                                      namespaces=namespaces))

            table_section_paragraphs = (self.xml.xpath("//v:code[@code='43682-4']/..//v:table//v:paragraph",
                                                       namespaces=namespaces))
            note_section_paragraphs = filter(lambda x: x not in table_section_paragraphs, note_section_paragraphs)

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    @property
    def Pharmacokinetics_Table(self):
        try:
            table_section_paragraphs = (self.xml.xpath("//v:code[@code='43682-4']/..//v:table",
                                                       namespaces=namespaces))

            text = list()
            for paragraph in table_section_paragraphs:
                table_string = ''.join(paragraph.xpath(".//v:caption/text()", namespaces=namespaces)).strip()
                table_string += '<table>'
                for row in paragraph.xpath(".//v:tr", namespaces=namespaces):
                    table_string += '<tr>'
                    for col in row.xpath(".//v:th", namespaces=namespaces):
                        table_string += '<td><b>{}</b></td>'.format(' '.join(col.xpath('.//text()')).strip())
                    for col in row.xpath(".//v:td", namespaces=namespaces):
                        colspan = col.get('colspan')
                        if colspan:
                            table_string += '<td colspan={}>{}</td>'.format(colspan, ' '.join(col.xpath('.//text()')).strip())
                        else:
                            table_string += '<td>{}</td>'.format(' '.join(col.xpath('.//text()')))
                    table_string += '</tr>'
                table_string += '</table>'
                text.append(table_string)

            return '\n\n'.join(text)
        except:
            return ""

    # CARCINOGENESIS & MUTAGENESIS & IMPAIRMENT OF FERTILITY SECTION - 34083-6
    @property
    def Carcinogenesis(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34083-6']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""


    # HOW SUPPLIED SECTION - 34069 - 5
    @property
    def How_Supplied(self):
        try:
            note_section_paragraphs = (self.xml.xpath("//v:code[@code='34069-5']""/..//v:paragraph",
                                                      namespaces=namespaces))

            text = list()
            for paragraph in note_section_paragraphs:
                text.append(' '.join(''.join(paragraph.xpath(".//text()")).split()))

            return '\n\n'.join(OrderedSet(text))
        except:
            return ""

    @property
    def Appl_No(self):
        try:
            Appl_no = list(set(self.xml.xpath("//v:approval/v:id/@extension", namespaces=namespaces)))
            return ' '.join(OrderedSet(Appl_no))
        except:
            return ""
