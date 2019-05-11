import math
from utils.Vector import Vector3
from utils.Color import Color
from utils.Ray import Ray
from random import random

def Trace(r, objects, lights):
    
    # Reflection Ray
    # Finding closes object on Ray
    min_dist = math.inf
    closest_object = None
    closest_hit_point = None
    for object in objects:
        hit_point = object.hit(r)
        if hit_point:
            distance = Vector3.magnitude(hit_point - r.origin)
            if distance < min_dist:
                min_dist = distance
                closest_object = object
                closest_hit_point = hit_point
   
    if closest_object is not None:
        # Calculate normal
        object_normal = closest_object.calculate_normal(closest_hit_point)

        # Checking Shadow Ray against all light sources
        intensity = 0
        for light in lights:
            object_in_way = False
            # Shadow Ray direction is based on type of light
            if light.type == "Directional":
                shadow_Ray_direction = light.direction.invert()
            elif light.type == "Point":
                shadow_Ray_direction = Vector3.normalize(light.position - closest_hit_point)

            # Adding very small normal value before tracing to light source, in order
            # to avoid noise in shading
            shadow_Ray = Ray(closest_hit_point + (object_normal * 0.01), shadow_Ray_direction)
            min_dist = Vector3.magnitude(light.position - closest_hit_point)
            # Checking Shadow Ray against all objects
            for object in objects:
                hit_point = object.hit(shadow_Ray)
                if hit_point:
                    distance = Vector3.magnitude(hit_point - shadow_Ray.origin)
                    if distance < min_dist:
                        object_in_way = True
                        break

            if not object_in_way:
                # Shading
                diff_angle = shadow_Ray_direction * object_normal
                # Clipping diff angle
                if diff_angle < 0:
                    diff_angle = 0
                intensity += light.intensity * diff_angle

        # Clipping intensity
        if intensity > 1:
            intensity = 1

        return closest_object.color * intensity

    # Return background Color
    return Color(1,1,1) # Background Color return


def RecursiveTrace(r, objects, lights, bounces=1, energy=1):
    
    # Reflection Ray
    # Finding closes object on Ray
    min_dist = math.inf
    closest_object = None
    closest_hit_point = None
    for object in objects:
        hit_point = object.hit(r)
        if hit_point:
            distance = Vector3.magnitude(hit_point - r.origin)
            if distance < min_dist:
                min_dist = distance
                closest_object = object
                closest_hit_point = hit_point
   
    color_to_return = Color(1,1,1) # Background color
    if closest_object is not None:
        # Calculate normal
        object_normal = closest_object.calculate_normal(closest_hit_point)

        if closest_object.material_type == 'Standard' or bounces == 0:
            color_to_return = closest_object.color

        elif closest_object.material_type == 'Reflective':
            reflected_ray_direction = r.direction - (object_normal * ((r.direction * object_normal) * 2))
            reflected_ray = Ray(closest_hit_point + (object_normal * 0.01), reflected_ray_direction)
            color_to_return = RecursiveTrace(reflected_ray, objects, lights, bounces-1, energy**0.5)
            color_to_return = color_to_return * closest_object.reflectness + closest_object.color * (1-closest_object.reflectness)

            # Applying fresnel
            angle_diff = r.direction.invert() * object_normal
            color_to_return = color_to_return * (1-angle_diff) + closest_object.color * angle_diff

        # Checking Shadow Ray against all light sources
        intensity = 0
        for light in lights:
            object_in_way = False
            # Shadow Ray direction is based on type of light
            if light.type == "Directional":
                shadow_Ray_direction = light.direction.invert()
            elif light.type == "Point":
                shadow_Ray_direction = Vector3.normalize(light.position - closest_hit_point)

            # Adding very small normal value before tracing to light source, in order
            # to avoid noise in shading
            shadow_Ray = Ray(closest_hit_point + (object_normal * 0.01), shadow_Ray_direction)
            min_dist = Vector3.magnitude(light.position - closest_hit_point)
            # Checking Shadow Ray against all objects
            for object in objects:
                hit_point = object.hit(shadow_Ray)
                if hit_point:
                    distance = Vector3.magnitude(hit_point - shadow_Ray.origin)
                    if distance < min_dist:
                        object_in_way = True
                        break

            if not object_in_way:
                # Shading
                diff_angle = shadow_Ray_direction * object_normal
                # Clipping diff angle
                if diff_angle < 0:
                    diff_angle = 0
                intensity += light.intensity * diff_angle

        # Clipping intensity
        if intensity > 1:
            intensity = 1

        return color_to_return * intensity * energy

    # Return background Color
    return color_to_return * energy # Background Color return


def RecursiveScatteredTrace(r, objects, lights, bounces=1, samples=3):
    
    # Reflection Ray
    # Finding closes object on Ray
    min_dist = math.inf
    closest_object = None
    closest_hit_point = None
    for object in objects:
        hit_point = object.hit(r)
        if hit_point:
            distance = Vector3.magnitude(hit_point - r.origin)
            if distance < min_dist:
                min_dist = distance
                closest_object = object
                closest_hit_point = hit_point
   
    color_to_return = Color(1,1,1) # Background color
    if closest_object is not None:
        # Calculate normal
        object_normal = closest_object.calculate_normal(closest_hit_point)

        if closest_object.material_type == 'Standard' or bounces == 0:
            color_to_return = closest_object.color

        elif closest_object.material_type == 'Reflective':
            reflected_ray_direction = r.direction - (object_normal * ((r.direction * object_normal) * 2))

            unit_sphere_center = closest_hit_point + reflected_ray_direction * ((1-closest_object.roughness) * 10)
            color_to_return = Color(0,0,0)
            for i in range(samples):
                random_unit_vector = unit_sphere_center + Vector3(random(),random(),random()).normalize()
                reflected_ray_direction = Vector3.normalize(random_unit_vector - closest_hit_point)
                reflected_ray = Ray(closest_hit_point + (object_normal * 0.01), reflected_ray_direction)

                color_to_return += RecursiveScatteredTrace(reflected_ray, objects, lights, bounces-1, samples)
                
            color_to_return *= 1/samples
            color_to_return = color_to_return * closest_object.reflectness + closest_object.color * (1-closest_object.reflectness)
            # Applying fresnel
            angle_diff = r.direction.invert() * object_normal
            color_to_return = color_to_return * (1-angle_diff) + closest_object.color * angle_diff
        
        elif closest_object.material_type == 'Lambertian':
            unit_sphere_center = closest_hit_point + object_normal

            color_to_return = Color(0,0,0)
            for i in range(samples):
                random_unit_vector = unit_sphere_center + Vector3(random(),random(),random()).normalize()
                random_ray_direction = Vector3.normalize(random_unit_vector - closest_hit_point)
                random_ray = Ray(closest_hit_point + (object_normal * 0.01), random_ray_direction)

                color_to_return += closest_object.color * RecursiveScatteredTrace(random_ray, objects, lights, bounces-1, samples)
            color_to_return *= 1/samples
        return color_to_return

    # Return background Color
    return color_to_return # Background Color return