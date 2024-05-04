import nbformat
import os

def extract_imports_from_code(code):
    """
    Extracts R package names from the notebook code cells where 'library' or 'require' are used.
    """
    imports = set()
    lines = code.split('\n')
    for line in lines:
        line = line.strip()
        if 'library(' in line:
            package_name = line.split('library(')[1].split(')')[0].strip().replace("'", "").replace('"', '')
            if package_name:
                imports.add(package_name)
        elif 'require(' in line:
            package_name = line.split('require(')[1].split(')')[0].strip().replace("'", "").replace('"', '')
            if package_name:
                imports.add(package_name)
    return imports



def save_cells_to_files(notebook, output_directory):
    """
    Saves each R code cell to a separate .R file.
    """
    os.makedirs(output_directory, exist_ok=True)
    valid_cell_index = 1
    for cell in notebook.cells:
        if cell.cell_type == 'code' and cell.source.strip():
            cell_file_path = os.path.join(output_directory, f"cell{valid_cell_index}.R")
            with open(cell_file_path, 'w', encoding='utf-8') as cell_file:
                cell_file.write(cell.source)
            valid_cell_index += 1

def save_requirements(imports, output_directory):
    """
    Creates a .R script to install all extracted R packages.
    """
    requirements_path = os.path.join(output_directory, 'install_packages.R')
    with open(requirements_path, 'w', encoding='utf-8') as file:
        for imp in imports:
            file.write(f'install.packages("{imp}")\n')

def process_notebook(notebook_path, output_directory):
    """
    Main function to process the R notebook.
    """
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    all_imports = set()
    for cell in nb.cells:
        if cell.cell_type == 'code':
            cell_imports = extract_imports_from_code(cell.source)
            all_imports.update(cell_imports)

    save_cells_to_files(nb, output_directory)
    save_requirements(all_imports, output_directory)
    print(f"Processed notebook. Files saved in {output_directory}")

# Example usage:
notebook_path = './example/Rexample.ipynb'
output_directory = './execution'
process_notebook(notebook_path, output_directory)
