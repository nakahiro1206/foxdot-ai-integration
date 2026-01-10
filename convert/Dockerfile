FROM ruby:2.7-slim

# Install build tools (if any native gems are needed) and cleanup
RUN apt-get update \
    && apt-get install -y build-essential --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install midilib gem
RUN gem install midilib

WORKDIR /app

# Copy the converter script
COPY main.rb /app/main.rb
RUN chmod +x /app/main.rb

# Default entrypoint runs the converter; pass arguments as: <input.mid> [output.rb]
ENTRYPOINT ["ruby", "/app/main.rb"]
