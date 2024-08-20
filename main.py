import json
import re
print("yi")

def open_contact():
    """Функция показа контактов в справочнике"""
    with open('Guide.json', 'r', encoding='utf-8') as file:
        obj_json = json.load(file)  # Десерилизует из файла json в объект
        if len(obj_json["Contacts"]) > 0:
            print("Контакты:")
            for elem_contact in obj_json["Contacts"]:
                print(f"id: {elem_contact['id']},"
                      f" Имя: {elem_contact['name']},"
                      f" Номер: {elem_contact['phone']},"
                      f" Комментарий: {elem_contact['comment']}")
        else:
            print("Справочник пустой")
    return exit_from_guide()


def create_contact():
    """Функция создания контакта в справочнике"""
    name = input("Задайте имя контакта: ")
    phone = input("Задайте телефон контакта: +")
    comment = input("Добавьте комментарий к контакту: ")
    flag_save_contact = False  # Флаг выхода из цикла

    while not flag_save_contact:
        save_contact = input("Сохранить контакт (да/нет): ")

        if save_contact.isalpha() and save_contact == "да" or save_contact == "нет":
            if save_contact == "да":
                with open('Guide.json', 'r', encoding='utf-8') as file:  # Считывает данные из файла
                    obj_json = json.load(file)  # Десерилизует из файла json в объект
                    if len(obj_json["Contacts"]) != 0:  # Если данные в справочнике есть, то
                        obj_json["Contacts"].reverse()  # Делает реверс списку, чтобы получить последний id
                        id_contact = obj_json["Contacts"][0]["id"] + 1
                    else:
                        id_contact = 1  # Если контактов в справочнике нет, то id объекта = 1

                with open('Guide.json', 'w', encoding='utf-8') as file:  # Записывает данные в файл
                    contact = {"id": id_contact,
                               "name": name,
                               "phone": phone,
                               "comment": comment}  # Контакты объекта в формате словаря
                    obj_json["Contacts"].reverse()  # Делает реверс списку, чтобы вернуть его в первоначальное положение
                    obj_json["Contacts"].append(contact)  # Добавляются контакты в список
                    (json.dump(obj_json, file, ensure_ascii=False))  # Серилизуются и записываются в файл
                print("Данные успешно записаны в справочник.")
            else:
                print("Сохранение контакта отменено.")
            flag_save_contact = True
        else:
            print("Введите актуальное значение:")

    return exit_from_guide()


def search_contact(search_criteria):
    """Функция поиска контактов по всем параметрам"""
    continue_search = None  # Флаг выхода из цикла
    search_word = input("введите данные для поиска: ")

    with open('Guide.json', 'r', encoding='utf-8') as file:  # Считывает данные из файла
        obj_json = json.load(file)  # Десерилизует из файла json в объект
        while continue_search != "нет":
            flag_result_search = False  # Флаг, показывает нашлись ли результаты

            # Проходится циклом по всей коллекции
            for elem_contact in obj_json["Contacts"]:
                # Если аргумент фукнции all, то ищет по всем данным
                if search_criteria == "all":
                    id_search = re.findall(fr'{search_word.lower()}.*', str(elem_contact['id']).lower())
                    name_search = re.findall(fr'{search_word.lower()}.*', elem_contact['name'].lower())
                    phone_search = re.findall(fr'{search_word.lower()}.*', elem_contact['phone'].lower())
                    comment_search = re.findall(fr'{search_word.lower()}.*', elem_contact['comment'].lower())

                    # Если нашел, то показывает все найденные данные
                    if len(id_search) != 0 or len(name_search) != 0 or len(phone_search) != 0 or len(comment_search) != 0:
                        print(f"id: {elem_contact['id']},"
                              f" Имя: {elem_contact['name']},"
                              f" Номер: {elem_contact['phone']},"
                              f" Комментарий: {elem_contact['comment']}")
                        flag_result_search = True
                # Если аргумент фукнции name, то ищет только по имени
                else:
                    name_search = re.findall(fr'{search_word.lower()}.*', elem_contact['name'].lower())

                    # Если нашел, то показывает все найденные данные
                    if len(name_search) != 0:
                        print(f"id: {elem_contact['id']},"
                              f" Имя: {elem_contact['name']},"
                              f" Номер: {elem_contact['phone']},"
                              f" Комментарий: {elem_contact['comment']}")
                        flag_result_search = True

            if not flag_result_search:
                print("Таких данных в справочнике нет.")

            continue_search = input("Продолжить поиск? (да/нет) ")

            if continue_search.isalpha() and continue_search == "да":
                search_word = input("введите данные для поиска: ")
            elif continue_search.isalpha() and continue_search == "нет":
                continue_search = "нет"
            else:
                while continue_search != "да" and continue_search != "нет":
                    print("Введите актуальные данные.")
                    continue_search = input("Продолжить поиск? (да/нет) ")
                if continue_search == "да":
                    search_word = input("введите данные для поиска: ")

    return exit_from_guide()


