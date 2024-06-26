FROM collabora/code:latest

USER root

COPY ./deployments/code/add-repo.sh /add-repo.sh

RUN chmod +x /add-repo.sh && /add-repo.sh

USER cool