FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y git

# Clone the repository
RUN git clone https://github.com/your-username/your-repo.git .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV NAME Themis

# Command to update the repository and run your application
CMD ["bash", "-c", "git pull && pip install --no-cache-dir -r requirements.txt && python app.py"]