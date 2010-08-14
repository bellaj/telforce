__doc__ = """ Includes the StringGen class which generates random character
            strings.
            -micron
            
            """

import random

class StringGen():
    """ Generates a list of random characters. """
    lletters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
               'p','q','r','s','t','u','v','w','x','y','z')
    uletters = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
                'P','Q','R','S','T','U','V','W','X','Y','Z')
    numbers = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    characters = ('!', '~','@','#','$','%','^','&','*','(',')')

    def gen_character(self):
        """ Returns a random character from the 'characters' list. """
        return random.choice(self.characters)
        
    def gen_letter(self, u=0):
        """ Returns a random letter from lletters or uletters depending
        on u and another random choice.
        
        param:
        u -- if true, include capital letters otherwise stick to lower-case.

        """
        if u:
            n = random.random()
            if n < 0.5:
                return random.choice(self.lletters)
            else:
                return random.choice(self.uletters)
        return random.choice(self.lletters)
    
    def gen_number(self):
        """ Return a random number from the numbers list 'numbers'. """
        return random.choice(self.numbers)
    
    def next_char(self, prev, u=0, s=0):
        """ The next character is 50% more likely to be of the same
        type as the previous.
        
        param:
        prev -- the previous character.
        u -- if true, use captial letters as well as lowercase.

        """
        n = random.random()
        if isinstance(prev, (int)):
            if n < 0.75:
                return self.gen_number()
            else:
                return self.gen_letter(u)
        else:
            if n < 0.25:
                return self.gen_number()
            else:
                return self.gen_letter(u)
            
    def generate(self, wlen, u=0, s=0):
        """ Generate a random string of len 'wlen'.
        params:
        wlen -- the length of the string to generate.

        """
        if random.random() < 0.5:
            prev = self.gen_number()
            stri = str(prev)
        else:
            stri = prev = self.gen_letter()
        for i in range(wlen-1):
            prev = self.next_char(prev)
            stri = stri + str(prev)
        return stri
        
if __name__ == "__main__":
    gen = StringGen()
    
    print('Generating strings..')
    for i in range(10):
        print(gen.generate(6))

    for i in range(10):
        print(gen.generate(7))

    for i in range(10):
        print(gen.generate(8))

    print('Done.')

        
