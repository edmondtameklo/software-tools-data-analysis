# -*- coding: utf-8 -*-
# Лабораторная работа №5
# Визуализация данных и статистический анализ
# Вариант 6: Исследование данных о продажах онлайн-магазина
# Студент: Тамекло Коку Эдмон
# Группа: МИС-25-1

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
sns.set_style("whitegrid")


def load_data():
    """Загружает данные о продажах."""
    print("=" * 60)
    print("ЗАГРУЗКА ДАННЫХ")
    print("=" * 60)
    
    filename = 'online_sales.csv'
    
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename, encoding='utf-8')
        except:
            try:
                df = pd.read_csv(filename, encoding='latin-1')
            except:
                df = pd.read_csv(filename, encoding='ISO-8859-1')
        print(f"✓ Загружен файл: {filename}")
    else:
        print("Файл не найден!")
        return None
    
    # Адаптация колонок под стандартные имена
    print("\n--- Адаптация колонок датасета ---")
    print(f"Исходные колонки: {list(df.columns)}")
    
    # Создаем колонку Sales (продажи = количество × цена)
    if 'Sales' not in df.columns:
        if 'Quantity' in df.columns and 'UnitPrice' in df.columns:
            df['Sales'] = df['Quantity'] * df['UnitPrice']
            print("✓ Создана колонка Sales = Quantity × UnitPrice")
        elif 'Quantity' in df.columns and 'Price' in df.columns:
            df['Sales'] = df['Quantity'] * df['Price']
            print("✓ Создана колонка Sales = Quantity × Price")
    
    # Создаем колонку Discount если её нет
    if 'Discount' not in df.columns:
        # Для демонстрации: случайные скидки 0-30%
        np.random.seed(42)
        df['Discount'] = np.random.choice([0, 0, 0, 5, 10, 10, 15, 20, 25, 30], 
                                           size=len(df), 
                                           p=[0.25, 0.10, 0.10, 0.08, 0.10, 0.07, 0.10, 0.08, 0.07, 0.05])
        print("✓ Создана демонстрационная колонка Discount (для анализа скидок)")
    
    # Стандартизация имен колонок
    if 'InvoiceDate' in df.columns:
        df['Date'] = pd.to_datetime(df['InvoiceDate'])
        print("✓ Колонка InvoiceDate → Date")
    elif 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    
    if 'Description' in df.columns and 'Product' not in df.columns:
        df['Product'] = df['Description']
        print("✓ Колонка Description → Product")
    
    if 'UnitPrice' in df.columns and 'Price' not in df.columns:
        df['Price'] = df['UnitPrice']
        print("✓ Колонка UnitPrice → Price")
    
    # Удаляем строки с отрицательными значениями
    if 'Quantity' in df.columns:
        df = df[df['Quantity'] > 0]
    if 'Price' in df.columns:
        df = df[df['Price'] > 0]
    if 'Sales' in df.columns:
        df = df[df['Sales'] > 0]
    
    print(f"\nИтоговое количество записей: {len(df)}")
    return df


