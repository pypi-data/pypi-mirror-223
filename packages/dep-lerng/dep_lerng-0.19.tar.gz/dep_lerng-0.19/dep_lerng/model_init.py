
from pytorch_lightning import LightningModule

import torch
from torch.optim import Adam
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.nn import functional as F

from torch.nn import Conv2d, Linear, BatchNorm2d, BatchNorm1d
from torch.nn.init import kaiming_normal_, ones_, zeros_

from torchmetrics import Accuracy, Precision, Recall, F1Score, ConfusionMatrix, MetricCollection, AUROC

from kornia.geometry.transform import rotate
import random

from argparse import ArgumentParser

#------------------------------
from .ResNet import Resnet
# from ResNet import Resnet
#------------------------------

torch.manual_seed(43)

torch.set_float32_matmul_precision("high")

class classifier(LightningModule):
    def __init__(self, class_weights, learning_rate, squeeze, dropout_p, b_momemt):
        super(classifier, self).__init__()
        self.save_hyperparameters()

        self.LR = learning_rate
        self.num_classes = 9

        self.moment = b_momemt

        self.cm_total = []
        self.all_classes = []

        self.class_weights = torch.as_tensor(class_weights, device = torch.device("cuda"))

        def weights_init(m):
            if isinstance(m, Conv2d):
                kaiming_normal_(m.weight.data)

            elif isinstance(m, Linear):
                kaiming_normal_(m.weight.data)

            elif isinstance(m, BatchNorm2d) or isinstance(m, BatchNorm1d):
                ones_(m.bias.data)
                zeros_(m.bias.data)

        self.net = Resnet(
            resnet_variant = '18', 
            squeeze = squeeze,
            dropout_p = dropout_p,
            b_moment = self.moment,
            )
        
        self.net.apply(weights_init)

        self.net = self.net.to(memory_format = torch.channels_last)

        # ----------------------Metrics

        standard_metrics = MetricCollection([
            Accuracy(task = 'multiclass', num_classes = self.num_classes, average = 'macro'),
            Precision(task = 'multiclass', num_classes = self.num_classes, average = 'macro'),
            Recall(task = 'multiclass', num_classes = self.num_classes, average = 'macro'),
            F1Score(task = 'multiclass', num_classes = self.num_classes, average = 'macro'),
        ])

        weighted_metrics = MetricCollection([
            Accuracy(task = 'multiclass', num_classes = self.num_classes, average = 'weighted'),
            Precision(task = 'multiclass', num_classes = self.num_classes, average = 'weighted'),
            Recall(task = 'multiclass', num_classes = self.num_classes, average = 'weighted'),
            F1Score(task = 'multiclass', num_classes = self.num_classes, average = 'weighted'),
        ])

        self.std_metrics = standard_metrics
        self.wei_metrics = weighted_metrics

        self.train_step_output = []
        self.train_step_target = []

        self.valid_step_output = []
        self.valid_step_target = []

        self.test_step_output = []
        self.test_step_target = []

        # self.types = ['None', 'Loc', 'Edge-Loc', 'Center', 'Edge-Ring', 'Scratch', 'Random', 'Near-full', 'Donut']

    def forward(self, x):

        # x1, x2, x3 = x
        x1, x2 = x

        p = 1
        rng = random.random()
        def radon_augment(feature, angle):
            return torch.cat((torch.roll(feature[:, 0, :, angle:], -1, dims = -2), feature[:, 1, :, :angle]), dim = -1).unsqueeze(1)

        if rng < p:
            angle = random.choice(range(0, 180))

            angle_tensor =  torch.tensor(angle, dtype = torch.float32, device = torch.device("cuda"))

            x1 = rotate(x1, angle_tensor) / 127
            x2 = radon_augment(x2, angle)
        
        else:
            x2 = radon_augment(x2, 0)


        x1 = x1.to(memory_format = torch.channels_last)
        x2 = x2.to(memory_format = torch.channels_last)
        return self.net((x1, x2))

    def training_step(self, batch, batch_idx):
            
        # x1, x2, x3, y = batch
        x1, x2, y = batch
        # pred_y = self((x1, x2, x3))
        pred_y = self((x1, x2))

        loss = F.cross_entropy(pred_y, y, weight = self.class_weights, label_smoothing = 0.05)
        # loss = F.multi_margin_loss(pred_y, y, weight = self.class_weights, margin = 0.5)

        self.train_step_output.extend(pred_y.argmax(dim=1).cpu().tolist())
        self.train_step_target.extend(y.cpu().tolist())

        self.log("train_loss", loss, on_epoch = True, on_step = False, rank_zero_only = True)

        return loss
    
    def on_train_epoch_end(self):

        train_output = torch.Tensor(self.train_step_output)
        train_target = torch.Tensor(self.train_step_target)

        train_metric_1 = self.std_metrics.clone(prefix = 'train_', postfix = '_macro').to('cpu')
        train_metric_2 = self.wei_metrics.clone(prefix = 'train_', postfix = '_weighted').to('cpu')

        m1 = train_metric_1(train_output, train_target)
        m2 = train_metric_2(train_output, train_target)

        self.log_dict(m1, on_epoch = True, on_step = False, rank_zero_only = True)
        self.log_dict(m2, on_epoch = True, on_step = False, rank_zero_only = True)

        self.train_step_output.clear()
        self.train_step_target.clear()
    
    def validation_step(self, batch, batch_idx):

        # x1, x2, x3, y = batch
        x1, x2, y = batch
        # pred_y = self((x1, x2, x3))
        pred_y = self((x1, x2))

        loss = F.cross_entropy(pred_y, y, weight = self.class_weights, label_smoothing = 0.05)
        # loss = F.multi_margin_loss(pred_y, y, weight = self.class_weights, margin = 0.5)

        self.valid_step_output.extend(pred_y.argmax(dim=1).cpu().tolist())
        self.valid_step_target.extend(y.cpu().tolist())

        self.log("valid_loss", loss, on_epoch = True, on_step = False, rank_zero_only = True)

    def on_validation_epoch_end(self):

        valid_output = torch.Tensor(self.valid_step_output)
        valid_target = torch.Tensor(self.valid_step_target)

        valid_metric_1 = self.std_metrics.clone(prefix = 'valid_', postfix = '_macro').to('cpu')
        valid_metric_2 = self.wei_metrics.clone(prefix = 'valid_', postfix = '_weighted').to('cpu')

        m1 = valid_metric_1(valid_output, valid_target)
        m2 = valid_metric_2(valid_output, valid_target)

        self.log_dict(m1, on_epoch = True, on_step = False, rank_zero_only = True)
        self.log_dict(m2, on_epoch = True, on_step = False, rank_zero_only = True)

        self.valid_step_output.clear()
        self.valid_step_target.clear()


    def test_step(self, batch, batch_idx):
        
        # x1, x2, x3, y = batch
        x1, x2, y = batch
        # pred_y = self((x1, x2, x3))
        pred_y = self((x1, x2))

        test_metric_1 = self.std_metrics.clone(prefix = 'test_', postfix = '_macro')
        test_metric_1 = self.wei_metrics.clone(prefix = 'test_', postfix = '_weighted')

        m1 = test_metric_1(pred_y, y)
        m2 = test_metric_1(pred_y, y)

        self.log_dict(m1, on_epoch = True, on_step = False, rank_zero_only = True)
        self.log_dict(m2, on_epoch = True, on_step = False, rank_zero_only = True)

        # pred_y = pred_y.float()    

        # print(torch.unique(pred_y))

        # o3 = self.test_metrics(pred_y, y)

        # o4 = self.test_metrics_alpha(pred_y, y)

        # cm = self.confusion_matrix(pred_y, y).tolist()
        # self.cm_total.append(cm)
        
        # self.log_dict(o3, on_epoch = True, on_step = False, rank_zero_only = True)

        # datum = [
        #     o4['allclass_MulticlassAccuracy'].tolist(),
        #     o4['allclass_MulticlassPrecision'].tolist(),
        #     o4['allclass_MulticlassRecall'].tolist(),
        #     o4['allclass_MulticlassF1Score'].tolist(),
        #     o4['allclass_MulticlassAUROC'].tolist(),
        # ]


        # data = plt.DataFrame(data = datum, index = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'AUROC'], columns = self.types)
        # self.all_classes.append(data)

    # def on_test_end(self):

        # cm = torch.Tensor(self.cm_total)
        # cm = sum(cm)
        # self.logger.experiment.log_confusion_matrix(matrix = cm)

        # self.all_classes = (sum(self.all_classes) / len(self.all_classes) ) * 100
        # self.logger.experiment.log_table("data.csv", self.all_classes, self.types)

    def configure_optimizers(self):

        n = 5

        optimizer = Adam(self.parameters(), lr = self.LR, amsgrad = True) 
        scheduler = ReduceLROnPlateau(optimizer = optimizer, factor = (10 ** (0.5) / 10), cooldown = 0, patience = 5, min_lr = 1E-9)

        return {"optimizer": optimizer, "lr_scheduler": scheduler, "monitor": "valid_loss"}
    
    