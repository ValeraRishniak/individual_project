import os
from pathlib import Path
import re
import shutil

_images = [] 
_video = []
_documents = []
_audio = []
_archives = []
_other = [] 
known_suffix_list = []
unknown_suffix_list = []
dict_for_return = { "images": _images,
                    "video": _video,
                    "documents": _documents,
                    "audio": _audio,
                    "archives": _archives,
                    "other": _other,
                    "known_suffix": known_suffix_list,
                    "unknown_suffix": unknown_suffix_list
                    }


def normalize(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    t_name = name.translate(TRANS)
    norm_name = re.sub(r'\W', '_', t_name)
    return norm_name

#функція в себе приймає шлях до теки яку потрібно відсортувати (some_input = r'C:\Users\Hewlett Packard\Desktop\Xlam')  
def sort(some_input):
    way_ = Path(some_input) # шлях в якому здійснюється видалення пустих папок
#нормалізація імені
    for root, dirs, files in os.walk(way_, topdown=False):
        for name_ in files:
                files_name = Path(name_) #имя файла (назва.розширення)
                file_path_ = os.path.join(root, name_) #путь к файлу/архиву/тп (для переміщення/перейменування/розархівування)
                #тут робимо зміну назви файла
                name_normalize = f"{normalize(files_name.name[0:-len(files_name.suffix)])}{files_name.suffix}"
                os.rename(file_path_, way_/name_normalize) #процес перейменування (шлях до файла що перейменовуєм, новий шлях де він буде)
#видалення пустих тек
    for root, dirs, files in os.walk(way_, topdown=False):
        for name in dirs:
            if len(os.listdir(os.path.join(root, name))) == 0:
                    os.rmdir(os.path.join(root, name))
#сортування та обробка
    for root, dirs, files in os.walk(way_, topdown=False):
        for name_ in files:
            files_name = Path(name_) #имя файла (назва.розширення)
            file_path_ = os.path.join(root, name_) #путь к файлу/архиву/тп (для переміщення/перейменування/розархівування)

            if files_name.suffix.lower() == '.jpg' or files_name.suffix.lower() == '.jpeg' or files_name.suffix.lower() == '.png' or files_name.suffix.lower() == '.svg':
                _images.append(files_name)
                known_suffix_list.append(files_name.suffix)
                dir_to_create = Path(way_) / 'images'
                dir_to_create.mkdir(exist_ok=True)
                shutil.move(file_path_, dir_to_create / files_name)

            elif files_name.suffix.lower() == '.avi' or files_name.suffix.lower() == '.mp4' or files_name.suffix.lower() == '.mov' or files_name.suffix.lower() == '.mkv':
                _video.append(files_name)
                known_suffix_list.append(files_name.suffix)
                dir_to_create = Path(way_) / 'video'
                dir_to_create.mkdir(exist_ok=True)
                shutil.move(file_path_, dir_to_create / files_name)

            elif files_name.suffix.lower() == '.doc' or files_name.suffix.lower() == '.docx' or files_name.suffix.lower() == '.txt' or files_name.suffix.lower() == '.pdf' or files_name.suffix.lower() == '.xlsx' or files_name.suffix.lower() == '.xls' or files_name.suffix.lower() == '.pptx':
                _documents.append(files_name)
                known_suffix_list.append(files_name.suffix)
                dir_to_create = Path(way_) / 'documents'
                dir_to_create.mkdir(exist_ok=True)
                shutil.move(file_path_, dir_to_create / files_name)

            elif files_name.suffix.lower() == '.mp3' or files_name.suffix.lower() == '.ogg' or files_name.suffix.lower() == '.wav' or files_name.suffix.lower() == '.amr':
                _audio.append(files_name)
                known_suffix_list.append(files_name.suffix)
                dir_to_create = Path(way_) / 'audio'
                dir_to_create.mkdir(exist_ok=True)
                shutil.move(file_path_, dir_to_create / files_name)

            elif files_name.suffix.lower() == '.zip' or files_name.suffix.lower() == '.gz' or files_name.suffix.lower() == '.tar':
                _archives.append(files_name)
                known_suffix_list.append(files_name.suffix)
                dir_to_create = Path(way_) / 'archives' # задаємо ім'я майбутньої папки
                dir_to_create.mkdir(exist_ok=True)       # створємо нову папку по суфіксу
                shutil.unpack_archive(file_path_, dir_to_create / Path(files_name).stem) #Розпаковуємо архів
                os.remove(file_path_) #видаляє архів, який ми вже опрацювали
                # p_file.rename(dir_to_create.joinpath(p_file.name)) # переміщуємо у нову створену по розширенню папку
            else:
                _other.append(files_name)
                unknown_suffix_list.append(files_name.suffix)
                #перенести в папку other
                dir_to_create = Path(way_) / 'other' # задаємо ім'я майбутньої папки
                dir_to_create.mkdir(exist_ok=True)       # створємо нову папку по суфіксу
                shutil.move(file_path_, dir_to_create / files_name) # переміщуємо у нову створену по розширенню папку
                
    return dict_for_return

if __name__ == '__main__':
    sort(r'C:\Users\Hewlett Packard\Desktop\Xlam')