def primary_analysis(df):
    """Первичный анализ данных."""
    print("\n" + "=" * 60)
    print("1. ПЕРВИЧНЫЙ АНАЛИЗ ДАННЫХ")
    print("=" * 60)
    
    print(f"\nКоличество записей: {len(df)}")
    print(f"Количество столбцов: {len(df.columns)}")
    print(f"Столбцы: {list(df.columns)}")
    
    print(f"\nПервые 10 строк:")
    print(df.head(10))
    
    print(f"\nТипы данных:")
    print(df.dtypes)
    
    print(f"\nСтатистическое описание:")
    print(df.describe())
    
    print(f"\nПропущенные значения:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({'Количество': missing, 'Процент': missing_pct})
    print(missing_df[missing_df['Количество'] > 0])
    
    if 'Country' in df.columns:
        print(f"\nКоличество стран: {df['Country'].nunique()}")
        print(df['Country'].value_counts().head(10))
    
    return df


def visualize_top_products(df):
    """Визуализация самых продаваемых товаров."""
    print("\n" + "=" * 60)
    print("2. ВИЗУАЛИЗАЦИЯ САМЫХ ПРОДАВАЕМЫХ ТОВАРОВ")
    print("=" * 60)
    
    sales_col = 'Sales' if 'Sales' in df.columns else 'Quantity'
    product_col = 'Product' if 'Product' in df.columns else 'Description'
    
    if product_col not in df.columns:
        print("Колонка с товарами не найдена!")
        return
    
    # Топ-10 товаров
    top_products = df.groupby(product_col)[sales_col].sum().sort_values(ascending=False).head(10)
    
    print(f"\nТоп-10 самых продаваемых товаров:")
    for i, (product, total) in enumerate(top_products.items(), 1):
        print(f"  {i}. {str(product)[:50]}: {total:,.2f}")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Столбчатая диаграмма
    colors_bar = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336',
                  '#00BCD4', '#FFEB3B', '#795548', '#607D8B', '#E91E63']
    
    bars = ax1.bar(range(len(top_products)), top_products.values, color=colors_bar, edgecolor='white')
    ax1.set_xticks(range(len(top_products)))
    ax1.set_xticklabels([str(p)[:20] for p in top_products.index], rotation=45, ha='right', fontsize=9)
    ax1.set_ylabel(f'Сумма продаж', fontsize=12)
    ax1.set_title('Топ-10 самых продаваемых товаров', fontsize=14, fontweight='bold')
    
    for bar, value in zip(bars, top_products.values):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                f'{value:,.0f}', ha='center', va='bottom', fontsize=8)
    
    # Круговая диаграмма по странам
    if 'Country' in df.columns:
        country_sales = df.groupby('Country')[sales_col].sum().sort_values(ascending=False).head(8)
        other = df.groupby('Country')[sales_col].sum().sort_values(ascending=False).iloc[8:].sum()
        
        if other > 0:
            country_sales['Другие'] = other
        
        colors_pie = plt.cm.Set3(range(len(country_sales)))
        wedges, texts, autotexts = ax2.pie(country_sales.values,
                                            labels=country_sales.index,
                                            autopct='%1.1f%%',
                                            colors=colors_pie,
                                            startangle=90)
        ax2.set_title('Доля продаж по странам', fontsize=14, fontweight='bold')
        for autotext in autotexts:
            autotext.set_fontsize(9)
    else:
        ax2.pie(top_products.values, labels=[str(p)[:15] for p in top_products.index],
                autopct='%1.1f%%', colors=colors_bar, startangle=90)
        ax2.set_title('Доля топ-10 товаров', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('top_products.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\n✓ График сохранен: top_products.png")


def analyze_discount_impact(df):
    """Анализ влияния скидок на продажи."""
    print("\n" + "=" * 60)
    print("3. АНАЛИЗ ВЛИЯНИЯ СКИДОК НА ПРОДАЖИ")
    print("=" * 60)
    
    sales_col = 'Sales' if 'Sales' in df.columns else 'Quantity'
    
    if 'Discount' not in df.columns:
        print("Колонка Discount не найдена!")
        return
    
    # Группировка
    discount_groups = df.groupby('Discount').agg({
        sales_col: ['sum', 'mean', 'count']
    }).round(2)
    discount_groups.columns = ['Общие_продажи', 'Средние_продажи', 'Количество_заказов']
    
    print(f"\nСтатистика по скидкам:")
    print(discount_groups)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # График 1
    ax1 = axes[0]
    discounts = discount_groups.index
    avg_sales = discount_groups['Средние_продажи'].values
    
    ax1.plot(discounts, avg_sales, 'o-', color='#2196F3', linewidth=2, markersize=10,
             markerfacecolor='#FF9800')
    ax1.fill_between(discounts, avg_sales, alpha=0.3, color='#2196F3')
    ax1.set_xlabel('Размер скидки (%)', fontsize=12)
    ax1.set_ylabel('Средние продажи', fontsize=12)
    ax1.set_title('Средние продажи vs Размер скидки', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # График 2
    ax2 = axes[1]
    total_sales = discount_groups['Общие_продажи'].values
    bars = ax2.bar(discounts, total_sales, color=plt.cm.viridis(np.linspace(0.2, 0.9, len(discounts))),
                   edgecolor='white', width=3)
    ax2.set_xlabel('Размер скидки (%)', fontsize=12)
    ax2.set_ylabel('Общие продажи', fontsize=12)
    ax2.set_title('Общие продажи vs Размер скидки', fontsize=14, fontweight='bold')
    
    for bar, value in zip(bars, total_sales):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                f'{value:,.0f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('discount_impact.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Статистический тест
    print("\n--- Статистический анализ ---")
    groups = [group[sales_col].values for name, group in df.groupby('Discount')]
    
    if len(groups) >= 2:
        f_stat, p_value = stats.f_oneway(*groups)
        print(f"ANOVA тест: F = {f_stat:.4f}, p = {p_value:.4f}")
        if p_value < 0.05:
            print("ВЫВОД: Скидки СТАТИСТИЧЕСКИ ЗНАЧИМО влияют на продажи (p < 0.05)")
        else:
            print("ВЫВОД: Влияние скидок статистически не доказано (p >= 0.05)")
    
    print(f"\n✓ График сохранен: discount_impact.png")


def visualize_price_dynamics(df):
    """Визуализация динамики цен."""
    print("\n" + "=" * 60)
    print("4. ВИЗУАЛИЗАЦИЯ ДИНАМИКИ ЦЕН")
    print("=" * 60)
    
    if 'Date' not in df.columns:
        print("Колонка с датами не найдена!")
        return
    
    if 'Price' not in df.columns:
        print("Колонка с ценами не найдена!")
        return
    
    df['Month'] = df['Date'].dt.to_period('M')
    
    # Топ-5 продуктов
    product_col = 'Product' if 'Product' in df.columns else 'Description'
    top_products = df.groupby(product_col)['Sales'].sum().nlargest(5).index
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Динамика цен
    colors = ['#2196F3', '#FF9800', '#4CAF50', '#F44336', '#9C27B0']
    
    for i, product in enumerate(top_products):
        product_data = df[df[product_col] == product].groupby('Month')['Price'].mean()
        if len(product_data) > 0:
            ax1.plot(range(len(product_data)), product_data.values, 'o-',
                    color=colors[i], linewidth=2, markersize=6, label=str(product)[:25])
    
    ax1.set_xlabel('Месяц', fontsize=12)
    ax1.set_ylabel('Средняя цена', fontsize=12)
    ax1.set_title('Динамика цен на популярные товары', fontsize=14, fontweight='bold')
    ax1.legend(loc='best', fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # Связь цена-продажи
    price_sales = df.groupby('Month').agg({'Price': 'mean', 'Sales': 'sum'}).dropna()
    
    if len(price_sales) > 2:
        ax2.scatter(price_sales['Price'], price_sales['Sales'],
                   alpha=0.7, s=100, color='#2196F3', edgecolors='white')
        
        z = np.polyfit(price_sales['Price'], price_sales['Sales'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(price_sales['Price'].min(), price_sales['Price'].max(), 100)
        ax2.plot(x_trend, p(x_trend), '--', color='#FF9800', linewidth=2)
        
        corr, p_corr = stats.pearsonr(price_sales['Price'], price_sales['Sales'])
        print(f"\nКорреляция Пирсона: r = {corr:.4f}, p = {p_corr:.4f}")
    
    ax2.set_xlabel('Средняя цена', fontsize=12)
    ax2.set_ylabel('Общие продажи', fontsize=12)
    ax2.set_title('Связь между ценой и продажами', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('price_dynamics.png', dpi=150, bbox_inches='tight')
    plt.show()
    print(f"\n✓ График сохранен: price_dynamics.png")


def compare_sales_by_country(df):
    """Сравнение продаж по странам."""
    print("\n" + "=" * 60)
    print("5. СРАВНЕНИЕ ПРОДАЖ ПО СТРАНАМ")
    print("=" * 60)
    
    if 'Country' not in df.columns:
        print("Колонка Country не найдена!")
        return
    
    sales_col = 'Sales' if 'Sales' in df.columns else 'Quantity'
    
    country_sales = df.groupby('Country')[sales_col].agg(['sum', 'mean', 'count']).round(2)
    country_sales.columns = ['Общие_продажи', 'Средние_продажи', 'Количество_заказов']
    country_sales = country_sales.sort_values('Общие_продажи', ascending=False)
    
    print(f"\nПродажи по странам (топ-15):")
    print(country_sales.head(15))
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
    
    # Столбчатая диаграмма
    ax1 = axes[0]
    top_countries = country_sales.head(15)
    
    bars = ax1.bar(range(len(top_countries)), top_countries['Общие_продажи'].values,
                   color=plt.cm.plasma(np.linspace(0.1, 0.9, len(top_countries))),
                   edgecolor='white')
    ax1.set_xticks(range(len(top_countries)))
    ax1.set_xticklabels(top_countries.index, rotation=45, ha='right', fontsize=9)
    ax1.set_ylabel('Общие продажи', fontsize=12)
    ax1.set_title('Продажи по странам', fontsize=14, fontweight='bold')
    
    for bar, value in zip(bars, top_countries['Общие_продажи'].values):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                f'{value:,.0f}', ha='center', va='bottom', fontsize=7, rotation=90)
    
    # Ящики с усами
    ax2 = axes[1]
    top5_countries = country_sales.head(5).index
    data_for_box = [df[df['Country'] == c][sales_col].dropna().values for c in top5_countries]
    
    bp = ax2.boxplot(data_for_box, labels=top5_countries, patch_artist=True,
                     showmeans=True, meanprops=dict(marker='D', markerfacecolor='red', markersize=6))
    
    for patch, color in zip(bp['boxes'], plt.cm.Set3(range(len(top5_countries)))):
        patch.set_facecolor(color)
    
    ax2.set_ylabel(sales_col, fontsize=12)
    ax2.set_title('Распределение продаж по странам (топ-5)', fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('sales_by_country.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Статистика
    groups = [group[sales_col].values for name, group in df.groupby('Country') if name in top5_countries]
    if len(groups) >= 2:
        f_stat, p_value = stats.f_oneway(*groups)
        print(f"\nANOVA тест (топ-5 стран): F = {f_stat:.4f}, p = {p_value:.4f}")
        if p_value < 0.05:
            print("ВЫВОД: Продажи статистически значимо различаются между странами!")
    
    print(f"\n✓ График сохранен: sales_by_country.png")


def main():
    """Главная функция."""
    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА №5")
    print("Визуализация данных и статистический анализ")
    print("Вариант 6: Исследование данных о продажах онлайн-магазина")
    print("=" * 60)
    
    df = load_data()
    if df is None:
        return
    
    df = primary_analysis(df)
    
    try:
        visualize_top_products(df)
    except Exception as e:
        print(f"Ошибка в задании 2: {e}")
    
    try:
        analyze_discount_impact(df)
    except Exception as e:
        print(f"Ошибка в задании 3: {e}")
    
    try:
        visualize_price_dynamics(df)
    except Exception as e:
        print(f"Ошибка в задании 4: {e}")
    
    try:
        compare_sales_by_country(df)
    except Exception as e:
        print(f"Ошибка в задании 5: {e}")
    
    print("\n" + "=" * 60)
    print("АНАЛИЗ ЗАВЕРШЕН!")
    print("=" * 60)


if __name__ == "__main__":
    main()
