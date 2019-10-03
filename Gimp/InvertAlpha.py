#!/usr/bin/env python

import math
from array import *
from gimpfu import *


# Print to the error console of gimp
def PrintGimp(text):
   pdb.gimp_message(text)

def InvertAlpha(image, layer):
   # Do nothing if image has no alpha
   if(layer.has_alpha == False):
      PrintGimp("Layer has no alpha channel")
      return
   
   layerTarget = gimp.Layer(image, layer.name + "Inv", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
   image.add_layer(layerTarget,1)
   
   width = layer.width
   height = layer.height

   # It is faster to work with regions when changing pixel data
   # than accessing each pixel individually using the pdb.gimp_drawable_set_pixel
   # methode.
   #
   # Example for writing into a pixel reagion can be found here
   # http://gimpbook.com/scripting/slides/pixelrgns.html
   pixelRegionSource = layer.get_pixel_rgn(0,0,width,height,False,False)
   pixelRegionTarget = layerTarget.get_pixel_rgn(0,0,width,height,True,False)
   
   for x in range(width):
      for y in range(height):
         pixel = pixelRegionSource[x,y] # returns pixel as string
         pixelAsArray = array("B", pixel) # string to int
         pixelAsArray[3] = 255 - pixelAsArray[3] # invert alpha
         pixelRegionTarget[x,y] = pixelAsArray.tostring()
     
   layerTarget.flush()
   layerTarget.update(0, 0, width, height)


register(
        "InvertAlpha",
        "Inverts the alpha channel of a layer and places the result into a new layer",
        "Inverts the alpha channel of a layer and places the result into a new layer",
        "James Henstridge",
        "James Henstridge",
        "1997-1999",
        "<Image>/Filters/MyScripts/InvertAlpha",
        "RGB*, GRAY*",
        [],
        [],
        InvertAlpha)

main()
