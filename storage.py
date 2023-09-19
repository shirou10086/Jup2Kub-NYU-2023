from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()

pv_body = client.V1PersistentVolume(
    api_version="v1",
    kind="PersistentVolume",
    metadata=client.V1ObjectMeta(name="my-ebs-pv"),
    spec=client.V1PersistentVolumeSpec(
        capacity={"storage": "10Gi"},
        access_modes=["ReadWriteOnce"],
        aws_elastic_block_store=client.V1AWSElasticBlockStoreVolumeSource(
            volume_id="<wJalrXUtnFEMI/K7MDENG/bPxRfiCYsdsffcwaqada>",
            fs_type="ext4"
        )
    )
)

v1.create_persistent_volume(body=pv_body)

pvc_body = client.V1PersistentVolumeClaim(
    api_version="v1",
    kind="PersistentVolumeClaim",
    metadata=client.V1ObjectMeta(name="my-ebs-pvc"),
    spec=client.V1PersistentVolumeClaimSpec(
        access_modes=["ReadWriteOnce"],
        resources=client.V1ResourceRequirements(
            requests={"storage": "10Gi"}
        )
    )
)

v1.create_namespaced_persistent_volume_claim(namespace="default", body=pvc_body)
def create_efs_pv_pvc(name, namespace, efs_dns_name):
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
