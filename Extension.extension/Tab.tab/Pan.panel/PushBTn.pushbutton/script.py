# -*- coding: utf-8 -*-

__title__ = "Add Tags"
__author__ = "Cherry"
__doc__ = "This is a python script that adds tag"

from pyrevit import revit, DB, forms

# Теперь импортируем Snippets._selection
from Snippets._selection import get_selected_elements

def main():

    # Получаем активный документ
    doc = revit.doc
    uidoc = revit.uidoc

    # Выбираем элементы деталей 
    selection = get_selected_elements(uidoc)

    # Начинаем транзакцию
    with DB.Transaction(doc, "Добавить тег детали") as t:
        t.Start()
        
        for elem_id in selection:
            elem = doc.GetElement(elem_id)
            
            # Проверяем, есть ли у элемента категория
            if elem.Category:
                elem_category_name = elem.Category.Name  # Читаем имя категории
                elem_category_id = elem.Category.Id      # Получаем ID категории
                
                print("Элемент ID {} относится к категории: {}".format(elem.Id, elem_category_name))
            
            # Проверяем, является ли элемент деталью
            # if elem.Category and elem.Category.Id == DB.Category.GetCategory(doc, DB.BuiltInCategory.OST_DetailComponents).Id:
                # Получаем точку вставки тега (центр элемента)
            bbox = elem.get_BoundingBox(None)
            if bbox:
                tag_position = bbox.Min + (bbox.Max - bbox.Min) / 2
                tag_position = DB.XYZ(tag_position.X, tag_position.Y, 0)  # Оставляем Z = 0
                
                # Создаем тег
                tag = DB.IndependentTag.Create(
                    doc, doc.ActiveView.Id,
                    DB.Reference(elem),
                    False, DB.TagMode.TM_ADDBY_CATEGORY,
                    DB.TagOrientation.Horizontal,
                    tag_position
                )
                
                if tag:
                    print("Тег {} добавлен для элемента ID {}".format(tag_position, elem.Id))
            # else:
            #     print("Пропущен элемент ID {} (не деталь)".format(elem.Id))
        
        t.Commit()

    forms.alert("Готово! Теги добавлены.")

if __name__ == "__main__":
    main()