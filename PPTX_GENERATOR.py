from morphy_using import name_change
from pptx import Presentation
import os


def PPTX_GENERATOR(data):
    prs = Presentation(data['template'])
    for shape in prs.slides[0].shapes:  # перебираем объекты на слайде
        if (shape.has_text_frame):
            for i in data.items():
                try:
                    if i[0] == shape.text_frame.text.lower():
                        shape.text_frame.paragraphs[0].runs[0].text = name_change(
                            i[1])
                except:
                    if i[0] == shape.text_frame.text.lower():
                        shape.text_frame.paragraphs[0].runs[0].text = i[1]

    # указываем создателя
    prs.core_properties.author = ""
    # заголовок файла (ВАЖНО ДЛЯ PDF он в заголовке пишется)
    prs.core_properties.title = ""

    #  для хранения сертификатов создаём две папки, в которых тоже будут папки
    #  внитри GENERATED_PPTX и GENERATED_PDF будут папки-даты
    
    prs.save('GENERATED_PPTX/' + data['date'] + '/' +
             data['file_name'] + '_' + data['id'] + '.pptx')
    # имя файла для перевода его в PDF
    return(data['file_name'] + '_' + data['id'])
