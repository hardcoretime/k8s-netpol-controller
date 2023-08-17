# k8s-netpol-controller
Study project

## About
Controller finds deployments without network policy and create default deny policy for them(network policy does not work in minikube).

## Usage
### Local
Prerequisites:
* python3.10+
* make(4.3+)
* docker(20.10.21+)
* minikube(v1.31.1+)
* kubectl(v1.27.4+)

Start minikube and build docker image with k8s-netpol-controller:
```
minikube start --vm-driver=virtualbox
make docker_build
```

Create namespace:
```
kubectl create ns k8s-netpol-controller
```

Create deployments:
```
for i in {1..15}; do kubectl create deployment kubernetes-bootcamp-${i} -n k8s-netpol-controller --image=gcr.io/google-samples/kubernetes-bootcamp:v1;done
```

Check that network policies do not exist:
```
kubectl get netpol -n k8s-netpol-controller
```

Run controller:
```
make run_controller
```

Check default network policies:
```
kubectl get netpol -n k8s-netpol-controller
```

### Running in k8s cluster
Prerequisites:
* service account
* role and rolebinding(or cluster role and cluster role binding)
* deployment
