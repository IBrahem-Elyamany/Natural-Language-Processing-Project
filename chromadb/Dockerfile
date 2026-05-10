FROM chromadb/chroma:latest

USER root

# Install tools to download and extract the database
RUN apt-get update && \
    apt-get install -y wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Pass the ZIP file URL via an argument
# Usage: docker build --build-arg DB_ZIP_URL="your_link_here" -t my-chromadb .
ARG DB_ZIP_URL="https://www.kaggle.com/code/svzip/317122072"

# The default persist directory in the Chroma container is /chroma/chroma
WORKDIR /chroma/chroma

# Download the zip file and extract it
# We account for the fact that the zip might contain the folder 'my_vector_db' or just the raw files
RUN wget -qO vector_db.zip "$DB_ZIP_URL" && \
    unzip -q vector_db.zip -d extracted_db && \
    mv extracted_db/* .; \
    rm -rf vector_db.zip extracted_db

EXPOSE 8000
