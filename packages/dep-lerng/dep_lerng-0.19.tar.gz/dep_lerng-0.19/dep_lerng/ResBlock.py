
from torch.nn import Module, Conv2d, Linear, MaxPool2d, AvgPool2d, Sequential, BatchNorm2d, Dropout, AdaptiveAvgPool2d, AdaptiveMaxPool2d, Dropout2d, LPPool2d
from torch.nn import BatchNorm2d, GroupNorm, LazyLinear, Identity, Sigmoid, Flatten, Unflatten
from torch.nn import Mish, ReLU, LeakyReLU, PReLU, SELU
from torch import mul

from torchvision.ops import DropBlock2d

from kornia.augmentation import Resize
import torch

#------------------------------
from .custom_blocks import AFF,MSCAM, SAM, iAFF, ECA

# from custom_blocks import AFF,MSCAM, SAM, iAFF, ECA
#------------------------------

torch.manual_seed(43)

acti = Mish(inplace = True)
# acti = PReLU()

# torch.set_float32_matmul_precision("high")

def ResBlock(modifiers, squeeze, moment, layer = None):

    """
    Vanilla Block : Original Residual Block as mentioned in 1512.03385 [Deep Residual Learning for Image Recognition]

    Bottleneck Block : Original Bottleneck Block as mentioned in 1512.03385 [Deep Residual Learning for Image Recognition]
    
    Bottleneck Block V2 : Modifies Residual Blocks to have larger learning capacity, as mentioned in 1812.01187 [Bag of Tricks for Image Classification with Convolutional Neural Networks]

    Next Block : Replaces Convolutions with Grouped Convolutions as see in 1611.05431 [Aggregated Residual Transformations for Deep Neural Networks]
    """

    depth, flavor = modifiers

    if flavor == 'vanilla':
        return Vanilla_Block(depth, squeeze, moment, layer)

    elif flavor == 'bottleneck':
        return Bottleneck_Block(depth, squeeze, moment, layer)

    # elif flavor == 'custom':

    #     if modifiers[0] in [0, 1]:
    #         return Vanilla_Block(modifiers, squeeze, augment, layer) 
    #     elif modifiers[0] in [2, 3]:
    #         return Bottleneck_Block_V2(modifiers, squeeze, augment, layer)


class Vanilla_Block(Module):
    def __init__(self,  depth, squeeze, moment, layer = None):
        super(Vanilla_Block, self).__init__()

        layer_depth = depth
        self.layer_depth = layer_depth
        self.squeeze = squeeze

        self.layer = layer

        if layer == 'first':

            if layer_depth == 0:

                # i_channel = 64
                # o_channel = 64

                
                i_channel = 16
                o_channel = 16

                stride = 1

            else:

                # i_channel = 32 * (2 ** layer_depth)
                i_channel = 8 * (2 ** layer_depth)
                o_channel = i_channel * 2
                stride = 2
        else:

            # i_channel = 64 * (2 ** layer_depth)
            i_channel = 16 * (2 ** layer_depth)
            o_channel = i_channel
            stride = 1



        p = 0
        block_size = 3 + (layer_depth * 2)

        if squeeze:
            
            r = 16

            # self.SE = MSCAM(o_channel, r)
            self.SE = ECA()
            self.spatial = SAM()

        self.vanilla_block = Sequential(
                Conv2d(in_channels = i_channel, out_channels = o_channel, kernel_size = 3, stride = 1, padding = 1, bias = False),
                BatchNorm2d(o_channel, momentum = moment),
                acti,
                # DropBlock2d(p = 0.25, block_size = 2 ** (5 - layer_depth)),

                Conv2d(in_channels = o_channel, out_channels = o_channel, kernel_size = 3, stride = stride, padding = 1, bias = False),
                BatchNorm2d(o_channel, momentum = moment),
                # DropBlock2d(p = 0.25, block_size = 2 ** (5 - layer_depth)),
            )
        
        if layer == 'first' and layer_depth != 0: 

            self.downsample = Sequential(
                AvgPool2d(kernel_size = stride, stride = stride),
                
                Conv2d(in_channels = i_channel, out_channels = o_channel, kernel_size = 1, stride = 1, padding = 0, bias = False),
                BatchNorm2d(o_channel, momentum = moment),
                acti,
                # DropBlock2d(p = 0.25, block_size = 2 ** (5 - layer_depth)),
            )

        self.final_acti = acti

    def forward(self, x):

        identity = x
        x = self.vanilla_block(x)

        if self.layer == 'first' and self.layer_depth != 0:
            identity = self.downsample(identity)

        if self.squeeze:    
            # x = self.SE(identity, x)
            x = self.SE(x)
            x = self.spatial(x)

        x += identity
        x = self.final_acti(x)

        return x 


class Bottleneck_Block(Module):
    def __init__(self,  depth, squeeze, layer = None):
        super(Bottleneck_Block, self).__init__()

        layer_depth = depth
        self.layer_depth = layer_depth
        self.squeeze = squeeze

        self.layer = layer

        if layer == 'first':

            if layer_depth == 0:

                i_channel = 64
                m_channel = i_channel
                o_channel = 256
                stride = 1

            else:

                i_channel = 128 * (2 ** layer_depth)
                m_channel = i_channel // 2
                o_channel = i_channel * 2
                stride = 2

        else:

            i_channel = 256 * (2 ** layer_depth)
            m_channel = i_channel // 4
            o_channel = i_channel
            stride = 1


        p = 0
        block_size = 3 + (layer_depth * 2)

        if squeeze:

            r = 16

            self.SE = Sequential(
                MSCAM(o_channel, r),
                SAM(),
            )
    
            # self.SE = AFF(o_channel, r)

        self.bottleneck_block = Sequential(
                Conv2d(in_channels = i_channel, out_channels = m_channel, kernel_size = 1, stride = 1, padding = 0, bias = False),
                BatchNorm2d(m_channel),
                acti,

                Conv2d(in_channels = m_channel, out_channels = m_channel, kernel_size = 3, stride = stride, padding = 1, bias = False),
                BatchNorm2d(m_channel),
                acti,

                Conv2d(in_channels = m_channel, out_channels = o_channel, kernel_size = 1, stride = 1, padding = 0, bias = False),
                BatchNorm2d(o_channel),
                # acti,
            )

        if layer == 'first': 
            self.downsample = Sequential(
                AvgPool2d(kernel_size = stride, stride = stride),

                Conv2d(in_channels = i_channel, out_channels = o_channel, kernel_size = 1, stride = 1, padding = 0, bias = False),
                BatchNorm2d(o_channel),
                acti,
            )

        self.final_acti = acti

    def forward(self, x):

        identity = x

        x = self.bottleneck_block(x)

        if self.layer == 'first':
            identity = self.downsample(identity)

        if self.squeeze:    
            x = self.SE(x, identity)

        x = self.final_acti(x)

        return x









