import torch
import torch.utils.data

import util.const as const
import util.load as load
import util.submit as submit
import util.run_length as run_length



class RLErunner(torch.utils.data.dataset.Dataset):
    def __init__(self):
        self.pred_dir = const.ENSEMBLE_PROB_DIR
        self.img_names = load.list_npy_in_dir(pred_dir)
        return

    def __len__(self):
        return len(self.img_names)

    def __getitem__(self, idx):

        img_name = self.img_names[idx]

        pred_path = os.path.join(self.pred_dir, img_name + '.npy')
        img_prob = np.load(pred_path)
        # TODO handle the case if file not found

        # generate image mask
        img_mask = np.zeros(img_prob.shape)
        img_mask[img_prob > 0.5] = 1

        rle = run_length.encode(img_mask)
        return img_name, rle


def get_rle_loader():

    dataset = RLErunner()

    loader = torch.utils.data.dataloader.DataLoader(
                                dataset,
                                batch_size=1,
                                shuffle=False,
                                num_workers=8,
                            )
    return loader
