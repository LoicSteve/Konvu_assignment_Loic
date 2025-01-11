# Dockerfile

FROM python:3.11-slim

# 1) Install make (and optionally other packages like git, build-essential, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    sqlite3 \
 && rm -rf /var/lib/apt/lists/*

# 2) Set a working directory
WORKDIR /app

# 3) Copy only requirements first
COPY requirements.txt .

# 4) Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5) Copy the rest of the files
COPY . .

# 6) Default command: drop to a shell (so you can run `make` manually)
CMD ["/bin/bash"]
