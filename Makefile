verify: verify_python_code verify_dockerfile

verify_python_code:
	flake8 --max-line-length=120 k8s_netpol_controller
 
verify_dockerfile:
	docker run --rm --interactive hadolint/hadolint < Dockerfile

docker_build:
	docker build . --tag k8s-netpol-controller:latest

run_controller:
	docker run --rm \
	  --volume ${HOME}/.kube:/root/.kube \
	  --volume ${HOME}/.minikube/ca.crt:${HOME}/.minikube/ca.crt \
	  --volume ${HOME}/.minikube/profiles:${HOME}/.minikube/profiles \
	  --env ENVIRONMENT=local \
	    k8s-netpol-controller:latest
