FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy project
COPY . /app
COPY ./requirements.txt /requirements.txt



# Set work directory
WORKDIR /app
EXPOSE 8000


# Create new user
RUN adduser --disabled-password --no-create-home app

# Make directories to map static and media root and modify directory ownership
RUN mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol 

#Make virtual, upgrade pip and install requirements
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt 

# Set user
USER app

#set path
ENV PATH="/py/bin:$PATH"