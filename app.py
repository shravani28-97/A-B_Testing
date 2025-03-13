import os

# Using triple single-quotes for script_content, so we can freely use triple double-quotes inside the code.
script_content = '''import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    st.title("Difference-in-Differences Pricing Analysis (Enhanced)")

    st.write(\"\"\"
    **Welcome!** This app shows how changing a product's price (the "treatment") 
    affects outcomes like sales or revenue, compared to products that did not change price (the "control").
    
    Even if you’re not a data expert, don't worry: we'll guide you step by step!
    \"\"\")

    # 1. Data Upload
    st.header("1. Upload Your Data")
    uploaded_file = st.file_uploader("Upload your CSV data (with date, treatment, post, quantity_sold, etc.)", type="csv")
    if not uploaded_file:
        st.info("Please upload a CSV to proceed.")
        return

    df = pd.read_csv(uploaded_file, parse_dates=["date"])

    st.subheader("Quick Peek at Your Data")
    st.write(df.head(10))
    st.write(\"\"\"
    - **date**: the day of each observation  
    - **treatment**: 1 if a product is in the price-change group, 0 if it's in the control group  
    - **post**: 1 if the date is after the price change, 0 if before  
    - **quantity_sold** (or other outcome): how many units sold that day  
    \"\"\")

    # 2. Let user pick the outcome variable
    possible_outcomes = [
        col for col in df.columns
        if col not in ["treatment", "post", "date", "product_id"]
    ]
    outcome_var = st.selectbox(
        "Select the outcome variable you want to analyze (e.g., quantity_sold or revenue):",
        possible_outcomes,
        index=0
    )

    # 3. Fit the DiD Model
    st.header("2. Run the Difference-in-Differences Model")
    formula = f"{outcome_var} ~ treatment + post + treatment:post"
    st.markdown(f"**Using this regression formula**: `{formula}`")

    model = smf.ols(formula, data=df).fit()

    st.subheader("Statistical Results")
    st.text(model.summary())

    # 4. More In-Depth, Non-Technical Interpretation
    st.header("3. Business Interpretation (Non-Technical)")

    coefs = model.params
    pvals = model.pvalues
    conf_ints = model.conf_int()

    # Extract results
    intercept = coefs.get("Intercept", float("nan"))
    treat_coef = coefs.get("treatment", float("nan"))
    post_coef = coefs.get("post", float("nan"))
    did_coef = coefs.get("treatment:post", float("nan"))

    # Helper to format confidence intervals
    def ci_str(term):
        if term in conf_ints.index:
            low, high = conf_ints.loc[term]
            return f"[{low:.2f}, {high:.2f}]"
        return "[N/A, N/A]"

    st.markdown(f\"\"\"
    **Intercept** = **{intercept:.2f}**  
    - 95% CI: {ci_str('Intercept')}  
    This is the **baseline outcome** for the control group **before** the price change. 
    On a typical day in the pre-period, the control group averages around {intercept:.1f} {outcome_var}.
    \"\"\")

    st.markdown(f\"\"\"
    **Treatment** = **{treat_coef:.2f}**  
    - 95% CI: {ci_str('treatment')}  
    This shows **how much higher or lower** the treatment group was **before** the 
    price change, compared to the control group. 
    If it’s negative, the treatment group was selling fewer units than control (pre-change). 
    If positive, they were selling more.
    \"\"\")

    st.markdown(f\"\"\"
    **Post** = **{post_coef:.2f}**  
    - 95% CI: {ci_str('post')}  
    This reflects how the control group changed **after** the price-change date 
    (even though they did not actually change their price). 
    Think of it as general market shifts affecting everyone in the post period.
    \"\"\")

    st.markdown(f\"\"\"
    **Treatment x Post (DiD)** = **{did_coef:.2f}**  
    - 95% CI: {ci_str('treatment:post')}  
    This is the **extra change** the treatment group experienced, 
    above and beyond any general changes captured by 'post'. 
    - **Positive**: The treatment group improved more (or declined less) than the control group after the price change.
    - **Negative**: The treatment group declined more (or grew less) than the control group after the price change.
    \"\"\")

    st.write(\"\"\"
    In simpler terms:
    - **If 'treatment:post' is significantly positive**, raising the price might have increased revenue or didn't hurt sales much.
    - **If 'treatment:post' is significantly negative**, raising the price likely reduced sales more than if you hadn't changed the price.
    \"\"\")

    # 5. Visualizing Pre-Treatment Trends
    st.header("4. Check the 'Parallel Trends' (Pre‐Treatment)")
    st.write(\"\"\"
    Before we trust these results, let's ensure the treatment and control groups 
    were moving similarly before the price change—this is the "Parallel Trends" assumption.
    \"\"\")

    intervention_date = st.date_input("Pick your known intervention date:", value=df["date"].min())
    pre_df = df[df["date"] < pd.to_datetime(intervention_date)]
    if pre_df.empty:
        st.warning("No data before that intervention date, so we can't plot pre‐treatment trends.")
        return

    grouped_pre = pre_df.groupby(["date","treatment"])[outcome_var].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=grouped_pre, x="date", y=outcome_var, hue="treatment", ax=ax)
    ax.set_title(f"Average {outcome_var} Over Time (Pre‐Treatment)")
    ax.set_xlabel("Date")
    ax.set_ylabel(f"Avg {outcome_var}")
    st.pyplot(fig)

    st.write(\"\"\"
    - If these lines move **roughly in parallel** (though offset), 
      the assumption is likely satisfied.
    - If they diverge a lot pre-change, the DiD estimate might be biased.
    \"\"\")

    st.markdown(\"\"\"---
    **Thank you for using this app!**

    If you have questions about how to interpret these results, 
    think of 'treatment:post' as the crucial measure of whether 
    changing your price helped or hurt you compared to not changing.
    \"\"\")

if __name__ == "__main__":
    main()
'''
