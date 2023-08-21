import subprocess
import datetime
import os

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
        subprocess.run(["reprounzip", "docker", "setup", rpz_file, container_name], check=True)
    except subprocess.CalledProcessError:
        print(f"Error during reprounzip docker setup for {rpz_file}. Exiting.")
        return

    try:
        subprocess.run(["reprounzip", "docker", "run", container_name], check=True)
    except subprocess.CalledProcessError:
        print(f"Error during reprounzip docker run for {container_name}. Exiting.")
        return

    print(f"Unpacking and dockerization completed for {rpz_file}. Container name: {container_name}")

if __name__ == "__main__":
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
                    auto_unpack_and_dockerize(rpz_name)
