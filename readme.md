# Python implmentation of simple recursive raytracer

## Requirements
- opencv
- python3
- numpy

## Latest up to date file is parallel_rendering_bucket.py which has the follwing features

## Includes:
- Lambertian diffuse model
- Fresnel reflections

## Will be included in future:
- Referaction

## Issues:
- Camera coordinate system is messed (will be fixed soon)

## Material types:
You can specify the following material types at the time of creating an object
- Lambertian
- Reflective

### Example: 
objects = [
    sphere(vector3(-300.0,0.0,300.0), 100.0, color(0.2,0.2,0.2), material_type='Reflective'), 
    sphere(vector3(-150.0,0.0,150.0), 100.0, color(0.9,0.9,0.9), material_type='Lambertian'), 
    sphere(vector3(0.0,0.0,0.0), 100.0, color(1.0,0.1,0.1), material_type='Lambertian'), 
    sky(vector3(0.0,0.0,0.0), 100000.0, color(1.0,1.0,1.0)), 
    plane(vector3(0.0,-100.0, 0.0), vector3(0.0,1.0,0.0), color(1.0,1.0,1.0), material_type='Reflective'),
]

### In the current file the materials are defined at line number 332 (in future things are supposed be placed properly though)

### If for some reason you cant run the latest file, i have included my first, second, third and fourth attempts, which lack features but you can try them out
