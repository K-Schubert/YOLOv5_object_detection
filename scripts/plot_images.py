import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import random

'''
This module samples images from the dataset and creates a mosaic for display purposes.
'''

n_images = 3
image_dirs = os.listdir("../data/birds/")[1:4]
sampled_dirs = random.sample(image_dirs, n_images)

fig, axs = plt.subplots(1,3,figsize=(6,2))

axs = axs.ravel()

for i in range(n_images):
	img = mpimg.imread(f'../data/birds/{sampled_dirs[i]}/00000000.jpg')
	axs[i].axis('off')
	axs[i].grid(None)
	axs[i].imshow(img, aspect='auto')

plt.subplots_adjust(wspace=0, hspace=0)

plt.savefig("../plots/mosaic.jpg")
plt.show()



