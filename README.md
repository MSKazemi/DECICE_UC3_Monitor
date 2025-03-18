docker build -t ros2-json-publisher .
docker run -p 8000:8000 -p 8001:8001 ros2-json-publisher
kubectl apply -f k8s_deployment.yaml
docker build -t ros2-fastapi-prometheus .

docker run -p 8000:8000 -p 8001:8001 ros2-fastapi-prometheus



docker build -t kazemi/uc3-monitoring .
docker push kazemi/uc3-monitoring
