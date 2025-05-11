import os
import random
import shutil

def train_val_split(image_src_path, label_src_path, train_ratio):
    train_image_path = os.path.join(image_src_path, 'train')
    val_image_path = os.path.join(image_src_path, 'val')
    train_label_path = os.path.join(label_src_path, 'train')
    val_label_path = os.path.join(label_src_path, 'val')
    
    os.makedirs(train_image_path, exist_ok=True)
    os.makedirs(val_image_path, exist_ok=True)
    os.makedirs(train_label_path, exist_ok=True)
    os.makedirs(val_label_path, exist_ok=True)
    
    image_files = [f for f in os.listdir(image_src_path) if f.endswith('.jpg') or f.endswith('.JPG') or f.endswith('.png')]
    random.shuffle(image_files)
    
    train_size = int(len(image_files) * train_ratio)
    
    train_files = image_files[:train_size]
    val_files = image_files[train_size:]
    
    for file in train_files:
        shutil.move(os.path.join(image_src_path, file), os.path.join(train_image_path, file))
        label_file = file.replace('.jpg', '.txt').replace('.JPG', '.txt').replace('.png', '.txt')
        shutil.move(os.path.join(label_src_path, label_file), os.path.join(train_label_path, label_file))
    
    for file in val_files:
        shutil.move(os.path.join(image_src_path, file), os.path.join(val_image_path, file))
        label_file = file.replace('.jpg', '.txt').replace('.JPG', '.txt').replace('.png', '.txt')
        shutil.move(os.path.join(label_src_path, label_file), os.path.join(val_label_path, label_file))
        
if __name__ == "__main__":
    image_path = "./dataset1/images"
    label_path = "./dataset1/labels"
    train_val_split(image_path, label_path, 0.8)