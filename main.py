import os
import pickle
from prettytable import PrettyTable


class Contact:

    def __init__(self, name, email, number, /):
        self.name = name
        self.email = email
        self.number = number
        self.fullcontact = f'{self.name} {self.number} {self.email}'

    def rename(self):
        self.name = input(f'Введите новое имя контакту {self.name}: ')

    def change_mail(self):
        self.email = self.email = input(f'Введите новую почту для контакта {self.name}: ')

    def change_number(self):
        self.number = input(f'Введите новый номер для контакта {self.name}: ')


class Contacts(list):

    def save(self):
        with open('./contacts', 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load():
        if os.path.getsize('./contacts') > 0:
            with open('./contacts', 'rb') as f:
                return pickle.load(f)
        else:
            return Contacts()

    def show_contacts(self):
        th = ['Имя', 'Номер', 'Почта']
        table = PrettyTable(th)
        for contact in self:
            table.add_row([contact.name, contact.number, contact.email])
        print(table)
        # for contact in self:
        #     contact.show()

    def add(self):
        name = input('Введите имя контакта: ') or '-'
        email = input('Введите почту контакта: ') or '-'
        number = input('Введите номер контакта: ') or '-'
        new_contact = Contact(name, email, number)
        self.append(new_contact)
        self.save()

    def del_contact(self):
        name = input('Введите имя контакта, который хотите удалить: ')
        removed = False
        for contact in self:
            if contact.name == name:
                removed = True
                self.remove(contact)
                print(f'Контакт с именем {name} успешно удален!')
                self.save()
        if not removed:
            print('Контакта с таким именем не найдено')

    def contacts_rename(self):
        contact_name = input('Введите имя контакта, который хотите переименовать: ')
        renamed = False
        for contact in self:
            if contact.name == contact_name:
                renamed = True
                contact.rename()
        if not renamed:
            print('Нет контакта с таким именем. Попробуйте снова')

    def contacts_change_number(self):
        contact_name = input('Введите имя контакта, у которого хотите изменить номер: ')
        number_changed = False
        for contact in self:
            if contact.name == contact_name:
                number_changed = True
                contact.change_number()
        if not number_changed:
            print('Нет контакта с таким именем. Попробуйте снова')

    def contacts_change_mail(self):
        contact_name = input('Введите имя контакта, у которого хотите изменить почту: ')
        mail_changed = False
        for contact in self:
            if contact.name == contact_name:
                mail_changed = True
                contact.change_mail()
        if not mail_changed:
            print('Нет контакта с таким именем. Попробуйте снова')


contacts = Contacts.load()
commands = {
    'help': lambda: print('Чтобы воспользоваться коммандой введите ее порядковый номер\n1.Показать '
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


while True:
    command = input('Введите комманду: ')
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
        print('Введите "help" чтобы узнать комманды или "end", чтобы завершить сеанс', end='\n')

