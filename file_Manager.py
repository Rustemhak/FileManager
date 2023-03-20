import os
import shutil
from tabulate import tabulate
from distutils.dir_util import copy_tree


class FileManager:
    def __init__(self):
        self.root_directory = "D:/"
        self.display_data = []
        self.allowed_files = self.list_directory()[1]  # Объекты в разрешенной для изменения директории
        self.types_files = []

    def move_between_directories(self):  # Перемещение по разрешенным директориям
        chosen_directory = int(input('Введите ID директории чтобы переместиться: '))
        location = self.id_choice(chosen_directory)
        if location:
            self.root_directory += f'/{location}'
            self.refresh_directory()

    def move_up(self):  # Подняться вверх по директории
        location = self.root_directory.split('/')
        location.pop()
        up = '/'.join(location)
        if len(location) == 0:
            print('Нельзя подняться ещё выше')
        else:
            self.root_directory = up
            self.refresh_directory()

    def copy_files(self):
        start_id = int(input('ID директории/ID файла из который производится копирование: '))
        print(self.allowed_files[start_id])

        start_directory = f"{self.root_directory}/{self.id_choice(start_id)}"
        end_id = int(input('ID директории чтобы скопировать в неё: '))
        end_directory = f"{self.root_directory}/{self.id_choice(end_id)}"
        try:
            if self.types_files[start_id] == 'Directory':
                copy_tree(start_directory, end_directory)
            elif self.types_files[start_id] == 'File':
                shutil.copy(start_directory, end_directory)

        except OSError as e:
            print(f'Error: {e.filename} - {e.strerror}')
        except IndexError as e:
            print(f'Сначала нужно посмотреть на список файлов')
        else:
            print('Успешное копирование')

    def refresh_directory(self):
        self.allowed_files = self.list_directory()[1]

    def list_directory(self):
        self.display_data = []
        files = os.scandir(path=self.root_directory)
        file_id = 1
        for each in files:
            object_data = f' - Directory - {each.name} - {file_id}' if each.is_dir() else f' - File - {each.name} -' \
                                                                                          f' {file_id}'
            object_info = object_data.split(' - ')
            object_info.pop(0)
            self.display_data.append(object_info)
            file_id += 1
        self.types_files = [i[0] for i in self.display_data]
        data = tabulate((i for i in self.display_data), headers=['Type', 'Name', 'ID'], tablefmt='pipe',
                        stralign='center')
        return data, self.display_data

    def id_choice(self, object_id):
        ids = [i[2] for i in self.allowed_files]
        names = [i[1] for i in self.allowed_files]
        if str(object_id) in ids:
            return names[object_id - 1]
        else:
            print('Указанный ID не найден, укажите ID из списка')

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
