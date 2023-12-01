# Solar Energy Scenario Generation

To derive hourly data from the installed capacities of solar generation, we use a series of regression models that capture yearly, weekly, and daily seasonality.

Denote hours $\mathcal{H}$ as the set of days that are holidays, $\mathcal{W}_j$ as the set of days that are weekday $j$, $h$ as the hour of the day, and $d$ as a day from the training and scenario data. 

For power generation from solar the regression model considers seasonal variation using multiple trigonometric terms with a maximum cycle length of 365 days. We fit a separate model for each hour of the day. The resulting regression model is given by

$Y_{dh} = \beta^0_{h} + \beta^1_{h}d + \sum_{i = 1}  \left( \beta^4_{hi} \sin\left(\frac{di 2\pi}{365}\right) + \beta^5_{hi} \cos\left(\frac{di 2\pi}{365}\right)\right)$

After fitting the model to the data, we calculate the prediction errors using historical data. These errors are then further analyzed using clustering techniques. The aim is to group errors that are similar in magnitude. For this purpose, we employed the KMeans algorithm, a widely-used unsupervised clustering method known for its efficiency and effectiveness.

Subsequently, we construct a Markov chain in which each state represents a different cluster of prediction errors. The transition probabilities between these states are determined by analyzing the sequence of error clusters over time in the historical data. We define a transition matrix $T$ of size $k \times k$ (where $k$ is the number of clusters), which represents the probabilities of transitioning from one cluster to another in consecutive time periods.

With established regression models and an understanding of error patterns and transitions through clustering, we have performed simulations for future time periods. For the simulation process, we utilized the transition matrix derived from the clustering analysis to simulate the sequence of states (clusters) for a future time period. Starting from a randomly selected initial state, the simulation proceeded by selecting the next state based on the transition probabilities. For each state, a representative error pattern was randomly selected from the corresponding cluster and applied to adjust the values predicted by the regression models. This process was repeated to generate a sequence of hourly data for the desired number of days.

The simulation enabled us to create future scenarios that reflect not only the patterns captured by the regression models but also the randomness and state transitions identified in the clustering analysis.
