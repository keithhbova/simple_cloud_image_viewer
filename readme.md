# Image Viewer for Cloud Image Processing

This code serves as a framework for simple image processing. The website was designed using BootStrap Studio, and the web server was written using python's flask. It takes a compressed folder of images and serves it to a gallery, where the end user can view metrics. 

## How to build:

```bash
docker build -f DockerFile -t myflaskapp .
```
## How to run:

```bash
docker run -p 5000:5000 myflaskapp
```

## Usage:

On your computer, organize the .jpgs you want to analyze into the following structure:

<img src="/assets/readme/tree.png" alt="Alt text" title="Optional title">

Compress the images folder. In your web browser, connect to the ip address returned by the docker daemon.

Upload the .zip on the upload page:

<img src="/assets/readme/upload_image.png" alt="Alt text" title="Optional title">

Click gallery to view the data:

<img src="/assets/readme/gallery.png" alt="Alt text" title="Optional title">

The default server does not implement any metrics; however, you can edit the run_me.py file and easily add your own metrics. 

<img src="/assets/readme/metrics.png" alt="Alt text" title="Optional title">
