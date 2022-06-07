docker swarm init

docker service create --name registry --publish published=5000,target=5000 registry:2

docker build adaptor/ --tag 127.0.0.1:5000/sprc3_adaptor
docker build grafana/ --tag 127.0.0.1:5000/sprc3_grafana

docker push 127.0.0.1:5000/sprc3_adaptor
docker push 127.0.0.1:5000/sprc3_grafana

docker stack deploy -c stack.yml sprc3
