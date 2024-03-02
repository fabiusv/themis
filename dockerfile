# Use the official Python image as a base
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the content of the local src directory to the working directory
COPY themis/ .

# Install dependencies
RUN pip install numpy \
	fastapi \
	openai \
	parsedatetime==2.6 \
	pycountry==22.3.5 \
	pydantic==2.0.3 \
	pydantic_core==2.3.0 \
	pymongo==4.4.1 \
	pytz==2023.3 \
	PyYAML==6.0.1 \
	regex==2023.6.3 \
	requests==2.31.0 \
	setuptools==67.6.1 \
	starlette==0.27.0 \
	sumy==0.11.0 \
	tqdm==4.65.0 \
	tzwhere==3.0.3 \
	urllib3==2.0.3 \
	uvicorn \
	python-dateutil \
	beautifulsoup4 \
	uvloop \
	watchfiles==0.19.0 \
	websockets==11.0.3 \
	timezonefinder==5.2.0 \
	geopy \
	python-dotenv
	
# Expose port 80
EXPOSE 4034

# Run uvicorn command
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "4034", "--reload"]
