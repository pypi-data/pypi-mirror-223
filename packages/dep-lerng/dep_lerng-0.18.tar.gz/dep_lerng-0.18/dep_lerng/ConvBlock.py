
from torch.nn import Module, Conv2d, Linear, MaxPool2d, AvgPool2d, Sequential, BatchNorm2d, Dropout, AdaptiveAvgPool2d, AdaptiveMaxPool2d, Dropout2d
from torch.nn import BatchNorm2d, GroupNorm, LazyLinear, Identity, Sigmoid, Flatten, Unflatten
from torch.nn import Mish, ReLU, LeakyReLU, PReLU, SELU
from torch import mul

from torchvision.ops import DropBlock2d

from kornia.augmentation import Resize
import torch

#------------------------------
from .custom_blocks import AFF
#------------------------------

torch.manual_seed(43)

acti = Mish(inplace = True)
# acti = PReLU()

# torch.set_float32_matmul_precision("high")

class ConvBlock(Module):
    def __init__(self,  modifiers, squeeze, augment, layer = None):
        super(ConvBlock, self).__init__()

        layer_depth = modifiers[0]
        self.layer_depth = layer_depth
        self.squeeze = squeeze
        self.augment = augment

        self.layer = layer

        if layer == 'first':

            if layer_depth == 0:

                i_channel = 64
                o_channel = 64
                stride = 1

            else:

                i_channel = 32 * (2 ** layer_depth)
                o_channel = i_channel * 2
                stride = 2
        else:

            i_channel = 64 * (2 ** layer_depth)
            o_channel = i_channel
            stride = 1



        p = 0
        block_size = 3 + (layer_depth * 2)

        if squeeze:
        
            # r = o_channel // 4
            r = 16

            self.SE = AFF(o_channel, r)

        self.vanilla_block = Sequential(
                Conv2d(in_channels = i_channel, out_channels = o_channel, kernel_size = 3, stride = 1, padding = 1, bias = False),
                BatchNorm2d(o_channel),
                acti,

                Conv2d(in_channels = o_channel, out_channels = o_channel, kernel_size = 3, stride = stride, padding = 1, bias = False),
                BatchNorm2d(o_channel),

                # DropBlock2d(p = p, block_size = block_size)


                # ConvBlock(in_channels = i_channel, out_channels = o_channel, kernel_size = 3, padding = 1, stride = 1, p = p, pre = False),
                # ConvBlock(in_channels = o_channel, out_channels = o_channel, kernel_size = 3, stride = stride, padding = 1, p = p, pre = False, activation = False),
            )
        
        if layer == 'first' and layer_depth != 0: 

            self.downsample = Sequential(
                AvgPool2d(kernel_size = stride, stride = stride),
                
                Conv2d(in_channels = i_channel, out_channels = o_channel, kernel_size = 1, stride = 1, padding = 0, bias = False),
                BatchNorm2d(o_channel),
                acti,
            )

        self.final_acti = acti

    def forward(self, x):

        identity = x
        x = self.vanilla_block(x)

        if self.layer == 'first' and self.layer_depth != 0:
            identity = self.downsample(identity)

        if self.squeeze:    
            x = self.SE(x, identity)

        x = self.final_acti(x)

        return x 
