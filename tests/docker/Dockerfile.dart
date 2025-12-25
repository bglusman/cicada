# Dart + scip_dart complete environment
# Includes Dart SDK and scip_dart indexer

FROM cicada-base

# Install Dart SDK
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    wget \
    && wget -qO- https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/dart.gpg \
    && echo 'deb [signed-by=/usr/share/keyrings/dart.gpg arch=amd64] https://storage.googleapis.com/download.dartlang.org/linux/debian stable main' | tee /etc/apt/sources.list.d/dart_stable.list \
    && apt-get update && apt-get install -y dart \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/lib/dart/bin:$PATH"
ENV PATH="/root/.pub-cache/bin:$PATH"

# Install scip_dart via pub global
RUN dart pub global activate scip

# Verify scip_dart is installed
RUN scip_dart --help > /dev/null 2>&1 && echo "✓ scip_dart installed"

WORKDIR /workspace
