import os
import pickle  # Модуль для сериализации данных
from prettytable import PrettyTable  # Модуль для красивого вывода контактов


# класс, отвечающий за действия внутри одного контакта
class Contact:

    # Инициализация инстанции класса ( конструктор )
    def __init__(self, name, email, number, /):
        self.name = name
        self.email = email
        self.number = number

    # Функции относящиеся к изменению данных внутри самого контакта
    def rename(self): self.name = input(f'Введите новое имя контакту {self.name}: ')

    def change_mail(self): self.email = input(f'Введите новую почту для контакта {self.name}: ')

    def change_number(self): self.number = input(f'Введите новый номер для контакта {self.name}: ')


# класс, отвечающий за действия со списком контактов
class Contacts(list):

    # сохранение контактов в файл с помощью модуля pickle и его метода dump()
    def save(self):
        with open('./contacts', 'wb') as f:
            pickle.dump(self, f)

    # восстановление объекта из файла статичным методом используя pickle.load()
    @staticmethod
    def load():
        if os.path.getsize('./contacts') > 0:  # проверяем не пустой ли файл
            with open('./contacts', 'rb') as f:
                return pickle.load(f)
        else:
            return Contacts()

    # вывод контактов в виде таблицы с помощью модуля prettytable
    def show_contacts(self):
        th = ['Имя', 'Номер', 'Почта']  # инициализация столбцов
        table = PrettyTable(th)  # создание таблицы
        # добавление данных в таблицу и вывод
        for contact in self:
            table.add_row([contact.name, contact.number, contact.email])
        print(table)

    # добавление контакта в список с последующим сохранением в файл
    def add(self):
        # если имя, почта или номер не введены, пустая строка заменяется на '-' ( прочерк )
        name = input('Введите имя контакта: ') or '-'
        email = input('Введите почту контакта: ') or '-'
        number = input('Введите номер контакта: ') or '-'
        new_contact = Contact(name, email, number)
        # self в данном случае типа list, так как мы от него наследуемся, поэтому он может использовать методы списка здесь и далее
        self.append(new_contact)
        self.save()

    # удаление контакта из списка
    def del_contact(self):
        name = input('Введите имя контакта, который хотите удалить: ')
        # переменная removed нужна для того, чтобы проверить, удален ли хотя бы один контакт, если нет выдает ошибку
        removed = False
        for contact in self:
            if contact.name == name:
                removed = True
                self.remove(contact)
                print(f'Контакт с именем {name} успешно удален!')
                self.save()
        if not removed:
            print('Контакта с таким именем не найдено')

    # переименование контакта: ищет в списке контакт с данным именем и вызывает у объекта подходящего контакта метод rename
    def contacts_rename(self):
        contact_name = input('Введите имя контакта, который хотите переименовать: ')
        renamed = False
        for contact in self:
            if contact.name == contact_name:
                renamed = True
                contact.rename()
        if not renamed:
            print('Нет контакта с таким именем. Попробуйте снова')

    # смена номера у контакта
    def contacts_change_number(self):
        contact_name = input('Введите имя контакта, у которого хотите изменить номер: ')
        number_changed = False
        for contact in self:
            if contact.name == contact_name:
                number_changed = True
                contact.change_number()
        if not number_changed:
            print('Нет контакта с таким именем. Попробуйте снова')

    # смена почты у контакта, аналогично предыдущим двум методам
    def contacts_change_mail(self):
        contact_name = input('Введите имя контакта, у которого хотите изменить почту: ')
        mail_changed = False
        for contact in self:
            if contact.name == contact_name:
                mail_changed = True
                contact.change_mail()
        if not mail_changed:
            print('Нет контакта с таким именем. Попробуйте снова')


# создаем инстанцию класса методом выгрузки данных из файла, если данных нет, создается пустой массив контактов
contacts = Contacts.load()

# словарь команд для упрощения дальнейшей работы с ними. Ключ - команда, значение - функция, которую она выполняет
commands = {
    'help': lambda: print('Чтобы воспользоваться командой введите ее порядковый номер\n1.Показать '
                          'контакты\n2.Добавить контакт\n3.Удалить контакт\n4.Переименовать контакт\n5.Изменить номер '
                          'у контакта\n6.Изменить почту у контакта\nЧтобы завершить '
                          'сессию напишите "end"'),
    '1': contacts.show_contacts,
    '2': contacts.add,
    '3': contacts.del_contact,
    '4': contacts.contacts_rename,
    '5': contacts.contacts_change_number,
    '6': contacts.contacts_change_mail
}

# первичное ознакомление пользователя с командами
commands['help']()

# сессия пользователя в виде бесконечного цикла до тех пор, пока не введена команда "end"
while True:
    command = input('Введите команду: ')
    if command in commands.keys():
        commands[command]()
    elif command == 'end':
        print('BB')
        saveChanges = input('Сохранить изменения? y/n\n==> ')
        if saveChanges.lower() == 'y' or saveChanges.lower() == 'да':
            contacts.save()
            print('Изменения успешно сохранены! До новых встреч!')
        break
    else:
        print('Введите "help" чтобы узнать команды или "end", чтобы завершить сеанс', end='\n')
