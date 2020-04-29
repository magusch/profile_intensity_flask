import numpy as np
from skimage import io as io2
from skimage import measure
import matplotlib.pyplot as plt
import time,io
import matplotlib

matplotlib.use('agg')



def line_intensity(file):
	image=io2.imread(file)
	horz=len(image[:,0])
	vert=len(image[0,:])
	profile_rgb=measure.profile_line(image,[int(horz/2), int(0.1*vert)],[int(horz/2), int(0.9*vert)], linewidth=int(0.8*horz))
	
	#profile_intensity=profile_rgb[:,0]*0.2126+profile_rgb[:,1]*0.7152+profile_rgb[:,2]*0.0722
	profile_intensity=profile_rgb[:,0]+profile_rgb[:,1]+profile_rgb[:,2]
	print()
	I=profile_intensity[int(0.55*len(profile_intensity)):].max()
	I0=profile_intensity[:int(0.45*len(profile_intensity))].max()
	IdI0=I/I0
	
	plt.plot(range(len(profile_intensity)),profile_intensity)
	plt.legend(['I/I0 = %s' %(IdI0)])
	plt.title('Profile of image')
	#plt.show()
	filename=str(time.time())[4:10]+'.jpg'
	plt.xlabel('Pixel distance')
	plt.ylabel('Pixel intensity')
	plt.savefig(file+ filename)
	plt.close()
	#plt.show()
	return filename
	#return intensity

if __name__ == '__main__':
	file ='image.jpg'
	intensity=line_intensity(file)
