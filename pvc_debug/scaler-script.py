from kubernetes import client, config

config.load_kube_config()


def update_replicas(namespace, deployments):
    # Chargement de la configuration Kubernetes
    config.load_kube_config()

    # Création d'un client Kubernetes
    api_instance = client.AppsV1Api()

    for deployment_name, new_replicas in deployments.items():
        try:
            # Récupération du déploiement
            deployment = api_instance.read_namespaced_deployment(name=deployment_name, namespace=namespace)

            # Mise à jour du nombre de réplicas
            deployment.spec.replicas = new_replicas

            # Patch du déploiement avec la nouvelle configuration
            resp = api_instance.patch_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
                body=deployment
            )

            print(
                f"Nombre de réplicas mis à jour pour le déploiement '{deployment_name}' dans l'espace de noms '{namespace}': {resp.spec.replicas}")

        except client.ApiException as e:
            print(f"Exception lors de la mise à jour des réplicas pour le déploiement '{deployment_name}' : {e}")


if __name__ == "__main__":
    # Exemple d'utilisation
    deployments = {
        "teastore-webui": 6,
        "teastore-persistence": 2,

    }

    update_replicas(namespace="default", deployments=deployments)
