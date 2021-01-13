import os
import pickle  # Модуль для сериализации данных
try:
	from prettytable import PrettyTable  # Модуль для красивого вывода контактов
except:
	print("Сначала запустите setup.bat")
	read()
	exit()


# проверка строки на пустоту
def is_empty(prop):
    while True:
        if not prop:
            print('Поле не может быть пустым')
            prop = input('Введите валидные данные: ')
        else:
            break


# класс, отвечающий за действия внутри одного контакта
class Contact:

    # Инициализация инстанции класса ( конструктор )
    def __init__(self, name, last_name, email, number, /):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.number = number

    # Функции относящиеся к изменению данных внутри самого контакта
    def rename(self):
        self.name = input(f'Введите новое имя контакту. Текущее - {self.name}: ')
        is_empty(self.name)
        while True:
            if not self.name.isalpha():
                print('Имя не должно содержать специальных символов, пробелов или цифр')
                self.name = input('Введите валидные данные: ')
            else:
                break
        self.last_name = input(f'Введите новую фамилию контакту. Текущяя - {self.last_name}: ')
        is_empty(self.last_name)
        while True:
            if not self.last_name.isalpha():
                print('Фамилия не должна содержать специальных символов, пробелов или цифр')
                self.last_name = input('Введите валидные данные: ')
            else:
                break

    def change_mail(self):
        self.email = input(f'Введите новую почту для контакта. Текущая - {self.email}: ')
        is_empty(self.email)
        while True:
            if '@' not in self.email:
                print('Почта должна содержать в себе символ собаки')
                self.email = input('Введите правильную почту: ')
            else:
                break

    def change_number(self):
        self.number = input(f'Введите новый номер для контакта. Текущий - {self.number}: ')
        is_empty(self.number)
        while True:
            if not self.number.isdecimal():
                print('Номер должен состоять только из цифр')
                self.number = input('Введите корректный номер: ')
            else:
                break


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
        if not len(self) > 0:
            print('В вашем списке еще нет контактов. Для начала создайте парочку.')
        else:
            th = ['Имя', 'Фамилия', 'Номер', 'Почта']  # инициализация столбцов
            table = PrettyTable(th)  # создание таблицы
            # добавление данных в таблицу и вывод
            for contact in self:
                table.add_row([contact.name, contact.last_name, contact.number, contact.email])
            print(table)

    # добавление контакта в список с последующим сохранением в файл
    def add(self):
        # проверки на валидность введенных данных
        name = input('Введите имя контакта: ')
        is_empty(name)
        while True:
            if not name.isalpha():
                print('Имя не должно содержать специальных символов, пробелов или цифр')
                name = input('Введите валидные данные: ')
            else:
                break
        last_name = input('Введите фамилию контакта: ')
        is_empty(last_name)
        while True:
            if not last_name.isalpha():
                print('Фамилия не должна содержать специальных символов, пробелов или цифр')
                last_name = input('Введите валидные данные: ')
            else:
                break
        email = input('Введите почту контакта: ')
        is_empty(email)
        while True:
            if '@' not in email:
                print('Почта должна содержать в себе символ собаки')
                email = input('Введите правильную почту: ')
            else:
                break
        number = input('Введите номер контакта: ')
        is_empty(number)
        while True:
            if not number.isdecimal():
                print('Номер должен состоять только из цифр')
                number = input('Введите корректный номер: ')
            else:
                break
        new_contact = Contact(name, last_name, email, number)
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

    # вы выбираете контакт и можете совершать с ним различные манипуляции ( переименовать, сменить номер или сменить почту)
    def select_contact(self):
        print('Choose contact to act with it')
        if not len(self) > 0:
            print('В вашем списке еще нет контактов. Для начала создайте парочку.')
        else:
            i = 1
            for contact in self:
                print(f'{i} - {contact.name}')
                i += 1
            selected_contact = self[int(input('Введите индекс контакта ( указан перед именем ): ')) - 1]
            print(f'Выбран контакт {selected_contact.name}')
            while True:
                action = input('Введите номер действия, которое вы хотите совершить с контактом: \n'
                               '1 - Переименовать\n'
                               '2 - Сменить почту\n'
                               '3 - Сменить номер\n'
                               '4 - Назад\n==> ')
                if action == '4':
                    break
                elif action == '1':
                    selected_contact.rename()
                    self.save()
                elif action == '2':
                    selected_contact.change_mail()
                    self.save()
                elif action == '3':
                    selected_contact.change_number()
                    self.save()
                else:
                    print('Нет такой команды. Попробуйте снова или вернитесь назад введя "4"')


# создаем инстанцию класса методом выгрузки данных из файла, если данных нет, создается пустой массив контактов
contacts = Contacts.load()

# словарь команд для упрощения дальнейшей работы с ними. Ключ - команда, значение - функция, которую она выполняет
commands = {
    'help': lambda: print('Чтобы воспользоваться командой введите ее порядковый номер\n1.Показать '
                          'контакты\n2.Добавить контакт\n3.Удалить контакт\n4.Выбрать контакт\nЧтобы завершить '
                          'сессию напишите "end"'),
    '1': contacts.show_contacts,
    '2': contacts.add,
    '3': contacts.del_contact,
    '4': contacts.select_contact
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
