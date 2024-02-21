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

Note: The volume is mounted to the host folder /repos/GraphFusion. Please change it to the host folder where you cloned the repository.

To run bash in the running container: 
```bash
docker exec -it gf_container bash
```

## Some examples of how to use the app

### Network visualization

[GraphFusion example - Vis.webm](https://github.com/CarlosJesusGH/GraphFusion/assets/8160204/a648a82b-989e-4757-8e7d-9dc29a9ac000)

### Clustering, enrichment, and [Drugstone](https://drugst.one/)

[GraphFusion example - Clust and Enrich and Drugstone.webm](https://github.com/CarlosJesusGH/GraphFusion/assets/8160204/2f98fc46-1292-4305-a87d-bfa4b0313658)

### Data fusion with an iCell setup

[GraphFusion example - iCell.webm](https://github.com/CarlosJesusGH/GraphFusion/assets/8160204/f0486c9f-87c2-4120-be9e-e5c1f9286350)

### Data fusion with a Matrix Completion setup

[GraphFusion example - PSB.webm](https://github.com/CarlosJesusGH/GraphFusion/assets/8160204/aa2ed2c5-b234-44aa-af6e-5833853c39be)

