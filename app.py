import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    st.title("Difference-in-Differences Pricing Analysis (NEW VERSION)")

    st.write("""
    **HELLO FROM MY NEW APP** – This text helps confirm you're seeing the updated version.
    This app demonstrates a simple DiD analysis to see how a price change (treatment) 
    impacts quantity sold or revenue.
    """)

    # 1. Data Upload
    st.subheader("1. Data Upload")
    uploaded_file = st.file_uploader("Upload your CSV data", type="csv")
    if not uploaded_file:
        st.info("Please upload a CSV file with columns: date, treatment, post, quantity_sold, etc.")
        return

    df = pd.read_csv(uploaded_file, parse_dates=["date"])
    st.subheader("2. Quick Data Preview")
    st.write(df.head(10))

    # 2. Let user select an outcome variable
    possible_outcomes = [col for col in df.columns if col not in ["treatment", "post", "date", "product_id"]]
    outcome_var = st.selectbox("Select outcome variable for DiD model:", possible_outcomes, index=0)

    # 3. Run DiD Regression
    st.subheader("3. Run the Difference-in-Differences Model")
    formula = f"{outcome_var} ~ treatment + post + treatment:post"
    model = smf.ols(formula, data=df).fit()
    st.write(f"**Model Formula**: `{formula}`")
    st.text(model.summary())

    # 4. Quick Business Interpretation
    st.subheader("4. Business Interpretation")
    coefs = model.params
    pvals = model.pvalues

    # Extract terms safely
    intercept = coefs.get("Intercept", float("nan"))
    treat_coef = coefs.get("treatment", float("nan"))
    post_coef = coefs.get("post", float("nan"))
    did_coef = coefs.get("treatment:post", float("nan"))

    st.markdown(f"""  
    **Intercept**: {intercept:.2f}  
    - Baseline outcome for control (pre-period).

    **Treatment**: {treat_coef:.2f}  
    - Difference between treatment & control in pre-period.

    **Post**: {post_coef:.2f}  
    - Change for control in post-period.

    **Treatment x Post (DiD)**: {did_coef:.2f}  
    - Additional effect for treatment group after intervention 
      (beyond control's post change).

    *Negative DiD means the treatment group dropped more than control; 
    positive means treatment group rose more.* 
    """)

    # 5. Parallel Trends Visualization
    st.subheader("5. Parallel Trends Visualization (Pre‐Treatment)")
    intervention_date = st.date_input("Intervention Date", value=df["date"].min())
    pre_df = df[df["date"] < pd.to_datetime(intervention_date)]
    if pre_df.empty:
        st.warning("No data before the chosen intervention date, so cannot plot pre‐treatment trends.")
        return

    grouped_pre = pre_df.groupby(["date","treatment"])[outcome_var].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=grouped_pre, x="date", y=outcome_var, hue="treatment", ax=ax)
    ax.set_title(f"Average {outcome_var} Over Time (Pre‐Treatment)")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
