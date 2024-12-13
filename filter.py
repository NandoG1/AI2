from pycocotools.coco import COCO
import os

# Define your path for labels
label_dir = 'C:\\SE\\New folder (3)'

def filter_annotations(coco, category_mapping):
    filtered_annotations = []
    
    # Loop through all images in the COCO dataset
    for img_id in coco.getImgIds():
        img_info = coco.loadImgs(img_id)[0]
        ann_ids = coco.getAnnIds(imgIds=img_id)
        anns = coco.loadAnns(ann_ids)

        # Filter annotations to keep only the desired categories
        filtered_anns = [ann for ann in anns if ann['category_id'] in category_mapping]
        
        # If there are relevant annotations for this image, store them
        if filtered_anns:
            filtered_annotations.append({
                'image_id': img_id,
                'image_info': img_info,
                'annotations': filtered_anns
            })
    
    return filtered_annotations

# Define the desired animal categories (16-25)
animal_classes = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

# Create a category mapping to convert COCO IDs to YOLO class IDs
category_mapping = {coco_id: idx for idx, coco_id in enumerate(animal_classes)}

# Load COCO dataset
train_annotation_file = 'C:\\Users\\Asus TUF\\Downloads\\annotations_trainval2017\\annotations\\instances_val2017.json'
coco_train = COCO(train_annotation_file)

# Filter annotations
filtered_annotations = filter_annotations(coco_train, category_mapping)

# Check the filtered annotations for the first image
if filtered_annotations:
    print("First image filtered annotations:")
    first_image = filtered_annotations[0]
    print(f"Image ID: {first_image['image_id']}")
    print(f"Image Info: {first_image['image_info']}")
    print(f"Number of filtered annotations: {len(first_image['annotations'])}")
else:
    print("No filtered annotations found.")



def convert_to_yolo(filtered_annotations, category_mapping, img_dir, label_dir):
    for img_data in filtered_annotations:
        img_id = img_data['image_id']
        img_info = img_data['image_info']
        annotations = img_data['annotations']
        
        # Get the image width and height
        img_width = img_info['width']
        img_height = img_info['height']
        
        # Create YOLO label file (same name as image but with .txt extension)
        label_file = os.path.join(label_dir, f"{os.path.splitext(img_info['file_name'])[0]}.txt")
        
        with open(label_file, 'w') as f:
            for ann in annotations:
                # Get the class id (YOLO format)
                category_id = ann['category_id']
                yolo_class_id = category_mapping[category_id]
                
                # Get the bounding box (COCO format: [x_min, y_min, width, height])
                x_min, y_min, width, height = ann['bbox']
                
                # Convert bounding box to YOLO format (center_x, center_y, width, height)
                center_x = (x_min + width / 2) / img_width
                center_y = (y_min + height / 2) / img_height
                yolo_width = width / img_width
                yolo_height = height / img_height
                
                # Write the YOLO format line to the label file
                f.write(f"{yolo_class_id} {center_x} {center_y} {yolo_width} {yolo_height}\n")

# Example usage
img_dir = 'C:\\Users\\Asus TUF\\Downloads\\val2017\\val2017'  # Directory where images are stored
convert_to_yolo(filtered_annotations, category_mapping, img_dir, label_dir)

