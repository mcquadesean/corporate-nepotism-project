library(stargazer)
library(dplyr)
library(lmtest)
library(readxl)
data <- read_excel(".../24_month_lag_robust.xlsx")

# interaction var
data$treat_time <- data$treatment * data$time

# run regression
model24robust <- lm(score ~ treatment + time + treat_time + log(employees) + log(market_cap) + information_technology + communication_services + health_care + energy + industrials + financials + consumer_staples + consumer_discretionary + real_estate + utilities, data=data)

# viewing results
summary(model24robust)

stargazer(model24robust, type = "text", title = "Regression Results: 24 Month Lagged Dependent Variable", align = TRUE)
