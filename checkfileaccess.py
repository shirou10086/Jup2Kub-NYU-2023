library(magrittr)
library(stringr)

# Function to collect called functions from an R file
collect_called_functions_from_file <- function(filename) {
  code <- readLines(filename)
  # Use regex to extract function calls
  calls <- str_extract_all(code, "\\b[a-zA-Z0-9_.]+(?=\\()") %>% unlist()
  # Filter out NA and make the function calls unique
  unique(na.omit(calls))
}

# Check if any of the called functions are related to file access operations
checks_file_access <- function(called_functions) {
  file_operations <- c('read.csv', 'write.csv', 'readLines', 'writeLines', 'file', 'file.create',
                       'file.remove', 'file.rename', 'file.copy', 'dir.create', 'unlink',
                       'readRDS', 'saveRDS', 'load', 'save', 'download.file', 'read.xlsx', 'write.xlsx')
  any(called_functions %in% file_operations)
}

# Generate a report about file access
generate_file_access_report <- function(directory_path = "./execution", report_file_path = "./execution/fileaccess.txt", file_prefix = "cell", file_extension = ".R", file_count = 10) {
  accessed_files <- character()

  for (i in 1:file_count) {
    file_path <- file.path(directory_path, paste0(file_prefix, i, file_extension))
    if (file.exists(file_path)) {
      called_functions <- collect_called_functions_from_file(file_path)
      if (checks_file_access(called_functions)) {
        accessed_files <- c(accessed_files, basename(file_path))
      }
    }
  }

  writeLines(sapply(accessed_files, tools::file_path_sans_ext), report_file_path)
}

# Example usage
# generate_file_access_report()
