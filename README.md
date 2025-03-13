# Pricing Analytics App

Analyze how price changes impact product sales or revenue with an easy, interactive Streamlit app.

Overview

This repository contains a Streamlit application that uses a Difference-in-Differences (DiD) approach to measure the causal effect of a price change on outcomes like quantity sold or revenue. Even non‐technical users can upload their data and see business-friendly interpretations of the results.

Features
CSV Upload: Easily upload your own dataset (with columns like date, treatment, post, quantity_sold, etc.).
Automatic DiD Regression: The app estimates the treatment effect using statsmodels under the hood.
Plain-English Interpretations: Each coefficient is explained in non‐technical terms for managers or stakeholders.
Parallel Trends Check: Visualize pre‐intervention trends to validate the DiD assumption.
Demo

Usage Guide

Upload your CSV
Must contain at least:
date (converted to datetime)
treatment (1 if product is in price-change group, 0 if control)
post (1 if date >= intervention date, 0 if before)
quantity_sold (or your main outcome)
Choose Outcome Variable
Select “quantity_sold” or “revenue” (or any numeric column) as the dependent variable.
Interpret the Results
The app runs a Difference-in-Differences model and displays each coefficient in plain language.
Key metric is treatment:post:
Positive → The treatment group’s outcome increases more than the control (net effect).
Negative → The treatment group’s outcome decreases more than the control, suggesting the price change might have hurt sales.
Check Parallel Trends
The app plots average pre‐treatment outcomes for both groups.
If lines are roughly parallel before the price change, the DiD approach is more valid.
Project Structure

Difference_in_Difference_App

├─ new_apps.py               # The main Streamlit app file

├─ requirements.txt      # List of Python dependencies

└─ README.md             # This file





Have ideas or bug fixes?

Fork this repo
Create a branch for your feature/fix
Submit a Pull Request (PR) to discuss and merge your changes
License

Author: Shravani Immidi
