
# coding: utf-8

# # Classification: Instant Recognition with Caffe
# 
# In this example we'll classify an image with the bundled CaffeNet model (which is based on the network architecture of Krizhevsky et al. for ImageNet).
# 
# We'll compare CPU and GPU modes and then dig into the model to inspect features and the output.

# ### 1. Setup
# 
# * First, set up Python, `numpy`, and `matplotlib`.

# In[4]:


# set up Python environment: numpy for numerical routines, and matplotlib for plotting
import numpy as np
import matplotlib.pyplot as plt
# display plots in this notebook
get_ipython().run_line_magic('matplotlib', 'inline')

# set display defaults
plt.rcParams['figure.figsize'] = (10, 10)        # large images
plt.rcParams['image.interpolation'] = 'nearest'  # don't interpolate: show square pixels
plt.rcParams['image.cmap'] = 'gray'  # use grayscale output rather than a (potentially misleading) color heatmap


# * Load `caffe`.

# In[5]:


import caffe
# If you get "No module named _caffe", either you have not built pycaffe or you have the wrong path.


# * If needed, download the reference model ("CaffeNet", a variant of AlexNet).

# In[6]:


get_ipython().system('ls Caffe/')


# In[7]:


import os
caffe_root = "Caffe/"
if os.path.isfile(caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'):
    print 'CaffeNet found.'
else:
    print 'Downloading pre-trained CaffeNet model...'
    get_ipython().system('../scripts/download_model_binary.py ../models/bvlc_reference_caffenet')


# ### 2. Load net and set up input preprocessing
# 
# * Set Caffe to CPU mode and load the net from disk.

# In[8]:


caffe.set_mode_cpu()

caffe_root = "/home/jack/Desktop/Ubuntu16.04/notebooks/Caffe/Caffe/"
model_def = caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
model_weights = caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)


# * Set up input preprocessing. (We'll use Caffe's `caffe.io.Transformer` to do this, but this step is independent of other parts of Caffe, so any custom preprocessing code may be used).
# 
#     Our default CaffeNet is configured to take images in BGR format. Values are expected to start in the range [0, 255] and then have the mean ImageNet pixel value subtracted from them. In addition, the channel dimension is expected as the first (_outermost_) dimension.
#     
#     As matplotlib will load images with values in the range [0, 1] in RGB format with the channel as the _innermost_ dimension, we are arranging for the needed transformations here.

# In[9]:


# load the mean ImageNet image (as distributed with Caffe) for subtraction
caffe_root = "/home/jack/Desktop/Ubuntu16.04/notebooks/Caffe/Caffe/"
mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
print 'mean-subtracted values:', zip('BGR', mu)

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR


# ### 3. CPU classification
# 
# * Now we're ready to perform classification. Even though we'll only classify one image, we'll set a batch size of 50 to demonstrate batching.

# In[10]:


# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
net.blobs['data'].reshape(50,        # batch size
                          3,         # 3-channel (BGR) images
                          227, 227)  # image size is 227x227


# * Load an image (that comes with Caffe) and perform the preprocessing we've set up.

# In[11]:


caffe_root = "/home/jack/Desktop/Ubuntu16.04/notebooks/Caffe/Caffe/"
image = caffe.io.load_image(caffe_root + 'examples/images/cat.jpg')
transformed_image = transformer.preprocess('data', image)
plt.imshow(image)


# * Adorable! Let's classify it!

# In[12]:


# copy the image data into the memory allocated for the net
net.blobs['data'].data[...] = transformed_image

### perform classification
output = net.forward()

output_prob = output['prob'][0]  # the output probability vector for the first image in the batch

print 'predicted class is:', output_prob.argmax()


# * The net gives us a vector of probabilities; the most probable class was the 281st one. But is that correct? Let's check the ImageNet labels...

# In[13]:


get_ipython().system('locate /data/ilsvrc12/get_ilsvrc_aux.sh')


# In[14]:


# load ImageNet labels
caffe_root = "/home/jack/Desktop/Ubuntu16.04/notebooks/Caffe/Caffe/"
labels_file = caffe_root + 'data/ilsvrc12/synset_words.txt'
if not os.path.exists(labels_file):
    get_ipython().system('/home/jack/Desktop/Ubuntu16.04/notebooks/Caffe/Caffe/data/ilsvrc12/get_ilsvrc_aux.sh')
    
