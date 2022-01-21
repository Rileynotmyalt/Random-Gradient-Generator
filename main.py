from PIL import Image,ImageOps
import random

#voronoi

#defaults
saveRGB=False
advanced=False
maxCh=20
maxrgb=[254,254,254]
minrgb=[1,1,1]

def chooseColor(choice):
  if True in [char.isdigit() for char in choice]:
    choice=choice.replace('(','')
    choice=choice.replace(')','')
    if ',' in choice:
      choice=choice.replace(' ','')
      sr,sg,sb=choice.split(',',3)
    else:
      sr,sg,sb=choice.split(' ',3)
    srgb=[int(sr),int(sg),int(sb)]
    for i in srgb:
      if i>255:
        i=255
      elif i<0:
        i=0
    sr,sg,sb=srgb[0],srgb[1],srgb[2]

  elif choice.lower() in colorsDict:
    sr,sg,sb=colorsDict[choice.lower()]
  
  elif choice=='':
    sr,sg,sb=(random.randint(0,255),random.randint(0,255),random.randint(0,255))

  else:
    print('Invalid input, try \'red\' or \'255,0,0\'')
    sr,sg,sb=chooseColor(input('Pick a color: '))
  
  return(sr,sg,sb)

#color choices
colorsDict = {
  'black':(0,0,0),
  'white':(255,255,255),
  'red':(255,0,0),
  'orange':(255,165,0),
  'yellow':(255,255,0),
  'green':(0,255,0),
  'blue':(0,0,255),
  'purple':(127,0,255)
}

#alpha test
def alphaTest(alpha):
  global mask
  global imx
  global imy

  
  try: #test if mask input was given or valid
    mask=Image.open(alpha)

    #if gradient and alpha size are not the same
    if mask.width!=imx or mask.height!=imy:
      
      #if alpha is larger than gradient
      if mask.width>imx or mask.height>imy:
        print('\nAlpha appears to be larger than the gradient.')
        print('(1) SCALE aplha to gradient size')
        print('(2) CROP alpha to gradient size')
        print('(3) set gradient to size of alpha')
        
        choice=int(input('Scale Mode: '))
        if choice==1:#scale alpha to gradient size
          mask=ImageOps.fit(mask,(imx,imy))
        if choice==2:#crop alpha to gradient size
          mask=mask.crop((0,0,imx,imy))
        if choice==3:#set gradient size to alpha size
          imx=mask.width
          imy=mask.height
      
      #if alpha is smaller than gradient
      elif mask.width<imx or mask.height<imy:
        print('\nAlpha appears to be smaller than the gradient')
        print('(1) Set gradient to size of alpha')
        print('(2) Scale alpha to gradient')
        print('(3) Custom rescale')

        choice=int(input('Scale Mode: '))
        if choice==1: #scale gradient to alpha
          imx=mask.width
          imy=mask.height
        if choice==2: #scale alpha to gradient
          mask=ImageOps.fit(mask,(imx,imy))
        if choice==3: #custom menu
          #create temporary clear mask size of gradient
          tempmask=Image.new('RGBA',(imx,imy),color=(0,0,0,0))

          #Alpha size input
          try:
            ax=int(input('\nAlpha Width:  '))
            if ax>imx: #size check width
              ax=imx
          except:
            ax=mask.width
          try:
            ay=int(input('Alpha Height: '))
            if ay>imx: #size check height
              ay=imx
          except:
            ay=mask.height
          
          #resize alpha
          mask=ImageOps.fit(mask,(ax,ay))
          print('\n(0) Input Custom Values')
          print('(1) Top Left')
          print('(2) Top Right')
          print('(3) Bottom Right')
          print('(4) Bottom Left')
          print('(5) Center')
          choice=int(input('Align Mode: '))
          if choice==0: #custom
            print('\nTop left corner of gradient is 0,0')
            print('Placement of Alpha is based on the alpha\'s top left corner')
            choice=input('x,y: ')
            if True in [char.isdigit() for char in choice]:
              choice=choice.replace('(','')
              choice=choice.replace(')','')
              if ',' in choice:
                choice=choice.replace(' ','')
                x,y=choice.split(',',2)
              else:
                x,y=choice.split(' ',2)
              x=int(x)
              y=int(y)
              tempmask.paste(mask,box=(x,y))
          if choice==1: #Top Left
            tempmask.paste(mask)
          if choice==2: #Top Right
            tempmask.paste(mask,box=(imx-mask.width,0))
          if choice==3: #bottom right
            tempmask.paste(mask,box=(imx-mask.width,imy-mask.height))
          if choice==4:
            tempmask.paste(mask,box=(0,imy-mask.height))
          if choice==5:
            tempmask.paste(mask,box=(int(imx/2 - mask.width/2) , int(imy/2 - mask.height/2)))
          
          mask=tempmask
   
  except:
    if alpha!='':
      print('Invalid Input, Try again.')
      alphaTest(input('Alpha File Name: '))
    else:
      pass
      

#input
#advanced Choice 
adv=input('Advanced? (y/n)')
if adv.lower()=='y':
  advanced=True

imy=int(input('Image Height: '))
imx=int(input('Image Width:  '))

