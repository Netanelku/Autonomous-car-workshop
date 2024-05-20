import cv2
import numpy as np
from matplotlib import pyplot as plt

def find_and_localize_object(query_image):  # query_image):
    # Initialize SIFT detector
    sift = cv2.SIFT_create()
    image_collection = [
        cv2.imread("Figure_1.png", 0),
        cv2.imread("Figure_2.png", 0)
    ]

    # Detect keypoints and descriptors for the query image
    kp1, des1 = sift.detectAndCompute(query_image, None)

    # Initialize variables to store the best match
    best_match_index = -1
    best_match_score = 0  # Initialize with a large value

    # Set a threshold for match score
    threshold = 3  # Adjust as needed

    # Iterate through the image collection
    for i, img in enumerate(image_collection):
        # Detect keypoints and descriptors for the current image
        kp2, des2 = sift.detectAndCompute(img, None)

        # Create FLANN matcher
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        # Match descriptors
        matches = flann.knnMatch(des1, des2, k=2)

        # Ratio test to find good matches
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)

        # Calculate the match score
        match_score = len(good_matches)

        # Print match score for each image
        print(f"Match score for image {i + 1}: {match_score}, Threshold: {threshold}, Best match score: {best_match_score}")

        # Update the best match if the current image has a higher number of good matches
        if match_score > best_match_score and match_score > threshold:
            best_match_score = match_score
            best_match_index = i

            # Store the best matches and keypoints for visualization
            best_matches = good_matches
            best_kp2 = kp2

    # If a suitable match is found, localize the object in the query image
    if best_match_index != -1:
        # Get keypoints coordinates of good matches
        train_pts = np.float32([best_kp2[m.trainIdx].pt for m in best_matches]).reshape(-1, 2)

        # Calculate the centroid of matched keypoints
        centroid = np.mean(train_pts, axis=0)
        # Get dimensions of the image
        h, w = query_image.shape[:2]
        # Calculate distance from centroid to center of the image
        distance_to_center = centroid[0] - w / 2
        print(centroid, w)
        # Determine the location of the centroid with respect to the center
        if distance_to_center < -w * 0.1:
            location = "left"
        elif distance_to_center > w * 0.1:
            location = "right"
        else:
            location = "middle"

        # Draw matches
        img_matches = cv2.drawMatches(query_image, kp1, image_collection[best_match_index], best_kp2, best_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        
        # Plot the matches
        plt.figure(figsize=(12, 6))
        plt.imshow(img_matches, cmap='gray')
        plt.title(f'Feature Matching with Image {best_match_index + 1}')
        plt.show()

        return {"best_match_index": best_match_index, "distance_to_center": distance_to_center, "location": location}

    else:
        print("No suitable match found.")
        return None