labels = np.loadtxt(labels_file, str, delimiter='\t')

print 'output label:', labels[output_prob.argmax()]


# * "Tabby cat" is correct! But let's also look at other top (but less confident predictions).

# In[15]:


# sort top six predictions from softmax output
top_inds = output_prob.argsort()[::-1][:6]  # reverse sort and take five largest items

print 'probabilities and labels:'
zip(output_prob[top_inds], labels[top_inds])


# * We see that less confident predictions are sensible.

# ### 4. Switching to GPU mode
# 
# * Let's see how long classification took, and compare it to GPU mode.

# In[16]:


get_ipython().run_line_magic('timeit', 'net.forward()')


# * That's a while, even for a batch of 50 images. Let's switch to GPU mode.

# In[17]:


#caffe.set_device(0)  # if we have multiple GPUs, pick the first one
#caffe.set_mode_gpu()
net.forward()  # run once before timing to set up memory
get_ipython().run_line_magic('timeit', 'net.forward()')


# * That should be much faster!

# ### 5. Examining intermediate output
# 
# * A net is not just a black box; let's take a look at some of the parameters and intermediate activations.
# 
# First we'll see how to read out the structure of the net in terms of activation and parameter shapes.
# 
# * For each layer, let's look at the activation shapes, which typically have the form `(batch_size, channel_dim, height, width)`.
# 
#     The activations are exposed as an `OrderedDict`, `net.blobs`.

# In[19]:


# for each layer, show the output shape
for layer_name, blob in net.blobs.iteritems():
    print layer_name + '\t' + str(blob.data.shape)


# * Now look at the parameter shapes. The parameters are exposed as another `OrderedDict`, `net.params`. We need to index the resulting values with either `[0]` for weights or `[1]` for biases.
# 
#     The param shapes typically have the form `(output_channels, input_channels, filter_height, filter_width)` (for the weights) and the 1-dimensional shape `(output_channels,)` (for the biases).

# In[20]:


for layer_name, param in net.params.iteritems():
    print layer_name + '\t' + str(param[0].data.shape), str(param[1].data.shape)


# * Since we're dealing with four-dimensional data here, we'll define a helper function for visualizing sets of rectangular heatmaps.

# In[21]:


def vis_square(data):
    """Take an array of shape (n, height, width) or (n, height, width, 3)
       and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)"""
    
    # normalize data for display
    data = (data - data.min()) / (data.max() - data.min())
    
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = (((0, n ** 2 - data.shape[0]),
               (0, 1), (0, 1))                 # add some space between filters
               + ((0, 0),) * (data.ndim - 3))  # don't pad the last dimension (if there is one)
    data = np.pad(data, padding, mode='constant', constant_values=1)  # pad with ones (white)
    
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    
    plt.imshow(data); plt.axis('off')


# * First we'll look at the first layer filters, `conv1`

# In[22]:


# the parameters are a list of [weights, biases]
filters = net.params['conv1'][0].data
vis_square(filters.transpose(0, 2, 3, 1))


# * The first layer output, `conv1` (rectified responses of the filters above, first 36 only)

# In[23]:


feat = net.blobs['conv1'].data[0, :36]
vis_square(feat)


# * The fifth layer after pooling, `pool5`

# In[24]:


feat = net.blobs['pool5'].data[0]
vis_square(feat)


# * The first fully connected layer, `fc6` (rectified)
# 
#     We show the output values and the histogram of the positive values

# In[25]:


feat = net.blobs['fc6'].data[0]
plt.subplot(2, 1, 1)
plt.plot(feat.flat)
plt.subplot(2, 1, 2)
_ = plt.hist(feat.flat[feat.flat > 0], bins=100)


# * The final probability output, `prob`

# In[26]:


feat = net.blobs['prob'].data[0]
plt.figure(figsize=(15, 3))
plt.plot(feat.flat)


# Note the cluster of strong predictions; the labels are sorted semantically. The top peaks correspond to the top predicted labels, as shown above.

# ### 6. Try your own image
# 
# Now we'll grab an image from the web and classify it using the steps above.
# 
# * Try setting `my_image_url` to any JPEG image URL.

# In[27]:


