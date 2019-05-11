# Python implmentation of raytracer

## Running instruction:
Run the files from their directory. There are seperate scene files for different material types, but you can combine them once you get hold of whats going on.

#### Check images in output_results folder.

## Requirements
- opencv
- python3
- numpy

## Features
- Supports multiple light sources
- Point lights
- Directional lights
- Supports spheres and planes
- Lambertian diffuse
- Reflections
- Blurry reflections
- Fresnel Reflections

## Will be included in future:
- Multi thread rendering (removed temporarily)
- Dielectric material (removed temporarily)
- Referactive material

## Fixed issues:
- Camera coordinate system
- Code structure

## Example for usage: 
#### You can define objects, lights and camera in the scene file's main function like:
objects = [
        sphere(vector3(-300.0,0.0,300.0), 100.0, color(0.5,0.5,0.5)), 
        sphere(vector3(-150.0,0.0,150.0), 100.0, color(0.9,0.9,0.9)), 
        sphere(vector3(0.0,0.0,0.0), 100.0, color(1.0,0.1,0.1)), 
        sphere(vector3(150.0,0.0,150.0), 100.0, color(0.1,0.1,1.0)), 
        sphere(vector3(300.0,0.0,300.0), 100.0, color(0.1,1.0,0.1)), 
        plane(vector3(0.0,-100.0, 0.0), vector3(0.0,1.0,0.0), color(1.0,1.0,1.0)),
    ]

lights = [
        pointLight(vector3(500.0, 500.0, -500.0), color(1.0, 1.0, 1.0), intensity=0.5),
        directionalLight(vector3(0.0, 1000.0, 0.0), vector3(0.3, -0.7, 0), color(1.0, 1.0, 1.0), intensity=0.5),
    ]

cam = camera(
        camera_origin=vector3(0.0,90.0,-400.0),
        camera_forward=vector3(0,0,1),
        camera_right=vector3(1,0,0),
        camera_down=vector3(0,-1,0),
        fov=65,
        render_size=render_size,
        samples=samples
    )