if advanced==True:
  print('\nThis Picks the color of the pixel in the top left corner of the image.')
  print('\ninput a color')
  print('\'red\',\'orange\',\'yellow\',\'green\',\'blue\',\'purple\',\'white\',\'black\'')
  print('or an r,g,b input. try \'200 200 50\' or \'(200,200,50)\'')
  print('Inputing nothing will return a random color')


sr,sg,sb=chooseColor(input('Pick a color: '))

if advanced==True:
  print('\n(1) Total Range')
  print('(2) Range from starting color')
  rMode=input('Range Mode: ')

  #from max
  if rMode=='1':

    #max
    fromMax=input('Maximum RGB value (255): ')
    if True in [char.isdigit() for char in fromMax] and int(fromMax)<=255:
      maxrgb=[int(fromMax) for x in maxrgb]

    #min 
    fromMin=input('Minimum RGB value (0):   ')
    if True in [char.isdigit() for char in fromMin] and int(fromMin)>=0:
      minrgb=[int(fromMin) for x in minrgb]

  #from start color
  elif rMode=='2':
    print('\nEx: Range from starting color: 40')
    print('if starting color = (100,100,100) the max is (140,140,140), the min is (60,60,60)')
    fromStart=int(input('Range from starting color: '))

    if True in [char.isdigit() for char in str(fromStart)]:
      srgb=[sr,sg,sb]
      for i in range(len(srgb)):
        if fromStart+srgb[i]<255:
          maxrgb[i]=srgb[i]+fromStart
        else:
          maxrgb[i]=255

        if srgb[i]-fromStart>0:
          minrgb[i]=sr-fromStart
        else:
          minrgb[i]=0
  
  #save RGB channels
  print('\nSave image of RGB channels seperately.')
  srgb=input('(y/n): ')
  if srgb.lower()=='y':
    saveRGB=True

  #sensitivity
  print('\nEx: 0 = no change, 10 = can completely change colors per pixel')
  print('Default: .8')
  while 1:
    try:
      sens=input('Sensitivity: ')
      if sens=='':
        sens=0.8
        maxCh=int((float(sens)/10)*255)
        break
      maxCh=int((float(sens)/10)*255)
      break
    except ValueError:
      print('Invalid Input (try: \'1.2\')\n')
    except:
      print('Unexpected Error (try: \'1.2\')\n')

  print('\nEx: Alpha.png')
  alphaTest(input('Alpha File Name: '))
  

im=Image.new("RGB",(int(imx),int(imy)))
pix=im.load()

pix[0,0]=sr,sg,sb

redR=0
greenR=0
blueR=0

print('\nGenerating Image...')

for j in range(im.size[1]): #height
  for i in range(im.size[0]): #width
    rgbval=[random.randint(0,maxCh),random.randint(0,maxCh),random.randint(0,maxCh)]

    if j==0 and i==0: #if first pix
      continue
    
    if i!=0: #if not on the first pix of row
      (r,g,b) = pix[i-1,j] #current row colors
    else:
      (r,g,b) = pix[i,j-1]
    
    if j>0: #if not on the first row
      (r1,g1,b1) = pix[i,j-1] #row above
      (r,g,b) = ( int((r+r1)/2) , int((g+g1)/2) , int((b+b1)/2) )

    Rrgb=[redR,greenR,blueR]
    rgb=[r,g,b]

    for inx in range(len(Rrgb)): #for r g and b chan
      ran=random.randint(0,2)
      if ran==2 or rgb[inx] <= minrgb[inx]+rgbval[inx]: 
        #if current color is lower than min, +
        Rrgb[inx]+=rgbval[inx]
      if ran==0 or rgb[inx] >= maxrgb[inx]-rgbval[inx]: 
        #if current color is higher than max, -
        Rrgb[inx]-=rgbval[inx]
    
    pix[i,j]=(int(r)+Rrgb[0],int(g)+Rrgb[1],int(b)+Rrgb[2],255)
       
    redR=0
    greenR=0
    blueR=0


try:  #try to add mask
  newim=Image.new("RGBA",(im.width,im.height))
  newim.paste(im,mask=mask)
  newim.save('Image.png')
except:
  im.save('Image.png')

if saveRGB==True:

  #Red matrix
  rmatrx=(1, 0, 0, 0,
          0, 0, 0, 0,
          0, 0, 0, 0)
  #green matrix
  gmatrx=(0, 0, 0, 0,
          0, 1, 0, 0,
          0, 0, 0, 0)
  #blue matrix
  bmatrx=(0, 0, 0, 0,
          0, 0, 0, 0,
          0, 0, 1, 0)

  imr=im.convert('RGB',matrix=rmatrx)
  img=im.convert('RGB',matrix=gmatrx)
  imb=im.convert('RGB',matrix=bmatrx)
  try:
    newim=Image.new("RGBA",(im.width,im.height))
    newim.paste(imr,mask=mask)
    imr=newim

    newim=Image.new("RGBA",(im.width,im.height))
    newim.paste(img,mask=mask)
    img=newim

    newim=Image.new("RGBA",(im.width,im.height))
    newim.paste(imb,mask=mask)
    imb=newim
  except:
    pass
  imr.save('ImageRed.png')
  img.save('ImageGreen.png')
  imb.save('ImageBlue.png')

print('\nImage Generated.')