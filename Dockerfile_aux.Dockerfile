# Use the current latest image as a parent image
FROM carlosjesusgh/graphfusion:latest

# -----------------------------------------------------------------------
# NEW TASKS HERE (tasks not included in original Dockerfile)
SHELL ["conda", "run", "-n", "env_37", "/bin/bash", "-c"]
RUN python -m pip install pip install pyvis

# -----------------------------------------------------------------------
# FINAL STANDARD CONFIG
SHELL ["/bin/sh", "-c"]
WORKDIR ${HOMEDIR}
EXPOSE 8000
RUN rm -rf ${REPODIR}
ENTRYPOINT ["/home/init_script.sh"]

# -----------------------------------------------------------------------
# HELPFUL SNIPPETS
# docker pull carlosjesusgh/graphfusion:latest
# OR: docker image tag carlosjesusgh/graphfusion:latest carlosjesusgh/graphfusion:bkp
# dockerbuildaux
# OR: docker build . -f Dockerfile_aux.Dockerfile -t carlosjesusgh/graphfusion:vYYMMDD --progress=plain
# dockerpush
# OR: docker image push carlosjesusgh/graphfusion:vYYMMDD && docker image tag carlosjesusgh/graphfusion:vYYMMDD carlosjesusgh/graphfusion:latest && docker image push carlosjesusgh/graphfusion:latest