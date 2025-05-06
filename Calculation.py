from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def init_monthly_stats(start_year, start_month, end_year, end_month):
    """Инициализирует словарь для всех месяцев в указанном диапазоне"""
    monthly_stats = {}
    year = start_year
    month = start_month
    while (year < end_year) or (year == end_year and month <= end_month):
        monthly_stats[(year, month)] = {'tickets': 0, 'sla_sum': 0.0}
        month += 1
        if month > 12:
            month = 1
            year += 1
    return monthly_stats


# Инициализация статистики
monthly_stats = init_monthly_stats(2022, 1, 2024, 12)

# Чтение Excel-файла
file_path = "C:\\Users\\Alksq\\Downloads\\Testovoe_zadanye.xlsx"
try:
    df = pd.read_excel(file_path, engine='openpyxl')
except Exception as e:
    print(f"Ошибка чтения файла: {e}")
    exit()

# Проверка наличия нужных столбцов
required_columns = ['Дата создания тикета', 'Количество тикетов', 'СЛА']
if not all(col in df.columns for col in required_columns):
    print("Ошибка: В файле отсутствуют необходимые столбцы.")
    exit()

# Обработка данных
for index, row in df.iterrows():
    try:
        date_str = str(row['Дата создания тикета'])
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        year_month = (date.year, date.month)

        tickets = int(row['Количество тикетов'])

        sla_str = str(row['СЛА']).replace('%', '').replace(',', '.')
        sla = float(sla_str) * 100

        if year_month in monthly_stats:
            monthly_stats[year_month]['tickets'] += tickets
            monthly_stats[year_month]['sla_sum'] += sla * tickets
    except Exception as e:
        continue


# Вывод результатов
print("Месяц\t\tКоличество тикетов\tSLA (%)")
for year in range(2022, 2025):
    for month in range(1, 13):
        ym_key = (year, month)
        if ym_key not in monthly_stats:
            continue
        stats = monthly_stats[ym_key]
        avg_sla = (stats['sla_sum'] / stats['tickets']) if stats['tickets'] > 0 else 0
        print(f"{year}-{month:02d}\t{stats['tickets']}\t\t\t{avg_sla:.2f}%")
# Создаем DataFrame для визуализации
results = []
for year in range(2022, 2025):
    for month in range(1, 13):
        ym_key = (year, month)
        if ym_key not in monthly_stats:
            continue
        stats = monthly_stats[ym_key]
        avg_sla = (stats['sla_sum'] / stats['tickets']) if stats['tickets'] > 0 else 0
        results.append({
            'Дата': f"{year}-{month:02d}-01",  # Первый день месяца для правильного парсинга
            'Количество тикетов': stats['tickets'],
            'SLA (%)': avg_sla
        })

df_plot = pd.DataFrame(results)
df_plot['Дата'] = pd.to_datetime(df_plot['Дата'])  # Преобразуем в datetime

# Настройка стиля seaborn
sns.set_theme(style="whitegrid", palette="pastel")

# График количества тикетов
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_plot, x='Дата', y='Количество тикетов', marker='o')
plt.title('Динамика количества тикетов (2022-2024)')
plt.xlabel('Месяц')
plt.ylabel('Тикетов')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# График SLA
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_plot, x='Дата', y='SLA (%)', marker='o', color='orange')
plt.title('Динамика SLA (2022-2024)')
plt.xlabel('Месяц')
plt.ylabel('SLA (%)')
plt.ylim(0, 100)  # Ограничиваем шкалу от 0% до 100%
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()