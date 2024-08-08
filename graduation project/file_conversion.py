import csv

# Путь к исходному и конечному CSV файлам
input_csv_file = 'arrival1.csv'  # Исходный файл с другим разделителем,';'
output_csv_file = 'prillet.csv'  # Результирующий файл с разделителем ','

# Открываем исходный файл для чтения
with open(input_csv_file, mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter=';') 
    
    # Получение всех строк из исходного файла, оставляя только первые 6 столбцов
    rows = [row[:6] for row in reader]  # Сохраняем только первые 6 элементов каждой строки

# Открываем новый файл для записи
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile, delimiter=',')  # Указываем новый разделитель
    
    # Записываем все строки в новый файл
    writer.writerows(rows)

print(f'Файл успешно сохранён как {output_csv_file} с разделителем "," и только первыми 6 столбцами.')
