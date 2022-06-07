Radoi Bogdan-Mihai 344C3

Din directorul principal se va rula scriptul run.sh.
Acesta va crea serviciile:

-registry = registrul
-sprc3_adaptor = cel care primeste mesaje de la client si le trimite catre broker mqtt
-sprc3_influxdb = baza de date influxdb
-sprc3_mosquitto = broker mqtt
-sprc3_grafana = componenta grafana care realizeaza graficul folosind datele din
baza de date

Pentru a accesa Grafana se foloseste localhost:80 si se introduc username-ul (asistent)
si parola (grafanaSPRC2021)

Am populat baza de date folosind un client custom scris in Python care va trimite
json-uri la broker pentru a testa functionalitatea dashboard-urilor din Grafana.
Acesta se ruleaza folosind client.sh

Pentru a opri aplicatia si a parasi swarm-ul se poate folosi scriptul clean.sh din
directorul principal.

Au fost folosite urmatoarele imagini
grafana: https://hub.docker.com/r/grafana/grafana
influxdb: https://hub.docker.com/_/influxdb
mqtt: https://hub.docker.com/_/eclipse-mosquitto

Au fost expuse port-urile 1883 pentru mqtt si 80 pentru Grafana.
		
