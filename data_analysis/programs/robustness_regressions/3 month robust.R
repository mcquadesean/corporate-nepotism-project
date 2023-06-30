library(stargazer)
library(dplyr)
library(lmtest)
library(readxl)
data <- read_excel("C:/Users/user/Documents/Honors Thesis/regressions/robustness regs/3/3_month_lag_robust.xlsx")

# interaction var
data$treat_time <- data$treatment * data$time

# run regression
model3robust <- lm(score ~ treatment + time + treat_time + log(employees) + log(market_cap) + information_technology + communication_services + health_care + energy + industrials + financials + consumer_staples + consumer_discretionary + real_estate + utilities, data=data)

# viewing results
summary(model3robust)

stargazer(model3robust, type = "text", title = "Regression Results: 3 Month Lagged Dependent Variable", align = TRUE)
