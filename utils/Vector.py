import math
import numpy as np

class Vector3():

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


    def normalize(self):
        '''
        Returns: 
        
            Vector3

        Description: 
            
            returns unit vector

        '''
        
        denom = math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        denom = 0.00001 if denom <= 0 else denom
        k = 1/denom
        return Vector3(self.x*k, self.y*k, self.z*k)


    def magnitude(self):
        '''
        Returns: 
        
            scalar

        Description: 
            
            returns magnitude of the vector

        '''

        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    
    def invert(self):
        '''
        Returns: 
        
            Vector3

        Description:

            inverts all the components

        '''

        return Vector3(-self.x, -self.y, -self.z)

    
    def __neg__(self):  # Operator -
        '''
        Returns: 
        
            Vector3

        Description:

            inverts all the components

        '''

        return Vector3(-self.x, -self.y, -self.z)


    def __add__(self, other):  # Operator +
        '''
        Returns: 
        
            Vector3

        Description:

            If passed with Vector3, adds the two vectors

            If passed with scalar, adds the scalar to all components of the vector

        '''

        if type(other).__name__ == 'Vector3':
            return Vector3(self.x+other.x, self.y+other.y, self.z+other.z)
        else:
            return Vector3(self.x+other, self.y+other, self.z+other)

    
    def __sub__(self, other):  # Operator -
        '''
        Returns: 
        
            Vector3

        Description:

            If passed with Vector3, subtracts the two vectors

            If passed with scalar, subtracts the scalar to all components of the vector

        '''

        if type(other).__name__ == 'Vector3':
            return Vector3(self.x-other.x, self.y-other.y, self.z-other.z)
        else:
            return Vector3(self.x-other, self.y-other, self.z-other)


    def __mul__(self, other):  # Operator *
        '''
        Returns: 
        
            Vector3

        Description:

            if passed with Vector3, performs dot product of the two

            if passed with scalar, multiplies scalar with all components of vector

        '''

        if type(other).__name__ == 'Vector3':
            return Vector3(self.x*other.x , self.y*other.y , self.z*other.z)
        else:
            return Vector3(self.x*other, self.y*other, self.z*other)


    def dot(self, other):
        '''
        Returns: 
        
            Vector3

        Description:

            if passed with Vector3, performs dot product of the two

            if passed with scalar, multiplies scalar with all components of vector

        '''
        
        return np.dot([self.x,self.y,self.z], [other.x,other.y,other.z])


    def cross(self, other):
        '''
        Returns: 
        
            Vector3

        Description:

            performs cross product

        '''
        cross = np.cross([self.x,self.y,self.z], [other.x,other.y,other.z])
        return Vector3(cross[0], cross[1], cross[2])