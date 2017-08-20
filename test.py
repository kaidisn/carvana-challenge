import torch
from torch.autograd import Variable
import numpy as np

import time
import argparse

import util.exp as exp
import util.evaluation as evaluation
import util.visualization as viz
import util.submit as submit
import util.tile as tile

from dataloader import *
import config



def tester(exp_name, data_loader, tile_borders, net, criterion, is_val=False, DEBUG=False):

    if torch.cuda.is_available():
        net.cuda()
        criterion = criterion.cuda()
    net.eval()  # Change model to 'eval' mode

    # initialize stats
    if is_val:
        epoch_val_loss = 0
        epoch_val_accuracy = 0
    else:
        predictions = {}

    epoch_start = time.time()

    for i, (img_name, images, targets) in enumerate(data_loader):
        iter_start = time.time()

        images = images.float()  # convert to FloatTensor
        targets = targets.float()

        images = Variable(images, volatile=True) # no need to compute gradients
        targets = Variable(targets, volatile=True)

        if torch.cuda.is_available():
            images = images.cuda()
            targets = targets.cuda()

        outputs = net(images)

        # compute dice
        masks = (outputs > 0.5).float()

        # remove tile borders
        images = tile.remove_tile_borders(images, train_tile_borders)
        masks = tile.remove_tile_borders(masks, train_tile_borders)
        targets = tile.remove_tile_borders(targets, train_tile_borders)

        # remove tile borders
        images = tile.remove_tile_borders(images, tile_borders)
        masks = tile.remove_tile_borders(masks, tile_borders)
        targets = tile.remove_tile_borders(targets, tile_borders)

        iter_end = time.time()

        if is_val:
            accuracy = evaluation.dice(mask, target)
            loss = criterion(outputs, targets)

            # Update stats
            epoch_val_loss     += loss.data[0]
            epoch_val_accuracy += accuracy
        else:
            # assuming batch size == 1
             # TODO modify for case with batch size > 1
            img_name = img_name[0]
            predictions[img_name] = mask
            print('Iter {}/{}, Image {}: {:.2f} sec spent'.format(i, len(data_loader), img_name, iter_end - iter_start))

        if DEBUG and accuracy < 0.9:
            # convert to numpy array
            image = images.data[0].cpu().numpy()
            mask = masks.data[0].cpu().numpy()
            target = targets.data[0].cpu().numpy()

            if is_val:
                print('Iter {}, {}: Loss {:.3f}, Accuracy: {:.4f}'.format(i, img_name, loss.data[0], accuracy))
                viz.visualize(image, mask, target)
            else:
                viz.visualize(image, mask)
    # for loop ends

    if is_val:
        epoch_val_loss     /= len(data_loader)
        epoch_val_accuracy /= len(data_loader)
        print('Validation Loss: {:.3f} Validation Accuracy:{:.5f}'.format(epoch_val_loss, epoch_val_accuracy))
    else:
        predictions = tile.stitch_predictions(predictions)
        submit.save_predictions(exp_name, predictions)

    epoch_end = time.time()
    print('{:.2f} sec spent'.format(epoch_end - epoch_start))

    if is_val:
        net.train()  # Change model bacl to 'train' mode
        return epoch_val_loss, epoch_val_accuracy
    else:
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('exp_name', nargs='?', default='DynamicUnet')
    args = parser.parse_args()

    exp_name = args.exp_name

    cfg = config.load_config_file(exp_name)
    # data_loader, tile_borders = get_small_loader(
    data_loader, tile_borders = get_val_loader(
    # data_loader, tile_borders = get_test_loader(
        cfg['test']['batch_size'],
        cfg['test']['paddings'],
        cfg['test']['tile_size'],
        cfg['test']['hflip'],
        cfg['test']['shift']
    )

    net, _, criterion, _ = exp.load_exp(exp_name)

    tester(exp_name, data_loader, tile_borders, net, criterion)
    # epoch_val_loss, epoch_val_accuracy = tester(exp_name, data_loader, tile_borders, net, criterion, is_val=True)
