# carvana-challenge
My Solution for [Carvana Image Masking Challenge on Kaggle](https://www.kaggle.com/c/carvana-image-masking-challenge)

## Requirements
* python 3.6
* numpy
* pytorch
* pandas
* pyyaml
* [crayon](https://github.com/torrvision/crayon)
* [pydensecrf](https://github.com/lucasb-eyer/pydensecrf)
    * `pip install cython` and then `pip install pydensecrf`


## Usage

### Train/Test
1. Extract data downloaded from Kaggle to `./data`:

```
data
├── metadata.csv
├── sample_submission.csv
├── test_hq
│   ├── 0004d4463b50_01.jpg
│   ├── 0004d4463b50_02.jpg
        ...
│   └── 846faa0eb79f_04.jpg
├── train_hq
│   ├── 00087a6bd4dc_01.jpg
│   ├── 00087a6bd4dc_02.jpg
        ...
│   └── fff9b3a5373f_16.jpg
├── train_masks
│   ├── 00087a6bd4dc_01_mask.gif
│   ├── 00087a6bd4dc_02_mask.gif
        ...
│   └── fff9b3a5373f_16_mask.gif
└── train_masks.csv
```

Images are all of size 1918 x 1280    

2. Run `crayon` and then `python train.py`

3. Run `python test.py`

### Other Scripts

* To find numbers that are divislbe by `2^n`, run `python scripts/divisble.py <start_number> <end_number>`

For instance, `python scripts/divisble.py 900 1300`

## To-dos

- [x] load data
- [x] train/val split
- [x] prepare small dataset
- [x] implement run length encoding
- [x] add experiment config loading
- [x] try a simple UNet
- [x] visualize groundtruth and prediction
- [x] add DICE validation
- [x] add data augmentation: random horizontal flipping
- [x] add data augmentation: padding
- [x] try the original UNet
- [x] train/predict-by-tile
- [x] add DICE score during training
- [x] add validation loss and DICE score during training
- [x] add optimizer and loss to experiment setting in .yml
- [x] try modified UNet with UpSampling layers
- [x] improve tile.py: make it able to cut image into halves
- [x] complete util/tile.py: stitch_predictions()
- [x] complete util/submit.py
- [x] add data augmentation: random shift
- [x] add boundary weighted loss
- [ ] experimenting with UNet parameters and architectures/modules
    - [ ] larger UNets
    - [ ] different UNet mos
    - [ ] try Adam or other optimizers
    - [ ] try different losses
- [ ] add CRF
- [ ] try a memory-efficient DenseNet

