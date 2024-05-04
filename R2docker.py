import os
import subprocess

def get_r_version(default_version='4.4.0'):
    """
    Retrieve the R version using the Rscript command. If unable to retrieve, return the default version.
    Make sure add R in sys PATH!
    """
    try:
        result = subprocess.run(['R', '--version'], capture_output=True, text=True)
        version_line = result.stdout.split('\n')[0]
        version = version_line.split()[2]
        return version
    except Exception as e:
        print(f"Error retrieving R version, using default version {default_version}. Error: {e}")
        return default_version

def create_dockerfile(file_name, requirements_path, dockerfiles_path, r_version):
    dockerfile_content = f'''
    FROM r-base:{r_version}
    WORKDIR /app
    COPY . /app
    RUN apt-get update && apt-get install -y libcurl4-openssl-dev libssl-dev
    RUN Rscript install_packages.R
    CMD ["Rscript", "{os.path.basename(file_name)}"]
    '''

    dockerfile_path = os.path.join(dockerfiles_path, f"Dockerfile_{file_name.split('.')[0]}")
    with open(dockerfile_path, 'w') as file:
        file.write(dockerfile_content)
    return dockerfile_path


def build_docker_image(dockerfile_path, image_tag, context_path):
    print('Creating docker image...')
    try:
        subprocess.run(["docker", "build", "-f", dockerfile_path, "-t", image_tag, context_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during Docker image build: {e}")

# Example usage
output_dir = './execution'
requirements_path = os.path.join(output_dir, 'install_packages.R')
dockerfiles_path = os.path.join(output_dir, 'docker')
r_version = get_r_version()

os.makedirs(dockerfiles_path, exist_ok=True)

for file in os.listdir(output_dir):
    if file.endswith('.R') and file.startswith('cell'):
        dockerfile_path = create_dockerfile(file, 'install_packages.R', dockerfiles_path, r_version)
        build_docker_image(dockerfile_path, f"{file.split('.')[0]}", output_dir)
