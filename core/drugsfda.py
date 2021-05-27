import collections
import pandas as pd
import re
import pdftotext
import requests

from static.constants import FILE_PATH


class DrugsFDA:
    def __init__(self, fda_app_num):
        self.FDA_Application_Number = None
        drugs_fda_df = pd.read_csv(FILE_PATH.DRUGSFDA_ORIGIN_DOCS, encoding="ISO-8859-1", delimiter='\t', dtype=str)
        drugs_fda_application_df = pd.read_csv(FILE_PATH.DRUGSFDA_ORIGIN_APPLICATION, encoding="ISO-8859-1",
                                               delimiter='\t',
                                               dtype=str)
        drugs_fda_df = pd.merge(drugs_fda_df, drugs_fda_application_df, how='left', on='ApplNo')
        drugs_fda_df['FullApplNo'] = drugs_fda_df.ApplType + drugs_fda_df.ApplNo
        drugs_fda_df.ApplicationDocsDate = pd.to_datetime(drugs_fda_df.ApplicationDocsDate).dt.date
        drug_df = drugs_fda_df[(drugs_fda_df.FullApplNo == fda_app_num) & (drugs_fda_df.ApplicationDocsTypeID == '2')] \
            .sort_values(['ApplicationDocsDate'], ascending=False)
        if drug_df.shape[0] > 0:
            drug = drug_df.iloc[0]
            self.FDA_Application_Number = fda_app_num
            self.Docs_Date = drug.ApplicationDocsDate
            self.Docs_Url = drug.ApplicationDocsURL
            self.Pdf = DrugsFDAPdf(get_pdf(self.Docs_Url))


def get_pdf(url):
    try:
        r = requests.get(url)
        with open('templbl.pdf', 'wb') as fd:
            fd.write(r.content)
        f = open('templbl.pdf', 'rb')
        pdf = pdftotext.PDF(f)
        return '\n\n'.join(pdf)
    except:
        return ''


def build_dict_helper(title_idx_list, content_list):
    content_dict = {}
    for i, title_idx in enumerate(title_idx_list):
        if i == len(title_idx_list) - 1:
            content_dict[title_idx[1]] = content_list[title_idx[0] + 1:]
        else:
            content_dict[title_idx[1]] = content_list[title_idx[0] + 1:title_idx_list[i + 1][0]]
    return content_dict


def group_sentence_helper(sentence_list):
    end_list = [(i, item) for i, item in enumerate(sentence_list)
                if len(item.split(' ')) <= 5 or item[-1] == '.' or item[-1] == ':']
    group_sentence = []
    if len(end_list) > 0:
        for i, end in enumerate(end_list):
            if i == 0:
                group_sentence.append(' '.join(sentence_list[:end[0] + 1]))
            else:
                group_sentence.append(' '.join(sentence_list[end_list[i - 1][0] + 1:end[0] + 1]))
        if end_list[-1] != len(sentence_list) - 1:
            group_sentence.append(' '.join(sentence_list[end_list[-1][0] + 1:]))
    return group_sentence


def print_dict(dict):
    ordered_dict = collections.OrderedDict(sorted(dict.items()))
    dict_content_list = []
    for dict_key, dict_value in ordered_dict.items():
        dict_content_list.append(dict_key)
        dict_content_list = dict_content_list + group_sentence_helper(dict_value)
    return dict_content_list


