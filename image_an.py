import numpy as np
from skimage import io as io2
from skimage import measure
import matplotlib.pyplot as plt
import time,io
import matplotlib

matplotlib.use('agg')



def line_intensity(file):
	image=io2.imread(file)
	profile_rgb=measure.profile_line(image,[0,0],[len(image[:,0]),0], linewidth=len(image[0,:]))
	
	#print(q[250])
	profile_intensity=profile_rgb[:,0]*0.2126+profile_rgb[:,1]*0.7152+profile_rgb[:,2]*0.0722
	plt.plot(range(len(profile_intensity)),profile_intensity)
	#plt.show()
	filename=str(time.time())[4:10]+'.jpg'
	# #bytes_image = io.BytesIO()
	plt.savefig(file+ filename)
	#plt.show()
	return filename
	#return intensity

if __name__ == '__main__':
	file ='image.jpg'
	intensity=line_intensity(file)
