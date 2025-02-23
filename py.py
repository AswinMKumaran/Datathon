from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolov8l.pt")

img_path = "/Users/sanjaychakrapani/Desktop/test.png"

results = model(img_path, conf=0.3, imgsz=1280)

base_score = 100

penalty = 3

image = cv2.imread(img_path)
img_height, img_width, _ = image.shape
total_pixels = img_height * img_width

excluded_classes = {0}

def calculate_obstructed_area(results, min_conf=0.6):
    total_obstructed_pixels = 0

    for r in results:
        for box in r.boxes:
            if int(box.cls) not in excluded_classes and box.conf > min_conf:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                box_area = (x2 - x1) * (y2 - y1)
                total_obstructed_pixels += box_area

    obstruction_percentage = (total_obstructed_pixels / total_pixels) * 100
    return obstruction_percentage

obstruction_percentage = calculate_obstructed_area(results, min_conf=0.6)

visibility_score = max(base_score - (penalty * obstruction_percentage), 0)

def filter_results(results, min_conf=0.6):
    for r in results:
        r.boxes = [box for box in r.boxes if int(box.cls) not in excluded_classes and box.conf > min_conf]
    return results

filtered_results = filter_results(results, min_conf=0.6)

def show_results(results, score, window_name="YOLO Detection"):
    for r in results:
        img = r.plot()
        cv2.putText(img, f"Visibility Score: {score:.2f}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow(window_name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

show_results(filtered_results, visibility_score, "Filtered YOLO Detection")

print(f"Final Visibility Score: {visibility_score:.2f}")

