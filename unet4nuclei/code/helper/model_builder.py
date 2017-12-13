import keras.layers
import keras.models
import tensorflow as tf

# hyperparameters TODO maybe move to main file?
FLAG_BN = True
FLAG_DO = False
FLAG_DO_LAST_LAYER = False
CONST_DO_RATE = 0.5



option_dict_conv = {"activation": "relu", "border_mode": "same"}
option_dict_bn = {"mode": 0, "momentum" : 0.9}


# returns a core model from gray input to 64 channels of the same size
def get_core(dim1, dim2):
    
    x = keras.layers.Input(shape=(dim1, dim2, 1))

    # DOWN

    a = keras.layers.Convolution2D(64, 3, 3, **option_dict_conv)(x)  
    # a = tf.Print(a, [x], summarize = 100)
    if FLAG_BN:
        a = keras.layers.BatchNormalization(**option_dict_bn)(a)
    if FLAG_DO:
        a = keras.layers.Dropout(CONST_DO_RATE)(a)

    a = keras.layers.Convolution2D(64, 3, 3, **option_dict_conv)(a)
    if FLAG_BN:
        a = keras.layers.BatchNormalization(**option_dict_bn)(a)
    if FLAG_DO:
        a = keras.layers.Dropout(CONST_DO_RATE)(a)

    y = keras.layers.MaxPooling2D()(a)

    b = keras.layers.Convolution2D(128, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        b = keras.layers.BatchNormalization(**option_dict_bn)(b)
    if FLAG_DO:
        b = keras.layers.Dropout(CONST_DO_RATE)(b)

    b = keras.layers.Convolution2D(128, 3, 3, **option_dict_conv)(b)
    if FLAG_BN:
        b = keras.layers.BatchNormalization(**option_dict_bn)(b)
    if FLAG_DO:
        b = keras.layers.Dropout(CONST_DO_RATE)(b)

    y = keras.layers.MaxPooling2D()(b)

    c = keras.layers.Convolution2D(256, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        c = keras.layers.BatchNormalization(**option_dict_bn)(c)
    if FLAG_DO:
        c = keras.layers.Dropout(CONST_DO_RATE)(c)

    c = keras.layers.Convolution2D(256, 3, 3, **option_dict_conv)(c)
    if FLAG_BN:
        c = keras.layers.BatchNormalization(**option_dict_bn)(c)
    if FLAG_DO:
        c = keras.layers.Dropout(CONST_DO_RATE)(c)

    y = keras.layers.MaxPooling2D()(c)

    d = keras.layers.Convolution2D(512, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        d = keras.layers.BatchNormalization(**option_dict_bn)(d)
    if FLAG_DO:
        d = keras.layers.Dropout(CONST_DO_RATE)(d)

    d = keras.layers.Convolution2D(512, 3, 3, **option_dict_conv)(d)
    if FLAG_BN:
        d = keras.layers.BatchNormalization(**option_dict_bn)(d)
    if FLAG_DO:
        d = keras.layers.Dropout(CONST_DO_RATE)(d)

    # UP

    d = keras.layers.UpSampling2D()(d)

    y = keras.layers.merge([d, c], concat_axis=3, mode="concat")

    e = keras.layers.Convolution2D(256, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        e = keras.layers.BatchNormalization(**option_dict_bn)(e)
    if FLAG_DO:
        e = keras.layers.Dropout(CONST_DO_RATE)(e)

    e = keras.layers.Convolution2D(256, 3, 3, **option_dict_conv)(e)
    if FLAG_BN:
        e = keras.layers.BatchNormalization(**option_dict_bn)(e)
    if FLAG_DO:
        e = keras.layers.Dropout(CONST_DO_RATE)(e)

    e = keras.layers.UpSampling2D()(e)

    y = keras.layers.merge([e, b], concat_axis=3, mode="concat")

    f = keras.layers.Convolution2D(128, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        f = keras.layers.BatchNormalization(**option_dict_bn)(f)
    if FLAG_DO:
        f = keras.layers.Dropout(CONST_DO_RATE)(f)

    f = keras.layers.Convolution2D(128, 3, 3, **option_dict_conv)(f)
    if FLAG_BN:
        f = keras.layers.BatchNormalization(**option_dict_bn)(f)
    if FLAG_DO:
        f = keras.layers.Dropout(CONST_DO_RATE)(f)

    f = keras.layers.UpSampling2D()(f)

    y = keras.layers.merge([f, a], concat_axis=3, mode="concat")

    # HEAD

    y = keras.layers.Convolution2D(64, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.Convolution2D(64, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO_LAST_LAYER:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)
    
    return [x, y]


def get_model_3_class(dim1, dim2):
    
    [x, y] = get_core(dim1, dim2)

    y = keras.layers.Convolution2D(3, 1, 1, **option_dict_conv)(y)

    y = keras.layers.Activation("softmax")(y)

    model = keras.models.Model(x, y)
    
    return model


def get_model_1_class(dim1, dim2):
    
    [x, y] = get_core(dim1, dim2)
    
    y = keras.layers.Convolution2D(1, 1, padding="same", activation="sigmoid")(y)
    
    model = keras.models.Model(x,y)

    return model


def get_model_1_class_no_skip(dim1, dim2):
    
    x = keras.layers.Input(shape=(dim1, dim2, 1))

    # DOWN

    y = keras.layers.Convolution2D(64, 3, 3, **option_dict_conv)(x)  
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.Convolution2D(64, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.MaxPooling2D()(y)

    y = keras.layers.Convolution2D(128, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.Convolution2D(128, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.MaxPooling2D()(y)

    y = keras.layers.Convolution2D(256, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.Convolution2D(256, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.MaxPooling2D()(y)

    y = keras.layers.Convolution2D(512, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.Convolution2D(512, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    # UP

    y = keras.layers.UpSampling2D()(y)

    y = keras.layers.Convolution2D(256, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.Convolution2D(256, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.UpSampling2D()(y)

    y = keras.layers.Convolution2D(128, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.Convolution2D(128, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.UpSampling2D()(y)

    # HEAD

    y = keras.layers.Convolution2D(64, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.Convolution2D(64, 3, 3, **option_dict_conv)(y)
    if FLAG_BN:
        y = keras.layers.BatchNormalization(**option_dict_bn)(y)
    if FLAG_DO_LAST_LAYER:
        y = keras.layers.Dropout(CONST_DO_RATE)(y)

    y = keras.layers.Convolution2D(1, 1, padding="same", activation="sigmoid")(y)
    
    model = keras.models.Model(x,y)
    
    return model