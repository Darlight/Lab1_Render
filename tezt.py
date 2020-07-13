"""
Universidad del Valle de Guatemala
Gráficas por computadora
Seccion 10
Lic. Dennis Aldana
Mario Perdomo
18029

tezt.py
Proposito: Un framebuffer simple para pintar un punto con modificaciones simples como:
- Cambiar de color de los puntos
- Crear un punto
- Modificaciones del tamaño de la venta principal
"""
#struc pack
# wikipedia bmp file format
import struct
#opcion = 0
def char(c):
    # un char que vale un caracter de tipo string
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    #convierte el numero de posicion de pixel a 2 bytes
    return struct.pack('=h', c)

def dword(c):
    #4 bytes de la estructura de un framebuffer
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([b, g, r])

class Render(object):
    def __init__(self):
        #Tamanio del bitmap
        self.windowWidth = 0
        self.windowHeight = 0
        self.viewPortWidth = 0
        self.viewPortHeight = 0
        self.color = RED
        self.xPort = 0
        self.yPort = 0
        self.framebuffer = []
    #Basicamente __init__ ^ hace esta funcion, asi que cree esta funcion por estética
    def glInit(self):
        return "Bitmap creado... \n"

    def glCreateWindow(self, width, height):
        self.windowWidth = width
        self.windowHeight = height
        self.framebuffer = [
            [BLACK for x in range(self.windowWidth)]
            for y in range(self.windowHeight)
        ]

    def glViewPort(self, x, y, width, height):
        self.xPort = x
        self.yPort = y
        self.viewPortWidth = width
        self.viewPortHeight = height

    def glClear(self):
        self.framebuffer = [
            [BLUE for x in range(self.windowWidth)]
            for y in range(self.windowHeight)
        ]

    def glClearColor(self, r=0, g=0, b=0):
        self.framebuffer = [
            [color(r,g,b) for x in range(self.windowWidth)]
            for y in range(self.windowHeight)
        ]

    def glVertex(self, x, y):
        #Formula sacada de:
        # https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glViewport.xhtml
        newX = round((x + 1)*(self.viewPortWidth/2)) + self.xPort
        newY = round((y + 1)*(self.viewPortHeight/2)) + self.yPort
        self.framebuffer[newY][newX] = self.color

    def glColor(self, r=0, g=0, b=0):
        #self.framebuffer[self.yPort][self.xPort] = color(r,g,b)
        self.color = color(r,g,b)
        

    def glFinish(self, filename):
        f = open(filename, 'bw')
        # file header
        f.write(char('B'))
        f.write(char('M'))

        f.write(dword(14 + 40 + self.windowWidth * self.windowHeight * 3))

        f.write(dword(0))

        f.write(dword(14 + 40))

        # image header 
        f.write(dword(40))
        f.write(dword(self.windowWidth))
        f.write(dword(self.windowHeight))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.windowWidth * self.windowHeight * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # pixel data
        for x in range(self.windowWidth):
            for y in range(self.windowHeight):
                f.write(self.framebuffer[y][x])
        f.close()



#def point(self, x, y):
#   self.framebuffer[y][x] = color(255, 0, 0)

#Colores como constantes
GREEN = color(0, 255, 0)
RED = color(255, 0, 0)
BLUE = color(0, 0, 255)
BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255) 

#bitmap es el producto final, debo hacer un  menu completo 
# 128, 64
bitmap = Render()
print(bitmap.glInit())
bitmap.glCreateWindow(128,64)
bitmap.glViewPort(10,10,64,32)
bitmap.glClear()
bitmap.glVertex(1,1)
bitmap.glVertex(-1,-1)
bitmap.glVertex(0,0)
bitmap.glFinish('out.bmp')

#Ya no hice el menu <_< 
#No era necesarioa crearlo...
#while opcion != 3:
 #   opcion = int(input("============\n Escritor de imágenes BMP \n============ \n Eliga la opcion que desea: \n 1- Cambiar color de un punto \n 2- Cambiar color de la ventana \n 3 - Salir del progrma \n"))
   # if opcion == 1:
  #      print("algo")
    #elif opcion == 2:
     #   print("algo2")



