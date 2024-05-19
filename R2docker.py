import os
import subprocess
import sys
import re


def get_version_r(default_version='4.4.0'):
    """
    Retrieve the R version using the Rscript command. If unable to retrieve, return the default version.
    Make sure to add R in system PATH!
    """
    try:
        result = subprocess.run(['Rscript', '--version'], capture_output=True, text=True)
        version_line = result.stdout.split('\n')[0]
        # 使用正则表达式提取版本号
        match = re.search(r"\b\d+\.\d+\.\d+\b", version_line)
        if match:
            print("Matching"+match.group(0))
            return match.group(0)
        print("UnMatching"+match.group(0))
    except FileNotFoundError as e:
        print(f"Error: Rscript not found. Ensure R is installed and in your PATH. Using default version {default_version}. Error: {e}")
    except Exception as e:
        print(f"Error retrieving R version, using default version {default_version}. Error: {e}")

    return default_version


def create_dockerfile_r(file_name, requirements_path, dockerfiles_path, r_version):
    dockerfile_content = f'''
    FROM r-base:{r_version}
    WORKDIR /app

    # Copy all necessary files
    COPY {file_name} /app
    COPY ResultsHub.py /app
    COPY ResultsHubForR.py /app
    COPY J2kResultsHub_pb2.py /app
    COPY J2kResultsHub_pb2_grpc.py /app
    COPY {requirements_path} /app
    COPY install_packages.R /app

    # Install R dependencies
    RUN Rscript install_packages.R

    # Set the command to run the R script
    CMD ["Rscript", "/app/{os.path.basename(file_name)}"]
    '''

    dockerfile_path = os.path.join(dockerfiles_path, f"Dockerfile_{file_name.split('.')[0]}")
    with open(dockerfile_path, 'w') as file:
        file.write(dockerfile_content)
    return dockerfile_path


def build_docker_image_r(dockerfile_path, image_tag, context_path):
    print('Creating docker image...')
    try:
        subprocess.run(["docker", "build", "-f", dockerfile_path, "-t", image_tag, context_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during Docker image build: {e}")
'''
# Example usage
output_dir = './execution'
requirements_path = os.path.join(output_dir, 'install_packages.R')
dockerfiles_path = os.path.join(output_dir, 'docker')
r_version = get_version_r()

os.makedirs(dockerfiles_path, exist_ok=True)

for file in os.listdir(output_dir):
    if file.endswith('.R') and file.startswith('cell'):
        dockerfile_path = create_dockerfile_r(file, 'install_packages.R', dockerfiles_path, r_version)
        build_docker_image_r(dockerfile_path, f"{file.split('.')[0]}", output_dir)
'''
