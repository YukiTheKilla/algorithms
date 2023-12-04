import os
import random
import pandas as pd
import numpy as np
import time
import hashlib
import openpyxl
import subprocess

numbers_to_hash = [89156651327,
89868999648,
89639261431,
89837232568,
89099367499,
]

base_folder = r'C:\Users\Acer\Desktop\study\algos\3.lab'

input_excel_file = os.path.join(base_folder, '3 задача-исследование', 'scoring_data_v.1.2.xlsx')
hashcat_path = os.path.join(base_folder, 'hashick', 'hashcat.exe')

excel_hash_sha1 = os.path.join(base_folder, 'hash_sha1.xlsx')
excel_hash_sha2_256 = os.path.join(base_folder, 'hash_sha2_256.xlsx')
excel_hash_md5 = os.path.join(base_folder, 'hash_md5.xlsx')

hash_md5 = os.path.join(base_folder, 'hash_md5.txt')
hash_sha1 = os.path.join(base_folder, 'hash_sha1.txt')
hash_sha2_256 = os.path.join(base_folder, 'hash_sha2_256.txt')

salt_md5 = os.path.join(base_folder, 'salt_md5.txt')
salt_sha1 = os.path.join(base_folder, 'salt_sha1.txt')
salt_sha2_256 = os.path.join(base_folder, 'salt_sha2_256.txt') 


def read_phone_numbers():
    df = pd.read_excel(input_excel_file) 
    phone_real_numbers = df.iloc[:, 2].head(5).values
    print_real_numbers = phone_real_numbers.astype(str)
    print(print_real_numbers)
    return phone_real_numbers
    
def excel_to_txt(input_excel, output_txt):
    # Чтение данных из Excel
    df = pd.read_excel(input_excel, usecols=[0])  # Предполагаем, что нужный столбец - первый (индекс 0)

    # Формирование пути для сохранения текстового файла в той же директории, что и Excel файл
    output_txt_path = os.path.join(os.path.dirname(input_excel), output_txt)

    # Запись данных в текстовый файл с отступом в один enter после каждой строки
    with open(output_txt_path, 'w') as txt_file:
        for  index, row in df.iterrows():
            txt_file.write(str(row[0]) + '\n')
        
def create_hashes(num_hashes, numbers, hash_type, file_path, salt):
    if os.path.exists(file_path):
        os.remove(file_path)
    # Создаем новый Excel-файл
    wb = openpyxl.Workbook()
    sheet = wb.active

    # Заголовок
    sheet['A1'] = 'Hash'

    for i in range(num_hashes):
        # Выбираем одно число из списка
        num = numbers[i % len(numbers)]
        
        multiple_salt = salt * (10**random.randint(0,8))

        # Генерация строки для хеширования
        data_to_hash = f"{num + multiple_salt}"

        # Создаем объект хеша
        hash_object = hashlib.new(hash_type)
        hash_object.update(data_to_hash.encode('utf-8'))

        # Получаем хеш и добавляем в Excel
        hash_value = hash_object.hexdigest()
        sheet.cell(row=i + 2, column=1, value=hash_value)

    # Сохраняем в файл Excel
    wb.save(file_path)
    print(f"Хеши успешно записаны в {file_path}")
    
def hashcat_command_find_phones_with_salt(type_of_hash, hash_path, salt_output_path):
    # Check if the output file exists and delete it if it does
    if os.path.exists(salt_output_path):
        os.remove(salt_output_path)

    # Set the working directory to the correct path
    os.chdir(os.path.join(base_folder, 'hashick'))

    # Run hashcat with specified parameters
    subprocess.run([
        hashcat_path,
        '--potfile-disable',
        '-O',
        '-D', '2',
        '--force',
        '-m', str(type_of_hash),
        '-a', '3',
        '-i',
        '--increment-min=11',
        '--increment-max=11',
        hash_path,
        '8?d?d?d?d?d?d?d?d?d?d?d?d',
        '--quiet',
        '--outfile-format=2',
        '-o', salt_output_path
    ])

    subprocess.run([
        hashcat_path,
        '--potfile-disable',
        '-O',
        '-D', '2',
        '--force',
        '-m', str(type_of_hash),
        '-a', '3',
        '-i',
        '--increment-min=11',
        '--increment-max=11',
        hash_path,
        '9?d?d?d?d?d?d?d?d?d?d?d?d',
        '--quiet',
        '--outfile-format=2',
        '-o', salt_output_path
    ])

    # Move back to the original directory
    os.chdir(base_folder)
    
def count_salt(salt_path):
    phone_real_numbers = read_phone_numbers()
    numbers_with_salt = np.loadtxt(salt_path,delimiter='\n')

    result_matrix = np.abs(np.subtract.outer(numbers_with_salt, phone_real_numbers))

    unique_elements, element_counts = np.unique(result_matrix, return_counts=True)

    # Находим элементы, которые встречаются k раз
    k_repeated_elements = unique_elements[element_counts == 5]
    k_repeated_elements_str = str(k_repeated_elements)

    print("salt is", k_repeated_elements_str)

if __name__ == "__main__":
    excel_to_txt(input_excel_file,hash_md5)
    hashcat_command_find_phones_with_salt(0,hash_md5,salt_md5)
    count_salt(salt_md5)
    
    create_hashes(50000, numbers_to_hash, "sha1", excel_hash_sha1, 581)
    excel_to_txt(excel_hash_sha1,hash_sha1)
    
    start_time = time.time()
    hashcat_command_find_phones_with_salt(100,hash_sha1,salt_sha1)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken for sha1: {elapsed_time} seconds")
    
    create_hashes(50000, numbers_to_hash, "sha256", excel_hash_sha2_256, 581)
    excel_to_txt(excel_hash_sha2_256,hash_sha2_256)
    
    start_time = time.time()
    hashcat_command_find_phones_with_salt(1400,hash_sha2_256,salt_sha2_256)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken for sha2-256: {elapsed_time} seconds")
    
    create_hashes(50000, numbers_to_hash, "md5", excel_hash_md5, 581)
    excel_to_txt(excel_hash_md5,hash_md5)
    
    start_time = time.time()
    hashcat_command_find_phones_with_salt(0,hash_md5,salt_md5)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken for md5: {elapsed_time} seconds")
    
    