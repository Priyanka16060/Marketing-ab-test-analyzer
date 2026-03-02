from statsmodels.stats.proportion import proportions_ztest
import numpy as np
import pandas as pd

df = pd.read_csv('data/marketing_clean.csv')

psa_group = df[df['test_group'] == 'psa']   
ad_group  = df[df['test_group'] == 'ad']    # treatment

n_psa = len(psa_group)
n_ad  = len(ad_group)
conv_psa = psa_group['converted'].sum()
conv_ad  = ad_group['converted'].sum()

# Two-proportion Z-test
count = np.array([conv_ad, conv_psa])
nobs  = np.array([n_ad, n_psa])
z_stat, p_value = proportions_ztest(count, nobs)

# Conversion rates and lift
p_psa = conv_psa / n_psa
p_ad  = conv_ad  / n_ad
diff  = p_ad - p_psa
se    = np.sqrt(p_psa*(1-p_psa)/n_psa + p_ad*(1-p_ad)/n_ad)
ci_low, ci_high = diff - 1.96*se, diff + 1.96*se
relative_lift   = (p_ad - p_psa) / p_psa * 100

print(f"PSA (control) rate:  {p_psa:.4f} ({p_psa*100:.2f}%)")
print(f"Ad (treatment) rate: {p_ad:.4f}  ({p_ad*100:.2f}%)")
print(f"Absolute lift:       {diff*100:.3f}%")
print(f"Relative lift:       {relative_lift:.2f}%")
print(f"Z-statistic:         {z_stat:.4f}")
print(f"P-value:             {p_value:.6f}")
print(f"95% CI:              [{ci_low:.4f}, {ci_high:.4f}]")

if p_value < 0.05:
    print("✓ REJECT null — ads significantly improve conversions")
else:
    print("✗ FAIL to reject null — no significant ad effect")
    
from statsmodels.stats.power import NormalIndPower

analysis = NormalIndPower()
power = analysis.power(
    effect_size=diff / np.sqrt(p_psa*(1-p_psa)),
    nobs1=n_psa,
    alpha=0.05
)
print(f"Statistical Power: {power:.3f}")
   