
from torch.nn import Module, Conv2d, Linear, MaxPool2d, AvgPool2d, Sequential, Dropout2d, Dropout, AdaptiveAvgPool2d, LazyConv2d, AlphaDropout, Bilinear
from torch.nn import BatchNorm1d, BatchNorm2d, GroupNorm, LazyLinear, LazyBatchNorm1d, LogSoftmax, MultiheadAttention
from torch.nn import Mish, ReLU, LeakyReLU, PReLU, SELU, Tanh, Sigmoid, ELU, Flatten, Softmax
from torch import flatten, unsqueeze

import torch

#------------------------------
from .custom_blocks import AFF,MSCAM, SAM, iAFF, ECA
#------------------------------

torch.manual_seed(43)
  
# torch.set_float32_matmul_precision("high")

acti = Mish(inplace = True)
# acti = PReLU()

moment = 1E-1

class ClassifierNet(Module):
    def __init__(self, resnet_variant, augment, n_features, dropout_p, num_classes = 8):
        super(ClassifierNet, self).__init__()

        self.augment = augment

        if resnet_variant in ['18', '34']:
            cnn_features = 128
        else:
            cnn_features = 2048
        q = 10
        q2 = 128
        if augment:
            final_features = 292
            # final_features = 256
        else:
            final_features = cnn_features
        

        self.wafer_fc = Sequential(
            Linear(128, 128),
            Softmax(),
            Linear(128, num_classes),            
            # Sigmoid(),
        )

        self.radon_fc = Sequential( 
            Linear(128, 128),
            acti,
            Linear(128, num_classes),
            Softmax(),
        )

        self.regional = Sequential(
            Linear(9, 9),
            acti,
            # Sigmoid(),
        )

        self.statistical = Sequential(
            Linear(1, 1),
            acti,
            # Sigmoid(),
        )

        self.density = Sequential(
            Linear(26, 26),
            acti,
            # Sigmoid(),
        )
 
        self.final_x = Sequential(
            Linear(36, num_classes),
        )

        self.final_fc = Sequential(
            Conv2d(128, 128, kernel_size = 1, bias = False),
            acti,
            BatchNorm2d(128),
            ECA(),

            Conv2d(128, 9, kernel_size = 1, bias = False),
            Flatten()
        )

    def forward(self, x):   

        if self.augment:
            # x1, x2, x3 = x
            x1, x2 = x

            # x3_A, x3_B, x3_C = x3

            # x1_attention = self.wafer_fc(x1)
            # x1 = x1 * x1_attention

            # x2_attention = self.radon_fc(x2)
            # x2 = x2 * x2_attention

            # x3_A_attention = self.regional(x3_A)
            # x3_A = x3_A * x3_A_attention

            # x3_B_attention = self.statistical(x3_B)
            # x3_B = x3_B * x3_B_attention

            # x3_C_attention = self.density(x3_C)
            # x3_C = x3_C * x3_C_attention
            
            # x3_A = x3_A.unsqueeze(2).unsqueeze(3)
            # x3_B = x3_B.unsqueeze(2).unsqueeze(3)
            # x3_C = x3_C.unsqueeze(2).unsqueeze(3)

            # x1 = self.wafer_fc(x1)
            # x2 = self.radon_fc(x2)
            # x3_A = self.regional(x3_A)
            # x3_B = self.statistical(x3_B)
            # x3_C = self.density(x3_C)

            # x3 = torch.cat((x3_A, x3_B, x3_C), dim = 1)

            # x3 = self.final_x(x3)

            # x1 = self.acti(self.bn(self.bilin(x1, x2)))
            # x1 = torch.cat((x1, x2, x3_A, x3_B, x3_C), dim = 1)
            x1 = torch.cat((x1, x2), dim = 1)
            x1 = self.final_fc(x1)

        else:
            x1 = x

            # x1 = self.wafer_fc(x1)
            x1 = self.final_fc(x1)

        return x1
    