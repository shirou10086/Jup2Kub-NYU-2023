import subprocess
import sys
import os

def trace_and_pack_notebook(notebook_path):
    """跟踪并打包 Jupyter Notebook"""
    try:
        print(f"正在跟踪 {notebook_path}...")
        subprocess.run(["reprozip-jupyter", "trace", notebook_path], check=True)

        rpz_file = "notebook_environment.rpz"
        print("正在打包环境...")
        subprocess.run(["reprozip", "pack", rpz_file], check=True)

        return rpz_file
    except subprocess.CalledProcessError as e:
        print(f"错误：{e}")
        sys.exit(1)

def convert_to_docker_image(rpz_file, image_name="notebook_environment"):
    """将打包的环境转换为 Docker 镜像"""
    unpack_dir = "/tmp/notebook_unpack"
    if not os.path.exists(unpack_dir):
        os.makedirs(unpack_dir)

    try:
        print("正在转换为 Docker 镜像...")
        subprocess.run(["reprounzip", "docker", "setup", rpz_file, unpack_dir], check=True)

        os.chdir(unpack_dir)
        subprocess.run(["docker", "build", "-t", image_name, "."], check=True)
    except subprocess.CalledProcessError as e:
        print(f"错误：{e}")
        sys.exit(1)

def run_docker_container(image_name="notebook_environment"):
    """运行 Docker 镜像"""
    try:
        print("正在运行 Docker 容器...")
        subprocess.run(["docker", "run", "-p", "8888:8888", image_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"错误：{e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法：python main.py [ipynb文件路径]")
        sys.exit(1)

    notebook_path = sys.argv[1]
    rpz_file = trace_and_pack_notebook(notebook_path)
    convert_to_docker_image(rpz_file)
    # 运行下面的函数将直接启动容器，这可能不是你每次都想做的事情。
    # run_docker_container()
