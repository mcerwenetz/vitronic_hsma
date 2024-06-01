FROM python:3-alpine

RUN python -m pip install --upgrade pip
# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the image
COPY requirements.txt /app/requirements.txt

# Copy logfile into image
COPY lost.log /app/lost.log

# Install the Python packages from requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the script.py file into the image
COPY checkexpiry.py /app/checkexpiry.py
COPY sql_funcs.py /app/sql_funcs.py
# Run the Python script
CMD ["python3", "checkexpiry.py","2"]