# download an image
#my_image_url = "http://cdn.thehorse.com/images/cms/2017/07/lean-performance-horse.jpg?preset=medium"  # paste your URL here
my_image_url = "https://s7d1.scene7.com/is/image/PETCO/dog-category-090617-369w-269h-hero-cutout-d?fmt=png-alpha"

# for example:
# my_image_url = "https://upload.wikimedia.org/wikipedia/commons/b/be/Orang_Utan%2C_Semenggok_Forest_Reserve%2C_Sarawak%2C_Borneo%2C_Malaysia.JPG"
get_ipython().system('wget -O image.jpg $my_image_url')

# transform it and copy it into the net
image = caffe.io.load_image('image.jpg')
net.blobs['data'].data[...] = transformer.preprocess('data', image)

# perform classification
net.forward()

# obtain the output probabilities
output_prob = net.blobs['prob'].data[0]

# sort top five predictions from softmax output
top_inds = output_prob.argsort()[::-1][:5]

plt.imshow(image)

print 'probabilities and labels:'
zip(output_prob[top_inds], labels[top_inds])


# In[29]:


get_ipython().run_cell_magic('writefile', 'compile_caffe_ubuntu_16.04.sh', '#!/bin/bash\n\nset -v\nNUMBER_OF_CORES=2\n\napt-get update  \napt-get -y install make\napt-get -y install cmake\napt-get -y install git  \napt-get -y install curl  \napt-get -y install gcc-4.6 build-essential  \napt-get -y install python-dev  \napt-get -y install python-pip  \npip install --upgrade pip  \npip install numpy  \napt-get -y install liblmdb-dev  \napt-get -y install libhdf5-serial-dev  \napt-get -y install libleveldb-dev libsnappy-dev  \napt-get -y install libopencv-dev  \napt-get -y install libprotobuf-dev  \napt-get -y install protobuf-compiler  \napt-get -y install --no-install-recommends libboost-all-dev  \napt-get -y install libgflags-dev  \napt-get -y install libgoogle-glog-dev  \napt-get -y install libatlas-base-dev  \ngit clone https://github.com/BVLC/caffe.git Caffe  \ncd Caffe  \n\n\n# Prepare Python binding (pycaffe)\ncd python\nfor req in $(cat requirements.txt); do pip install $req; done\necho "export PYTHONPATH=$(pwd):$PYTHONPATH " >> ~/.bash_profile # to be able to call "import caffe" from Python after reboot\nsource ~/.bash_profile # Update shell \ncd ..\n\n# Compile caffe and pycaffe\ncp Makefile.config.example Makefile.config\nsed -i \'8s/.*/CPU_ONLY := 1/\' Makefile.config # Line 8: CPU only\napt-get -y install -y libopenblas-dev\nsed -i \'33s/.*/BLAS := open/\' Makefile.config # Line 33: to use OpenBLAS\n# Note that if one day the Makefile.config changes and these line numbers change, we\'re screwed\n# Maybe it would be best to simply append those changes at the end of Makefile.config \necho "export OPENBLAS_NUM_THREADS=($NUMBER_OF_CORES)" >> ~/.bash_profile \nmkdir build\ncd build\ncmake ..\ncd ..\nmake all -j$NUMBER_OF_CORES # 4 is the number of parallel threads for compilation: typically equal to number of physical cores\nfor requirement in $(cat ./python/requirements.txt); do  \n    pip install $requirement\ndone  \nmake pycaffe  -j$NUMBER_OF_CORES\nmake test\nmake runtest\n#make matcaffe\nmake distribute\ncp -ar ./Caffe/distribute /usr/local/caffe  \nif [[ -z $(cat ~/.bashrc | grep /usr/local/caffe/bin) ]] ; then  \n    echo -e "\\n# Adds Caffe to the PATH variable" >> ~/.bashrc\n    echo "export PATH=\\$PATH:/usr/local/caffe/bin" >> ~/.bashrc\n    echo "export CPATH=\\$CPATH:/usr/local/caffe/include" >> ~/.bashrc\n    echo "export PYTHONPATH=\\$PYTHONPATH:/usr/local/caffe/python" >> ~/.bashrc\n    echo "export LD_LIBRARY_PATH=\\$LD_LIBRARY_PATH:/usr/local/caffe/lib" >> ~/.bashrc\n    source ~/.bashrc\nfi  ')

