from morphy_using import name_change
from pptx import Presentation
import os


def PPTX_GENERATOR(name, UID, today_date):
    prs = Presentation(name[3]+'.pptx')
    for shape in prs.slides[0].shapes:  # перебираем объекты на слайде
        if (shape.has_text_frame):
            if(shape.text_frame.text == 'Name'):  # ищим поле где написано Name
                shape.text_frame.paragraphs[0].runs[0].text = name_change(
                    name[0])  # зписываем туда ФИО
            if(shape.text_frame.text == 'Type1'):  # ищим поле где написано Type1
                # зписываем туда тип
                shape.text_frame.paragraphs[0].runs[0].text = name[1]
            if(shape.text_frame.text == 'Type2'):  # ищим поле где написано Type2
                # зписываем туда степень
                shape.text_frame.paragraphs[0].runs[0].text = name[2]
            if(shape.text_frame.text == 'DocumentID'):  # ищим поле где написано DocumentID
                # # зписываем туда уникальный идентификатор сертификата
                shape.text_frame.paragraphs[0].runs[0].text = UID
    # указываем создателем Кванториум
    prs.core_properties.author = "Кванториум Новосибирск"
    # заголовок файла (ВАЖНО ДЛЯ PDF он в заголовке пишется)
    prs.core_properties.title = "Сертификат"

    #  для хранения сертификатов создаём две папки, в которых тоже будут папки
    #  внитри GENERATED_PPTX и GENERATED_PDF будут папки-даты
    os.makedirs('GENERATED_PPTX/{}'.format(today_date),
                exist_ok=True)  # создаём папку
    os.makedirs('GENERATED_PDF/{}'.format(today_date),
                exist_ok=True)  # создаём папку
    prs.save('GENERATED_PPTX/' + today_date + '/' +
             name[1] + '_' + name[0] + '_' + UID + '.pptx')
    # имя файла для перевода его в PDF
    return(name[1] + '_' + name[0] + '_' + UID)
