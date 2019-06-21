import os.path
import yaml
import boto3
from kubernetes import client, config
import auth
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configure your cluster name and region here
KUBE_FILEPATH = '/tmp/kubeconfig'
CLUSTER_NAME = '${var.cluster-name}'
REGION = '${var.aws-region-name}'

# We assuem that when the Lambda container is reused, a kubeconfig file exists.
# If it does not exist, it creates the file.

if not os.path.exists(KUBE_FILEPATH):

    os.rename("/var/task/kubeconfig", "/tmp/kubeconfig")
    os.rename("/var/task/aws-iam-authenticator", "/tmp/aws-iam-authenticator")

def handler(event, context):

    # Get Token
    eks = auth.EKSAuth(CLUSTER_NAME)
    token = eks.get_token()
    # Configure
    config.load_kube_config(KUBE_FILEPATH)
    configuration = client.Configuration()
    configuration.api_key['authorization'] = token
    configuration.api_key_prefix['authorization'] = 'Bearer'
    # API
    api = client.ApiClient(configuration)
    v1 = client.CoreV1Api(api)

    print(open(KUBE_FILEPATH).read())
    # Get all the pods
    ret = v1.list_namespaced_pod("default")

    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
