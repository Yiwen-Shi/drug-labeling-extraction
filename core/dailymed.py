import re
import requests
from core.SPL import SPL
from static.constants import URL


def label_admef(pharmacokinetics):
    admef_pattern = ['absorption',
                     'distribution',
                     'metabolism',
                     'excretion',
                     'elimination',
                     'effect of food',
                     'effects of food',
                     'effect on food',
                     'food',
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
    # Pattern 1
    admef_content_list = re.split('\n|\\\\n', pharmacokinetics)
    admef_content_list = list(filter(len, admef_content_list))
    admef_idx_list = [(i, item) for i, item in enumerate(admef_content_list)
                      if item
                      and len(item.split(' ')) <= 10
                      and ',' not in item
                      and item[-1] != '.'
                      and re.search(r'|'.join(admef_pattern), item.lower())]
    absorption = ''
    distribution = ''
    metabolism = ''
    excretion = ''
    food_effect = ''
    other = ''
    if len(list(filter(lambda item: re.search(r'|'.join(adme_pattern), item[1].lower()),
                       admef_idx_list))) > 0:
        admef_dict = build_dict_helper(admef_idx_list, admef_content_list)
        absorption = dict_value_helper(admef_dict, 'Absorption')
        distribution = dict_value_helper(admef_dict, 'Distribution')
        metabolism = dict_value_helper(admef_dict, 'Metabolism')
        excretion = dict_value_helper(admef_dict, 'Excretion|Elimination')
        food_effect = dict_value_helper(admef_dict, 'food effect|food effects|effect of food|effects of food')
        admef_content_list = remove_admef(admef_content_list, admef_dict)
    # Pattern 2
    for paragraph in admef_content_list:
        if re.search(':|—|-|–', paragraph):
            title = re.split(':|—|-|–', paragraph)[0]
            if len(title.split(' ')) < 4:
                if re.search(r'absorption', title.lower()) and not absorption:
                    absorption = paragraph
                    admef_content_list.remove(paragraph)
                if re.search(r'distribution', title.lower()) and not distribution:
                    distribution = paragraph
                    admef_content_list.remove(paragraph)
                if re.search(r'metabolism', title.lower()) and not metabolism:
                    metabolism = paragraph
                    admef_content_list.remove(paragraph)
                if re.search(r'excretion|elimination', title.lower()) and not excretion:
                    excretion = paragraph
                    admef_content_list.remove(paragraph)
                if re.search(r'|'.join(['effect of food',
                                        'effects of food',
                                        'effect on food',
                                        'food']), title.lower()) and not food_effect:
                    food_effect = paragraph
                    admef_content_list.remove(paragraph)
    other = '\n\n'.join(admef_content_list)
    # Food Effect in Absorption
    if absorption:
        absorption_list = absorption.split('\n\n')
        for paragraph in absorption_list:
            if re.search(r'|'.join(['^effect of food',
                                    '^effects of food',
                                    '^effect on food',
                                    '^food']), paragraph.lower()):
                if not food_effect:
                    food_effect = paragraph
                    absorption_list.remove(paragraph)
        absorption = '\n\n'.join(absorption_list)
    return absorption, distribution, metabolism, excretion, food_effect, other


def build_dict_helper(title_idx_list, content_list):
    content_dict = {}
    for i, title_idx in enumerate(title_idx_list):
        if i == len(title_idx_list) - 1:
            content_dict[title_idx[1]] = content_list[title_idx[0] + 1:]
        else:
            content_dict[title_idx[1]] = content_list[title_idx[0] + 1:title_idx_list[i + 1][0]]
    return content_dict


def dict_value_helper(dist, key):
    value_list = []
    for dict_key, dict_value in dist.items():
        if re.search(rf'{key.lower()}', dict_key.lower()):
            value_list.extend(filter(len, dict_value))
    return '\n\n'.join(value_list)


def remove_admef(content_list, admef_dict):
    content_list = list(content_list)
    for dict_key, dict_value in admef_dict.items():
        if re.search(r'|'.join(['absorption',
                                'distribution',
                                'metabolism',
                                'excretion',
                                'elimination',
                                'effect of food',
                                'effects of food',
                                'effect on food',
                                'food']), dict_key.lower()):
            content_list.remove(dict_key)
            content_list = list(filter(lambda x: x not in dict_value, content_list))
    return content_list


class DailyMed:
    def __init__(self, setid):
        self.SETID = setid
        if setid:
            try:
                base_url = URL.DAILYMED_SPL
                r = requests.get(url=base_url + setid + '.xml')
                spl = SPL(r.content)
                self.FDA_Application_Number = spl.Appl_No
                self.Drug_Name = spl.Drug_Name
                self.Effective_Date = spl.Effective_Date
                self.Boxed_Warning = spl.Box_Warning
                self.Indication = spl.Indication
                self.Dosage_Administration = spl.Dosage_Administration
                self.Pregnancy = spl.Pregnancy
                self.Teratogenic_Effects = spl.Teratogenic_Effects
                self.Nonteratogenic_Effects = spl.Nonteratogenic_Effects
                self.Lactation = spl.Lactation
                self.Nursing_Mothers = spl.Nursing_Mothers
                self.Females_Males_of_Reproductive_Potential = spl.Females_Males_of_Reproductive_Potential
                self.Mechanism_of_Action = spl.Mechanism_of_Action
                self.Pharmacodynamics = spl.Pharmacodynamics
                self.Pharmacokinetics = spl.Pharmacokinetics
                self.Pharmacokinetics_Table = spl.Pharmacokinetics_Table
                self.Carcinogenesis = spl.Carcinogenesis
                self.How_Supplied = spl.How_Supplied
                self.Information_for_Patients = spl.Information_for_Patients

                tube_keywords = ['ng tube', '(ng) tube', 'nasogastric tube', 'gastrostomy tube', 'jejunal tube', 'feeding tube']
                tube_list = []
                for paragraph in self.Dosage_Administration.split('\n\n'):
                    if re.search(r'|'.join(tube_keywords), paragraph.lower()):
                        tube_list.append(paragraph)
                self.Feeding_Tube = '\n\n'.join(tube_list)

                self.Absorption, self.Distribution, self.Metabolism, self.Excretion, self.Food_Effect, self.Other = label_admef(self.Pharmacokinetics)

            except:
                self.SETID = None
