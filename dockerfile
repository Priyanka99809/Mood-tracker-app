FROM python:3.9-slim

# Create app directory
WORKDIR /app

# Install app dependencies
COPY src/requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY src /app

# expose the flask port
EXPOSE 5000
CMD [ "python", "server.py" ]