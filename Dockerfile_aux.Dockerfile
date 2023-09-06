# Use the current latest image as a parent image
FROM carlosjesusgh/graphfusion:latest

# -----------------------------------------------------------------------
# NEW TASKS HERE (tasks not included in original Dockerfile)
ADD ./start_dir ${STARTDIR}
WORKDIR ${HOMEDIR}
RUN cp ${STARTDIR}/init_script_dev.sh .
RUN chmod 744 init_script_dev.sh

# -----------------------------------------------------------------------
# FINAL STANDARD CONFIG
SHELL ["/bin/sh", "-c"]
WORKDIR ${HOMEDIR}
EXPOSE 8000
RUN rm -r ${REPODIR}
ENTRYPOINT ["/home/init_script.sh"]

# -----------------------------------------------------------------------
# HELPFUL SNIPPETS
# docker pull carlosjesusgh/graphfusion:latest
# dockerbuildaux
# OR: docker build . -f Dockerfile_aux.Dockerfile -t carlosjesusgh/graphfusion:v230906 --progress=plain
# dockerpush
# OR: docker image push carlosjesusgh/graphfusion:v230906 && docker image tag carlosjesusgh/graphfusion:v230906 carlosjesusgh/graphfusion:latest && docker image push carlosjesusgh/graphfusion:latest