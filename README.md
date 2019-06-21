# eks-lambda-python
Orchestrating Amazon Kubernetes Service (EKS) from AWS Lambda

The original article can be found here with detailed explanation about the project: https://medium.com/@alejandro.millan.frias/managing-kubernetes-from-aws-lambda-7922c3546249
I also use this script to create the KUBECONFIG file:
https://gist.github.com/innovia/fbba8259042f71db98ea8d4ad19bd708

## Run a sample mongo database with persistent volume
``
🐳 kubectl create -f mongo-emptydir.yaml                          
pod/mongo created
``
## Create ServiceAccount
``
🐳 kubectl apply -f ServiceAccount.yaml
serviceaccount/myservice3 created
``
## Create Role
``
🐳 kubectl apply -f Role.yaml
role.rbac.authorization.k8s.io/my-role created
``
## Create RoleBinding
``
🐳 kubectl apply -f RoleBinding.yaml
rolebinding.rbac.authorization.k8s.io/my-role-binding created
``
## Create Kubeconfig File
`````````````````````
🐳 ./kubernetes_add_service_account_kubeconfig.sh myservice3 default
Creating target directory to hold files in /tmp/kube...done
Getting secret of service account myservice3 on default
Secret name: myservice3-token-l65c2

Extracting ca.crt from secret...done
Getting user token from secret...done
Setting current context to: minikube
Cluster name: minikube
Endpoint: https://192.168.99.104:8443

Preparing k8s-myservice3-default-conf
Setting a cluster entry in kubeconfig...Cluster "minikube" set.
Setting token credentials entry in kubeconfig...User "myservice3-default-minikube" set.
Setting a context entry in kubeconfig...Context "myservice3-default-minikube" modified.
Setting the current-context in the kubeconfig file...Switched to context "myservice3-default-minikube".

All done! Test with:
KUBECONFIG=/tmp/kube/k8s-myservice3-default-conf kubectl get pods
you should not have any permissions by default - you have just created the authentication part
You will need to create RBAC permissions
No resources found.
`````````````````````
## Test
```
🐳 eks-lambda-python kubectl --kubeconfig /tmp/kube/k8s-myservice3-default-conf get pod
NAME    READY   STATUS              RESTARTS   AGE
mongo   0/1     ContainerCreating   0          3m25s
`

TODO:
- Add Terraform Support.

