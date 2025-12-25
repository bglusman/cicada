# Java + coursier complete environment
# Includes Java JDK and coursier (for scip-java fallback)

FROM cicada-base

# Install Java
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install Coursier (used by JVM indexer for scip-java fallback)
RUN curl -fL "https://github.com/coursier/coursier/releases/latest/download/cs-x86_64-pc-linux.gz" | gzip -d > /usr/local/bin/cs && \
    chmod +x /usr/local/bin/cs

# Verify coursier is installed
RUN cs --help > /dev/null 2>&1 && echo "✓ coursier installed"

WORKDIR /workspace