class DrugsFDAPdf:
    filter_pattern = ['^Reference ID:', '^[0-9]+$', '^Page', '^$']
    title_pattern = ['^FULL PRESCRIBING INFORMATION$',
                     '^\d+\s+INDICATIONS AND USAGE$',
                     '^\d+\s+DOSAGE AND ADMINISTRATION$',
                     '^\d+\s+DOSAGE FORMS AND STRENGTHS$',
                     '^\d+\s+CONTRAINDICATIONS$',
                     '^\d+\s+WARNINGS AND PRECAUTIONS$',
                     '^\d+\s+ADVERSE REACTIONS$',
                     '^\d+\s+DRUG INTERACTIONS$',
                     '^\d+\s+USE IN SPECIFIC POPULATIONS$',
                     '^\d+\s+DRUG ABUSE AND DEPENDENCE$',
                     '^\d+\s+OVERDOSAGE$',
                     '^\d+\s+DESCRIPTION$',
                     '^\d+\s+CLINICAL PHARMACOLOGY$',
                     '^\d+\s+NONCLINICAL TOXICOLOGY$',
                     '^\d+\s+CLINICAL STUDIES$',
                     '^\d+\s+HOW SUPPLIED/STORAGE AND HANDLING$',
                     '^\d+\s+PATIENT COUNSELING INFORMATION$',
                     '^Medication Guide$',
                     '^MEDICATION GUIDE$']
    admef_pattern = ['^absorption$',
                     '^distribution$',
                     '^metabolism$',
                     '^excretion$',
                     '^elimination$',
                     '^effect of food$',
                     '^effects of food$',
                     '^food effect$',
                     '^food effects$',
                     'table',
                     'figure',
                     'population',
                     'impairment',
                     'geriatric',
                     'pediatric',
                     'gender',
                     'race',
                     'ethnicity',
                     'interaction',
                     'interactions',
                     'racial',
                     'age',
                     'populations',
                     'weight',
                     'half-life']
    adme_pattern = ['absorption', 'distribution', 'metabolism', 'excretion', 'elimination']

    def build_pdf_content_dict(self, pdf_content):
        pdf_content_dict = {}

        pdf_content_list = pdf_content.split('\n')
        pdf_content_list = list(map(lambda s: re.sub(r'\s+', ' ', s).strip(), pdf_content_list))
        pdf_content_list = list(filter(lambda s: not re.search(r'|'.join(self.filter_pattern), s), pdf_content_list))

        title_idx_list = [(i, item) for i, item in enumerate(pdf_content_list) if
                          re.search(r'|'.join(self.title_pattern), item)]
        # level 1 title
        if pdf_content_list and len(title_idx_list) > 0:
            pdf_content_dict = build_dict_helper(title_idx_list, pdf_content_list)
            # level 2 title
            for key, value in pdf_content_dict.items():
                if re.search(r'^\d+', key):
                    section_number = re.search(r'^\d+', key).group()
                    sub_title_idx_list = [(i, item) for i, item in enumerate(value) if
                                          re.search(rf'^{section_number}\.\d+\s+.+$', item)]
                    if len(sub_title_idx_list) > 0:
                        pdf_content_dict[key] = build_dict_helper(sub_title_idx_list, value)
                        pharmacokinetics = list(
                            filter(lambda t: 'pharmacokinetics' in t[1].lower(), sub_title_idx_list))
                        # level 3 title: ADMEF
                        if len(pharmacokinetics) > 0:
                            admef_content_list = pdf_content_dict[key][pharmacokinetics[0][1]]
                            admef_idx_list = [(i, item) for i, item in enumerate(admef_content_list)
                                              if len(item.split(' ')) <= 10
                                              and ',' not in item
                                              and item[-1] != '.'
                                              and re.search(r'|'.join(self.admef_pattern), re.sub(r'[^a-z ]+', '', item.lower().strip()))]
                            if len(list(filter(lambda item: re.search(r'|'.join(self.adme_pattern), item[1].lower()),
                                               admef_idx_list))) > 0:
                                pdf_content_dict[key][pharmacokinetics[0][1]] = build_dict_helper(admef_idx_list, admef_content_list)
        return pdf_content_dict

    def dict_value_helper(self, path):
        current_dict = self.pdf_content_dict
        found = False
        value = ''
        for i, key in enumerate(path):
            if type(current_dict) is dict:
                for dict_key, dict_value in current_dict.items():
                    if re.search(rf'{key.lower()}', dict_key.lower()):
                        current_dict = dict_value
                        if i == len(path) - 1:
                            found = True
                        break
            else:
                return value
        if found:
            if type(current_dict) is list:
                value = '\n\n'.join(group_sentence_helper(current_dict))
            else:
                value = '\n\n'.join(print_dict(current_dict))
        return value

    def pharmacokinetics_non_admef(self):
        pharmacokinetics_list = self.Pharmacokinetics.split('\n\n')
        pharmacokinetics_list = [x for x in pharmacokinetics_list if x not in self.Absorption.split('\n\n')]
        pharmacokinetics_list = [x for x in pharmacokinetics_list if x not in self.Distribution.split('\n\n')]
        pharmacokinetics_list = [x for x in pharmacokinetics_list if x not in self.Metabolism.split('\n\n')]
        pharmacokinetics_list = [x for x in pharmacokinetics_list if x not in self.Excretion.split('\n\n')]
        pharmacokinetics_list = [x for x in pharmacokinetics_list if x not in self.Food_Effect.split('\n\n')]
        pharmacokinetics_list = [x for x in pharmacokinetics_list if not re.search(r'|'.join(self.adme_pattern + ['^effect of food', '^effects of food', '^food effect', '^food effects']), x.lower())]
        return '\n\n'.join(pharmacokinetics_list)

    def __init__(self, pdf_content):
        self.pdf_content_dict = self.build_pdf_content_dict(pdf_content)

        self.Boxed_Warning = self.dict_value_helper(['FULL PRESCRIBING INFORMATION'])
        self.Indication = self.dict_value_helper(['INDICATIONS AND USAGE'])
        self.Dosage_Administration = self.dict_value_helper(['DOSAGE AND ADMINISTRATION'])
        self.Pregnancy = self.dict_value_helper(['USE IN SPECIFIC POPULATIONS', 'Pregnancy'])
        self.Lactation = self.dict_value_helper(['USE IN SPECIFIC POPULATIONS', 'Lactation'])
        self.Nursing_Mother = self.dict_value_helper(['USE IN SPECIFIC POPULATIONS', 'Nursing Mother'])
        self.Females_Males_of_Reproductive_Potential = self.dict_value_helper(['USE IN SPECIFIC POPULATIONS',
                                                                               'Females and Males of Reproductive Potential|Females & Males of Reproductive Potential'])
        self.Mechanism_of_Action = self.dict_value_helper(['CLINICAL PHARMACOLOGY', 'Mechanism of Action'])
        self.Pharmacodynamics = self.dict_value_helper(['CLINICAL PHARMACOLOGY', 'Pharmacodynamics'])
        self.Pharmacokinetics = self.dict_value_helper(['CLINICAL PHARMACOLOGY', 'Pharmacokinetics'])
        self.Absorption = self.dict_value_helper(['CLINICAL PHARMACOLOGY', 'Pharmacokinetics', 'Absorption'])
        self.Distribution = self.dict_value_helper(['CLINICAL PHARMACOLOGY', 'Pharmacokinetics', 'Distribution'])
        self.Metabolism = self.dict_value_helper(['CLINICAL PHARMACOLOGY', 'Pharmacokinetics', 'Metabolism'])
        # self.Elimination = self.dict_value_helper(['CLINICAL PHARMACOLOGY', 'Pharmacokinetics', 'Elimination'])
        self.Excretion = self.dict_value_helper(['CLINICAL PHARMACOLOGY', 'Pharmacokinetics', 'Excretion'])
        self.Excretion += self.dict_value_helper(['CLINICAL PHARMACOLOGY', 'Pharmacokinetics', 'Elimination'])
        self.Food_Effect_1 = self.dict_value_helper(
            ['CLINICAL PHARMACOLOGY', 'Pharmacokinetics', 'food effect|food effects|effect of food|effects of food'])
        self.Food_Effect_2 = ''
        self.Cytotoxic = self.dict_value_helper(['NONCLINICAL TOXICOLOGY', 'Carcinogenesis'])
        self.How_Supplied = self.dict_value_helper(['HOW SUPPLIED'])
        self.Information_for_Patients = self.dict_value_helper(['PATIENT COUNSELING INFORMATION'])

        if self.Pharmacokinetics:
            paragraph_list = self.Pharmacokinetics.split('\n\n')
            for paragraph in paragraph_list:
                if re.search(r'^absorption\s*(:|—|-|–)', paragraph.lower()) and not self.Absorption:
                    title = re.split(':|—|-|–', paragraph)[0]
                    self.Absorption = paragraph[len(title)+1:].strip()
                if re.search(r'^distribution\s*(:|—|-|–)', paragraph.lower()) and not self.Distribution:
                    title = re.split(':|—|-|–', paragraph)[0]
                    self.Distribution = paragraph[len(title)+1:].strip()
                if re.search(r'^metabolism\s*(:|—|-|–)', paragraph.lower()) and not self.Metabolism:
                    title = re.split(':|—|-|–', paragraph)[0]
                    self.Metabolism = paragraph[len(title)+1:].strip()
                if re.search(r'^(excretion|elimination)\s*(:|—|-|–)', paragraph.lower()) and not self.Excretion:
                    title = re.split(':|—|-|–', paragraph)[0]
                    self.Excretion = paragraph[len(title)+1:].strip()
                if re.search(r'^(food effect|food effects|effect of food|effects of food)\s*(:|—|-|–)', paragraph.lower()) and not self.Food_Effect_1:
                    title = re.split(':|—|-|–', paragraph)[0]
                    self.Food_Effect_1 = paragraph[len(title)+1:].strip()

        if self.Absorption:
            paragraph_list = self.Absorption.split('\n\n')
            for paragraph in paragraph_list:
                if re.search(r'^(food effect|food effects|effect of food|effects of food)\s*(:|—|-|–)', paragraph.lower()):
                    paragraph_list.remove(paragraph)
                    title = re.split(':|—|-|–', paragraph)[0]
                    self.Food_Effect_2 = paragraph[len(title)+1:].strip()
                    self.Food_Effect_1 = ''
            self.Absorption = '\n\n'.join(paragraph_list)

        self.Food_Effect = self.Food_Effect_1 if self.Food_Effect_1 else self.Food_Effect_2

        self.Other = self.pharmacokinetics_non_admef()

        tube_keywords = ['ng tube', '(ng) tube', 'nasogastric tube', 'gastrostomy tube', 'jejunal tube', 'feeding tube']
        tube_list = []
        for paragraph in self.Dosage_Administration.split('\n\n'):
            if re.search(r'|'.join(tube_keywords), paragraph.lower()):
                tube_list.append(paragraph)
        self.Feeding_Tube = '\n\n'.join(tube_list)
