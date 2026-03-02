import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('data/marketing_clean.csv')

# ── Chart 4: Ads Frequency Curve ────────────────────────
ad_users = df[df['test_group'] == 'ad'].copy()

bins   = [0,5,10,20,40,80,150,300,2000]
labels = ['1-5','6-10','11-20','21-40','41-80','81-150','151-300','300+']
ad_users['ads_bin'] = pd.cut(ad_users['total_ads'],
                              bins=bins, labels=labels)

freq_conv = ad_users.groupby('ads_bin', observed=False)['converted'].mean() * 100

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(len(freq_conv)), freq_conv.values,
        marker='o', color='#c84b11', linewidth=2.5, markersize=8)
ax.fill_between(range(len(freq_conv)), freq_conv.values,
                alpha=0.12, color='#c84b11')
ax.set_xticks(range(len(freq_conv)))
ax.set_xticklabels(labels)
ax.set_title('Conversion Rate vs Number of Ads Seen', fontsize=14, pad=15)
ax.set_xlabel('Number of Ads Seen')
ax.set_ylabel('Conversion Rate (%)')
ax.axvline(x=freq_conv.values.argmax(), color='#1a6b3c',
           linestyle='--', linewidth=1.5, label=f'Peak: {labels[freq_conv.values.argmax()]} ads')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('reports/ads_frequency_curve.png', dpi=150)
plt.show()
print("✅ Chart 4 saved")

# ── Chart 5: Hour of Day Heatmap ─────────────────────────
hour_day = df.groupby(['most_ads_day', 'most_ads_hour'])['converted'].mean().unstack()

day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
hour_day  = hour_day.reindex(day_order)

fig, ax = plt.subplots(figsize=(16, 5))
sns.heatmap(
    hour_day,
    cmap='YlOrRd',
    ax=ax,
    linewidths=0.3,
    linecolor='white',
    cbar_kws={'label': 'Conversion Rate'},
    fmt='.3f',
    annot=False
)
ax.set_title('Conversion Rate by Day & Hour  (When to Show Ads)', fontsize=14, pad=15)
ax.set_xlabel('Hour of Day (0 = Midnight, 23 = 11pm)')
ax.set_ylabel('Day of Week')
plt.tight_layout()
plt.savefig('reports/hour_heatmap.png', dpi=150)
plt.show()
print("✅ Chart 5 saved")