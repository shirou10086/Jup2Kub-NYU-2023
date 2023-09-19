import subprocess
import storage

def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        print(e.stderr)

def build_docker_image(image_name, tag, docker_file="Dockerfile"):
    print("Building Docker image...")
    run_command(["docker", "build", "-t", f"{image_name}:{tag}", "-f", docker_file, "."])

def push_docker_image(image_name, tag):
    print("Pushing Docker image to repository...")
    run_command(["docker", "push", f"{image_name}:{tag}"])

def deploy_to_kubernetes(image_name, tag):
    pv, pvc = storage.create_efs_pv_pvc("my-efs", "default", "fs-0fe8790d8133d66cf.efs.eu-west-2.amazonaws.com")

    with open("efs-pv.yaml", "w") as file:
        file.write(pv)

    with open("efs-pvc.yaml", "w") as file:
        file.write(pvc)

    run_command(["kubectl", "apply", "-f", "efs-pv.yaml"])
    run_command(["kubectl", "apply", "-f", "efs-pvc.yaml"])

    deployment_content = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-container
        image: {image_name}:{tag}
        volumeMounts:
        - name: efs-volume
          mountPath: /mnt/efs
      volumes:
      - name: efs-volume
        persistentVolumeClaim:
          claimName: my-efs-pvc
    """

    with open("deployment.yaml", "w") as file:
        file.write(deployment_content)

    run_command(["kubectl", "apply", "-f", "deployment.yaml"])
    
def main():
    image_name = input("Please enter the image name (e.g., your-repo/your-image-name): ").strip()
    tag = "latest"

    build_docker_image(image_name, tag)
    push_docker_image(image_name, tag)
    deploy_to_kubernetes(image_name, tag)

if __name__ == "__main__":
    main()
