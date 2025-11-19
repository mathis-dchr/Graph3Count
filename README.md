# Graph3Count
Project for the Graphs and Applications course at Tongji University. This project involves modeling the Tricount peer-to-peer expense management application using graph theory.

## Prerequisites
- Basic knowledge of graph theory, terminology, and key algorithms
- Docker installed on your machine and a basic understanding of Docker
- Comfortable using the command-line interface (CLI)
- Some web fundamentals (HTML and JavaScript in particular) for the graphical interface
- A good understanding of Python



## How to use the project
- Make sure you have Docker installed on your machine. (https://docs.docker.com/)
- Clone the repository to your machine: `git clone https://github.com/mathis-dchr/Graph3Count.git`
- In your terminal, at the project root, run: `docker compose up -d`

This command will install all the tools and dependencies necessary for the project, as well as create the environment (container) to run the project. You can delete the image and the container (`Graph3Count`) associated with the project at any time if you wish.

- Still in your terminal, run: `docker exec -it Graph3Count bash` to enter the development container.
- In the `/data` folder you can copy and paste the `intent.template.yaml` file into `intent.yaml` file and fill it as you wish.
- Once all participants and transactions have been recorded, you can run the `main.py` file in the container with this command: `python main.py`
- Open a browser and enter the address: `http://localhost:8080`. You can then observe the graph created from the executed Python commands.



## Modeling
Each person is represented by a vertex. Each edge represents what one person **owes** to another.



## Structure

### Engine
>- Tool : Docker
>- Files: `.dockerignore`, `docker-compose.yaml`, `Dockerfile`

This project is containerized with Docker. It is strongly recommended that you use Docker, even locally on your machine, to test the project. To learn more about Docker, including how to install it: https://docs.docker.com/

That being said, you can always install (or you may already have installed) the necessary tools and dependencies (see below) on your machine. If so, you are free to use the project directly on your machine. Note that in this case, you will need to run the Python server manually to use the frontend with the command: `python -m http.server 8080 --bind 0.0.0.0`

### Data
>- Language: JSON
>- File: `intent.yaml`, `data.json`

The `intent.yaml` file allows you to record the list of participants and the expenses between participants (see the `intent.template.yaml` file for the structure). It is the entry point between the user and the project.

The `data.json` file stores the graph's adjacency matrix and the names of the people (see the `data.template.json` file for the structure). This file is used both by the backend for resolution and by the frontend to display the graph associated with this matrix.

Matrix structure:
```
matrix = [[0, 34.9, 51.4, 10.9, ...],
          [60.2, 0, 26.1, 5, ...],
          [6.5, 29.4, 0, 18.2, ...],
           ...
          [45.8, 22.7, 78.2, ..., 0]]
```

Structure of  names:
```
nodes = [{ "id": 0, "name": "Sarah" },
         { "id": 1, "name": "Jack" },
         { "id": 2, "name": "Victoria" },
         ...
         { "id": n, "name": "James" }]
```

Note that the graph is:
- Weighted: the amount (in RMB)
- Directed: the edge represents what person A **owes** to person B
- Loop-free: normally, no one owes money to themselves
- Incomplete: not everyone **owes** money to everyone else

### Frontend
>- Language: HTML, JavaScript
>- Tool: a browser (Firefox, Chrome, Safari, ...)
>- File: `index.html`

This section simply provides a visual representation of the graph associated with the algorithm (see backend). It is not mandatory and is completely independent.

### Backend
>- Language: Python
>- Tool: Python3.13
>- Libraries: NumPy, PyYAML
>- Files: `main.py`, `graph.py`, `requirements.txt`

This is the heart of the problem. Here we find the structure for creating the graph as an object, as well as the algorithm that allows the problem to be solved.



## Resources
- https://github.com/gondyb/tricount-algorithm
- https://github.com/davymariko/Tricount
- https://medium.com/@alexbrou/split-bills-with-friends-the-algorithm-behind-tricount-and-splitwise-using-integer-programming-48cd01999507

- https://tricount.com/
- https://www.splitwise.com/