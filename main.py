library(jsonlite)
library(httr)

# Load configuration from a JSON file
load_config <- function(file_path) {
  config <- fromJSON(file_path)
  return(config)
}

# Run a system command and capture output
run_system_command <- function(command) {
  tryCatch({
    output <- system(command, intern = TRUE)
    cat("Command output:\n", output, "\n")
  }, error = function(e) {
    cat("Error running command:", e$message, "\n")
  })
}

build_and_push_docker <- function(dockerfile_path, image_name_tag) {
  build_command <- sprintf("docker build -t %s %s", image_name_tag, dockerfile_path)
  push_command <- sprintf("docker push %s", image_name_tag)

  run_system_command(build_command)
  run_system_command(push_command)
}

main <- function(config_file) {
  config <- load_config(config_file)

  dockerfiles_path <- config$execution$dockerfiles_path
  output_dir <- config$execution$output_dir
  dockerhub_username <- config$execution$dockerhub_username
  dockerhub_repository <- config$execution$dockerhub_repository

  image_name_tag <- sprintf("%s/%s:latest", dockerhub_username, dockerhub_repository)
  build_and_push_docker(dockerfiles_path, image_name_tag)
}

main("J2K_CONFIG.json")
