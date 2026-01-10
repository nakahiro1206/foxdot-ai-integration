# run basic_pitch via docker

# base file located at ./basic-pitch/Dockerfile
# FROM apache/beam_python3.10_sdk:2.51.0

# RUN --mount=type=cache,target=/var/cache/apt \
#   apt-get update \
#   && apt-get install --no-install-recommends -y --fix-missing \
#     sox \
#     libsndfile1 \
#     libsox-fmt-all \
#     ffmpeg \
#     libhdf5-dev \
#   && rm -rf /var/lib/apt/lists/*

# COPY . /basic-pitch
# WORKDIR basic-pitch
# RUN --mount=type=cache,target=/root/.cache \
#   pip3 install --upgrade pip && \
#   pip3 install --upgrade setuptools wheel && \
#   pip3 install -e '.[train]' 

# build the docker image
# should be executed root dir.
docker build -t basic-pitch ./basic-pitch

# run the docker image
# file structure
# - input_audio/
#   - cinematic-knocking-81199.mp3
# - output_data/
#   - (output files will be saved here)
docker run --rm -v "$(pwd)/input_audio":/input_audio -v "$(pwd)/output_data":/output_data basic-pitch basic-pitch /output_data /input_audio/cinematic-knocking-81199.mp3

# launch bash in the container
docker run --rm -it -v "$(pwd)/input_audio":/input_audio -v "$(pwd)/output_data":/output_data --entrypoint /bin/bash basic-pitch
basic-pitch /output_data /input_audio/cinematic-knocking-81199.mp3
# run with logging
basic-pitch /output_data /input_audio/cinematic-knocking-81199.mp3 2>&1 | tee /tmp/basicpitch.log; echo exit:$?

# TODO
# default config dismissed saved_models/
# so need to pass the local path to saved_models/ via -v option
# e.g.
# -v "$(pwd)/basic-pitch/saved_models":/basic-pitch/saved_models