import subprocess
import datetime
import os
from collections import deque

class PodQueue:
    def __init__(self):
        self.queue = deque()

    def add_pod(self, pod_name):
        if self.queue:
            # if not empty,set last one as producer
            producer_pod = self.queue[-1]
            print(f"{producer_pod} is set as producer.")

        # adding new pod in the queue
        self.queue.append(pod_name)
        print(f"{pod_name} is added to the queue as consumer.")

    def get_consumer(self):
        return self.queue[0] if self.queue else None

def auto_pack(command, file):
    full_command = command + [file]
    try:
        subprocess.run(["reprozip", "trace"] + full_command, check=True)
    except subprocess.CalledProcessError:
        print(f"Error during reprozip trace for {file}. Exiting.")
        return

    rpz_name = f"experiment_{file.replace('/', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.rpz"

    try:
        subprocess.run(["reprozip", "pack", rpz_name], check=True)
    except subprocess.CalledProcessError:
        print(f"Error during reprozip pack for {file}. Exiting.")
        return

    print(f"Packing completed for {file}. Filename: {rpz_name}")
    return rpz_name

def auto_unpack_and_dockerize(rpz_file):
    container_name = f"container_{rpz_file.replace('/', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    try:
        result = subprocess.run(["reprounzip", "docker", "setup", rpz_file, container_name], check=True, stdout=subprocess.PIPE, text=True)

        # Extract the docker image name from the command output
        for line in result.stdout.split("\n"):
            if "Docker image" in line:
                docker_image_name = line.split()[-1]  # Get the last word, which should be the image name
                print(f"Docker Image Name: {docker_image_name}")
                break
    except subprocess.CalledProcessError:
        print(f"Error during reprounzip docker setup for {rpz_file}. Exiting.")
        return

    print(f"Unpacking and dockerization completed for {rpz_file}. Container name: {container_name}")

if __name__ == "__main__":
    pod_queue = PodQueue()
    directory = input("Enter the directory containing the files you want to trace, pack, unpack, and dockerize: ")

    # Mapping of file extensions to commands
    commands = {
        '.py': ['python'],
        '.java': ['java'],
        '.cpp': ['g++', '-o', 'output'],  # This compiles the C++ file. You might want to adjust this.
        '.c': ['gcc', '-o', 'output'],    # This compiles the C file. Adjust as needed.
        '.R': ['Rscript'],
        '.m': ['matlab', '-nodisplay', '-nosplash', '-r']  # This runs the MATLAB script. Adjust flags as needed.
    }

    for root, dirs, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in commands:
                full_path = os.path.join(root, file)
                rpz_name = auto_pack(commands[ext], full_path)
                if rpz_name:
                    container_name = auto_unpack_and_dockerize(rpz_name)
                    if container_name:
                        pod_queue.add_pod(container_name)
