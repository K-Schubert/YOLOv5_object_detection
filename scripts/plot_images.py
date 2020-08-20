import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import random
import glob

'''
This module samples images from the dataset and creates a mosaic for display purposes.
'''

n_images = 100
image_dirs = os.listdir("../data/birds/")
sampled_dirs = random.sample(image_dirs, n_images)

fig, axs = plt.subplots(10,10,figsize=(6,6))

axs = axs.ravel()

for i in range(n_images):
	jpg_file = glob.glob(f'../data/birds/{sampled_dirs[i]}/*.jpg')[0]
	img = mpimg.imread(jpg_file)
	axs[i].axis('off')
	axs[i].grid(None)
	axs[i].imshow(img, aspect='auto')

plt.subplots_adjust(wspace=0, hspace=0)

plt.savefig("../plots/mosaic.jpg")
plt.show()



