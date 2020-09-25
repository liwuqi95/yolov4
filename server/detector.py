import cv2
import requests
import numpy as np
import tensorflow as tf

def detect(image):
    img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    image_data = cv2.resize(original_image, (416, 416))
    image_data = image_data / 255.
    images_data = [image_data.tolist()]

    response = requests.post('http://localhost:8501/v1/models/model:predict', json={"instances": images_data})
    response = tf.convert_to_tensor(response.json()['predictions'])

    boxes = response[:, :, 0:4]
    pred_conf = response[:, :, 4:]

    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape(
            pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class=50,
        max_total_size=50,
        iou_threshold=0.45,
        score_threshold=0.25
    )

    results = []
    for box, score, label in zip(boxes[0].numpy(), scores[0].numpy(), classes[0].numpy()):
        if score > 0:
            results.append({
                'class': label.item(),
                'confidance': score.item(),
                'box': box.tolist()
            })
    return results
