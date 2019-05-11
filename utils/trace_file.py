import math
from vector import vector3
from color import color
from ray import ray

def trace(r, objects, lights):
    
    # Reflection ray
    # Finding closes object on ray
    min_dist = math.inf
    closest_object = None
    closest_hit_point = None
    for object in objects:
        hit_point = object.hit(r)
        if hit_point:
            distance = vector3.magnitude(hit_point - r.origin)
            if distance < min_dist:
                min_dist = distance
                closest_object = object
                closest_hit_point = hit_point
   
    if closest_object is not None:
        # Calculate normal
        object_normal = closest_object.calculate_normal(closest_hit_point)

        # Checking Shadow ray against all light sources
        intensity = 0
        for light in lights:
            object_in_way = False
            # Shadow ray direction is based on type of light
            if light.type == "Directional":
                shadow_ray_direction = light.direction.invert()
            elif light.type == "Point":
                shadow_ray_direction = vector3.normalize(light.position - closest_hit_point)

            # Adding very small normal value before tracing to light source, in order
            # to avoid noise in shading
            shadow_ray = ray(closest_hit_point + (object_normal * 0.01), shadow_ray_direction)
            min_dist = vector3.magnitude(light.position - closest_hit_point)
            # Checking Shadow ray against all objects
            for object in objects:
                hit_point = object.hit(shadow_ray)
                if hit_point:
                    distance = vector3.magnitude(hit_point - shadow_ray.origin)
                    if distance < min_dist:
                        object_in_way = True
                        break

            if not object_in_way:
                # Shading
                diff_angle = shadow_ray_direction * object_normal
                # Clipping diff angle
                if diff_angle < 0:
                    diff_angle = 0
                intensity += light.intensity * diff_angle

        # Clipping intensity
        if intensity > 1:
            intensity = 1

        return closest_object.color * intensity

    # Return background color
    return color(1,1,1) # Background color return