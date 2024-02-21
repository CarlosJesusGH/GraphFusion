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



https://github.com/CarlosJesusGH/GraphFusion/assets/8160204/8eba00ff-9d83-467a-9112-d401a46c1006



## Run the application in a docker container for development
```bash
docker run -it -p 8000:8000 -v /repos/GraphFusion:/home/GraphFusion_host --entrypoint "/home/init_script_dev.sh" --name gf_container carlosjesusgh/graphfusion:latest
```

Note: The volume is mounted to the host folder /repos/GraphFusion. Change it to the host folder where you cloned the repository.

To run bash in the running container: 
```bash
docker exec -it gf_container bash
```
