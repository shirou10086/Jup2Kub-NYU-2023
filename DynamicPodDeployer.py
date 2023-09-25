import subprocess
from kubernetes import client, config

class PodManager:
    def __init__(self):
        self.pods = {}

    def add_pod(self, name, is_producer, is_consumer, topic=None):
        self.pods[name] = {
            'is_producer': is_producer,
            'is_consumer': is_consumer,
            'topic': topic
        }


class DynamicPodDeployer:
    def __init__(self, pod_manager):
        self.pod_manager = pod_manager
        config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def deploy_all_pods(self, image_name, tag):
        for pod_name, pod_info in self.pod_manager.pods.items():
            self.deploy_to_kubernetes(image_name, tag, pod_name, pod_info)

    def deploy_to_kubernetes(self, image_name, tag, pod_name, pod_info):
        env_content = ""
        if pod_info['is_producer']:
            env_content += f"""
            - name: PRODUCER_TOPIC
              value: "{pod_info['topic']}"
            """
        if pod_info['is_consumer']:
            env_content += f"""
            - name: CONSUMER_TOPIC
              value: "{pod_info['topic']}"
            """

        pv, pvc = self.create_efs_pv_pvc(f"{pod_name}-efs", "default", "fs-0fe8790d8133d66cf.efs.eu-west-2.amazonaws.com")

        with open(f"{pod_name}-efs-pv.yaml", "w") as file:
            file.write(pv)

        with open(f"{pod_name}-efs-pvc.yaml", "w") as file:
            file.write(pvc)

        run_command(["kubectl", "apply", "-f", f"{pod_name}-efs-pv.yaml"])
        run_command(["kubectl", "apply", "-f", f"{pod_name}-efs-pvc.yaml"])

        deployment_content = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {pod_name}-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {pod_name}
  template:
    metadata:
      labels:
        app: {pod_name}
    spec:
      containers:
      - name: {pod_name}-container
        image: {image_name}:{tag}
        env:
        - name: KAFKA_BROKER
          value: "my-broker-address"
        {env_content}
        volumeMounts:
        - name: efs-volume
          mountPath: /mnt/efs
      volumes:
      - name: efs-volume
        persistentVolumeClaim:
          claimName: {pod_name}-efs-pvc
        """

        with open(f"{pod_name}-deployment.yaml", "w") as file:
            file.write(deployment_content)

        run_command(["kubectl", "apply", "-f", f"{pod_name}-deployment.yaml"])

    def create_efs_pv_pvc(self, name, namespace, efs_dns_name):
        pv = {
            "apiVersion": "v1",
            "kind": "PersistentVolume",
            "metadata": {
                "name": name
            },
            "spec": {
                "capacity": {
                    "storage": "5Gi"
                },
                "accessModes": ["ReadWriteMany"],
                "persistentVolumeReclaimPolicy": "Retain",
                "storageClassName": "efs",
                "csi": {
                    "driver": "efs.csi.aws.com",
                    "volumeHandle": efs_dns_name
                }
            }
        }

        pvc = {
            "apiVersion": "v1",
            "kind": "PersistentVolumeClaim",
            "metadata": {
                "name": name,
                "namespace": namespace
            },
            "spec": {
                "accessModes": ["ReadWriteMany"],
                "storageClassName": "efs",
                "resources": {
                    "requests": {
                        "storage": "5Gi"
                    }
                }
            }
        }

        return pv, pvc


def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        print(e.stderr)


def main():
    image_name = input("Please enter the image name (e.g., your-repo/your-image-name): ").strip()
    tag = "latest"

    # initialize PodManager
    pod_manager = PodManager()
    # pod_manager.add_pod(...)  # 

    # deploy Pods
    deployer = DynamicPodDeployer(pod_manager)
    deployer.deploy_all_pods(image_name, tag)


if __name__ == "__main__":
    main()
