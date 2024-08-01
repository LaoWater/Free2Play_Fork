import cv2
import mediapipe as mp
import numpy as np
import os
import json
from metrics_classes_v2 import StationsMetrics, TracksMetrics
from tracks_processing import calculate_origin_nexus, calculate_nebula_nexus, calculate_horizon_nexus

def draw_square(image, center, color=(0, 0, 255), size=1):
    cv2.rectangle(image, (center[0] - size, center[1] - size), (center[0] + size, center[1] + size), color, -1)

def draw_grid(image, grid_size=8, color=(200, 200, 200)):
    h, w, _ = image.shape
    for y in range(0, h, grid_size):
        for x in range(0, w, grid_size):
            cv2.rectangle(image, (x, y), (x + grid_size - 1, y + grid_size - 1), color, 1)

def read_and_convert_rgb(img_path):
    image = cv2.imread(img_path)
    image = cv2.resize(image, (510, 680))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb

def process_image_mediapipe(img_path):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    image_rgb = read_and_convert_rgb(img_path)
    pose_results = pose.process(image_rgb)
    mp_drawing.draw_landmarks(image_rgb, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    return pose_results, image_rgb

def image_blueprint(image_path, stations_metrics):
    blueprint_image = np.ones((680, 510, 3), dtype=np.uint8) * 255
    draw_grid(blueprint_image)
    pose_results, image_rgb = process_image_mediapipe(image_path)
    height, width, _ = image_rgb.shape
    index = 0
    nose_landmark = pose_results.pose_landmarks.landmark[0]
    nose_x, nose_y = int(nose_landmark.x * width), int(nose_landmark.y * height)
    desired_x = width // 2
    desired_y = int(height * 0.2)
    shift_x = desired_x - nose_x
    shift_y = desired_y - nose_y

    for idx, landmark in enumerate(pose_results.pose_landmarks.landmark):
        cx, cy = int(landmark.x * width) + shift_x, int(landmark.y * height) + shift_y
        if index > 8 or index == 0:
            stations_metrics.update_landmark(index, (cx, cy))
            draw_square(blueprint_image, (cx, cy), color=(255, 0, 0))
        if 10 < index < 13:
            stations_metrics.update_landmark(index, (cx, cy))
        draw_square(blueprint_image, (cx, cy - 70), color=(0, 0, 255))
        if index == 11:
            draw_square(blueprint_image, (cx, cy - 15), color=(45, 100, 99))
        index += 1

    stations_metrics.calculate_tracks()
    return blueprint_image
