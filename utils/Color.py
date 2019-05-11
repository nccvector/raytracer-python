class Color():

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


    def __add__(self, other):  # Operator +
        '''
        Returns: 
        
            vector3

        Description:

            If passed with vector3, adds the two vectors

            If passed with scalar, adds the scalar to all components of the vector

        '''

        if type(other).__name__ == 'Color':
            return Color(self.r+other.r, self.g+other.g, self.b+other.b)
        else:
            return Color(self.r+other, self.g+other, self.b+other)


    def __mul__(self, other):  # Operator *
        '''
        Returns: 
        
            scalar if passed with vector3

            vector3 if passed with scalar

        Description:

            if passed with vector3, performs dot product of the two

            if passed with scalar, multiplies scalar with all components of vector

        '''

        if type(other).__name__ == 'Color':
            return Color(self.r*other.r, self.g*other.g, self.b*other.b)
        else:
            return Color(self.r*other, self.g*other, self.b*other)