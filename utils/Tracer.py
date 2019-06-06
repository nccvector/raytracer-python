import math
from utils.Vector import Vector3
from utils.Ray import Ray
from random import random

def Trace(r, objects, bounce_samples, bounces=1):
    if bounces >= 0:
        # Checking closest hit
        closest_hit_point = None # needed to calculate normal for spheres
        closest_object = None
        min_dist = math.inf
        for object in objects:
            hit_point = object.hit(r)
            if hit_point is not None:
                distance = Vector3.magnitude(r.origin - hit_point)
                if distance < min_dist:
                    closest_hit_point = hit_point
                    closest_object = object
                    min_dist = distance

        if closest_object is not None:
            if closest_object.type == 'Light':
                return closest_object.color
            else:
                avg_bounce_color = Vector3(0,0,0)
                for _ in range(bounce_samples):
                    # If closest object is object, we need its normal
                    normal = closest_object.calculate_normal(closest_hit_point)
                    rl_origin = closest_hit_point + normal * 0.00001
                    rl_direction = r.direction - (normal * (Vector3.dot(r.direction, normal) * 2.0))
                    rl_direction += Vector3(0.5-random(),0.5-random(),0.5-random()) * closest_object.material.roughness
                    rl_direction = Vector3.normalize(rl_direction)

                    rl_ray = Ray(rl_origin, rl_direction)
                    rl_color = Trace(rl_ray, objects, bounce_samples=bounce_samples-1, bounces=bounces-1)

                    if rl_color is not None:
                        avg_bounce_color += rl_color
                
                if bounce_samples > 1:
                    avg_bounce_color *= 1/bounce_samples

                return closest_object.material.color * avg_bounce_color

    return None