import os
import shutil
from tabulate import tabulate
from distutils.dir_util import copy_tree


class FileManager:
    def __init__(self):
        self.root_directory = r"D:\test_files"
        self.display_data = []
        self.allowed_files = self.list_directory()[1]  # Объекты в разрешенной для изменения директории

    def create_directory(self):
        directory_name = str(input("Название новой директории: "))
        if not os.path.exists(f'{self.root_directory}/{directory_name}'):
            os.makedirs(f'{self.root_directory}/{directory_name}')
            print(f'Директория "{directory_name}" успешно создана')
            self.refresh_directory()
        else:
            print("Директория уже существует")

    def create_file(self):
        file_name = str(input("Имя файла: "))
        if not os.path.exists(f'{self.root_directory}/{file_name}'):
            new_file = open(f"{self.root_directory}/{file_name}", "w")
            # new_file.write(str(input('Введите текст для записи в файл: ')))
            new_file.close()
            print(f'Файл "{file_name}" успешно создан')
            self.refresh_directory()
        else:
            print('Файл с таким названием уже существует')

    def overwrite_file(self):
        file_id = int(input('Введите ID файла для записи: '))
        location = self.id_choice(file_id)
        try:
            with open(f'{self.root_directory}/{location}', mode='w') as f:
                f.write(str(input('Введите текст для записи в файл: ')))
        except FileNotFoundError:
            print(f'Файл с  ID = "{file_id}" не найден')
        except IsADirectoryError:
            print('Это директория')
        else:
            print('Текст успешно записан в файл')

    def read_file(self):
        file_id = int(input('Введите ID файла чтобы прочитать: '))
        file_name = self.id_choice(file_id)
        try:
            file_location = f"{self.root_directory}/{file_name}"
            with open(file_location, "r") as f:
                text = f.read()
            for line in text.splitlines():
                print(line)
        except FileNotFoundError:
            print(f'Файл с ID = "{file_id}" не найден')

    def delete_file(self):
        file_id = int(input('Введите ID файла чтобы удалить'))
        file_name = self.id_choice(file_id)
        try:
            os.remove(f"{self.root_directory}/{file_name}")
        except OSError as e:
            print(f'Error: {e.filename} - {e.strerror}')
        else:
            print(f'Файл "{file_name}" успешно удалён')
            self.refresh_directory()

    def move_between_directories(self):  # Перемещение по разрешенным директориям
        chosen_directory = int(input('Введите ID директории чтобы переместиться: '))
        location = self.id_choice(chosen_directory)
        self.root_directory += f'/{location}'
        self.refresh_directory()

    def move_up(self):  # Подняться вверх по директории
        location = self.root_directory.split('\\')
        location.pop()
        up = '\\'.join(location)
        self.root_directory = up
        self.refresh_directory()

    def rename_file(self):
        file_id = int(input('Введите ID файла, чтобы переименовать: '))
        file_to_rename = f"{self.root_directory}/{self.id_choice(file_id)}"
        new_name = str(input('Введите новое название файла: '))
        try:
            os.rename(file_to_rename, f'{self.root_directory}/{new_name}')
        except OSError as e:
            print(f'Error: {e.filename} - {e.strerror}')
        else:
            print('Успешное переименование')
            self.refresh_directory()

    def copy_files(self):
        start_id = int(input('ID директории из который производится копирование: '))
        start_directory = f"{self.root_directory}/{self.id_choice(start_id)}"
        end_id = int(input('ID директории чтобы скопировать в неё: '))
        end_directory = f"{self.root_directory}/{self.id_choice(end_id)}"
        try:
            copy_tree(start_directory, end_directory)
        except OSError as e:
            print(f'Error: {e.filename} - {e.strerror}')
        else:
            print('Успешное копирование')

    def move_files(self):
        self.list_directory()
        start_id = int(input('ID Файла для перемещения: '))
        start_location = f"{self.root_directory}/{self.id_choice(start_id)}"
        end_id = int(input('ID директории куда переместить: '))
        end_directory = f"{self.root_directory}/{self.id_choice(end_id)}"
        try:
            shutil.move(start_location, end_directory)
        except OSError as e:
            print(f'Error: {e.filename} - {e.strerror}')
        else:
            print('Успешное перемещение')

    def refresh_directory(self):
        self.allowed_files = self.list_directory()[1]

    def list_directory(self):
        self.display_data = []
        files = os.scandir(path=self.root_directory)
        file_id = 1
        for each in files:
            object_data = f' - Directory - {each.name} - {file_id}' if each.is_dir() else f' - File - {each.name} - {file_id}'
            object_info = object_data.split(' - ')
            object_info.pop(0)
            self.display_data.append(object_info)
            file_id += 1
        data = tabulate((i for i in self.display_data), headers=['Type', 'Name', 'ID'], tablefmt='pipe',
                        stralign='center')
        return data, self.display_data

    def id_choice(self, object_id):
        ids = [i[2] for i in self.allowed_files]
        names = [i[1] for i in self.allowed_files]
        if str(object_id) in ids:
            return names[object_id - 1]

    def CLI(self):
        print('-----------Файловый менеджер-----------\n')
        commands = [['1', 'Просмотр директории'],
                    ['2', 'Переход в директорию'],
                    ['3', 'Подняться вверх по директории'],
                    ['4', 'Копирование из папки в папку']]
        # ['10', 'Перемещение файлов'], ['11', 'Переименовать файл']]
        help_page = tabulate((i for i in commands), headers=['ID', 'Метод'], tablefmt='github', stralign='center')
        print(help_page)
        while True:
            choose = str(input(
                '\nhelp - список команд, exit - выйти из файлового менеджера\nВведите ID команды чтобы продолжить: '))
            print('\n')
            if choose == '1':
                print(self.list_directory()[0])
            # if choose == '2':
            #     self.create_directory()
            # if choose == '3':
            #     self.delete_directory()
            elif choose == '2':
                self.move_between_directories()
            # if choose == '5':
            #     self.create_file()
            # if choose == '6':
            #     self.overwrite_file()
            # if choose == '7':
            #     self.read_file()
            # if choose == '8':
            #     self.delete_file()
            elif choose == '3':
                self.move_up()
            elif choose == '4':
                self.copy_files()
            # if choose == '10':
            #     self.move_files()
            # if choose == '11':
            #     self.rename_file()
            elif choose.lower() == 'help':
                print(f'\n{help_page}')
            elif choose.lower() == 'exit':
                exit()
            else:
                print('Неверная команда, введите команду из списка выше')


def main():
    manager = FileManager()
    manager.CLI()


if __name__ == '__main__':
    main()
