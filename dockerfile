# Use the official Python image as a base
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the content of the local src directory to the working directory
COPY themis/ .

# Install dependencies
RUN pip install numpy \
	annotated-types \
	anyio \
	azure-cognitiveservices-speech \
	beautifulsoup4 \
	breadability \
	cachetools \
	certifi \
	chardet \
	charset-normalizer \
	cleo \
	click \
	crashtest \
	defusedxml \
	distro \
	dnspython \
	docopt \
	fastapi \
	geographiclib \
	geopy \
	google-api-core \
	google-api-python-client \
	google-auth \
	google-auth-httplib2 \
	google-auth-oauthlib \
	google-cloud \
	googleapis-common-protos \
	h11 \
	httpcore \
	httplib2 \
	httpx \
	idna \
	joblib \
	keyboard \
	lxml \
	lxml_html_clean \
	nltk \
	notion-client \
	notion-exporter \
	notion2md \
	numpy \
	oauthlib \
	openai \
	parsedatetime \
	pip \
	proto-plus \
	protobuf \
	pyasn1 \
	pyasn1_modules \
	pycountry \
	pydantic \
	pydantic_core \
	pymongo \
	pymstodo \
	pyparsing \
	python-dateutil \
	python-dotenv \
	pytz \
	PyYAML \
	rapidfuzz \
	regex \
	requests \
	requests-oauthlib \
	rsa \
	setuptools \
	shapely \
	six \
	sniffio \
	soupsieve \
	starlette \
	sumy \
	tenacity \
	timezonefinder \
	tqdm \
	typing_extensions \
	tzwhere \
	uritemplate \
	urllib3 \
	uvicorn \
	uvloop \
	watchfiles \
	websockets

	
# Expose port 80
EXPOSE 4034

# Run uvicorn command
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "4034", "--reload"]
