# -*- coding: utf-8 -*-
__title__ = "tag_gpt"
__author__ = "n"
__doc__ = "tag_gpt for revit tags"

import requests
from pyrevit import forms
import os
import subprocess 

def write_string_to_file_and_open(text, folder_name):
    
    current_dir = os.path.abspath(__file__)
    parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))  # Поднимаемся на 2 уровня выше
    target_dir = os.path.join(parent_dir, folder_name, "Test.pushbutton")
    file_name = "script.py"
    
    # Проверяем, существует ли папка, и создаем, если нет
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)  # Без exist_ok
    
    # Полный путь к файлу
    file_path = os.path.join(target_dir, file_name)
    
    # Записываем строку в файл
    with open(file_path, "w") as file:
        file.write(text)
    
    forms.alert('Файл создан: {}'.format(file_path))
     # Открываем файл в PyCharm (замените путь на ваш pycharm.exe, если нужно)
    # try:
    #     subprocess.Popen(["pycharm", file_path])  # Если PyCharm в PATH
    # except FileNotFoundError:
    #     print("PyCharm не найден. Убедитесь, что он добавлен в PATH.")

def main():
    # запрашиваем у пользователя промпт для тега
    user_prompt = forms.ask_for_string(
        prompt='введите промпт для тега (например, поставить тег справа от элементов)',
        title='tag_gpt: запрос промпта'
    )
    if not user_prompt:
        forms.alert('нет введенного промпта', exitscript=True)
    
    # webhook url with llm
    webhook_url = 'https://back.n3ur0.space/webhook-test/gen'  
    
    payload = {'prompt': user_prompt}
    try:
        response = requests.post(webhook_url, json=payload, timeout=3000, verify=False)
        response.raise_for_status()
    except Exception as e:
        forms.alert('ошибка при отправке промпта: {}'.format(e), exitscript=True)
    
    try:
        data = response.json()
    except Exception as e:
        forms.alert('ошибка при обработке ответа: {}'.format(e), exitscript=True)
    
    generated_code = data.get('output')
    if not generated_code:
        forms.alert('код не получен от llm', exitscript=True)
    
    folder_name = forms.ask_for_string(
        prompt='введите название кнопки',
        title='Название кнопки'
        )
    folder_name = folder_name.replace(' ', '_') + ".panel"
    write_string_to_file_and_open(generated_code, folder_name)
    
if __name__ == '__main__':
    main()
