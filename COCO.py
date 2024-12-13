import os
import json
from pycocotools.coco import COCO

def convert_to_yolo(coco, img_dir, label_dir, category_mapping):
    os.makedirs(label_dir, exist_ok=True)
    
    # Loop through all images in the COCO dataset
    for img_id in coco.getImgIds():
        img_info = coco.loadImgs(img_id)[0]
        ann_ids = coco.getAnnIds(imgIds=img_id)
        anns = coco.loadAnns(ann_ids)

        img_width = img_info['width']
        img_height = img_info['height']

        label_file = os.path.join(label_dir, f"{os.path.splitext(img_info['file_name'])[0]}.txt")
        
        with open(label_file, 'w') as f:
            for ann in anns:
                category_id = ann['category_id']
                if category_id not in category_mapping:
                    continue  # Skip categories not in the target list
                
                yolo_class_id = category_mapping[category_id]
                
                # COCO bbox format: [x_min, y_min, width, height]
                bbox = ann['bbox']
                x_min, y_min, bbox_width, bbox_height = bbox
                x_center = x_min + bbox_width / 2
                y_center = y_min + bbox_height / 2

                # Normalize values
                x_center /= img_width
                y_center /= img_height
                bbox_width /= img_width
                bbox_height /= img_height

                # Write YOLO format
                f.write(f"{yolo_class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")

# Define paths
# train_annotation_file = '/path/to/filtered_train_annotations.json'
# train_image_dir = '/path/to/filtered_train_images/'
# train_label_dir = '/path/to/labels/train/'

val_annotation_file = 'C:\\Users\\Asus TUF\\Downloads\\annotations_trainval2017\\annotations\\instances_val2017.json'
val_image_dir = 'C:\\SE\\New folder'
val_label_dir = 'C:\\SE\\New folder (2)'

# Define your target animal categories and their YOLO remapping
animal_classes = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
category_mapping = {coco_id: idx for idx, coco_id in enumerate(animal_classes)}

# Convert training labels
# coco_train = COCO(train_annotation_file)
# convert_to_yolo(coco_train, train_image_dir, train_label_dir, category_mapping)

# Convert validation labels
coco_val = COCO(val_annotation_file)
convert_to_yolo(coco_val, val_image_dir, val_label_dir, category_mapping)

print("Labels generated successfully!")
