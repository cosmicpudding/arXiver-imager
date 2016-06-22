# ArXiv image grabber
import urllib
import os
import sys
import random
from numpy import *
from scipy import misc
from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['serif']})
import matplotlib.pyplot as pl
import unicodedata
import re
import time
import platform

# Start time
stime = time.time()

# Check architecture
archit = platform.platform().lower()

os.system('rm -rf temp')
os.system('mkdir temp')

# Set folder containing figures
folder = '1201.2700'
linkformat = 'AuthorEtAl-%s' % folder
arxiverflag = False

print 'Processing... %s' % folder

# Get the actual tarball
link = 'http://arxiv.org/e-print/%s' % folder
out = open('temp/%s' % folder,'w')
print '... downloading ...'
out.write(urllib.urlopen(link).read())
out.flush()

# Comment out temporarily for testing
os.system('tar --directory temp -xvf %s' % ('temp/%s' % folder))

#######################################################################################

# FIND IMAGES

# Check if jpg, or eps, or pdf, or png
fignames = []
figtype = None

# Look for all types of images
figs =  os.popen('find temp -name "*.pdf"')
for x in figs:
    fignames.append(x.strip())

figs =  os.popen('find temp -name "*.eps"')
for x in figs:
    fignames.append(x.strip())

figs =  os.popen('find temp -name "*.ps"')
for x in figs:
    fignames.append(x.strip())

figs =  os.popen('find temp -name "*.jpg"')
for x in figs:
    fignames.append(x.strip())

figs =  os.popen('find temp -name "*.png"')
for x in figs:
    fignames.append(x.strip())


#######################################################################################

# CONVERT IMAGES
                
# Now that images are found
figures = []

if len(fignames) == 0:
    print "I'm outta here!"

else:

    # For each figure in list
    for i in range(0,len(fignames)):
        fname = fignames[i]
        figtype = fname.split('.')[-1]
        print fname,figtype

        # Ignore "whitespace" figures!
        if 'whitespace' in fname:
            continue

        # check for arxiverflag
        if arxiverflag == True:

            # Only consider figures of use
            if fname.split('/')[-1] not in specfigs:
                print 'Skipping non-specified author figure...'
                continue

            else:
                ipip+=1

        else:
            ipip = i

        if figtype == 'pdf':

                # Convert to jpg
                retval = 0
                retval = os.system('pdfcrop %s' % fname)
                if (retval < 0):
                    continue
                if 'linux' in archit:
                    retval = os.system('convert -resize 1024 -density 200 -background white -flatten %s temp/%s_f%i.jpg' % (fname.split('.pdf')[0]+'-crop.pdf',linkformat,(ipip+1)))
                if 'darwin' in archit:
                    retval = os.system('sips -Z 1024 -s format jpeg %s --out temp/%s_f%i.jpg' % (fname.split('.pdf')[0]+'-crop.pdf',linkformat,(ipip+1)))
                if (retval < 0):
                    continue
                figures.append('temp/%s_f%i.jpg' % (linkformat,(ipip+1)))
                
        elif figtype == 'eps':

                # Convert to jpg
                retval = 0
                retval = os.system('ps2pdf -dEPSCrop %s %s' % (fname,(fname.split('.eps')[0]+'.pdf')))
                if (retval < 0):
                    continue
                retval = os.system('pdfcrop %s' % (fname.split('.eps')[0]+'.pdf'))
                if (retval < 0):
                    continue
                if 'linux' in archit:
                    retval = os.system('convert -resize 1024 -density 200 -background white -flatten %s temp/%s_f%i.jpg' % (fname.split('.eps')[0]+'-crop.pdf',linkformat,(ipip+1)))
                if 'darwin' in archit:
                    retval = os.system('sips -Z 1024 -s format jpeg %s --out temp/%s_f%i.jpg' % (fname.split('.eps')[0]+'-crop.pdf',linkformat,(ipip+1)))
                if (retval < 0):
                    continue
                figures.append('temp/%s_f%i.jpg' % (linkformat,(ipip+1)))
                
        elif figtype == 'ps':
            
                # Convert to jpg
                retval = 0
                retval = os.system('ps2eps -B -C < %s > temp/f%i.eps' % (fname,(ipip+1)))
                if (retval < 0):
                    continue
                retval = os.system('ps2pdf -dEPSCrop temp/f%i.eps temp/f%i.pdf' % ((ipip+1),(ipip+1)))
                if (retval < 0):
                    continue
                retval = os.system('pdfcrop temp/f%i.pdf' % (ipip+1))
                if (retval < 0):
                    continue
                if 'linux' in archit:
                    retval = os.system('convert -resize 1024 -density 200 -background white -flatten temp/f%i-crop.pdf temp/%s_f%i.jpg' % ((ipip+1),linkformat,(ipip+1)))
                if 'darwin' in archit:
                    retval = os.system('sips -Z 1024 -s format jpeg temp/f%i-crop.pdf --out temp/%s_f%i.jpg' % ((ipip+1),linkformat,(ipip+1)))
                if (retval < 0):
                    continue
                figures.append('temp/%s_f%i.jpg' % (linkformat,(ipip+1)))

        elif figtype == 'png':

                # Convert to jpg
                retval = 0
                if 'linux' in archit:
                    retval = os.system('convert -resize 1024 -density 200 -background white -flatten %s temp/%s_f%i.jpg' % (fname,linkformat,(ipip+1)))
                if 'darwin' in archit:
                    retval = os.system('sips -Z 1024 -s format jpeg %s --out temp/%s_f%i.jpg' % (fname,linkformat,(ipip+1)))
                if (retval < 0):
                    continue
                figures.append('temp/%s_f%i.jpg' % (linkformat,(ipip+1)))

        elif figtype == 'jpg':

                # Change name of jpg
                os.system('mv %s temp/%s_f%i.jpg' % (fname,linkformat,(ipip+1)))
                figures.append('temp/%s_f%i.jpg' % (linkformat,(ipip+1)))

