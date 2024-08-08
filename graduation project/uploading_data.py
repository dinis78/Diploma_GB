import pandas as pd
import csv
# Путь к  CSV файлу
csv_file_path = 'prillet.csv'

# Читаем CSV файл в DataFrame
data = pd.read_csv(csv_file_path)

# Просмотрим данные
print(data)


