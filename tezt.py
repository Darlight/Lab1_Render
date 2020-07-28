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

#Colores como constantes
GREEN = color(0, 255, 0)
RED = color(255, 0, 0)
BLUE = color(0, 0, 255)
BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255) 

class Render(object):
    def __init__(self):
        #Tamanio del bitmap
        self.framebuffer = []
        self.color = WHITE
        self.bg_color = BLACK
        self.xPort = 0
        self.yPort = 0
        self.glCreateWindow()
    
    #Basicamente __init__ ^ hace esta funcion, asi que cree esta funcion por estética
    def glInit(self):
        return "Bitmap creado... \n"

    def point(self, x, y):
        self.framebuffer[y][x] = self.color

    def glCreateWindow(self, width=800, height=600):
        self.windowWidth = width
        self.windowHeight = height
        self.glClear()
        self.glViewPort(self.xPort, self.yPort, width, height)

    def glViewPort(self, x, y, width, height):
        self.xPort = x
        self.yPort = y
        self.viewPortWidth = width
        self.viewPortHeight = height

    def glClear(self):
        self.framebuffer = [
            [self.bg_color for x in range(self.windowWidth)] for y in range(self.windowHeight)
        ]

    def glClearColor(self, r=0, g=0, b=0):
        self.bg_color = color(r,g,b)

    def glVertex(self, x, y):
        #Formula sacada de:
        # https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glViewport.xhtml
        newX = round((x + 1)*(self.viewPortWidth/2) + self.xPort)
        newY = round((y + 1)*(self.viewPortHeight/2) + self.yPort)
        #funcion point para optimar
        self.point(newX,newY)

    def glColor(self, r=0, g=0, b=0):
        #self.framebuffer[self.yPort][self.xPort] = color(r,g,b)
        #Cambiar los valores de 0-255 a 0-1
        self.color = color(r,g,b)

    def glLine(self, placement, ycardinal = False):
        #variables condicionales y misma formula del vertex
        position = ((placement + 1) * (self.viewPortHeight/2) + self.yPort) if ycardinal else ((placement+1) * (self.viewPortWidth/2) + self.xPort)
        return round(position)

    def Line(self,x1,y1,x2,y2):
        x1 = self.glLine(x1)
        x2 = self.glLine(x2)
        y1 = self.glLine(y1,True)
        y2 = self.glLine(y2,True)
    

        steep = abs(y2 - y1) > abs(x2 - x1)

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        offset = 0
        threshold = dx

        y = y1
        for x in range(x1, x2):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)
            
            offset += dy*2

            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += dx*2
    

            
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

        #ESTA COSA ERA MI ERROR, HABIA COLOCADO MAL LAS COORDENADAS 
        for x in range(self.windowHeight):
            for y in range(self.windowWidth):
                f.write(self.framebuffer[x][y])
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



