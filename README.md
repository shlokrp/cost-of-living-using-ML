# Cost of Living Prediction

## Overview

This project focuses on forecasting **future cost of living values** across global cities using advanced **data science** and **machine learning techniques**. It integrates historical datasets, inflation rates, and user inputs (such as lifestyle preferences and demographics) to provide **personalized cost of living predictions**.

A **web-based interface** was developed to ensure accessibility and usability, featuring an interactive dashboard with data visualizations and city-to-city comparisons.

---

## Features

* Forecasting cost of living using multiple ML models:

  * ARIMA
  * SARIMA
  * LSTM
  * Exponential Smoothing
  * Polynomial Regression
  * Ensemble Models

* **Data Integration**

  * Historical cost of living data (2000–2022)
  * Inflation rates
  * User lifestyle preferences

* **Web Application**

  * Built with Flask (Python) backend
  * Frontend with HTML, CSS, and JavaScript
  * Covers over **3000 cities worldwide**
  * Personalized predictions and trend visualizations

* **Visualization Dashboard**

  * City-to-city comparisons
  * Historical and forecasted trends
  * Graphical representations of cost dynamics

---

## Methodology

1. **Data Collection** – Global cost of living dataset (2022 base year) + inflation rates (2000–2022).
2. **Preprocessing** – Handling missing values, outliers, and normalization.
3. **Exploratory Data Analysis (EDA)** – Identifying patterns and correlations.
4. **Feature Engineering** – Creating informative variables for better predictions.
5. **Model Development** – Implementing time series and machine learning models.
6. **Validation** – Using MAE and MAPE for accuracy assessment.
7. **Integration** – Incorporating user preferences and inflation trends.
8. **Deployment** – Flask-based web app with interactive dashboard.
9. **Continuous Improvement** – Updates based on user feedback and evolving data.

---

## Results

* **Best performing models**:

  * SARIMA (up to 94.3% accuracy)
  * Exponential Smoothing (average 90%+ accuracy globally)
* Ensemble models showed stable results across different time ranges.
* Forecasts tailored to both **macro-level city trends** and **individual user needs**.

---

## Challenges

* Limited availability of historical cost of living datasets.
* Heavy reliance on inflation rates as a major factor.
* Integration of models with a real-time web interface.
* Computational challenges while forecasting for 3000+ cities.

---

## Future Improvements

* Acquire larger and more granular datasets (multi-year, intra-city).
* Incorporate additional economic indicators (wages, housing, demographics).
* Enhance validation with more real-world testing data.
* Expand visualization capabilities for deeper user insights.
* Optimize backend for faster large-scale forecasting.

---

## Tech Stack

* **Programming**: Python
* **Frameworks**: Flask, NumPy, Pandas, Scikit-learn, Statsmodels, TensorFlow/Keras
* **Frontend**: HTML, CSS, JavaScript
* **Visualization**: Matplotlib, Plotly
* **Deployment**: Flask-based web interface

