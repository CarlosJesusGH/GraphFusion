# Use an official Ubuntu as a parent image
FROM ubuntu:18.04

MAINTAINER Carlos Garcia-Hernandez carlos.garcia2@bsc.es

RUN echo "-----------------------------------------------------------------------"

ENV HOMEDIR=/home
ENV REPODIR=/home/GraphFusion
ENV SETUPDIR=/home/GraphFusion/setup_dir
ENV SERVERDIR=/home/GraphFusion/WebServer
ENV STARTDIR=/home/GraphFusion/start_dir

# clone souce repository with working directories
RUN dpkg --add-architecture i386
RUN apt -y update
RUN apt -y upgrade
RUN apt install -y git
RUN pwd && ls
WORKDIR ${HOMEDIR}
RUN git clone https://github.com/CarlosJesusGH/GraphFusion.git
RUN pwd && ls
RUN ls ${REPODIR}

# WORKDIR creates the path if it doesn't exist. It is like bash-CD, but it persist across intermidiate images, it means that
WORKDIR ${SETUPDIR}

RUN echo "-----------------------------------------------------------------------"

# Update apt and install needed packages
RUN apt install -y wget nano tree htop ncdu
RUN apt install lib32ncurses5-dev -y
RUN apt install libjpeg-dev zlib1g-dev -y
RUN apt install libstdc++5 libstdc++5:i386 -y
RUN apt install libboost-all-dev -y
RUN apt install octave -y
RUN apt install octave-statistics -y
RUN mkdir /usr/share/octave/4.2.2/m/+containers && wget -P /usr/share/octave/4.2.2/m/+containers http://hg.savannah.gnu.org/hgweb/octave/raw-file/b04466113212/scripts/%2Bcontainers/Map.m
# RUN apt install -y build-essential wget git libxrender-dev nano tree htop libxml2-dev cmake
# RUN apt install virtualenv -y
# RUN apt install python2.7 python-pip -y
# RUN virtualenv GC3Env --distribute
# this is necessary before 'pip install MySQL-python'
RUN apt install -y libmysqlclient-dev

RUN echo "-----------------------------------------------------------------------"

# Download, install and update miniconda
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
# 
RUN \
	# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    wget -c https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-Linux-x86_64.sh && \
	chmod +x Miniconda3-py37_4.10.3-Linux-x86_64.sh && \
    # bash Miniconda3-latest-Linux-x86_64.sh -b
    bash Miniconda3-py37_4.10.3-Linux-x86_64.sh -b
    # -p $HOME/miniconda3 \
	# export PATH=$HOME/miniconda3/bin:$PATH

# Initialize conda in bash config fiiles:
RUN conda init
RUN conda init bash

RUN conda --version
RUN conda env list

RUN echo "-----------------------------------------------------------------------"

# Create GC3Env conda environment and install requirements
RUN conda create -y -n GC3Env python=2.7

# Make RUN commands use the new environment:    [1]
# SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]

# Make RUN commands use the new environment:    [1]
SHELL ["conda", "run", "-n", "GC3Env", "/bin/bash", "-c"]
RUN echo $CONDA_DEFAULT_ENV
RUN python --version
RUN \
    pip install -r requirements_GC3Env.txt && \
    # pip install mysql-python
    pip freeze

RUN echo "-----------------------------------------------------------------------"

RUN \
    pip install MySQL-python==1.2.5 && \
    pip install scikit-image==0.11.3 && \
    pip freeze

RUN echo "-----------------------------------------------------------------------"

# to start the service, maybe we could also use something like this: [3]
# SHELL ["/sbin/init", "-d"]
# I didn't try it but it might work

# The default shell on Linux is ["/bin/sh", "-c"] [2]
SHELL ["/bin/sh", "-c"]

RUN apt install -y mysql-server
RUN apt install -y apache2 apache2-utils

RUN ls /var/lib/mysql/
RUN ls /etc/mysql/

RUN service mysql start
RUN service apache2 start

RUN \
    service mysql restart && \
    mysql --execute="CREATE DATABASE GraphFusion; CREATE DATABASE gc3;" && \
    mysql --execute="SHOW DATABASES;"

RUN echo "-----------------------------------------------------------------------"

