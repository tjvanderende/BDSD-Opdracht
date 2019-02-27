import docker
import re
client = docker.from_env()
import tldextract
urls = [
    "https://heerenveen.christenunie.nl",
    "http://www.seniorenrotterdam.nl",
    "https://www.partijwestvoorne.nl",
"https://www.cda.nl/",
"https://www.christenunie.nl",
"https://d66.nl",
"https://groenlinks.nl",
"https://www.partijvoordedieren.nl",
"https://www.sgp.nl",
"https://www.vvd.nl"
"https://50pluspartij.nl",
"https://forumvoordemocratie.nl",
"http://www.bij1.org",
"http://www.vvdzoetermeer.nl",
"https://zoetermeer.groenlinks.nl",
"https://zoetermeer.pvv.nl",
"https://zoetermeer.sp.nl",
"https://zoetermeer.pvda.nl"
"https://zoetermeer.christenunie-sgp.nl",
"https://zoetermeervooruit.nl",
"https://zozoetermeer.nl",
"https://www.pdvz.nl"
]
port = 80
for url in urls:
    ext = tldextract.extract(url)
    container = client.containers.run(name=ext.domain+"-"+str(port), detach=True, image="poliscraper", auto_remove=True, environment=["INPUT="+url], ports={'4000/tcp': port}, links={'MONGODB': 'mongo'})
    port +=1

