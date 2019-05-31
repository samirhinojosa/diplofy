FROM python:3

# Copy default endpoint specific user settings overrides into container to specify Python path
COPY .devcontainer/settings.vscode.json /root/.vscode-remote/data/Machine/settings.json

ENV PYTHONUNBUFFERED 1

RUN mkdir /workspace
WORKDIR /workspace

# Install Python dependencies from requirements.txt if it exists
COPY .devcontainer/requirementsdevcontainer.txt requirementsdevcontainer.txt* /workspace/
RUN if [ -f "requirementsdevcontainer.txt" ]; then pip install -r requirementsdevcontainer.txt && rm requirementsdevcontainer.txt; fi

# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*