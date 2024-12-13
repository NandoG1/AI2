from pycocotools.coco import COCO
import shutil
import os
import json

# Path to your COCO annotations file (e.g., train2017 or val2017)
annotation_file = 'C:\\Users\\Asus TUF\\Downloads\\annotations_trainval2017\\annotations\\instances_val2017.json'
image_dir = 'C:\\Users\\Asus TUF\\Downloads\\val2017\\val2017'
# Load the COCO dataset
coco = COCO(annotation_file)

# Define the 10 animal categories you want to filter
# Classes you want to keep
animal_classes = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

# Get image IDs for the selected classes
image_ids = set()
for class_id in animal_classes:
    image_ids.update(coco.getImgIds(catIds=class_id))

# Get image metadata
images = coco.loadImgs(list(image_ids))

# Directory to save filtered images
output_dir = 'C:\\SE\\New folder'
os.makedirs(output_dir, exist_ok=True)

for img in images:
    src_path = os.path.join(image_dir, img['file_name'])
    dest_path = os.path.join(output_dir, img['file_name'])
    shutil.copy(src_path, dest_path)

annotation_ids = coco.getAnnIds(imgIds=list(image_ids), catIds=animal_classes)
annotations = coco.loadAnns(annotation_ids)

# Create a new JSON structure
filtered_data = {
    'images': images,
    'annotations': annotations,
    'categories': [cat for cat in coco.loadCats(animal_classes)]
}

# Save the new annotation file
with open('/path/to/filtered_annotations.json', 'w') as f:
    json.dump(filtered_data, f)
