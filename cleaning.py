import pandas as pd

df = pd.read_csv('data/marketing_AB.csv')


print(df.shape)        
print(df.dtypes)
print(df.isnull().sum())

print(df['test group'].value_counts())

df['converted'] = df['converted'].astype(int)

df = df.rename(columns={
    'user id': 'user_id',
    'test group': 'test_group',
    'total ads': 'total_ads',
    'most ads day': 'most_ads_day',
    'most ads hour': 'most_ads_hour'
})

print(f"Duplicate users: {df['user_id'].duplicated().sum()}")
df = df.drop_duplicates(subset='user_id', keep='first')

print(df['total_ads'].describe())
df = df[df['total_ads'] <= 2000]

print(f"Clean dataset: {len(df)} rows")
df.to_csv('data/marketing_clean.csv', index=False)
