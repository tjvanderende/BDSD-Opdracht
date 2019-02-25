import docker
client = docker.from_env()

container = client.containers.run(detach=True, image="poliscraper", auto_remove=True, environment=["INPUT=https://www.pvda.nl"], ports={'4000/tcp': '80'}, links={'MONGODB': 'mongo'})
container = client.containers.run(detach=True,image="poliscraper", auto_remove=True, environment=["INPUT=https://heerenveen.christenunie.nl"], ports={'4000/tcp': '81'}, links={'MONGODB': 'mongo'})
container = client.containers.run(detach=True, image="poliscraper", auto_remove=True, environment=["INPUT=https://www.vvd.nl"], ports={'4000/tcp': '82'}, links={'MONGODB': 'mongo'})

print(container.logs())

