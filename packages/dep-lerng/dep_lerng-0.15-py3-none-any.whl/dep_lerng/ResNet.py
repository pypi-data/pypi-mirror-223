
from torch.nn import Module, Conv2d, Linear, MaxPool2d, AvgPool2d, Sequential, BatchNorm2d, Dropout, AdaptiveAvgPool2d, LazyConv2d, AlphaDropout, Bilinear
from torch.nn import BatchNorm1d, BatchNorm2d, GroupNorm, LazyLinear, LazyBatchNorm1d, LogSoftmax
from torch.nn import Mish, ReLU, LeakyReLU, PReLU, SELU, Tanh
from torch import flatten, unsqueeze

import torch

torch.manual_seed(43)

from .ResBlock import ResBlock
from .ConvBlock import ConvBlock
from custom_blocks import FastGlobalAvgPool2d, SAM, AFF, MSCAM
from ClassifierNet import ClassifierNet
  
# torch.set_float32_matmul_precision("high")

acti = Mish(inplace = True)
# acti = PReLU()

def make_layers(type, modifiers, squeeze, augment):

    layers = modifiers[0]
    flavor = modifiers[1]

    res_layers = []
 
    for i, num_blocks in enumerate(layers):
        
        layers = []

        depth = i

        if type == 'resnet':

            for d in range(num_blocks):
                if d+1 == num_blocks:
                    layers.append(ResBlock((depth, flavor), squeeze, augment, layer = 'last'))
                elif d == 0:
                    layers.append(ResBlock((depth, flavor), squeeze, augment, layer = 'first'))
                else:
                    layers.append(ResBlock((depth, flavor), squeeze, augment, layer = None))

        elif type == 'cnn':
            
            for d in range(num_blocks):
                if d+1 == num_blocks:
                    layers.append(ConvBlock((depth, flavor), squeeze, augment, layer = 'last'))
                elif d == 0:
                    layers.append(ConvBlock((depth, flavor), squeeze, augment, layer = 'first'))
                else:
                    layers.append(ConvBlock((depth, flavor), squeeze, augment, layer = None))

        res_layers.append(Sequential(*layers))

    return Sequential(*res_layers)

