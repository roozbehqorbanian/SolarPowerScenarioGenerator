import pandas as pd
import plotly.express as px
from sklearn.preprocessing import QuantileTransformer
import holidays
from solar_regression import SolarRegression
from solar_scenario_plots import solar_scenario_plots
from generate_scenarios import generate_scenarios
from transition_matrix_generation import perform_clustering_and_create_transition_matrix

config = {
    "num_scenarios": 10,  # Number of solar generation scenarios to generate
    "scenario_start_date": "2025-04-07 00:00", # The start date for creating scenarios
    "periods": 26,  # Number of weeks for scenario projection after the start date
    "cluster_count": 4, # Number of clusters for the errors and creating a transition matrix
    "transition_frequency": "2W",
    "train_data": "Spain_Solar_Generation_and_Capacity_Historical.xlsx" # Name of the excel file for historical data
}

# Calculate number of periods based on transition frequency
config["number_of_periods"] = 24 * pd.Timedelta(config["transition_frequency"]).days


# Read and preprocess data
data = (pd.read_excel(config['train_data'], index_col=0, parse_dates=True)
        .set_index("datetime")
        .interpolate())

solar_capacity = data.solar_capacity
df = data.copy()
df.solar /= solar_capacity

# Spanish Holidays
spanish_holidays = holidays.Spain()

# Quantile Transformation
qt = QuantileTransformer(n_quantiles=100, output_distribution="normal")
Y = pd.DataFrame(qt.fit_transform(df), index=df.index, columns=df.columns)

# Error Calculation and Solar Regression
prediction_errors = Y.copy()
datetime = Y.index
y = Y.solar
solar_reg = SolarRegression()
solar_reg.fit(datetime, y)
solar_predictions = solar_reg.predict(datetime)
prediction_errors["solar"] = y - solar_predictions

# Plotting Solar Prediction
solar_prediction_plot = px.line(x="datetime", y=["solar", "prediction"], data_frame=y.reset_index().assign(prediction=solar_predictions))
solar_prediction_plot.show()


n, p = prediction_errors.shape
clipsize = (n // config["number_of_periods"]) * config["number_of_periods"]
errors = prediction_errors.values[:clipsize].reshape((n // config["number_of_periods"], p * config["number_of_periods"]))

# Performs KMeans clustering on the provided error data and creates a transition matrix.
kmeans_model, transition_matrix = perform_clustering_and_create_transition_matrix(errors, config["cluster_count"])

# Scenario Generation
scenarios = generate_scenarios(config, p, kmeans_model, transition_matrix, errors,prediction_errors,solar_reg,qt,solar_capacity)

# Plot the scenarios
solar_scenario_plots(scenarios, 'solar_Generation', 'rgb(255, 161, 65)', 'rgb(255, 242, 228)', 'rgb(255, 128, 0)',
              'Solar Generation Scenarios', 'MW')