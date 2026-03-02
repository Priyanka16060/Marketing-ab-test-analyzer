import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.stats.proportion import proportions_ztest
import numpy as np

st.set_page_config(page_title="Marketing A/B Test Analyzer", layout="wide")

st.title("Marketing A/B Test Analyzer")
st.caption("Did ads outperform PSA? — 588K+ user sessions analyzed")
st.divider()

@st.cache_data
def load_data():
    df = pd.read_csv('data/marketing_clean.csv')
    return df

df = load_data()

st.sidebar.header("⚙ Test Parameters")
alpha = st.sidebar.slider("Significance Level (α)", 0.01, 0.10, 0.05)

st.sidebar.subheader("💰 Business Impact Calculator")
monthly_users = st.sidebar.number_input("Monthly Ad Impressions",
                                         value=1000000, step=100000)
order_value   = st.sidebar.number_input("Average Order Value ($)",
                                         value=50, step=5)

psa = df[df['test_group'] == 'psa']
ad  = df[df['test_group'] == 'ad']

n_psa    = len(psa)
n_ad     = len(ad)
conv_psa = psa['converted'].sum()
conv_ad  = ad['converted'].sum()

p_psa = conv_psa / n_psa
p_ad  = conv_ad  / n_ad
diff  = p_ad - p_psa
lift  = (p_ad - p_psa) / p_psa * 100

_, p_val = proportions_ztest(
    [conv_ad, conv_psa],
    [n_ad,    n_psa]
)

extra_conv     = diff * monthly_users
revenue_impact = extra_conv * order_value

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("PSA Conversion",  f"{p_psa:.2%}")
c2.metric("Ad Conversion",   f"{p_ad:.2%}")
c3.metric("Relative Lift",   f"{lift:.1f}%")
c4.metric("P-value",         f"{p_val:.6f}")
c5.metric("Monthly Revenue Impact", f"${revenue_impact:,.0f}")

if p_val < alpha:
    st.success(" Ads significantly outperform PSA — CONTINUE RUNNING ADS")
else:
    st.error("  No significant difference detected — RECONSIDER AD SPEND")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Conversion Rate: Ad vs PSA")
    summary = df.groupby('test_group')['converted'].mean().reset_index()
    summary.columns = ['Group', 'Conversion Rate']
    fig1 = px.bar(summary, x='Group', y='Conversion Rate',
                  color='Group',
                  color_discrete_map={'ad':'#1a3d6b','psa':'#c84b11'},
                  text=summary['Conversion Rate'].apply(lambda x: f"{x:.2%}"))
    fig1.update_traces(textposition='outside')
    fig1.update_layout(showlegend=False, yaxis_tickformat='.2%')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Conversion by Day of Week")
    day_order = ['Monday','Tuesday','Wednesday',
                 'Thursday','Friday','Saturday','Sunday']
    day_conv = df.groupby('most_ads_day')['converted']\
                 .mean().reindex(day_order).reset_index()
    day_conv.columns = ['Day', 'Conversion Rate']
    fig2 = px.bar(day_conv, x='Day', y='Conversion Rate',
                  color='Conversion Rate', color_continuous_scale='Reds',
                  text=day_conv['Conversion Rate'].apply(lambda x: f"{x:.2%}"))
    fig2.update_traces(textposition='outside')
    fig2.update_layout(yaxis_tickformat='.2%', coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader("Ad Frequency vs Conversion (Fatigue Analysis)")
    ad_users = df[df['test_group'] == 'ad'].copy()
    bins   = [0,5,10,20,40,80,150,300,2000]
    labels = ['1-5','6-10','11-20','21-40','41-80','81-150','151-300','300+']
    ad_users['ads_bin'] = pd.cut(ad_users['total_ads'],
                                  bins=bins, labels=labels)
    freq_conv = ad_users.groupby('ads_bin', observed=False)['converted']\
                        .mean().reset_index()
    freq_conv.columns = ['Ads Seen', 'Conversion Rate']
    fig3 = px.line(freq_conv, x='Ads Seen', y='Conversion Rate',
                   markers=True, color_discrete_sequence=['#c84b11'])
    fig3.update_traces(marker=dict(size=10), line=dict(width=2.5))
    fig3.update_layout(yaxis_tickformat='.2%')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Conversion Heatmap: Day × Hour")
    hour_day = df.groupby(['most_ads_day','most_ads_hour'])['converted']\
                 .mean().unstack()
    hour_day = hour_day.reindex(day_order)
    fig4 = px.imshow(hour_day,
                     color_continuous_scale='YlOrRd',
                     aspect='auto',
                     labels=dict(x='Hour of Day', y='Day of Week',
                                 color='Conv. Rate'))
    fig4.update_layout(xaxis_title='Hour of Day (0=Midnight)')
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

with st.expander("View Raw Summary Data"):
    summary_full = df.groupby('test_group').agg(
        Users=('user_id','count'),
        Conversions=('converted','sum'),
        Conversion_Rate=('converted','mean'),
        Avg_Ads_Seen=('total_ads','mean')
    ).reset_index()
    summary_full['Conversion_Rate'] = summary_full['Conversion_Rate']\
                                       .apply(lambda x: f"{x:.2%}")
    summary_full['Avg_Ads_Seen']    = summary_full['Avg_Ads_Seen']\
                                       .apply(lambda x: f"{x:.1f}")
    st.dataframe(summary_full, use_container_width=True)

st.caption("Dataset: Marketing A/B Testing | faviovaz | Kaggle · "
           "Analysis: Two-proportion Z-test | α = 0.05")