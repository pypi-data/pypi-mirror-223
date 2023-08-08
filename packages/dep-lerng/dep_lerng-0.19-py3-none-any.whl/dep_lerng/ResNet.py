
from torch.nn import Module, Conv2d, Linear, MaxPool2d, AvgPool2d, Sequential, BatchNorm2d, Dropout, AdaptiveAvgPool2d, LazyConv2d, AlphaDropout, Bilinear
from torch.nn import BatchNorm1d, BatchNorm2d, GroupNorm, LazyLinear, LazyBatchNorm1d, LogSoftmax
from torch.nn import Mish, ReLU, LeakyReLU, PReLU, SELU, Tanh
from torch import flatten, unsqueeze

import torch

torch.manual_seed(43)

#------------------------------
from .ResBlock import ResBlock
from .RadonBlock import RadonBlock
from .custom_blocks import FastGlobalAvgPool2d, SAM, AFF, MSCAM
from .ClassifierNet import ClassifierNet

# from ResBlock import ResBlock
# from RadonBlock import RadonBlock
# from custom_blocks import FastGlobalAvgPool2d, SAM, AFF, MSCAM
# from ClassifierNet import ClassifierNet
#------------------------------
  
# torch.set_float32_matmul_precision("high")

acti = Mish(inplace = True)
# acti = PReLU()

def make_layers(type, modifiers, squeeze, moment):

    layers = modifiers[0]
    flavor = modifiers[1]

    res_layers = []
 
    for i, num_blocks in enumerate(layers):
        
        layers = []

        depth = i

        if type == 'resnet':

            for d in range(num_blocks):
                if d+1 == num_blocks:
                    layers.append(ResBlock((depth, flavor), squeeze, moment, layer = 'last'))
                elif d == 0:
                    layers.append(ResBlock((depth, flavor), squeeze, moment, layer = 'first'))
                else:
                    layers.append(ResBlock((depth, flavor), squeeze, moment, layer = None))

        # elif type == 'cnn':
            
        #     for d in range(num_blocks):
        #         if d+1 == num_blocks:
        #             layers.append(ConvBlock((depth, flavor), squeeze, augment, layer = 'last'))
        #         elif d == 0:
        #             layers.append(ConvBlock((depth, flavor), squeeze, augment, layer = 'first'))
        #         else:
        #             layers.append(ConvBlock((depth, flavor), squeeze, augment, layer = None))

        elif type == 'radon':

            for d in range(num_blocks):
                if d+1 == num_blocks:
                    layers.append(ResBlock((depth, flavor), squeeze, moment, layer = 'last'))
                elif d == 0:
                    layers.append(ResBlock((depth, flavor), squeeze, moment, layer = 'first'))
                else:
                    layers.append(ResBlock((depth, flavor), squeeze, moment, layer = None))


        res_layers.append(Sequential(*layers))

    return Sequential(*res_layers)

class Resnet(Module):
    def __init__(self, resnet_variant, squeeze, dropout_p, b_moment):

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

        self.squeeze = squeeze
        self.moment = b_moment

        c = 16
        r = 1

        #---------------------------------------------------------------------------------- HEAD

        self.Head = Sequential(
            # Conv2d(in_channels = 1, out_channels = 32, kernel_size = 7, stride = 2, padding = 3, bias = False),
            # BatchNorm2d(32, momentum = moment),
            # acti,

            # MaxPool2d(kernel_size = 3, stride = 2, padding = 1),

            Conv2d(in_channels = 1, out_channels = c, kernel_size = 3, stride = 2, padding = 1, bias = False, groups = 1),
            BatchNorm2d(c, momentum = self.moment),
            acti,

            Conv2d(in_channels = c, out_channels = c, kernel_size = 3, stride = 1, padding = 1, bias = False, groups = 2),
            BatchNorm2d(c, momentum = self.moment),
            acti,

            Conv2d(in_channels = c, out_channels = c, kernel_size = 3, stride = 1, padding = 1, bias = False, groups = 2),
            BatchNorm2d(c, momentum = self.moment),
            acti,

            # MaxPool2d(kernel_size = 3, stride = 2, padding = 1),            
        )
            
        #---------------------------------------------------------------------------------- RESBLOCKS


        self.ResBlocks = make_layers('resnet', variants[resnet_variant], self.squeeze, self.moment)

        #---------------------------------------------------------------------------------- EXTRA FEATURES


        #-------------------------------------------------------------- HEAD

        self.feature_attention_head = Sequential(
            # Conv2d(in_channels = 1, out_channels = 32, kernel_size = 7, stride = 2, padding = 3, bias = False),
            # BatchNorm2d(32),
            # acti,

            Conv2d(in_channels = 1, out_channels = c, kernel_size = 3, stride = 1, padding = 1, bias = False),
            BatchNorm2d(c, momentum = self.moment),
            acti,

            Conv2d(in_channels = c, out_channels = c, kernel_size = 3, stride = 1, padding = 1, bias = False),
            BatchNorm2d(c, momentum = self.moment),
            acti,

            Conv2d(in_channels = c, out_channels = c, kernel_size = 3, stride = 1, padding = 1, bias = False),
            BatchNorm2d(c, momentum = self.moment),
            acti,

            # MaxPool2d(kernel_size = 3, stride = 2, padding = 1),
        )

        #-------------------------------------------------------------- RESBLOCKS

        self.feature_attention = make_layers('radon', variants['radon'], self.squeeze, self.moment)

        #---------------------------------------------------------------------------------- FULLY CONNECTED

        self.AvgPool = FastGlobalAvgPool2d(flatten = False)

        self.fc = ClassifierNet(dropout_p = dropout_p, b_moment = self.moment)

    def forward(self, x):

        # print(torch.cuda.memory_summary(device=None, abbreviated=False))

        x1, x2 = x

        #--------------------------------------- HEAD
 
        # print(torch.cuda.memory_summary(device=None, abbreviated=False))

        x1 = self.Head(x1)

        #--------------------------------------- RESBLOCKS

        # print(torch.cuda.memory_summary(device=None, abbreviated=False))

        x1 = self.ResBlocks(x1)
        x1 = self.AvgPool(x1)

        #-------------------- RESBLOCKS -- EXTRA FEATURES

        # print(torch.cuda.memory_summary(device=None, abbreviated=False))

        x2 = self.feature_attention_head(x2)
        # print(torch.cuda.memory_summary(device=None, abbreviated=False))
        x2 = self.feature_attention(x2)
        # print(torch.cuda.memory_summary(device=None, abbreviated=False))
        x2 = self.AvgPool(x2)
        # print(torch.cuda.memory_summary(device=None, abbreviated=False))

        # x1 = (x1, x2, x3)
        x = (x1, x2)

        #--------------------------------------- FULLY CONNECTED

        # print(torch.cuda.memory_summary(device=None, abbreviated=False))
        
        x = self.fc(x)

        return x
    