import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('data/marketing_clean.csv')

summary = df.groupby('test_group').agg(
    users=('user_id', 'count'),
    conversions=('converted', 'sum'),
    conversion_rate=('converted', 'mean'),
    avg_ads_seen=('total_ads', 'mean')
).reset_index()
print(summary)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
summary.plot(kind='bar', x='test_group', y='conversion_rate',
           ax=axes[0], color=['#1a3d6b', '#c84b11'], legend=False)
axes[0].set_title('Conversion Rate: Ad vs PSA')

ad_users = df[df['test_group'] == 'ad'].copy()
ad_users['ads_bucket'] = pd.cut(ad_users['total_ads'],
    bins=[0,5,15,30,60,100,2000],
    labels=['1-5','6-15','16-30','31-60','61-100','100+'])
bucket_conv = ad_users.groupby('ads_bucket')['converted'].mean()
bucket_conv.plot(kind='bar', ax=axes[1], color='#1a6b3c')
axes[1].set_title('Conversion Rate by Ads Seen (Ad group)')
axes[1].set_xlabel('Number of Ads Seen')

day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
day_conv = df.groupby('most_ads_day')['converted'].mean().reindex(day_order)
day_conv.plot(kind='bar', ax=axes[2], color='#c84b11')
axes[2].set_title('Conversion Rate by Day of Week')

plt.tight_layout()
plt.savefig('reports/eda_charts.png', dpi=150)
plt.show()