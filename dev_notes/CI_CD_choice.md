**Author: Dagmara Przygocka**
### Which CI/CD solutions?

 On the market there are two categories of CI/CD systems:
 - self hosted like Jenkins
 - cloud based service like Circle Ci or Github Actions
 
 The team decided to go with cloud service due to:
 - effort required to set up and manage the infrastructure
 - no requirements in terms of customization (all necessary tools and technologies we want to use are provided by cloud hosted services)
 - size of the team and the project
 
 The CI/CD pipeline cloud hosted service:
 Our choice of the service was depenedent on documentation accesibility, online community support and ease of use.
 The service we chose is GitHub actions, which is:
 - closely integrated with GitHub, which makes it easy to automate deployments 
 - easy to set and configure for developers who do not have previos experience with creating CI/CD pipelines
 - large library of pre-built actions which can serve as an example of configuration for our project
 - github actions is a part of github student pack which will allow us to experiment withour worrying about the cost
 - vast online community support (shared issues and solutions to problem we can encounter) 
 
 The configuration of of the pipeline is in file continous-deployment.yml in folder: .github/workflows.
 
 ```
name: Continuous Deployment

on:
  push:
    # Run workflow every time something is pushed to the main branch
    branches:
      - main
  # allow manual triggers for now too
  workflow_dispatch:
    manual: true

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Login to Docker Hub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Build and push minitwitimage
        uses: docker/build-push-action@v2
        with:
          context: .
          file: ./Dockerfile-minitwit
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/minitwitimage:latest
          cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/minitwitimage:webbuildcache
          cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/minitwitimage:webbuildcache,mode=max

      #- name: Build and push sqlite database
      #  uses: docker/build-push-action@v2
      #  with:
      #    context: .
      #    file: ./Dockerfile-sqlite
      #    push: true
      #    tags: ${{ secrets.DOCKER_USERNAME }}/sqliteimage:latest
      #    cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/sqliteimage:sqlitebuildcache
      #    cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/sqliteimage:sqlitebuildcache,mode=max

      - name: Build and push minitwit-api
        uses: docker/build-push-action@v2
        with:
          context: .
          file: ./Dockerfile-api
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/apiminitwit:latest
          cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/apiminitwit:webbuildcacheapi
          cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/apiminitwit:webbuildcacheapi,mode=max

      #- name: Test minitwit
      #  run: |
      #    docker build -t $DOCKER_USERNAME/minitwittestimage -f Dockerfile-minitwit-tests .
      #    yes 2>/dev/null | docker-compose up -d
      #    docker run --rm --network=itu-minitwit-network $DOCKER_USERNAME/minitwittestimage
      #  env:
      #    DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}

      - name: Configure SSH
        run: |
          mkdir -p ~/.ssh/
          echo "$SSH_KEY" > ~/.ssh/do_ssh_key
          chmod 600 ~/.ssh/do_ssh_key
        env:
          SSH_KEY: ${{ secrets.SSH_KEY }}

      - name: Deploy to server
        # Configure the ~./bash_profile and deploy.sh file on the Vagrantfile
        run: >
          ssh $SSH_USER@$SSH_HOST
          -i ~/.ssh/do_ssh_key -o StrictHostKeyChecking=no
          '/minitwit/deploy.sh'
        env:
          SSH_USER: ${{ secrets.SSH_USER }}
          SSH_HOST: ${{ secrets.SSH_HOST }}
 ```
 The file continous_deployment.yml file will be changed as the project evolves.
 
 The file contains following setup:
 - Trigger:
  - Trigger the workflow everytime there is a push to main branch. Additionally, allow manuall trigger of thw workflow.
 - Jobs:
  - Build: specify the virtual machine on which the job will be executed (ubuntu:latest)
  - Step: 
    - Login to docker using environmental variables for password and username with pre-build action: docker/login-action@v1 (version 1)
    - Set up docker buildx with pre-build action: docker/build-push-action@v2 (version 2)
    NOTE: Docker Buildx is a Docker CLI plugin that extends the capabilities of the Docker command-line tool to enable cross-platform builds and advanced build features. 
    It allows for building images for multiple architectures and platforms from a single build context, as well as providing advanced caching and build parallelization features.
    - build and push to DockerHub minitwitimage
      - the image is build using Dockerfile of the minitwit app called Dockerfile-minitwit
      - the tag of the image include the docker username of a person whose dockerHub we will use for the project
      - cache-from: specifies the cache entry to use when building the Docker image it will speed up the Docker build process by reusing previously cached layers.
      - cache-to: the cache entry to use after building the Docker image. The mode=max option is specified to ensure that all new layers created during the build are added to the cache. 
      This cache entry will be used to cache the newly created image layers and speed up future builds.
  - Step:
    - Similar to the one above but repeated for minitwit api
  - Step:
    - Similar to the one above but repeated for minitwit database
  - Step:
    - Configure SSH step creates a folder called .ssh and adds the private ssh key used to communicated with Digital Ocean. The corresponding public key is registered 
    on Digital Ocean which allows the github action to deploy the change
  - Step:
    - Deploy to server step uses the private ssh key and ssh to server hosted on Digital Ocean. 
    Runs deploy.sh script in minitwit folder on the virtual machine, which pulls the new images from the DockerHub and runs docker-compose.yml file.
 
 
  
 
 
