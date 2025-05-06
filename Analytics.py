import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, pearsonr

# Загрузка данных
df = pd.read_csv("C:\\Users\\Alksq\\PythonProject4\\monthly_stats.csv", parse_dates=['Дата'])
df['Год'] = df['Дата'].dt.year
df['Месяц'] = df['Дата'].dt.month

# 1. Описательная статистика
desc_stats = df[['Количество тикетов', 'SLA (%)']].describe()
print("=" * 50)
print("Описательная статистика:")
print(desc_stats)

# 2. Анализ сезонности (раздельные графики)
monthly_avg = df.groupby('Месяц').agg({
    'Количество тикетов': 'mean',
    'SLA (%)': 'mean'
}).reset_index()

# График для тикетов
plt.figure(figsize=(12, 5))
sns.lineplot(data=monthly_avg, x='Месяц', y='Количество тикетов', marker='o', color='blue')
plt.title('Сезонность количества тикетов ')
plt.xlabel('Месяц')
plt.ylabel('Среднее количество тикетов')
plt.xticks(range(1, 13), ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'])
plt.grid(True)
plt.show()

# График для SLA
plt.figure(figsize=(12, 5))
sns.lineplot(data=monthly_avg, x='Месяц', y='SLA (%)', marker='o', color='orange')
plt.title('Сезонность SLA ')
plt.xlabel('Месяц')
plt.ylabel('Средний SLA (%)')
plt.xticks(range(1, 13), ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'])
plt.ylim(0, 100)  # Ограничение для процентной шкалы
plt.grid(True)
plt.show()

# 3. Сравнение по годам
yearly_stats = df.groupby('Год').agg({
    'Количество тикетов': ['mean', 'sum'],
    'SLA (%)': 'mean'
}).reset_index()

print("\n" + "=" * 50)
print("Сравнение по годам:")
print(yearly_stats)

# 4. Корреляционный анализ
corr, p_value = pearsonr(df['Количество тикетов'], df['SLA (%)'])
print("\n" + "=" * 50)
print(f"Корреляция между нагрузкой и SLA: {corr:.2f} (p-value = {p_value:.4f})")

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Количество тикетов', y='SLA (%)', hue='Год', palette='viridis')
plt.title('Корреляция: Нагрузка vs SLA')
plt.show()

# 5. Проверка гипотез (t-тест для 2022 и 2024)
data_2022 = df[df['Год'] == 2022]['Количество тикетов']
data_2024 = df[df['Год'] == 2024]['Количество тикетов']
t_stat, p_val = ttest_ind(data_2022, data_2024, equal_var=False)
print("\n" + "=" * 50)
print(f"t-тест между 2022 и 2024: t = {t_stat:.2f}, p-value = {p_val:.4f}")

# 6. Выявление выбросов
Q1 = df['Количество тикетов'].quantile(0.25)
Q3 = df['Количество тикетов'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['Количество тикетов'] < lower_bound) | (df['Количество тикетов'] > upper_bound)]
print("\n" + "=" * 50)
print("Выбросы:")
print(outliers[['Дата', 'Количество тикетов']])

# 7. Прогнозирование (скользящее среднее)
df['Прогноз тикетов'] = df['Количество тикетов'].rolling(window=3).mean()
print("\n" + "=" * 50)
print("Прогноз на следующий месяц (скользящее среднее):")
print(f"Прогноз на январь 2025: {df['Прогноз тикетов'].iloc[-1]:.0f}")

# 8. Сохранение результатов
yearly_stats.to_csv('yearly_analysis.csv', index=False, encoding='utf-8-sig')
print("\nРезультаты сохранены в 'yearly_analysis.csv'")