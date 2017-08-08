import torch
from torch.autograd import Variable
import numpy as np

import time

import util.exp as exp
import util.evaluation as evaluation

from dataloader import *
import config


def tester(exp_name):
    cfg = config.load_config_file(exp_name)

    net, _, start_epoch = exp.load_exp(exp_name)

    data_loader = get_small_loader(
    # data_loader = get_val_loader(
    # data_loader = get_test_loader(
        cfg['train']['batch_size'],
        cfg['train']['paddings'],
        cfg['train']['tile_size']
    )
    IS_TEST = True

    # Testing setting
    DEBUG = cfg['DEBUG']

    if torch.cuda.is_available():
        net.cuda()

    net.eval()  # Change model to 'eval' mode (BN uses moving mean/var).

    pred_counts_by_img = [ {} for i in range(len(threshold_sets)) ]
    gt_counts_by_img = {}

    for i, (images, targets) in enumerate(data_loader):
        iter_start = time.time()

        images = images.float()  # convert from DoubleTensor   to FloatTensor
        images = Variable(images, volatile=True)

        if torch.cuda.is_available():
            images = images.cuda()

        outputs = net(images)
        output = outputs.data[0].cpu().numpy()

        # compute dice
        score = evaluation.dice(output, targets)

        iter_end = time.time()
        print('Iter {}/{}, Image {}, score:{}, {:.2f} sec spent'.format(i, len(data_loader), img_name, score, iter_end - iter_start))
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('exp_name', nargs='?', default='upsamplingUnet')
    args = parser.parse_args()

    exp_name = args.exp_name
    tester(exp_name)
