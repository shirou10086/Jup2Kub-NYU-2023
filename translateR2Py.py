
import os
import openai

from openai import OpenAI
client = OpenAI(
    # This is the default and can be omitted,put your api here
    api_key="xxx",
)
def translate_r_to_python_using_gpt4(file_path):
    if not file_path.endswith('.R'):
        return None, "Not an R script"

    try:
        with open(file_path, 'r') as file:
            r_script_content = file.read()
    except Exception as e:
        return None, f"Error reading file: {str(e)}"

    prompt = f"Translate the following R script to Python using rpy2:\n\n{r_script_content},Only Output: __(python code)"

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert in translating R to python code, and only output code, no explanation!"},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4",
            max_tokens=300
        )
        python_code = response.choices[0].message.content.strip()
        return python_code, None
    except Exception as e:
        return None, f"Error occurred while translating. Error: {str(e)}"

def translate_directory_r_to_py(directory_path):
    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.startswith('cell') and filename.endswith('.R'):
            file_path = os.path.join(directory_path, filename)
            python_code, error = translate_r_to_python_using_gpt4(file_path)
            if error:
                print(f"Error processing {filename}: {error}")
            else:
                # Remove first and last lines if they contain specific markdown for code blocks
                lines = python_code.split('\n')
                if lines[0].strip() == '```python':
                    lines = lines[1:]  # Remove the first line
                if lines[-1].strip() == '```':
                    lines = lines[:-1]  # Remove the last line

                output_file_path = os.path.join(directory_path, filename.replace('.R', '.py'))
                with open(output_file_path, 'w') as py_file:
                    py_file.write('\n'.join(lines))  # Write the modified code lines
                print(f"Translated {filename} to {output_file_path}")

                # Delete the original R file
                os.remove(file_path)
                print(f"Deleted original file: {filename}")