def change_contact():
    """Функция изменения контактов в справочнике"""
    # 1. Показывает все контакты
    with open('Guide.json', 'r', encoding='utf-8') as file:
        obj_json = json.load(file)
        if len(obj_json["Contacts"]) > 0:
            print("Контакты:")
            for elem_contact in obj_json["Contacts"]:
                print(f"id: {elem_contact['id']},"
                      f" Имя: {elem_contact['name']},"
                      f" Номер: {elem_contact['phone']},"
                      f" Комментарий: {elem_contact['comment']}")  # Десерилизует из файла json в объект)
        else:
            print("Справочник пустой")

    # 2. Запрашивает id контакта, который надо изменить
    remove_contact = input("\nВведите id контакта, который вы хотите изменить: ")
    id_contact = -1  # Содержит id контакта, который надо удалить

    # 3. Получает позицию нужного элемента в коллекции
    while True:
        if remove_contact.isdigit():
            for id_loop in range(len(obj_json["Contacts"])):
                if obj_json["Contacts"][id_loop]['id'] == int(remove_contact):
                    id_contact = id_loop
                    break

            if 0 <= id_contact <= len(obj_json["Contacts"]):
                break
            else:
                print("Не актуальные данные.")
                remove_contact = input("Введите id контакта, который вы хотите изменить: ")

        else:
            print("Не актуальные данные.")
            remove_contact = input("Введите id контакта, который вы хотите изменить: ")

    # 4. Получает где необходимо изменить данные и меняет их в коллекции
    while True:
        select_change = input("\nВыберите где внести изменения:\n"
                              "Имя - 1\n"
                              "Телефон - 2\n"
                              "Комментарий - 3\n")
        if select_change.isdigit() and select_change == "1":
            name_change = input("Введите желаемое имя: ")
            obj_json["Contacts"][id_contact]["name"] = name_change
            break
        elif select_change.isdigit() and select_change == "2":
            phone_change = input("Введите желаемый телефон: +")
            obj_json["Contacts"][id_contact]["phone"] = phone_change
            break
        elif select_change.isdigit() and select_change == "3":
            coment_change = input("Введите желаемый комментарий: ")
            obj_json["Contacts"][id_contact]["comment"] = coment_change
            break
        else:
            print("\nВведите актуальные данные.")

    # 5. Сохраняет данные в документе
    flag_save_change = False

    while not flag_save_change:
        save_change = input("Сохранить изменения (да/нет) : ")

        if save_change.isalpha() and save_change == "да" or save_change == "нет":
            if save_change == "да":
                with open('Guide.json', 'w', encoding='utf-8') as file:  # Записывает данные в файл
                    (json.dump(obj_json, file, ensure_ascii=False))  # Серилизуются и записываются в файл
                print("Данные успешно изменены в справочнике.")
            else:
                print("Изменение в контакте отменено.")
            flag_save_change = True
        else:
            print("Введите актуальное значение:")

    return exit_from_guide()


