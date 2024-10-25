# -*- coding: utf-8 -*-
"""IOAI_Adaptive_Attacks (on-site).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19cKEAE3JrNM-GRlaM1MChS0O8nrt6XGY

# Can **you** break computer vision model?
## On-site round

## Task 1: Break a network by hand

Suppose you have a neural network $M$, defined b $M(x) = \text{softmax}\left(x^\top\theta\right)$. Note that for $z\in\mathbb{R}^n$ we have $\text{softmax}(z)=\frac{1}{\sum_i \exp(z_i)}\cdot\left[\exp(z_1), \exp(z_2), \ldots, \exp(z_n)\right]$.

Further, let $x=[1.,2.,3.]$ be an input of interest and let $\theta=\begin{bmatrix}
    5. & -2. \\
    3. & 4. \\
    2. & -1.
\end{bmatrix}$. Compute an an adversarial example $x^\prime$ that maximizes the second coordinate of $M(x)$ under the constraint that $\|x^\prime-x\|_\infty \leq 1.$, i.e., you're creating an $\ell_\infty$ adversarial example with $\varepsilon=1$.

Your solution here

## Task 2: Alice heard you've attacked her latest model, so she created a new one! Can you break that one too?

Alice heard about your adaptive attack on AliceNet, so she's raised the bar with her latest robust model, AliceNetV2. According to her, there's no way to attack this new model!
Like last time, Alice won't share with you what her defense is!

Your task is to develop an adaptive *targeted* attack. In particular, you must find a way to make small perturbations to the input images such that AliceNetV2 outputs the class "dog" every time!

###Task Requirements

1. **Understand the Defense**: Analyze Alice's model to understand the type of defense implemented. This could involve reviewing the model architecture, preprocessing steps, or any additional mechanisms employed for defense.

2. **Design an Adaptive Targeted Attack**: Develop an attack strategy that goes around Alice's defense and makes AliceNetV2 output the calss "dog". This might involve modifying standard attack methods like PGD.

3. **Generate Adversarial Examples**: Modify all test images from the CIFAR-10 dataset using your adversarial attack. You are allowed to modify the original test images within an $\ell_\infty$ ball of radius $8/255$.

4. **Test Model Accuracy**: Evaluate how often the AliceNetV2 model predicts the label "dog" on these adversarially modified images.


###Deliverables

* Python code used for your attack and generation of the adversarial CIFAR-10 test set.
* A short (up to a few paragraphs) report detailing your analysis of the defense, the approach used for the adaptive attack, and the success rate of your attack on the CIFAR-10 test set.
"""

!pip install wget
import wget

import torch
import torch.nn as nn
import torch.nn.functional as F
import functools


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(
            in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False
        )
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(
            planes, planes, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.bn2 = nn.BatchNorm2d(planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion * planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(
                    in_planes,
                    self.expansion * planes,
                    kernel_size=1,
                    stride=stride,
                    bias=False,
                ),
                nn.BatchNorm2d(self.expansion * planes),
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        return F.relu(out)



def recursive_getattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split("."))


class AliceNetV2_inner(nn.Module):
    KERNEL_SIZE = 3
    IN_CHANNELS = 3
    AVG_POOL_SIZE = 8
    LINEAR_MUL = 4 * 4

    def __init__(self, num_blocks=2, in_planes=64, num_classes=10, debug=False):
        super().__init__()
        self.num_classes = num_classes
        self.debug = debug
        self.in_planes = in_planes
        self.kernel_size = self.KERNEL_SIZE
        self.num_blocks = num_blocks

        # pre-layer stuff
        self.conv1 = nn.Conv2d(
            self.IN_CHANNELS,
            self.in_planes,
            kernel_size=self.kernel_size,
            stride=1,
            padding=1,
            bias=False,
        )
        self.bn1 = nn.BatchNorm2d(self.in_planes)

        # make single layer with K BasicBlocks
        # BasicBLock: conv1, bn1, conv2, bn2, shortcut
        # each conv has `in_planes` filters
        get_block = lambda: BasicBlock(self.in_planes, self.in_planes, stride=1)
        self.layer = nn.Sequential(*[get_block() for _ in range(num_blocks)])

        # register blocks with setattr to make it compatible with masking code
        for idx, block in enumerate(self.layer):
            setattr(self, f"block{idx}", block)

        # post-layer stuff
        self.flatten = nn.Flatten()
        self.avg_pool_2d = nn.AvgPool2d(self.AVG_POOL_SIZE)
        self.linear = nn.Linear(self.in_planes * self.LINEAR_MUL, num_classes)

    def forward(self, x, *args, **kwargs):
        out = F.relu(self.bn1(self.conv1(x)))
        if self.debug:
            print(f"conv1: {out.shape}")
        out = self.layer(out)
        if self.debug:
            print(f"layer: {out.shape}")
        out = self.avg_pool_2d(out)
        if self.debug:
            print(f"avg_pool_2d: {out.shape}")
        out = self.flatten(out)
        out = self.linear(out)
        return out

    def get_components(self, add_weight_suffix=True):
        comps = ["conv1"]
        num_convs = 2
        for block_idx in range(self.num_blocks):
            for conv_idx in range(1, 1 + num_convs):
                comps.append(f"block{block_idx}.conv{conv_idx}")

        comps.append("linear")

        if add_weight_suffix:
            return ["{}.weight".format(c) for c in comps]
        return comps

    def get_component_dimensions(self):
        comps = self.get_components()
        comps_map = {}

        for c in comps:
            w = recursive_getattr(self, c)
            comps_map[c] = w.shape[0]

        return comps_map

class AliceNetV2(nn.Module):
    def __init__(self, num_blocks=2, in_planes=64, num_classes=10):
        super(AliceNetV2, self).__init__()
        self.model1 = AliceNetV2_inner(num_blocks=num_blocks, in_planes=in_planes, num_classes=num_classes)
        self.model2 = AliceNetV2_inner(num_blocks=num_blocks, in_planes=in_planes, num_classes=num_classes)
        self.model3 = AliceNetV2_inner(num_blocks=num_blocks, in_planes=in_planes, num_classes=num_classes)

    def forward(self, x):
        outputs = []
        for network in [self.model1, self.model2, self.model3]:
            out = network(x)
            outputs.append(out)
        outputs = torch.stack(outputs)
        network_predictions = torch.argmax(outputs, dim=-1)
        majority_votes = torch.mode(network_predictions, dim=0).values
        result = torch.zeros_like(out)
        for i, vote in enumerate(majority_votes):
            result[i, vote] = 1.
        return result


def get_alicenet_v2() -> AliceNetV2:

    model = AliceNetV2()

    url = 'https://www.dropbox.com/scl/fi/awpcptjv4jbrgljn58k0m/alice_model_v2_IOAI.pt?rlkey=1v9hzkkpyqm0xqcyl1dogfwz8&dl=1'
    wget.download(url, out='./alicenet_v2.pt', bar=None)
    trained_ckpt = torch.load('./alicenet_v2.pt', map_location="cpu")
    model.load_state_dict(trained_ckpt)

    return model

alicenetv2 = get_alicenet_v2()
# Your code here