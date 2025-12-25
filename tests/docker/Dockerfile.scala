# Scala + sbt + coursier complete environment
# Includes Java, sbt, and coursier (for scip-java fallback)

FROM cicada-base

# Install Java and sbt
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install sbt
RUN echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | tee /etc/apt/sources.list.d/sbt.list \
    && echo "deb https://repo.scala-sbt.org/scalasbt/debian /" | tee /etc/apt/sources.list.d/sbt_old.list \
    && curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add \
    && apt-get update && apt-get install -y sbt \
    && rm -rf /var/lib/apt/lists/*

# Install Coursier (used by JVM indexer for scip-java fallback)
RUN curl -fL "https://github.com/coursier/coursier/releases/latest/download/cs-x86_64-pc-linux.gz" | gzip -d > /usr/local/bin/cs && \
    chmod +x /usr/local/bin/cs

# Verify installations
RUN sbt --version > /dev/null 2>&1 && echo "✓ sbt installed"
RUN cs --help > /dev/null 2>&1 && echo "✓ coursier installed"

WORKDIR /workspace
