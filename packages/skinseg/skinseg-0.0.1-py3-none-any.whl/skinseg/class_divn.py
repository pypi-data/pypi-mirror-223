import os
import shutil
from tqdm import tqdm

isic_dir = './ISIC 2016 original/'
train_dir = isic_dir+'Train/'
test_dir = isic_dir+'Test/'

img_train_dir = train_dir
img_train_ben = img_train_dir+'ben/'
img_train_mel = img_train_dir+'mel/'
# TODO img_train_sk = img_train_dir+'SK/'

img_test_dir = test_dir
img_test_ben = img_test_dir+'ben/'
img_test_mel = img_test_dir+'mel/'
# TODO img_test_sk = img_test_dir+'SK/'

refs = [img_train_ben, img_train_mel, img_test_ben, img_test_mel]

src = './ISIC 2016 for maskgen (backup)/SEGMENTED/'

seg_dir = './ISIC 2016 for maskgen (backup)/ISIC 2016 segmented by CNN/'
seg_train_dir = seg_dir+'Train/'
seg_train_ben = seg_train_dir+'ben/'
seg_train_mel = seg_train_dir+'mel/'

seg_test_dir = seg_dir+'Test/'
seg_test_ben = seg_test_dir+'ben/'
seg_test_mel = seg_test_dir+'mel/'

dsts = [seg_train_ben, seg_train_mel, seg_test_ben, seg_test_mel]

for ref, dest in zip(refs, dsts):
    print(dest)
    for file in tqdm(os.listdir(ref), total=len(os.listdir(ref))):
        img = src+file
        target = dest+file
        if not os.path.exists(dest):
            os.makedirs(dest)
        shutil.copyfile(img, target)