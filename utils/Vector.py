import math

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
        
        k = 1/math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
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
        
            scalar if passed with Vector3

            Vector3 if passed with scalar

        Description:

            if passed with Vector3, performs dot product of the two

            if passed with scalar, multiplies scalar with all components of vector

        '''

        if type(other).__name__ == 'Vector3':
            return self.x*other.x + self.y*other.y + self.z*other.z
        else:
            return Vector3(self.x*other, self.y*other, self.z*other)


    def __mod__(self, other):  # Operator %
        '''
        Returns: 
        
            Vector3

        Description:

            performs cross product

        '''

        return Vector3(other.y*self.z-other.z*self.y, -(other.x*self.z-other.z-self.x), other.x*self.y-other.y-self.x)