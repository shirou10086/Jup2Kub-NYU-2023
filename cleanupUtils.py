# Function to delete a Kubernetes job
delete_job <- function(job_name, namespace) {
  command <- sprintf('kubectl delete job %s --namespace %s', job_name, namespace)
  output <- system(command, intern = TRUE)
  cat("Output:\n", output, "\n")
}

# Function to delete a persistent volume
delete_local_pv <- function(pv_name) {
  command <- sprintf('kubectl delete pv %s', pv_name)
  output <- system(command, intern = TRUE)
  cat("Output:\n", output, "\n")
}

# Function to delete a persistent volume claim
delete_pvc <- function(pvc_name, namespace) {
  command <- sprintf('kubectl delete pvc %s --namespace %s', pvc_name, namespace)
  output <- system(command, intern = TRUE)
  cat("Output:\n", output, "\n")
}

# Function to delete a stateful set
delete_statefulset <- function(statefulset_name, namespace) {
  command <- sprintf('kubectl delete statefulsets %s --namespace %s', statefulset_name, namespace)
  output <- system(command, intern = TRUE)
  cat("Output:\n", output, "\n")
}

# Function to delete a Kubernetes service
delete_service <- function(service_name, namespace) {
  command <- sprintf('kubectl delete service %s --namespace %s', service_name, namespace)
  output <- system(command, intern = TRUE)
  cat("Output:\n", output, "\n")
}

# Example usage:
# delete_job("example-job", "default")
# delete_local_pv("example-pv")
# delete_pvc("example-pvc", "default")
# delete_statefulset("example-set", "default")
# delete_service("example-service", "default")
