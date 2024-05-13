options(repos = c(CRAN = "https://cran.r-project.org"))
install.packages("reticulate")
library(reticulate)

use_python("/usr/bin/python3", required = TRUE)
env_name <- "python_env_for_r"
virtualenv_create(env_name)
use_virtualenv(env_name, required = TRUE)
py_install(c("grpcio", "grpcio-tools", "protobuf"), envname = env_name)

# ========== ABOVE SHOULD BE DONE DURING DOCKER BUILDING ==========

# Source the Python client
source_python("ResultsHubForR.py")

results_hub <- ResultsHubSubmission(1L)

int_list <- list(1, 2, 3, 4, 5)
results_hub$addVar("int_list", int_list)
results_hub$submit()

# Call the Python function
result <- fetchVarResult("int_list", 1L, "localhost")
print(result)