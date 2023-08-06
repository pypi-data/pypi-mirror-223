from tensorflow.keras.layers import Input, Dropout, concatenate, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model

def build_unet(input_shape=(224, 224, 3)):
    fil = 16

    inputs = Input(input_shape)

    conv1 = Conv2D(fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(inputs)
    conv1 = Conv2D(fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2), strides = (2, 2))(conv1)

    conv2 = Conv2D(2*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(pool1)
    conv2 = Conv2D(2*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2), strides = (2, 2))(conv2)

    conv3 = Conv2D(4*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(pool2)
    conv3 = Conv2D(4*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(conv3)
    pool3 = MaxPooling2D(pool_size=(2, 2), strides = (2, 2))(conv3)

    conv4 = Conv2D(8*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(pool3)
    conv4 = Conv2D(8*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(conv4)
    drop4 = Dropout(0.5)(conv4)
    pool4 = MaxPooling2D(pool_size=(2, 2), strides = (2, 2))(drop4)

    #bottleneck
    conv5 = Conv2D(16*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(pool4)
    conv5 = Conv2D(16*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(conv5)
    drop5 = Dropout(0.5)(conv5)

    up6 = Conv2D(8*fil, 2, strides = (1, 1), activation = 'relu', padding = 'same')(UpSampling2D(size = (2,2))(drop5))
    merge6 = concatenate([drop4,up6], axis = 3)
    conv6 = Conv2D(8*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(merge6)
    conv6 = Conv2D(8*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(conv6)

    up7 = Conv2D(4*fil, 2, strides = (1, 1), activation = 'relu', padding = 'same')(UpSampling2D(size = (2,2))(conv6))
    merge7 = concatenate([conv3,up7], axis = 3)
    conv7 = Conv2D(4*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(merge7)
    conv7 = Conv2D(4*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(conv7)

    up8 = Conv2D(2*fil, 2, strides = (1, 1), activation = 'relu', padding = 'same')(UpSampling2D(size = (2,2))(conv7))
    merge8 = concatenate([conv2,up8], axis = 3)
    conv8 = Conv2D(2*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(merge8)
    conv8 = Conv2D(2*fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(conv8)

    up9 = Conv2D(fil, 2, strides = (1, 1), activation = 'relu', padding = 'same')(UpSampling2D(size = (2,2))(conv8))
    merge9 = concatenate([conv1,up9], axis = 3)
    conv9 = Conv2D(fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(merge9)
    conv9 = Conv2D(fil, 3, strides = (1, 1), activation = 'relu', padding = 'same')(conv9)
    conv9 = Conv2D(2, 3, strides = (1, 1), activation = 'relu', padding = 'same')(conv9)

    outputs = Conv2D(1, 1, padding="same", activation="sigmoid")(conv9)

    model = Model(inputs, outputs, name = "U-Net")
    return model

if __name__ == "__main__":
    model = build_unet()
    model.summary()