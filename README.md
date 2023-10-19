# GraphFusion
An Intuitive Graph Analytics, Data Fusion, and Visualization Tool

## Pull/Update the docker image
```bash
docker pull carlosjesusgh/graphfusion:latest
```

## Run the application in a docker container (no development)
```bash
docker run -it --rm -p 8000:8000 --name gf_container carlosjesusgh/graphfusion:latest
```

## Run the application in a docker container for development
```bash
docker run -it --rm -p 8000:8000 -v /home/bscuser/repos/GraphFusion:/home/GraphFusion_host --entrypoint "/home/init_script_dev.sh" --name gf_container carlosjesusgh/graphfusion:latest
```

Note: The volume is mounted to the host folder /home/bscuser/repos/GraphFusion. Change it to your host folder.

To run bash in the running container: 
```bash
docker exec -it gf_container bash
```