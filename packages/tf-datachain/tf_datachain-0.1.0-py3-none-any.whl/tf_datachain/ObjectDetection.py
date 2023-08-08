import os
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import keras_cv
from keras_cv import visualization

def visualizeData(data, bounding_box_format):
    image = data["images"]
    annotation = {
        "classes": [data["bounding_boxes"]["classes"]],
        "boxes": [data["bounding_boxes"]["boxes"]]
    }
    visualization.plot_bounding_box_gallery(
        [image],
        value_range=(0, 255),
        rows=1,
        cols=1,
        y_pred=annotation,
        scale=5,
        font_scale=0.7,
        bounding_box_format=bounding_box_format,
        class_mapping=classMapping(),
    )

def visualizeDataset(dataset, boundingBoxFormat, rows=2, cols=2):
    for data in dataset.take(1):
        images = data["images"]
        bounding_boxes = data["bounding_boxes"]
        visualization.plot_bounding_box_gallery(
            images,
            value_range=(0,255),
            rows=rows,
            cols=cols,
            y_true=bounding_boxes,
            scale=5,
            font_scale=0.7,
            bounding_box_format=boundingBoxFormat,
            class_mapping=classMapping(),
        )

imageFolder = "data"
classNames = []

def classMapping():
    return dict(zip(range(len(classNames)), classNames))

def prepareAnnotation(*args: str):
    annotations = []
    if len(args) == 1:      # a file with items
        filePath = args[0]
        file = pd.read_csv(filePath)
        for i in file.shape[0]:
            annotations.append(file.iloc[i])
    elif len(args) == 2:    # seperate files
        folderPath = args[0]
        extension = args[1]
        for path in os.listdir(folderPath):
            if path.endswith(extension):
                annotations.append(folderPath + "/" + path)
    else:
        raise Exception(f"{len(args)} arguments is not supported")
    
    return annotations

def loadData(data, format: str, bounding_box_format: str):
    # parse data with given dataset format
    if format == "Pascal VOC XML":
        imagePath, thisClassIDs, thisBoxes = tf.py_function(__loadData_Pascal_VOC_XML, [data], [tf.string, tf.float32, tf.float32])
        thisClassIDs.set_shape([None,])
        thisBoxes.set_shape([None, 4])
        sourceBoundingBoxFormat = "xyxy"
    else:
        raise Exception(f"\"{format}\" is not a supported dataset format")
    
    # load image
    image = tf.io.read_file(imagePath)
    image = tf.image.decode_jpeg(image, channels=3)

    # convert bounding box format
    thisBoxes = keras_cv.bounding_box.convert_format(
        thisBoxes,
        images=image,
        source=sourceBoundingBoxFormat,
        target=bounding_box_format
    )

    return {
        "images": tf.cast(image, tf.float32),
        "bounding_boxes": {
            "classes": thisClassIDs,
            "boxes": thisBoxes
        }
    }

def datasetProcessing(dataset, batchSize: int, method: str, targetSize: tuple[float, float], bounding_box_format):
    dataset = dataset.shuffle(batchSize * 4)
    dataset = dataset.ragged_batch(batchSize, drop_remainder=True)
    
    if method == "Jittered Resize":
        augmenter = keras.Sequential([
            keras_cv.layers.RandomFlip(mode="horizontal", bounding_box_format=bounding_box_format),
            keras_cv.layers.JitteredResize(
                target_size=targetSize, scale_factor=(0.75, 1.3), bounding_box_format=bounding_box_format
            )
        ])
        dataset = dataset.map(augmenter, num_parallel_calls=tf.data.AUTOTUNE)
    elif method == "Resize":
        resizing = keras_cv.layers.Resizing(targetSize[0], targetSize[1], bounding_box_format=bounding_box_format, pad_to_aspect_ratio=True)
        dataset = dataset.map(resizing, num_parallel_calls=tf.data.AUTOTUNE)

    return dataset

####################################
# load data format library
####################################

def __loadData_Pascal_VOC_XML(annotationPath):
    import xml.etree.ElementTree as ET
    thisBoxes = []
    thisClassIDs = []
    annotationPath = annotationPath.numpy().decode("utf-8")
    root = ET.parse(annotationPath).getroot()
    for object in root.findall("object"):
        # load bounding boxes
        bndbox = object.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)
        thisBoxes.append([xmin, ymin, xmax, ymax])
        # load class IDs
        className = object.find("name").text
        classID = classNames.index(className)
        thisClassIDs.append(classID)
    # image file path
    imagePath = imageFolder + "/" + root.find('filename').text
    thisClassIDs = tf.cast(thisClassIDs, tf.float32)
    thisBoxes = tf.cast(thisBoxes, tf.float32)

    return (imagePath, thisClassIDs, thisBoxes)
