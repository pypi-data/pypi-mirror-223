import torch
import torchvision
import torch.nn as nn
import torchsummary


class VGG16(nn.Module):
    """
    每个卷积核大小都是3x3,后面步长为1,padding=1
    每个卷积后面都用了ReLU
    """
    def __init__(self,in_channel=3,out_channel=1000,num_hidden=512*7*7):
        super(VGG16,self).__init__()
        self.features=nn.Sequential(
            # block1
            nn.Conv2d(in_channel,64,(3, 3),(1, 1),1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, (3, 3), (1, 1), 1),
            nn.ReLU(inplace=True),

            nn.MaxPool2d(2,2),

            # block2
            nn.Conv2d(64, 128, (3, 3), (1, 1), 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, (3, 3), (1, 1), 1),
            nn.ReLU(inplace=True),

            nn.MaxPool2d(2, 2),

            # block3
            nn.Conv2d(128, 256, (3, 3), (1, 1), 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, (3, 3), (1, 1), 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, (3, 3), (1, 1), 1),
            nn.ReLU(inplace=True),

            nn.MaxPool2d(2, 2),

            # block4
            nn.Conv2d(256, 512, (3, 3), (1, 1), 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, (3, 3), (1, 1), 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, (3, 3), (1, 1), 1),
            nn.ReLU(inplace=True),

            nn.MaxPool2d(2, 2),

            # block5
            nn.Conv2d(512, 512, (3, 3), (1, 1), 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, (3, 3), (1, 1), 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, (3, 3), (1, 1), 1),
            nn.ReLU(inplace=True),

            nn.MaxPool2d(2, 2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d(output_size=(7, 7))
        self.classifier = nn.Sequential(
            nn.Linear(num_hidden, 4096),
            nn.ReLU(),
            nn.Dropout(),

            nn.Linear(4096, 4096),
            nn.ReLU(),
            nn.Dropout(),

            nn.Linear(4096, out_channel),
        )
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
    


