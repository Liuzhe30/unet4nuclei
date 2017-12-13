import helper.visualize
import helper.data_provider
import helper.model_builder

import skimage.io

import sys

import keras
import tensorflow as tf

# build session running on a specific GPU
configuration = tf.ConfigProto()
configuration.gpu_options.allow_growth = True
configuration.gpu_options.visible_device_list = "1"
session = tf.Session(config = configuration)

# apply session
keras.backend.set_session(session)

data_dir_x = "/home/jr0th/github/segmentation/data/BBBC022/test/x/"
data_dir_y = "/home/jr0th/github/segmentation/data/BBBC022/test/y_boundary_2/"

hard = True
rescale_labels = False

tag = 'DL_on_Hand_boundary_2'

out_label = 'pred_generator'

out_dir = '/home/jr0th/github/segmentation/out/' + tag + '/'

weights_path = '/home/jr0th/github/segmentation/checkpoints/' + tag + '/checkpoint_0010.hdf5'
batch_size = 10
bit_depth = 8

dim1 = 256
dim2 = 256

# get generator for test data
test_generator = helper.data_provider.single_data_from_images_1d_y(
    data_dir_x,
    data_dir_y,
    batch_size,
    bit_depth,
    dim1, 
    dim2,
    rescale_labels
)

# build model and laod weights
model = helper.model_builder.get_model_1_class(dim1, dim2)
model.load_weights(weights_path)

# get one batch of data from the generator
(test_x, test_y) = next(test_generator)

# get model predictions
y_pred = model.predict_on_batch(test_x)

# visualize them
if(hard):
    helper.visualize.visualize_boundary_hard(y_pred, test_x, test_y, out_dir=out_dir, label=out_label)
else:
    helper.visualize.visualize_boundary_soft(y_pred, test_x, test_y, out_dir=out_dir, label=out_label)