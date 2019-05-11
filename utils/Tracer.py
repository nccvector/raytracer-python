import math
from utils.Vector import Vector3
from utils.Color import Color
from utils.Ray import Ray

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