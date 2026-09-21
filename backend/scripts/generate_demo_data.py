import pandas as pd
import numpy as np
import random
import os

def generate():
    data_dir = "D:/Downloads/datapilot-ai/backend/data"
    os.makedirs(data_dir, exist_ok=True)

    np.random.seed(42)
    random.seed(42)

    # 1. Sales Data (500+ rows)
    dates = pd.date_range('2023-01-01', '2024-12-31', periods=500)
    products = ['Laptop Pro', 'Wireless Mouse', 'USB Hub', 'Monitor 27"', 'Keyboard Mechanical', 'Webcam 4K', 'Headset Pro', 'Tablet Air', 'Phone Case', 'Fast Charger 65W']
    categories = ['Electronics', 'Accessories', 'Peripherals']
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
    
    sales_df = pd.DataFrame({
        'date': dates,
        'product': [random.choice(products) for _ in range(500)],
        'category': [random.choice(categories) for _ in range(500)],
        'region': [random.choice(regions) for _ in range(500)],
        'quantity': np.random.randint(1, 50, 500),
        'unit_price': np.round(np.random.uniform(15, 650, 500), 2),
    })
    sales_df['revenue'] = np.round(sales_df['quantity'] * sales_df['unit_price'], 2)
    sales_df['cost'] = np.round(sales_df['revenue'] * np.random.uniform(0.4, 0.7, 500), 2)
    sales_df['profit'] = np.round(sales_df['revenue'] - sales_df['cost'], 2)
    sales_df['customer_id'] = [f'CUST-{random.randint(1000, 9999)}' for _ in range(500)]
    sales_df['payment_method'] = [random.choice(['Credit Card', 'PayPal', 'Bank Transfer', 'Stripe']) for _ in range(500)]
    
    # Introduce realistic data flaws for data cleaning & quality scoring tests
    sales_df.loc[random.sample(range(500), 12), 'region'] = np.nan
    sales_df.loc[random.sample(range(500), 6), 'cost'] = np.nan
    sales_df = pd.concat([sales_df, sales_df.iloc[10:15]]) # Add 5 duplicates
    sales_df.to_csv(os.path.join(data_dir, 'demo_sales.csv'), index=False)
    print("Generated demo_sales.csv (505 rows)")

    # 2. Marketing Data (200+ rows)
    mkt_dates = pd.date_range('2023-06-01', '2024-12-31', periods=200)
    campaigns = ['Summer Launch', 'Black Friday Special', 'Q1 Growth Push', 'Retargeting 2024', 'Brand Awareness']
    channels = ['Google Ads', 'Meta', 'LinkedIn', 'YouTube', 'TikTok Ads']
    
    impressions = np.random.randint(5000, 150000, 200)
    clicks = np.round(impressions * np.random.uniform(0.015, 0.06, 200)).astype(int)
    spend = np.round(clicks * np.random.uniform(0.8, 3.5, 200), 2)
    conversions = np.round(clicks * np.random.uniform(0.02, 0.12, 200)).astype(int)
    revenue = np.round(conversions * np.random.uniform(45, 220, 200), 2)
    
    mkt_df = pd.DataFrame({
        'date': mkt_dates,
        'campaign': [random.choice(campaigns) for _ in range(200)],
        'channel': [random.choice(channels) for _ in range(200)],
        'impressions': impressions,
        'clicks': clicks,
        'spend': spend,
        'conversions': conversions,
        'revenue': revenue
    })
    mkt_df['ctr'] = np.round((mkt_df['clicks'] / mkt_df['impressions']) * 100, 2)
    mkt_df['cpc'] = np.round(mkt_df['spend'] / np.maximum(mkt_df['clicks'], 1), 2)
    mkt_df['roas'] = np.round(mkt_df['revenue'] / np.maximum(mkt_df['spend'], 1), 2)
    mkt_df.to_csv(os.path.join(data_dir, 'demo_marketing.csv'), index=False)
    print("Generated demo_marketing.csv (200 rows)")

    # 3. Finance Data (100+ rows)
    fin_dates = pd.date_range('2023-01-01', '2024-12-31', periods=120)
    fin_categories = ['SaaS Subscriptions', 'Consulting Services', 'Cloud Infrastructure', 'Payroll', 'Marketing', 'Office & Legal', 'Hardware']
    fin_types = ['Revenue', 'Expense']
    
    fin_rows = []
    for d in fin_dates:
        is_rev = random.random() > 0.45
        cat = random.choice(['SaaS Subscriptions', 'Consulting Services']) if is_rev else random.choice(['Cloud Infrastructure', 'Payroll', 'Marketing', 'Office & Legal', 'Hardware'])
        amt = np.round(np.random.uniform(1500, 45000), 2) if is_rev else np.round(np.random.uniform(500, 18000), 2)
        fin_rows.append({
            'date': d,
            'category': cat,
            'type': 'Revenue' if is_rev else 'Expense',
            'amount': amt,
            'description': f"Transaction for {cat}",
            'department': random.choice(['Sales', 'Engineering', 'Marketing', 'Operations', 'Executive'])
        })
    fin_df = pd.DataFrame(fin_rows)
    fin_df.to_csv(os.path.join(data_dir, 'demo_finance.csv'), index=False)
    print("Generated demo_finance.csv (120 rows)")

    # 4. HR Data (100+ rows)
    departments = ['Engineering', 'Product', 'Sales', 'Marketing', 'Human Resources', 'Finance', 'Customer Support']
    positions = ['Software Engineer', 'Product Manager', 'Account Executive', 'Marketing Lead', 'HR Specialist', 'Financial Analyst', 'Support Specialist', 'Staff Engineer', 'VP']
    statuses = ['Active', 'Active', 'Active', 'Active', 'On Leave', 'Resigned']
    
    hr_rows = []
    for i in range(100):
        hire_date = pd.Timestamp('2020-01-01') + pd.Timedelta(days=random.randint(0, 1400))
        dept = random.choice(departments)
        pos = random.choice(positions)
        base_salary = 60000 if 'Specialist' in pos else (120000 if 'Staff' in pos or 'VP' in pos else 85000)
        salary = base_salary + random.randint(-10000, 35000)
        
        hr_rows.append({
            'employee_id': f"EMP-{1001 + i}",
            'name': f"Employee {i + 1}",
            'department': dept,
            'position': pos,
            'salary': salary,
            'hire_date': hire_date.strftime('%Y-%m-%d'),
            'status': random.choice(statuses),
            'performance_score': round(random.uniform(3.0, 5.0), 1),
            'satisfaction_rating': random.randint(1, 5)
        })
    hr_df = pd.DataFrame(hr_rows)
    hr_df.to_csv(os.path.join(data_dir, 'demo_hr.csv'), index=False)
    print("Generated demo_hr.csv (100 rows)")

if __name__ == "__main__":
    generate()
