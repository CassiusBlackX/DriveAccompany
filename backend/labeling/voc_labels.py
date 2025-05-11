import os
import xml.etree.ElementTree as ET

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(input_list, output_path, classes):
    for xml_file in input_list:
        image_id = os.path.splitext(os.path.basename(xml_file))[0]
        out_file = open(os.path.join(output_path, image_id + '.txt'), 'w')
        tree = ET.parse(xml_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

def main(input_dir, output_dir, classes_file):
    with open(classes_file, 'r') as f:
        classes = f.read().strip().split()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_list = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.xml')]
    convert_annotation(input_list, output_dir, classes)
    
if __name__ == "__main__":
    xml_dir = "./labels"
    output_dir = "txt_labels"
    classes_file = "classes.txt"
    main(xml_dir, output_dir, classes_file)
    