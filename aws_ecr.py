import boto3

ecr_client = boto3.client('ecr')

repo_name = 'ecommerce-repo'
response = ecr_client.create_repository(repositoryName=repo_name)

repository_uri = response['repository']['repositoryUri']
print(repository_uri)