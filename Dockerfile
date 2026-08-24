FROM python:3.13.2-alpine3.21

# Set working directory
WORKDIR /app

#Copy requirements file
COPY requirements.txt .

COPY . .


#Install dependencies listed in requirements file
RUN pip install --no-cache-dir -r requirements.txt