# Ruby + scip-ruby complete environment
# Includes Ruby runtime and scip-ruby indexer

FROM cicada-base

# Install Ruby
RUN apt-get update && apt-get install -y \
    ruby \
    ruby-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install scip-ruby (download binary from GitHub releases)
RUN curl -L "https://github.com/sourcegraph/scip-ruby/releases/download/v0.4.7/scip-ruby-linux-amd64" \
    -o /usr/local/bin/scip-ruby && \
    chmod +x /usr/local/bin/scip-ruby

# Verify scip-ruby is installed
RUN scip-ruby --help > /dev/null 2>&1 && echo "✓ scip-ruby installed"

WORKDIR /workspace
