install.packages("ggplot2", repos="http://cran.rstudio.com/")

# set python path
library(reticulate)
use_virtualenv("/root/.virtualenvs/r-reticulate", required = TRUE)
