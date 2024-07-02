# Scalable E-commerce on AWS EKS

This project is an online store built with Django and packed into containers. It uses AWS cloud services and Kubernetes to run smoothly and grow easily when needed.

### Pre-requisites:
- AWS Account
- AWS CLI
- Docker
- kubectl

---

### Steps for AWS-CLI Configuration:

- **Step-1:** Go to `AWS Console`, click on `Security Credentials` and create a new `Access Key`.

![Drawing 2024-07-02 10 13 18 excalidraw](https://github.com/rohit-rajput1/Django_ecommerce/assets/76991475/cc36a0a5-eef9-4c75-a992-4ff6ace05c95)

- **Step-2:** Now Download the **.csv file** and save it in your system securely.

![Screenshot from 2024-06-27 15-52-02](https://github.com/rohit-rajput1/Django_ecommerce/assets/76991475/6b8698d8-edd7-441c-af83-0549dc8ea68c)

- **Step-3:** Since this a Django Project, we will install `aws-cli` using pip.

```bash
pip install awscli
```

![Screenshot from 2024-06-27 15-59-32](https://github.com/rohit-rajput1/Django_ecommerce/assets/76991475/d4d9939f-5b34-4f5c-a979-ed184cbb75bc)

check the version of `aws-cli` installed.

```bash
aws --version
```

![Screenshot from 2024-06-27 16-06-26](https://github.com/rohit-rajput1/Django_ecommerce/assets/76991475/639cecea-22a4-4a78-a5d8-1bf5ae5984a2)

- **Step-4:** Now, configure the `aws-cli` using the `Access Key` and `Secret Key` from the **.csv file**.

```bash
aws configure
```

![imageedit_1_9030107237](https://github.com/rohit-rajput1/Django_ecommerce/assets/76991475/3e1d0364-f92b-4b39-98ce-1b2e0a450e13)

##### Thus we have successfully configured the `aws-cli` on our system.

---

### Creation of Python Script for ECR Client:

- **Step-1:** Create a new Python file named `aws_ecr.py` in the root directory of the project.

```python
import boto3

ecr_client = boto3.client('ecr')

repo_name = 'ecommerce-repo'
response = ecr_client.create_repository(repositoryName=repo_name)

repository_uri = response['repository']['repositoryUri']
print(repository_uri)
```

- **Step-2:** Run the Python script to create a new repository in `AWS Elastic Container Registry (ECR)`.

```bash
python aws_ecr.py
```

![Screenshot from 2024-06-27 18-50-34](https://github.com/rohit-rajput1/Django_ecommerce/assets/76991475/0f4b4c18-585f-41c0-97bb-a6ef0dedea62)

- **Step-3:** Now go to the `AWS Elastic Container Registry (ECR)` and verify the repository created.

![Screenshot from 2024-07-01 14-35-12](https://github.com/rohit-rajput1/Django_ecommerce/assets/76991475/f43047a9-4dd6-403e-92fe-f2fb56f8a515)

- **Step-4:** Now, go inside the created repository and click on `View push commands`, from that copy the commands and run them in the terminal to push the image to the repository.

![Screenshot from 2024-07-01 14-36-00](https://github.com/rohit-rajput1/Django_ecommerce/assets/76991475/3f579168-bc26-4ca8-8b7b-9445266f035c)

**`Note:`** Before running the command make sure you have Docker installed and running on your system and logged in to the Docker Hub.

**Command 1:** Does the login to the ECR.

![Screenshot from 2024-07-01 14-36-32](https://github.com/rohit-rajput1/rangam/assets/76991475/04cf6b27-40d2-4138-89b5-a31c48af94ae)

**Command 2:** Builds the Docker image.

![Screenshot from 2024-07-01 14-37-04](https://github.com/rohit-rajput1/rangam/assets/76991475/2ee0249f-f135-4363-8310-ca81a227ff40)

**Command 3:** Tags the Docker image.

![Screenshot from 2024-07-01 14-37-22](https://github.com/rohit-rajput1/rangam/assets/76991475/f600ff80-a8e5-4d70-a82e-9cf0b2e9977d)

**Command 4:** Pushes the Docker image to the ECR.

![Screenshot from 2024-07-01 14-42-43](https://github.com/rohit-rajput1/rangam/assets/76991475/bac141c7-d59e-438a-a152-8afc347c5a93)

- **Step-5:** Now, go to the `AWS Elastic Container Registry (ECR)` and verify the image pushed to the repository.

![Screenshot from 2024-07-01 14-44-43](https://github.com/rohit-rajput1/rangam/assets/76991475/ec2d9750-2c6e-444f-9bfa-a15d4b25f4f8)

---

### Deployment and Service Orchestration on AWS EKS:

- **Step-1:** Go to the `AWS Elastic Kubernetes Service (EKS)` and create a new cluster with proper cluster role having the permission called **`AmazonEKSClusterPolicy`**.

![Screenshot from 2024-07-01 14-46-13](https://github.com/rohit-rajput1/rangam/assets/76991475/e83bda82-0e3b-4703-944d-8db9157d1ad7)

![Screenshot from 2024-07-01 14-46-27](https://github.com/rohit-rajput1/rangam/assets/76991475/92cffbc2-b5da-43a1-a2a7-9f25692f32e0)

- **Step-2:** Now, we will specify the networkings of the cluster.

![Screenshot from 2024-07-01 14-49-37](https://github.com/rohit-rajput1/rangam/assets/76991475/432cb1c3-973b-4617-978b-30ec051fbbef)

- **Step-3:** Keep the Observability settings as `default` and create the cluster.

![image](https://github.com/rohit-rajput1/rangam/assets/76991475/37412889-e4b8-45a1-b9ed-b6b8e3fd1006)

- Now if we try to access the cluster, it will show the below message and give error.

```bash
kubectl get pods
```

![Screenshot from 2024-07-01 14-52-22](https://github.com/rohit-rajput1/rangam/assets/76991475/4987a47c-fb2c-4aaf-9c1f-84791716741b)

- **Step-4:** Before creating the `Node Group` for the cluster, we will create the `IAM Role` for the `Node Group` with the permission called **`AmazonEKSWorkerNodePolicy`**.

![Screenshot from 2024-07-01 15-01-58](https://github.com/rohit-rajput1/rangam/assets/76991475/c4915743-5fa5-4be8-be92-0d693fc787b6)

![Screenshot from 2024-07-01 15-03-02](https://github.com/rohit-rajput1/rangam/assets/76991475/abb13ac3-96b4-4c4a-bddd-8a451041bb4b)

- **Step-5:** Now we will create the `Node Group` for the cluster for that , Go to **Cluster** > **Compute** > **Add Node Group**.

![Screenshot from 2024-07-01 15-01-24](https://github.com/rohit-rajput1/rangam/assets/76991475/3e5c669e-7673-4e2e-98e7-0bb662e85390)

- **Step-6:** Now, we will configure the `Node Group` with the `IAM Role` created earlier.

![Screenshot from 2024-07-01 15-03-28](https://github.com/rohit-rajput1/rangam/assets/76991475/79a365e4-669c-480a-b318-49a06800bd52)

- **Step-7:** Here, we will setup the compute settings for the `Node Group` according to the requirements.

![Screenshot from 2024-07-01 15-05-15](https://github.com/rohit-rajput1/rangam/assets/76991475/ba54c3a1-2ea5-46a4-bb08-e05a7122898a)

- **Step-8:** At last we will keep the `Networking` settings as `default` and create the `Node Group`.

![Screenshot from 2024-07-01 15-05-42](https://github.com/rohit-rajput1/rangam/assets/76991475/6e0d00d5-aaef-4bdb-824e-19a469d2eb16)

- **Step-9:** Be patient and wait for the `Node Group` to be created, as it will take some time.

![Screenshot from 2024-07-01 17-10-46](https://github.com/rohit-rajput1/rangam/assets/76991475/d9e28240-c82a-4bb2-bfcd-ad849bd7fdce)

Check the status of the `Node Group` and `Cluster`.

![imageedit_5_6833080961](https://github.com/rohit-rajput1/rangam/assets/76991475/1b1efcf3-7e74-4e3a-b118-8df8ea595cd0)

- **Step-10:** After, this we will install kubectl and configure it with the cluster.

```bash
sudo snap install kubectl --classic
```

- After this we will update the `KUBECONFIG` file with the `kubeconfig` file of the cluster.

![Screenshot from 2024-07-01 17-18-15](https://github.com/rohit-rajput1/rangam/assets/76991475/b9c4eee6-f632-4e56-b3c9-211436f8bbf6)

- Check the default namespace of the cluster.

```bash
kubectl get namespace
```

![Screenshot from 2024-07-01 17-18-30](https://github.com/rohit-rajput1/rangam/assets/76991475/fc7c4558-422d-4dbb-942e-54b3cbe3d44c)

- Check the services running in the cluster.

```bash
kubectl get svc -n default
```

![Screenshot from 2024-07-01 17-18-59](https://github.com/rohit-rajput1/rangam/assets/76991475/684be5e4-d00e-45a5-b9a5-7acd63e0326e)

- We can, see that Deployment and Services are not running in the cluster as of now.

![Screenshot from 2024-07-01 17-38-44](https://github.com/rohit-rajput1/rangam/assets/76991475/3fe884b0-f7f2-45a1-8105-6bb3402d91f8)


### Python Script for Deployment and Service Orchestration:

- **Step-1:** Install the `kubernetes` library using pip.

```bash
pip install kubernetes
```

![Screenshot from 2024-07-01 17-13-14](https://github.com/rohit-rajput1/rangam/assets/76991475/22f2c399-3084-4bb6-b901-b56687b2abf8)

- **Step-2:** Create a new Python file named `eks.py` in the root directory of the project.

```python
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
```

- **Step-3:** Run the Python script to create a new Deployment and Service in the `AWS Elastic Kubernetes Service (EKS)` cluster.

```bash
python eks.py
```

![Screenshot from 2024-07-01 17-45-40](https://github.com/rohit-rajput1/rangam/assets/76991475/e361ea77-fb79-4af5-9e81-9dffb632b558)

- Now we have our pods, services and deployments running in the cluster.

**Pods:**
![Screenshot from 2024-07-01 17-46-43](https://github.com/rohit-rajput1/rangam/assets/76991475/23d752f3-8152-4899-8a03-9bf04a57cf18)

**Service:**
![Screenshot from 2024-07-01 17-47-40](https://github.com/rohit-rajput1/rangam/assets/76991475/cf843952-09bc-4383-b6f7-d4645a1fa9fa)

**Deployment:**
![Screenshot from 2024-07-01 17-47-06](https://github.com/rohit-rajput1/rangam/assets/76991475/90304448-1c68-4385-9fea-2129946e3257)

- **Step-4:** At last, we will do the port forwarding to access the Django application running in the cluster.

```bash
kubectl port-forward svc/django-ecommerce-service 8000:8000
```

**Before Port Forwarding**

![Drawing 2024-07-02 10 13 19 excalidraw](https://github.com/rohit-rajput1/rangam/assets/76991475/471acf7b-66d0-4d61-b2ce-3112df3f92a5)

**After Port Forwarding**

![Drawing 2024-07-02 10 13 20 excalidraw](https://github.com/rohit-rajput1/rangam/assets/76991475/94e30b6d-c3db-4e1a-9691-6a2c2cbae727)

#### Thus we can access the Django application running in the `AWS Elastic Kubernetes Service (EKS)` cluster.

---