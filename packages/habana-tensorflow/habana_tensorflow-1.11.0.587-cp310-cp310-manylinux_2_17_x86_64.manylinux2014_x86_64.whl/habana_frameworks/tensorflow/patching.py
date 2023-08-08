###############################################################################
# Copyright (C) 2023 Habana Labs, Ltd. an Intel Company
# All Rights Reserved.
#
# Unauthorized copying of this file or any element(s) within it, via any medium
# is strictly prohibited.
# This file contains Habana Labs, Ltd. proprietary and confidential information
# and is subject to the confidentiality and license agreements under which it
# was provided.
#
###############################################################################

import keras
import tensorflow as tf

@tf.function(jit_compile=False)
def keras_layers_convolutional_base_conv_Conv__jit_compiled_convolution_op(self, inputs, kernel):
    return self.convolution_op(inputs, kernel)

keras.layers.convolutional.base_conv.Conv._jit_compiled_convolution_op = keras_layers_convolutional_base_conv_Conv__jit_compiled_convolution_op

