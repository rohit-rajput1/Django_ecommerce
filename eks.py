from kubernetes import client, config

# Now we will load the kubernetes configuration
config.load_kube_config()

# Let's create a Kubernetes API Client.
api_client = client.ApiClient()

# Let's create a Deployment object.
deployment = client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="django-ecommerce"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "django-ecommerce"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "django-ecommerce"}),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="django-ecommerce",
                        image="024977362083.dkr.ecr.us-east-1.amazonaws.com/ecommerce-repo:latest",
                        ports=[client.V1ContainerPort(container_port=8000)]
                    )
                ]
            )
        )
    )
)

# Let's create a Deployment in the Kubernetes cluster.
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Here we have defined the service object.
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="django-ecommerce-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "django-ecommerce"},
        ports=[client.V1ServicePort(port=8000)]
    )
)

# Let's create a Service in the Kubernetes cluster.
api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)