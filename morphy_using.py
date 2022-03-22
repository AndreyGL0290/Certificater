import pymorphy2 as pmr
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker


def name_change(name, case='nominative'):
    if case == "nominative" or case == "именительный":
        return name
    # Нужно для свободного выбора падежа
    all_cases = {
    'genetive': Case.GENITIVE,
    'родительный': Case.GENITIVE,
    'accusative': Case.ACCUSATIVE,
    'винительный': Case.ACCUSATIVE, 
    'dative': Case.DATIVE, 
    'дательный': Case.DATIVE,
    'instrumental': Case.INSTRUMENTAL,
    'творительный': Case.INSTRUMENTAL,
    'prepositional': Case.PREPOSITIONAL,
    'предложный': Case.PREPOSITIONAL
    }
    morph = pmr.MorphAnalyzer(lang='ru')  # определение пола
    maker = PetrovichDeclinationMaker()  # склонение ФИО
    full_name = name.split()  # разбиение ФИО на составляющие

    gender = ""
    # Определяем пол по отчеству человека (если оно имеется)
    # Если последняя буква - ч, то это мужчина, иначе женщина
    if len(full_name) == 3:
        if full_name[-1][-1].lower() == 'ч':
            gender = Gender.MALE
        else:
            gender = Gender.FEMALE
        cased_middle_name = maker.make(NamePart.MIDDLENAME, gender, all_cases[case.lower()], full_name[2]) # Отчество
        cased_first_name = maker.make(NamePart.FIRSTNAME, gender, all_cases[case.lower()], full_name[1]) # Имя
        cased_lastname = maker.make(NamePart.LASTNAME, gender, all_cases[case.lower()], full_name[0]) # Фамилия
        final_name = f'{cased_lastname} {cased_first_name} {cased_middle_name}'
    elif len(full_name) == 2:
        for i in range(len(morph.parse(full_name[1]))):
            if 'masc' in morph.parse(full_name[1])[i].tag and 'nomn' in morph.parse(full_name[1])[i].tag:
                gender = Gender.MALE
                break
            elif 'femn' in morph.parse(full_name[1])[i].tag and 'nomn' in morph.parse(full_name[1])[i].tag:
                gender = Gender.FEMALE
                break
        
        # Если он не понял какого пола человек
        if gender == '':
            gender = Gender.MALE
        
        cased_first_name = maker.make(NamePart.FIRSTNAME, gender, all_cases[case.lower()], full_name[1]) # Имя
        cased_lastname = maker.make(NamePart.LASTNAME, gender, all_cases[case.lower()], full_name[0]) # Фамилия
        final_name = f'{cased_lastname} {cased_first_name}'
    else:
        for i in range(len(morph.parse(full_name[0]))):
            if 'masc' in morph.parse(full_name[0])[i].tag and 'nomn' in morph.parse(full_name[0])[i].tag:
                gender = Gender.MALE
                break
            elif 'femn' in morph.parse(full_name[0])[i].tag and 'nomn' in morph.parse(full_name[0])[i].tag:
                gender = Gender.FEMALE
                break
        
        # Если он не понял какого пола человек
        if gender == '':
            gender = Gender.MALE
        
        cased_first_name = maker.make(NamePart.FIRSTNAME, gender, all_cases[case.lower()], full_name[0]) # Имя
        final_name = f'{cased_first_name}'

    return final_name
