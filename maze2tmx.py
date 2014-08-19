
import getopt,sys

from random import *
from sys import *


def mapCsv(map,width,height):
    csv=""
    #chars=[' ','╶','╷','┌','╴','─','┐','┬','╵','└','│','├','┘','┴','┤','┼']
    chars=['1','9','11','13','15','2','4','6','8','10','12','14','16','3','5','7']
    for y in range(height-1):
     for x in range(width-1):
        u=map[x][y][0]
        l=map[x][y][1]
        d=map[x][y+1][0]
        r=map[x+1][y][1]
        char=u*8+l*4+d*2+r;
        csv=csv+chars[char]+","
        #if r==0: //Diplasiazei tous xaraktires an prokete gia ascii gia na deixnei orthogonio
        #    stdout.write(chars[0]);
        #else:
        #    stdout.write(chars[5]);
     csv=csv+'\n'
    #stdout.write('\n')
    return csv[:-2]
    
def fillMap(width,height):
    '''
    ┌─┬─┐ 
    ├─┼─┤ 
    └─┴─┘
    ''' 
    map=[]
    for x in range(width):
        ta=[] #set captured on edges and fix tile shapes
        for y in range(height):
         if x==0 and y==0:
          ta.append([0,0,1,0])
         elif x==0 and y==height-1:
           ta.append([0,0,1,0])
         elif x==0 or x==width-1:
          ta.append([1,0,1,0])
         elif y==0 or y==height-1:
          ta.append([0,1,1,0]) 
         else:
          ta.append([1,1,0,0]) #right, bottom, captured, backtrack        
        map.append(ta)
    return map


########################################################################
layerWidth=20
layerHeight=20
tileSize=32
tileSet="wall.png"
tileSetWidth=256
tileSetHeight=64


options, remainder = getopt.getopt(sys.argv[1:], 'x:y:s:n:a:q:v:h', ['width=','height=','tilesize=','tilesetname=','tilesetwidth=','tilesetheight' 
                                                           'verbose',
                                                           'help',
                                                           ])

for opt, arg in options:
    if opt in ('-x', '--width'):
       layerWidth=int(arg)
    elif opt in ('-y','--height'):
       layerHeight=int(arg)   
    elif opt in ('-s','--tilesize'):
       tileSize=int(arg)
    elif opt in ('-n','--tilesetname'):
       tileSet=arg
    elif opt in ('-a','--tilesetwidth'):
       tileSetWidth=int(arg)
    elif opt in ('-q','--tilesetheight'):
       tileSetHeight=int(arg)
    elif opt in ('-v', '--verbose'):
          verbose = True
    elif opt in ('-h','--help'):
         print """
Usage: maze2tmx [option] maze.tmx\n
Options:
-w, --width  : Optional,if not set the width is 20 tiles
-h, --height : Optional,if not set the heigth is 20 tiles
-s, --tilesize : Optional,if not set the tile is 32 pixel square
-n, --tilesetname : Optional,if not set the tile name is wall.png
-x, --tilesetwidth: Optional, if not set the width of tile set image is 256px
-y, --tilesetheight: Optional, if not set the height of tile set image is 64px 
-v, --verbose : Optional,letting you see just what the program is doing.
-h, --help    : This Help

maze.tmx is the output name, defaults to maze.tmx 

for example for 64 pixel tileset
maze2tmx -s 64 -n wall64.png -q 512 -v 128

"""
         exit(0)

tmx_filename="maze.tmx"
if len(remainder)!=0:
   tmx_filename=remainder[0]

width=layerWidth+1
height=layerHeight+1

#Initialize map
map = fillMap(width,height)

mazeStart=(1,1) #todo na vazo kana eikoniso start
mazeExit=(width-1,height-1) #todo na vazo kana eikonidio end
mazestart=mazeStart

x,y=mazestart
backtrack=1
captures=6
solutiontrack=0

while 1:
    if (x,y)==mazeExit:
        solutiontrack=backtrack

    if solutiontrack>0 and solutiontrack==map[x][y][3]:
        solutiontrack=solutiontrack-1
        map[x][y][4]=2

    if map[x][y][2]==0:
        map[x][y][2]=1
        captures=captures+1
        if captures%10000==0:
            print >> stderr, 100*captures/(width*height), "%" 

    map[x][y][3]=backtrack
    possibilities=[]
    for a,b in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        if a>=0 and a<width and b>=0 and b<height:
            if map[a][b][2]==0:
                possibilities.append((a,b))

    if len(possibilities)==0:
        map[x][y][3]=0
        backtrack=backtrack-1
        if backtrack==0:
            break
        for a,b in [(x+1,y),(x-1,y),(x,y+1),(x,y-1),(-1,-1)]:
            if a>=0 and a<width and b>=0 and b<height:
                if map[a][b][3]==backtrack:
                    break
                
        x=a
        y=b
        continue
    
    pos=randint(0,len(possibilities)-1)
    a,b=possibilities[pos]
    if a<x: map[a][b][0]=0
    if a>x: map[x][y][0]=0
    if b<y: map[a][b][1]=0
    if b>y: map[x][y][1]=0
    x=a
    y=b
    backtrack=backtrack+1
 

xmlHeader  = '<?xml version="1.0" encoding="UTF-8"?>\n'
xmlHeader = xmlHeader + '<map version="1.0" orientation="orthogonal" width="'+str(layerWidth)+'" height="'+str(layerHeight)+'" tilewidth="'+str(tileSize)+'" tileheight="'+str(tileSize)+'">\n' 
xmlHeader = xmlHeader + '<tileset firstgid="1" name="mazeTiles" tilewidth="'+str(tileSize)+'" tileheight="'+str(tileSize)+'">\n'
xmlHeader = xmlHeader + '<image source="'+tileSet+'" width="'+str(tileSetWidth)+'" height="'+str(tileSetHeight)+'"/>\n</tileset>\n'
xmlHeader = xmlHeader + '<layer name="Maze Layer" width="'+str(layerWidth)+'" height="'+str(layerHeight)+'">\n'
xmlHeader = xmlHeader + '<data encoding="csv">'

xmlFooter =  "</data>\n </layer>\n</map>"

csv = mapCsv(map,width,height)



xml = xmlHeader+csv+"\n"+xmlFooter

f = open(tmx_filename, 'w')
f.write(xml)
f.close()

exit(0)
