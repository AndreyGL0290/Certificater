from importlib.metadata import PackageNotFoundError
from morphy_using import name_change
from pptx import Presentation
from pptx.exc import PackageNotFoundError as PNFE

def PPTX_GENERATOR(data):
    try:
        prs = Presentation(data['template'])
    except PNFE:
        return "Template"
    for shape in prs.slides[0].shapes:  # перебираем объекты на слайде
        if (shape.has_text_frame):
            for key, value in data.items():
                
                try:
                    if key == shape.text_frame.text.lower() == 'name':
                        # Меняем слово-заместитель в презентации на склоненное значение этого слова в нашем словаре data
                        try:
                            shape.text_frame.paragraphs[0].runs[0].text = name_change(value, data['case'])
                        # Если падеж не указан отдельно в Excel файле, то используем значение по умолчанию
                        except KeyError:
                            shape.text_frame.paragraphs[0].runs[0].text = name_change(value)
                except:
                    if key == shape.text_frame.text.lower():
                        # Меняем слово-заместитель в презентации на значение этого слова в нашем словаре data
                        shape.text_frame.paragraphs[0].runs[0].text = value

    # указываем создателя
    prs.core_properties.author = ""
    # заголовок файла (ВАЖНО ДЛЯ PDF он в заголовке пишется)
    prs.core_properties.title = ""

    #  для хранения сертификатов создаём две папки, в которых тоже будут папки
    #  внитри GENERATED_PPTX и GENERATED_PDF будут папки-даты
    prs.save('GENERATED_PPTX/' + data['date'] + '/' + data['file_name'] + '_' + data['id'] + '.pptx')
    # имя файла для перевода его в PDF
    return (data['file_name'] + '_' + data['id'])


# # Дублируем слайд
# def duplicate_slide(pres, index=0):
#     template = pres.slides[index]
#     blank_slide_layout = pres.slide_layouts[0] # Говорим что слайд будет титульным (1 - титульный слайд)

#     copied_slide = pres.slides.add_slide(blank_slide_layout)
    

#     for shp in template.shapes:
#         el = shp.element
#         newel = copy.deepcopy(el)
#         copied_slide.shapes._spTree.insert_element_before(newel, 'p:extLst')

#     # Копируем .rels которые ведут нас к изображению, без этого картинка не отоброзится
#     for _, value in six.iteritems(template.part.rels):
#         # Make sure we don't copy a notesSlide relation as that won't exist
#         if "notesSlide" not in value.reltype:
#             copied_slide.part.rels.add_relationship(
#                 value.reltype,
#                 value._target,
#                 value.rId
#             )