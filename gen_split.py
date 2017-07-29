import os.path
import sys
import csv

import numpy as np

import util.load as load

def get_car_ids(img_names):
    car_ids = [ img_name.split('_')[0] for img_name in img_names ]
    car_ids = list(set(car_ids))
    print("There are {} car ids out of {} images. ".format(len(car_ids), len(img_names)))
    return car_ids

def get_img_names_from_car_ids(car_ids):
    img_names = []

    for car_id in car_ids:
        for i in range(1, 17):
            img_name = car_id + '_{:02d}'.format(i)
            img_names.append(img_name)

    return img_names

def save_imageset(img_names, savepath):

    img_names.sort()

    # one image name per row
    img_names = [ [img_name] for img_name in img_names ]

    # save into csv
    with open(savepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(img_names)
    return

DATA_DIR = './data'

train_imageset_path = os.path.join(DATA_DIR, 'train.csv')
val_imagest_path   = os.path.join(DATA_DIR, 'val.csv')

if os.path.isfile(train_imageset_path) and os.path.isfile(val_imagest_path):
    print("train/val split already exists: {} and {}".format(train_imageset_path, val_imagest_path))
    sys.exit()

train_dir = os.path.join(DATA_DIR, 'train')

img_names = load.list_img_in_dir(train_dir)
car_ids = get_car_ids(img_names)
num_cars = len(car_ids)

num_val = int(num_cars / 5)
np.random.shuffle(car_ids)
val_ids   = car_ids[:num_val]
train_ids = car_ids[num_val:]
print("{} cars for Training and {} cars for Validation".format(len(train_ids), len(val_ids)))

train_imgs = get_img_names_from_car_ids(train_ids)
val_imgs   = get_img_names_from_car_ids(val_ids)

# save into files
save_imageset(train_imgs, train_imageset_path)
save_imageset(val_imgs, val_imagest_path)
