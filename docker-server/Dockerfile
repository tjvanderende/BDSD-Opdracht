FROM ubuntu


# Update
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get -y install python3-pip

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

EXPOSE 80


CMD ["python3", "runner.py"]
