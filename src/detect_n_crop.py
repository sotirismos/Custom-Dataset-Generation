"""
@author: sotiris
"""

from mmdet.apis import init_detector, inference_detector

import os
from PIL import Image


model_list = ['/home/sotiris/Projects/mmdetection/checkpoints/bdd100k/cascade_rcnn_r50_fpn_1x_det_bdd100k.pth']
cfg_list = ['/home/sotiris/Projects/mmdetection/configs/bdd100k/cascade_rcnn_r50_fpn_1x_det_bdd100k.py']

default_settings = {"model_path": os.path.abspath(model_list[0]),
                     "config_path": os.path.abspath(cfg_list[0]),
                     }
for i in range(len(model_list)):
    assert os.path.isfile(default_settings['model_path']), "Not a valid model file %s"\
        % (default_settings['model_path'])
    assert os.path.isfile(default_settings['config_path']), "Not a valid model file %s"\
        % (default_settings['config_path'])

default_thresholds = {
            'thresh_car': 0.8,
            #'thresh_truck': 0.90,
            #'thresh_bus': 0.90,
            #'thresh_motorcycle': 0.90
            }


def infer_model(img_paths, multiple=False, settings=default_settings, thresholds=default_thresholds):
    # build the model from a config file and a checkpoint file
    model = init_detector(settings['config_path'], settings['model_path'], device='cuda:0')
    
    # detect objects from a single image
    detections_vehicle = {}
    for i, frame in enumerate(img_paths):
        frame_detections_vehicle = []
        img = Image.open(frame)
        print(frame)
        if img is not None:
            dets = inference_detector(model, frame)
            if multiple:
                for j, bbox in enumerate(dets[2]): # approach 1 -> keep all the detected objects
                    if bbox[4] >= thresholds['thresh_car']:
                        box_data = {}
                        box_data['box_points'] = [float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])]
                        box_data['confidence'] = float(bbox[4])
                        box_data['class'] = 'vehicle'
                        frame_detections_vehicle.append(box_data)
                        
                        # crop & save detected object 
                        x1 = float(bbox[0])
                        y1 = float(bbox[1])
                        x2 = float(bbox[2])
                        y2 = float(bbox[3])
                        img = Image.open(frame)
                        img = img.crop((x1, y1, x2, y2))
                        root_path = '/data/grubles/custom_cars_dataset/'
                        car_class = frame.split('/')[-2]
                        new_path = os.path.join(root_path, 'images_cropped', car_class)
                        os.makedirs(new_path, exist_ok=True)
                        img_output = os.path.join(new_path, f'frame_{i}_car_{j}.png')
                        img.save(img_output)
            else:    
                if len(dets[2]) > 0: # approach 2 -> keep only the object with the largest bbox area
                    area_new = 0
                    for j, bbox in enumerate(dets[2]):    
                        area = (float(bbox[2]) - float(bbox[0])) * (float(bbox[3]) - float(bbox[1]))
                        if area > area_new:
                            bbox = dets[2][j]
                            area_new = area
                    if bbox[4] >= thresholds['thresh_car']:
                        box_data = {}
                        box_data['box_points'] = [float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])]
                        box_data['confidence'] = float(bbox[4])
                        box_data['class'] = 'vehicle'
                        frame_detections_vehicle.append(box_data)
                
                        # crop & save detected object 
                        x1 = float(bbox[0])
                        y1 = float(bbox[1])
                        x2 = float(bbox[2])
                        y2 = float(bbox[3])
                        img = Image.open(frame)
                        img = img.crop((x1, y1, x2, y2))
                        root_path = '/data/grubles/custom_cars_dataset/calibration/'
                        car_class = frame.split('/')[-2]
                        new_path = os.path.join(root_path, 'images_cropped', car_class)
                        os.makedirs(new_path, exist_ok=True)
                        img_output = os.path.join(new_path, f'frame_{i}.png')
                        img.save(img_output)
        
        detections_vehicle[frame.split('/')[-1]] = frame_detections_vehicle 
    return detections_vehicle

    



