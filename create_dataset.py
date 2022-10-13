
from PIL import Image
import os, sys
from shutil import copyfile, rmtree
import numpy as np
import datasets
import tqdm
import istarmap
from multiprocessing import Pool

BASE_DIR = sys.argv[1]

def resize_image(file_path, dest_path, size):
    im = Image.open(file_path)
    imResize = im.resize((size,size), Image.ANTIALIAS)
    imResize.save(dest_path, 'PNG')

# Resize images.
def resize(path, dest, size=64):
    dirs = os.listdir(path)
    os.makedirs(dest, exist_ok=True)
    print('Listing', path)
    jobs = []
    for item in tqdm.tqdm(dirs):
        file_path = os.path.join(path, item)
        if os.path.isfile(file_path):
            f, e = os.path.splitext(item)
            dest_path = os.path.join(dest, f + '.png')
            jobs.append((file_path, dest_path, size))
    print('Processing', path)
    with Pool(16) as pool:
        for _ in tqdm.tqdm(pool.istarmap(resize_image, jobs), total=len(jobs)):
            pass

for folder in ['M/', 'F/']:
    resize(os.path.join(BASE_DIR, folder), os.path.join('./tmp', folder), size=32)

datasets.save_data(data_dir='./tmp', save_file='dataset_32x32.mat', target_size=(32,32))

print('Deleting tmp dataset dir')
rmtree('./tmp')
