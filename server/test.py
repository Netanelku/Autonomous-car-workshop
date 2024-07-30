import cv2
from detection import ObjectDetector

def test_detect_function():
    # Path to the test image
    test_image_path = 'object_bottleneww21.jpg'
    
    # Load the test image
    test_image = cv2.imread(test_image_path, cv2.IMREAD_COLOR)
    if test_image is None:
        print(f"Error: Unable to load image {test_image_path}")
        return
    
    # Initialize the ObjectDetector
    detector = ObjectDetector()
    
    # Detect objects in the test image
    results = detector.detect(test_image)
    
    # Print the results
    for result in results:
        label, confidence, x1, y1, x2, y2 = result
        centroid_x = (x1 + x2) // 2
        w = test_image.shape[1]
        if centroid_x < w * 0.4:
            location = "left"
        elif centroid_x > w * 0.6:
            location = "right"
        else:
            location = "middle"
        print(f"Detected {label} with confidence {confidence:.2f} at location {location}")

# Run the test function
test_detect_function()
