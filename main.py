# -*- coding: utf-8 -*-
"""Project1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ca-Ctm1cyayBLqDT53lHWChaeMwzNGTx
"""

import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self, name, fmt=':f'):
        self.name = name
        self.fmt = fmt
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def __str__(self):
        fmtstr = '{name} {val' + self.fmt + '} ({avg' + self.fmt + '})'
        return fmtstr.format(**self.__dict__)

"""### Software 1.0"""

def get_string_from_class(class_x, x):
  s = ['fizz', 'buzz', 'fizzbuzz']
  if  class_x == 0:
    return str(x)
  else:
    return s[class_x - 1]

def get_class(x):
  if x%15 == 0:
    ans = 3
  elif x%3 == 0:
    ans = 1
  elif x%5 == 0:
    ans = 2
  else:
    ans = 0
  return ans

def test_software_1(x):
  class_x = get_class(x)
  return get_string_from_class(class_x, x)

"""### Software 2.0"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader 
from torch.autograd import Variable
import pdb

def get_bit_representation(x):
  length = 10
  return np.array([int(i) for i in ("0"*length + "{0:b}".format(x))[-length:] ])


class train_dataset(Dataset):
  def __init__(self):
    super(train_dataset, self).__init__()
    self.arr = np.arange(101,1001)
    self.traindata = np.array(np.stack([get_bit_representation(x) for x in self.arr]), dtype=np.float32)

  def __getitem__(self, i):
    return self.traindata[i], get_class(self.arr[i])

  def __len__(self):
    return len(self.traindata)

class test_dataset(Dataset):
  def __init__(self, test_data):
    super(test_dataset, self).__init__()
    self.arr = np.array(test_data)
    self.testdata = np.array(np.stack([get_bit_representation(x) for x in self.arr]), dtype=np.float32)

  def __getitem__(self, i):
    return self.testdata[i], get_class(self.arr[i])

  def __len__(self):
    return len(self.testdata)


class MLP(nn.Module):
  def __init__(self, n_classes=4):
    '''
    Define the initialization function of LeNet, this function defines
    the basic structure of the neural network
    '''

    super(MLP, self).__init__()
    self.fc1 = nn.Linear(10, 64)
    self.fc2 = nn.Linear(64, 128)
    self.fc3 = nn.Linear(128, 64)
    self.clf = nn.Linear(64, n_classes)

  def forward(self, x):
    x = x.view(-1, 10)
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x = F.relu(self.fc3(x))
    out = self.clf(x)
    return out


def train_one_epoch(model, trainloader, optimizer, device):
  """ Training the model using the given dataloader for 1 epoch.

  Input: Model, Dataset, optimizer, 
  """

  model.train()
  avg_loss = AverageMeter("average-loss")
  for batch_idx, (img, target) in enumerate(trainloader):
    img = Variable(img).to(device)
    target = Variable(target).to(device)

    # Zero out the gradients
    optimizer.zero_grad()

    # Forward Propagation
    prob = model(img)
    loss = F.cross_entropy(prob, target)

    # backward propagation
    loss.backward()
    avg_loss.update(loss, img.shape[0])

    # Update the model parameters
    optimizer.step()

  return avg_loss.avg


def train_MLP():
  number_epochs = 500
  device = torch.device('cpu')  # Replace with torch.device("cuda:0") if you want to train on GPU
  model = MLP(4).to(device)
  dataset = train_dataset()
  trainloader = DataLoader(dataset, batch_size=1024, shuffle=True)

  optimizer = optim.Adam(model.parameters(), lr=0.001)

  track_loss = []
  for i in range(number_epochs):
    loss = train_one_epoch(model, trainloader, optimizer, device)
    track_loss.append(loss)
    print("\r{} out of {} done...".format(i, number_epochs), end="")

  plt.figure()
  plt.plot(track_loss)
  plt.title("training-loss-MLP")
  plt.savefig("./img/training_mlp.jpg")

  torch.save(model.state_dict(), "./models/MLP.pt")

def test_software_2(model, testloader):
    """ Training the model using the given dataloader for 1 epoch.

    Input: Model, Dataset, optimizer,
    """

    model.eval()
    avg_loss = AverageMeter("average-loss")

    y_gt = []
    y_pred_label = []

    for batch_idx, (img, y_true) in enumerate(testloader):
        img = Variable(img)
        y_true = Variable(y_true)
        out = model(img)
        y_pred = F.softmax(out, dim=1)
        y_pred_label_tmp = torch.argmax(y_pred, dim=1)

        loss = F.cross_entropy(y_pred, y_true)
        avg_loss.update(loss, img.shape[0])

        # Add the labels
        y_gt += list(y_true.numpy())
        y_pred_label += list(y_pred_label_tmp.numpy())

    return avg_loss.avg, y_gt, y_pred_label

"""### Testing"""

import argparse
import os

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--test-data')

  try:
    get_ipython
    list_args = ['--test-data', 'test_input.txt']
    args = parser.parse_args(list_args)
  except:
    args = parser.parse_args()
    args.test_data

  with open(args.test_data, 'r') as fread:
    test_data = []
    for line in fread.readlines():
      test_data.append(int(line))

  # Output for Software1.0
  with open("./Software1.txt", 'w') as fwrite:
    for x in test_data:
      out = test_software_1(x)
      fwrite.write("{}\n".format(out))

# Prepare output for Software2.0
  testdataset = test_dataset(test_data)
  testloader = DataLoader(testdataset, batch_size=1024, shuffle=False)
  model_MLP = MLP(4)
  model_MLP.load_state_dict(torch.load("./models/MLP.pt"))
  loss_test, y_gt, y_pred = test_software_2(model_MLP, testloader)

  # Output for Software2.0
  with open("./Software2.txt", 'w') as fwrite:
    for class_x, x in zip(y_pred, test_data):
      out = get_string_from_class(class_x, x)
      fwrite.write("{}\n".format(out))
