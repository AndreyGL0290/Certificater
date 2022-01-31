import pymorphy2 as pmr
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker


def name_change(name='Иванов Иван Иванович', case='dative'):
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