def del_contact():
    """Функция удаления контакта в справочнике"""
    # 1. Показывает все контакты
    with open('Guide.json', 'r', encoding='utf-8') as file:
        obj_json = json.load(file)  # Десерилизует из файла json в объект
        print("Контакты:")
        for elem_contact in obj_json["Contacts"]:
            print(f"id: {elem_contact['id']},"
                  f" Имя: {elem_contact['name']},"
                  f" Номер: {elem_contact['phone']},"
                  f" Комментарий: {elem_contact['comment']}")

        # 2. Запрашивает id контакта, который надо удалить
        remove_contact = input("\nВведите id контакта, который вы хотите удалить (0 - отменить удаление): ")

        if remove_contact == "0":
            return exit_from_guide()

        id_contact = -1  # Содержит id контакта, который надо удалить

        # 3. Получает позицию нужного элемента в коллекции
        while True:
            if remove_contact.isdigit() and remove_contact != "0":
                for id_loop in range(len(obj_json["Contacts"])):
                    if obj_json["Contacts"][id_loop]['id'] == int(remove_contact):
                        id_contact = id_loop
                        break

                # 4. Удаляет элемент из коллекции
                if 0 <= id_contact <= len(obj_json["Contacts"]):
                    if id_contact < len(obj_json["Contacts"]):
                        del obj_json["Contacts"][id_contact]
                    else:
                        del obj_json["Contacts"][id_contact - 1]
                    break
                else:
                    print("Не актуальные данные.")
                    remove_contact = input("Введите id контакта, который вы хотите удалить (0 - отменить удаление): ")
            elif remove_contact.isdigit() and remove_contact == "0":
                return exit_from_guide()
            else:
                print("Не актуальные данные.")
                remove_contact = input("Введите id контакта, который вы хотите удалить (0 - отменить удаление): ")

    with open('Guide.json', 'w', encoding='utf-8') as file:  # Записывает данные в файл
        json.dump(obj_json, file, ensure_ascii=False)  # Серилизуются и записываются в файл
        print("Контакт успешно удален.")

    return exit_from_guide()


def exit_from_guide():
    """Функция выхода в главное меню или полностью из справочника"""
    exit_menu = input("\nВыйти в главное меню - 1\n"
                      "Выйти из справочника - 2\n")

    while True:
        if exit_menu.isdigit() and 1 <= int(exit_menu) <= 2:
            if exit_menu == "1":
                return input("Нажмите цифру желаемого действия:\n"
                             "Показать контакты - 1\n"
                             "Создать контакт - 2\n"
                             "Найти контакт - 3\n"
                             "Изменить контакт - 4\n"
                             "Удалить контакт - 5\n"
                             "Выход - 6\n")
            else:
                print("До встречи!")
                return True
        else:
            print("Введите актуальное значение:")
            exit_menu = input("\nВыйти в главное меню - 1\n"
                              "Выйти из справочника - 2\n")


work_to_phone_guide = input("Открыть справочник (да/нет) ")

if work_to_phone_guide == "да":

    menu = input("Нажмите цифру желаемого действия:\n"
                 "Показать контакты - 1\n"
                 "Создать контакт - 2\n"
                 "Найти контакт - 3\n"
                 "Изменить контакт - 4\n"
                 "Удалить контакт - 5\n"
                 "Выход - 6\n")

    close_from_phone_guide = False  # Флаг выхода из цикла while
    data = None  # Содержит значение одной из функции

    while not close_from_phone_guide:

        if menu.isdigit() and 1 <= int(menu) <= 6:

            if menu == "1":
                data = open_contact()  # Функция показа контактов
            elif menu == "2":
                data = create_contact()  # Создать контакт
            elif menu == "3":
                while True:
                    select_search = input("Выберите желаемый поиск:\n"
                                          "По всем параметрам - 1\n"
                                          "По имени - 2\n")
                    if select_search.isdigit() and select_search == "1":
                        data = search_contact(search_criteria="all")  # Поиск контакта
                        break
                    elif select_search.isdigit() and select_search == "2":
                        data = search_contact(search_criteria="name")  # Поиск контакта
                        break
                    else:
                        print("Введите актуальные данные.")
            elif menu == "4":
                data = change_contact()
            elif menu == "5":
                data = del_contact()
            elif menu == "6":
                close_from_phone_guide = True
                print("До встречи!")

            if isinstance(data, str):  # Если фукция типа str, то присваеваем menu значение данной функции
                menu = data
            else:
                close_from_phone_guide = True  # Если bool, то значит пользователь запросил выход из справочника
        else:
            print("Введите актуальное значение:")
            print()
            menu = input("Нажмите цифру желаемого действия:\n"
                         "Показать контакты - 1\n"
                         "Создать контакт - 2\n"
                         "Найти контакт - 3\n"
                         "Изменить контакт - 4\n"
                         "Удалить контакт - 5\n"
                         "Выход - 6\n")

elif work_to_phone_guide == "нет":
    print("До встречи!")
else:
    print("Вы ввели не актуальные данные, до встречи!")
