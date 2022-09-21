import json


class JSON:
    "Класс для создания JSON файлов"
    def __init__(self, value, filename):
        self.value = value
        self.filename = filename
        with open(f'{self.filename}.JSON', 'w') as fp:
            json.dump(self.value, fp)
        fp.close()
    
    def __set__(self, instance, value):
        self.value = value
        with open(f'{self.filename}.JSON', 'w') as fp:
            json.dump(self.value, fp)
        fp.close()

    def __get__(self, instance):
        with open(f'{self.filename}.JSON', 'r') as fp:
            data = json.load(fp)
        fp.close()
        return data