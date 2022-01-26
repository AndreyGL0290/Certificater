import pymorphy2 as pmr
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker


def name_change(name, case='dative'):
    # Нужно для свободного выбора падежа
    all_cases = {
    'genetive': Case.GENITIVE, 
    'accusative': Case.ACCUSATIVE, 
    'dative': Case.DATIVE, 
    'instrumental': Case.INSTRUMENTAL, 
    'prepositional': Case.PREPOSITIONAL
    }
    morph = pmr.MorphAnalyzer(lang='ru')  # определение пола
    maker = PetrovichDeclinationMaker()  # склонение ФИО
    full_name = name.split()  # разбиение ФИО на составляющие

    gender = ""
    # Определяем пол по отчеству человека (если оно имеется)
    # Если последняя буква - ч, то это мужчина, иначе женщина
    if full_name[-1]:
        if full_name[-1][-1].lower() == 'ч':
            gender = Gender.MALE
        else:
            gender = Gender.FEMALE
    else:
        if 'masc' in morph.parse(full_name[1])[0].tag:
            gender = Gender.MALE
        elif 'femn' in morph.parse(full_name[1])[0].tag:
            gender = Gender.FEMALE

    cased_first_name = maker.make(
        NamePart.FIRSTNAME, gender, all_cases[case], full_name[1])
    cased_sur_name = maker.make(
        NamePart.LASTNAME, gender, all_cases[case], full_name[0])
    #  cased_patronymic = maker.make(
    #     NamePart.MIDDLENAME, gender, Case.DATIVE, full_name[2])

    final_name = cased_sur_name + ' ' + cased_first_name # + ' ' + cased_patronymic
    final_name = final_name.strip()

    return final_name


'''
    f_name = ''
    print()
    print(morph.parse(name))
    for elem in morph.parse(name):
        print(elem)
        if 'Patr' in elem.tag:
            f_name = elem
    print()

    is_name = any('Patr' in p.tag for p in morph.parse(name))
    print(is_name)
    print("Ok")
'''

'''
    if 'masc' in morph.parse(full_name[1])[0].tag:
        gender = Gender.MALE
    else:
        gender = Gender.FEMALE
    
    if 'masc' in morph.parse(full_name[1])[0].tag:
        cased_last_name = maker.make(NamePart.LASTNAME, Gender.MALE, Case.DATIVE, full_name[0])
        cased_name = maker.make(NamePart.FIRSTNAME, Gender.MALE, Case.DATIVE, full_name[1])
    elif 'femn' in morph.parse(full_name[1])[0].tag:
        cased_last_name = maker.make(NamePart.LASTNAME, Gender.FEMALE, Case.DATIVE, full_name[0])
        cased_name = maker.make(NamePart.FIRSTNAME, Gender.FEMALE, Case.DATIVE, full_name[1])
    try:
        if 'masc' in morph.parse(full_name[1])[0].tag:
            cased_middle_name = maker.make(NamePart.MIDDLENAME, Gender.MALE, Case.DATIVE, full_name[2])
            print("Hi", cased_middle_name)
        elif 'femn' in morph.parse(full_name[1])[0].tag:
            cased_middle_name = maker.make(NamePart.MIDDLENAME, Gender.FEMALE, Case.DATIVE, full_name[2])

        return [cased_last_name, cased_name, cased_middle_name]
    except IndexError:
        return [cased_last_name, cased_name, '']
'''
