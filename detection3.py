import os
import cv2
import numpy as np
import csv
from prettytable import PrettyTable


# Load the YOLOv3 object detection model
model_config = (r"C:\Users\rilin\Desktop\pythonProject\yolov3.cfg")
model_weights = (r"C:\Users\rilin\Desktop\pythonProject\yolov3.weights")
net = cv2.dnn.readNetFromDarknet(model_config, model_weights)
output_layers = net.getLayerNames()
output_layers = [output_layers[i - 1] for i in net.getUnconnectedOutLayers()]

# Define a function to perform object detection on a single frame
def detect_objects_in_frame(frame):
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True)
    net.setInput(blob)
    outputs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                width = int(detection[2] * frame.shape[1])
                height = int(detection[3] * frame.shape[0])
                left = int(center_x - width/2)
                top = int(center_y - height/2)
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
    return class_ids, confidences, boxes

# Define a function to perform object detection on a video file
def detect_objects_in_video(video_file):
    video = cv2.VideoCapture(video_file)
    object_counts = {}
    frame_count = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        frame_count += 1
        if frame_count % 60 == 0:
            class_ids, confidences, boxes = detect_objects_in_frame(frame)
            for class_id in class_ids:
                object_label = labels[class_id]
                object_counts[object_label] = object_counts.get(object_label, 0) + 1
    video.release()
    return object_counts

# Load the object detection labels
labels_file = (r"C:\Users\rilin\Desktop\pythonProject\coco.names")
with open(labels_file, "r") as f:
    labels = [line.strip() for line in f.readlines()]

# Get the list of video files in the folder
video_folder = (r"C:\Users\rilin\Desktop\pythonProject\5g")
video_files = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith(".mp4")][:600]

# Initialize a dictionary to store the three most detected objects for each video
video_objects = {}

# Process each video file and update the video_objects dictionary
for video_file in video_files:
    # Perform object detection on the video file
    object_counts = detect_objects_in_video(video_file)

    # Determine the three most detected objects in the video
    sorted_object_counts = sorted(object_counts.items(), key=lambda x: x[1], reverse=True)
    top_three_objects = [object_label for object_label, count in sorted_object_counts[:3]]

    # Add the three most detected objects to the video_objects dictionary
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    video_objects[video_name] = top_three_objects


# Print the results to the console and write them to a file
output_file = "video_objects.txt"
with open(output_file, "w") as f:
    f.write("Video Name\tMost Detected Object 1\tMost Detected Object 2\tMost Detected Object 3\n")
    for video_name, objects in video_objects.items():
        if len(objects) >= 3:
            f.write("{}\t{}\t{}\t{}\n".format(video_name, objects[0], objects[1], objects[2]))
            print("{}: {}, {}, {}".format(video_name, objects[0], objects[1], objects[2]))
        elif len(objects) == 2:
            f.write("{}\t{}\t{}\n".format(video_name, objects[0], objects[1]))
            print("{}: {}, {}".format(video_name, objects[0], objects[1]))
        elif len(objects) == 1:
            f.write("{}\t{}\n".format(video_name, objects[0]))
            print("{}: {}".format(video_name, objects[0]))
        else:
            f.write("{}\tN/A\n".format(video_name))
            print("{}: N/A".format(video_name))

table = PrettyTable()
table.field_names = ["Video Name", "Most Detected Object 1", "Most Detected Object 2", "Most Detected Object 3"]

# Add the data to the table
for video_name, objects in video_objects.items():
    if len(objects) >= 3:
        table.add_row([video_name, objects[0], objects[1], objects[2]])
    elif len(objects) == 2:
        table.add_row([video_name, objects[0], objects[1], ""])
    elif len(objects) == 1:
        table.add_row([video_name, objects[0], "", ""])
    else:
        table.add_row([video_name, "N/A", "", ""])

# Write the table to a file
import csv

with open('video_objects.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['Video Name', 'Object 1', 'Object 2', 'Object 3'])
    for video, objects in video_objects.items():
        writer.writerow([video] + objects)

