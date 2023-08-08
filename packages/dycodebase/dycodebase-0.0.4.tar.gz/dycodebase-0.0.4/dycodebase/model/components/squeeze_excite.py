import tensorflow as tf

class SqueezeExciteLayer(tf.keras.layers.Layer):
  def __init__(self, squeeze_factor=4,activation="relu", name=""):
    super(SqueezeExciteBlock,self).__init__(name)
    self.squeeze_factor = squeeze_factor
    self.pool = tf.keras.layers.GlobalAveragePooling1D()
    self.multiply = tf.keras.layers.Multiply()
    self.activation = tf.nn.gelu

  def build(self, input_shape):
    filters = input_shape[-1]
    self.reshape = tf.keras.layers.Reshape((1,filters))
    self.dense_1 = self.add_weight("dense_1",
                                  shape=[filters,
                                         filters//self.squeeze_factor],
                                  initializer="he_normal"
                                  )
    
    self.dense_2 = self.add_weight("dense_2",
                                  shape=[filters//self.squeeze_factor,
                                         filters],
                                  initializer="he_normal"
                                  )

  def call(self, inputs):
    x = self.pool(inputs)
    x = self.reshape(x)
    x =  tf.matmul(x, self.dense_1)
    x = self.activation(x)
    x = tf.matmul(x,self.dense_2)
    x = self.activation(x)
    x = self.multiply([x,inputs])
    return x

class SqueezeExciteBlock(tf.keras.layers.Layer):
    def __init__(self,squeeze_factor=4,activation="relu", name=""):
        super(SqueezeExciteBlock,self).__init__(name)
        self.squeeze_factor = squeeze_factor
        self.pool = tf.keras.layers.GlobalAveragePooling1D()
        self.multiply = tf.keras.layers.Multiply()
        self.dense1 = tf.keras.layers.Dense(
            filter//squeeze_factor,
            activation=activation,
            kernel_initializer="he_normal",
            use_bias=False
            )
        
        self.dense2 = tf.keras.layers.Dense(
            filter//squeeze_factor,
            activation=activation,
            kernel_initializer="he_normal",
            use_bias=False
            )
    def build(self, input_shape):
        self.reshape = tf.keras.layers.Reshape((1,input_shape[-1]))
        return super().build(input_shape)
        
    def call(self, inputs):
        x = self.pool(inputs)
        x = self.reshape(x)
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.multiply([x,inputs])
        return x
        
        
    