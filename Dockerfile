FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define environment variable

# Run app.py when the container launches
CMD ["python","/code/logs-to-report.py","-l","/data/Logs/","-o","/code/","-s","09.25","-e","10.31","-i","34-232-12-12"]