# redo figures array (accounting for missing fs that don't convert properly)
lefigures = []
for x in range(1,len(figures)+1):
    test = os.popen('ls temp/%s_f%i.jpg' % (linkformat,x))
    ys = []
    for y in test:
        ys.append(y.strip())
    if len(ys) > 0:
        lefigures.append(y.strip())

print "********"
print lefigures
print "********"

# Default arxiver image if no images have converted correctly
if len(lefigures) < 1:
    lefigures.append('arxiver.png')

scores = {}

#######################################################################################

# CHOOSE IMAGES

for figure in lefigures:
        print 'Processing',figure,'...'
        
        img = misc.imread(figure, flatten=True)
        ix = shape(img)[0] 
        iy = shape(img)[1] 
        inpx = ix*iy

        # fourier transform
        ift = log10(abs(fft.fft2(img)))
        ift[0][0] = 0.0
        ift = fft.fftshift(ift)
        ftm = ift.max()
        ift = ift / ftm

        # New shape
        fx = shape(ift)[0] 
        fy = shape(ift)[1] 
        fnpx = fx*fy

        # Get score
        inf = ift.sum() / fnpx

        # Store the score
        if inf in scores.keys():
            scores[inf].append(figure)
        else:
            scores[inf] = [figure]

# Process scores
scores2 = scores.keys()[::]
scores2.sort()

# Get max, min, middle
middle = int(len(scores)/2.0)

# Deal with potential less figures
final = []
if len(scores2) > 3:
    final.append(scores[scores2[0]][0])
    final.append(scores[scores2[middle]][0])
    final.append(scores[scores2[-1]][0])
elif len(scores2) == 3:
    final.append(scores[scores2[0]][0])
    final.append(scores[scores2[1]][0])
    final.append(scores[scores2[2]][0])
elif len(scores2) == 2:
    final.append(scores[scores2[0]][0])
    final.append(scores[scores2[1]][0])
elif len(scores2) == 1:
    final.append(scores[scores2[0]][0])

# Print the resulting choice
print final

# Print end time
etime = time.time() - stime 
print 'Total time to run arXiver (figure version): %.1f min' % (etime/60.)
