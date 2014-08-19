maze2tmx
========

Create Maze with TMX format

Usage: maze2tmx [option] maze.tmx
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