class Resnet(Module):
    def __init__(self, num_classes, resnet_variant, augment, squeeze):

        """
        Accepted Variants:
        18 : [2, 2, 2, 2] -- Vanilla Block
        34 : [3, 4, 6, 3] -- Vanilla Block
        50 : [3, 4, 6, 3] -- Bottleneck Block
        101 : [3, 4, 6, 3] -- Bottleneck Block
        152 : [3, 4, 6, 3] -- Bottleneck Block

        Accepted Augments:
        None : No Augmenting
        V1 : Augmented data goes through shallow NN first, outputting a single digit ## DEPRECATED ##

        V1_A : Only Augment 1 ## DEPRECATED ##
        V1_B : Only Augment 2 ## DEPRECATED ##


        V2 : Augmented is concated directly with original data ## DEPRECATED ##

        
        V3 : Augmented data is SE'd then chosen     by a NN to directly augment original wafer ## DEPRECATED ##
        V3-Kai   : Combines V3 and V1 together ## DEPRECATED ##
        V3-Kai A : Only Augment 1 ## DEPRECATED ## 
        V4-Kai B : Only Augment 2 ## DEPRECATED ##

        V4 
       
        """
        variants = {

            'radon' : [[2, 2, 2], 'vanilla'],

            '25_v2' : [[2, 4, 6, 2], 'bottleneck'],
            'custom' : [[2, 2, 2, 3], 'vanilla'],

            '18'  : [[2, 2, 2, 2], 'vanilla'],
            '34'  : [[3, 4, 6, 3], 'vanilla'],

            '50'  : [[3 ,4, 6, 3], 'bottleneck'],
            '101' : [[3 ,4, 23, 3], 'bottleneck'], 
            '152' : [[3, 8, 36, 3], 'bottleneck'],
        }

        super(Resnet, self).__init__()

        self.augment = augment
        self.squeeze = squeeze

        #---------------------------------------------------------------------------------- HEAD

        moment = 1E-2

        if resnet_variant in ['18', '34']:

            self.Head = Sequential(
            # Conv2d(in_channels = 1, out_channels = 32, kernel_size = 7, stride = 2, padding = 3, bias = False),
            # BatchNorm2d(32, momentum = moment),
            # acti,

            # MaxPool2d(kernel_size = 3, stride = 2, padding = 1),

            Conv2d(in_channels = 1, out_channels = 16, kernel_size = 3, stride = 2, padding = 1, bias = False, groups = 1),
            BatchNorm2d(16, momentum = moment),
            acti,

            Conv2d(in_channels = 16, out_channels = 16, kernel_size = 3, stride = 1, padding = 1, bias = False, groups = 2),
            BatchNorm2d(16, momentum = moment),
            acti,

            Conv2d(in_channels = 16, out_channels = 16, kernel_size = 3, stride = 1, padding = 1, bias = False, groups = 2),
            BatchNorm2d(16, momentum = moment),
            acti,

            # MaxPool2d(kernel_size = 3, stride = 2, padding = 1),            
        )
        
        else:
            self.Head = Sequential(

            Conv2d(in_channels = 1, out_channels = 64, kernel_size = 3, stride = 2, padding = 1, bias = False),
            BatchNorm2d(64),
            acti,

            Conv2d(in_channels = 64, out_channels = 64, kernel_size = 3, stride = 2, padding = 1, bias = False),
            BatchNorm2d(64),
            acti,

            Conv2d(in_channels = 64, out_channels = 64, kernel_size = 3, stride = 2, padding = 1, bias = False),
            BatchNorm2d(64),
            acti,

            # MaxPool2d(kernel_size = 3, stride = 2, padding = 1),
        )
            
        #---------------------------------------------------------------------------------- RESBLOCKS


        self.ResBlocks = make_layers('resnet', variants[resnet_variant], self.squeeze, self.augment)

        #---------------------------------------------------------------------------------- EXTRA FEATURES

        c = 16
        r = 1

        #-------------------------------------------------------------- HEAD

        self.feature_attention_head = Sequential(
            # Conv2d(in_channels = 1, out_channels = 32, kernel_size = 7, stride = 2, padding = 3, bias = False),
            # BatchNorm2d(32),
            # acti,

            Conv2d(in_channels = 1, out_channels = 16, kernel_size = 3, stride = 1, padding = 1, bias = False),
            BatchNorm2d(16, momentum = moment),
            acti,

            Conv2d(in_channels = 16, out_channels = 16, kernel_size = 3, stride = 1, padding = 1, bias = False),
            BatchNorm2d(16, momentum = moment),
            acti,

            Conv2d(in_channels = 16, out_channels = 16, kernel_size = 3, stride = 1, padding = 1, bias = False),
            BatchNorm2d(16, momentum = moment),
            acti,

            # MaxPool2d(kernel_size = 3, stride = 2, padding = 1),
        )

        #-------------------------------------------------------------- RESBLOCKS

        self.feature_attention = make_layers('resnet', variants['radon'], self.squeeze, self.augment)

        #---------------------------------------------------------------------------------- FULLY CONNECTED

        self.AvgPool = FastGlobalAvgPool2d(flatten = False)

        self.fc = ClassifierNet(resnet_variant, self.augment, 100, 0, num_classes)

    def forward(self, x):

        if self.augment:
            # x1, x2, x3 = x
            x1, x2 = x
        else:
            x1 = x

        #--------------------------------------- HEAD

        x1 = self.Head(x1)

        #--------------------------------------- RESBLOCKS

        x1 = self.ResBlocks(x1)
        x1 = self.AvgPool(x1)

        #-------------------- RESBLOCKS -- EXTRA FEATURES

        if self.augment:
            x2 = self.feature_attention_head(x2)
            x2 = self.feature_attention(x2)
            x2 = self.AvgPool(x2)

            # x1 = (x1, x2, x3)
            x1 = (x1, x2)

        #--------------------------------------- FULLY CONNECTED
        
        x1 = self.fc(x1)

        return x1
    