# RUN service mysql restart && mysql --execute="SHOW DATABASES;"

# RUN tar -xzf WebServer_bkp_*.tar.gz -C ${SERVERDIR}
RUN pwd && ls
WORKDIR ${SERVERDIR}

SHELL ["conda", "run", "-n", "GC3Env", "/bin/bash", "-c"]
RUN \
    service mysql restart && \
    ./manage.py makemigrations --setting=WebServer.settings_prod && \
    ./manage.py migrate --setting=WebServer.settings_prod --noinput && \
    ./manage.py syncdb --setting=WebServer.settings_prod --noinput && \
    python manage.py migrate

RUN echo "-----------------------------------------------------------------------"
# <!-- create environment with python 3.7 and install all the necessary packages -->

WORKDIR ${SETUPDIR}

SHELL ["/bin/sh", "-c"]
# RUN conda deactivate
RUN conda update conda -y
RUN conda config --append channels conda-forge
RUN conda config --append channels bioconda
#conda create --name env_37 --file /home/Downloads/GC3-WWW/drive_files/requirements_env37.txt
RUN conda create --name env_37 python=3.7
# RUN conda activate env_37
# SHELL ["conda", "run", "-n", "env_37", "/bin/bash", "-c"]
# RUN pwd && ls
RUN conda install --name env_37 --yes --file requirements_env37v2.txt
#conda install -c intel -y mkl-fft==1.3.0 mkl-random==1.2.2
# RUN conda install --name env_37 --yes -c intel -y mkl-fft mkl-random
RUN conda install -y --name env_37 -c conda-forge mkl_fft mkl_random
RUN conda install --name env_37 --yes -c anaconda setuptools ipython_genutils
RUN conda install --name env_37 --yes pandas==1.3.4

RUN echo "-----------------------------------------------------------------------"
# <!-- create environment with python 2.7 and install all the necessary packages -->

# conda deactivate
#conda create --name env_27 python=2.7 numpy networkx matplotlib ipykernel scipy scikit-learn -y
RUN conda create --name env_27 python=2.7 numpy networkx==1.11 matplotlib ipykernel scipy scikit-learn -y
RUN conda install -n env_27 -y -c bioconda gnuplot
# cp /home/Downloads/GC3-WWW/drive_files/icell_input_files/gnuplot-py-1.8.tar.gz .
RUN tar -xf gnuplot-py-1.8.tar.gz
# RUN rm gnuplot-py-1.8.tar.gz
RUN conda install -n env_27 decorator=4.4.0 -y
# conda deactivate
SHELL ["conda", "run", "-n", "env_27", "/bin/bash", "-c"]
# source activate env_27 && 
RUN python --version && cd gnuplot-py-1.8 && python setup.py install
# source activate env_27 && 
# RUN python --version
SHELL ["conda", "run", "-n", "env_27", "python", "-c"]
RUN import networkx; import Gnuplot; print('hello gnuplot world');
# cd ..
SHELL ["/bin/sh", "-c"]
RUN pwd && ls
RUN rm -r ${SETUPDIR}

RUN echo "-----------------------------------------------------------------------"

WORKDIR ${HOMEDIR}

EXPOSE 8000

RUN cp ${STARTDIR}/init_script.sh .
RUN chmod 744 init_script.sh
RUN chmod 744 init_script_dev.sh

RUN rm -r ${REPODIR}

# ENTRYPOINT ["/bin/bash", "-c"]
# ENTRYPOINT ["conda", "run", "-n", "GC3Env", "/bin/bash", "-c"]
# CMD ["/home/GraphFusion/start_dir/docker_container_start.sh"]
# ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "GC3Env", "/bin/sh", "-c"]
# CMD ["pwd && bash /home/init_script.sh"]

ENTRYPOINT ["/home/init_script.sh"]

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

# references:
# [1] https://pythonspeed.com/articles/activate-conda-dockerfile/
# [2] https://docs.docker.com/engine/reference/builder/#shell
# [3] https://stackoverflow.com/questions/46800594/start-service-using-systemctl-inside-docker-container
# [4] https://www.bmc.com/blogs/docker-cmd-vs-entrypoint/

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

# docker commands after update. re-build and push new image to dockerhub:
# dockerbuild && dockerpush