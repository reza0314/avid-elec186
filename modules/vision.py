from typing import List
from cv2 import circle, medianBlur, Canny, cvtColor, resize, dilate, threshold, VideoCapture, HoughCircles, imshow, waitKey, HoughLinesP
from cv2 import Mat, COLOR_BGR2GRAY, THRESH_BINARY, HOUGH_GRADIENT
import numpy as np
import cv2 as cv


class Vision():
    cam = VideoCapture(0)
    reference_x = ...
    reference_y = ...
    x_distance_per_pixel = ...
    y_distance_per_pixel = ...
    circle_radius = ...

    def __init__(self, x_distance: int, y_distance: int, circle_radius: int) -> None:
        self.x_distance_per_pixel = x_distance
        self.y_distance_per_pixel = y_distance
        self.circle_radius = circle_radius
        self.findReference()
        # print(self.x_distance_per_pixel,
        #       self.y_distance_per_pixel, self.circle_radius)

    def findCircles(self) -> List:
        # taking picture
        _, image = self.cam.read()
        # Image Processing
        processed_image = cvtColor(image, COLOR_BGR2GRAY)
        gray = cvtColor(image, COLOR_BGR2GRAY)
        processed_image = medianBlur(processed_image, 5)
        processed_image = Canny(processed_image, 100, 250)
        processed_image = dilate(processed_image, (40, 40))
        _, processed_image = threshold(
            processed_image, 100, 255, THRESH_BINARY)
        # Detecting Circles
        # TODO the value of max_radius dividend must be set
        max_radius = min(processed_image.shape)//9
        circles = HoughCircles(processed_image, HOUGH_GRADIENT,
                               2, 50, param1=500, param2=1, minRadius=0, maxRadius=max_radius)
        results = []
        for(x, y, r) in circles:
            if gray[y][x] > 200:
                results.append([(x-self.reference_x)*(self.x_distance_per_pixel),
                               (y-self.reference_y)*(self.x_distance_per_pixel), r])
        if len(results) > 0:
            print(f'{len(results)} ceramics found at:', end=" ")
            for i in results:
                print(f' (x = {i[0]}, y = {i[1]})', end=' ')
            return results
        return None

    def test(self):
        import numpy as np
        _, img = self.cam.read()
        processed_image = cvtColor(img, COLOR_BGR2GRAY)
        # or use cv2.bilateralBlur()
        processed_image = medianBlur(processed_image, 5)
        processed_image = Canny(processed_image, 100, 250)
        processed_image = dilate(processed_image, (40, 40))
        _, processed_image = threshold(
            processed_image, 100, 255, THRESH_BINARY)
        # print(dilated)

        imshow("dia", processed_image)
        max_radius = min(processed_image.shape)//9
        circles = HoughCircles(processed_image, HOUGH_GRADIENT,
                               2, 50, param1=500, param2=1, minRadius=0, maxRadius=max_radius)
        # print(cv.minEnclosingCircle(processed_image))
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            circle(img, (x, y), int(1*r), (0, 0, 255), 1)
        imshow("circles", img)
        print('here')
        waitKey(0)
        return

    # TODO implement following functions
    def findReference(self) -> None:
        _, img = self.cam.read()
        processed_image = cvtColor(img, COLOR_BGR2GRAY)
        max_radius = min(processed_image.shape)//15
        circles = HoughCircles(processed_image, HOUGH_GRADIENT,
                               2, 50, param1=500, param2=1, minRadius=40, maxRadius=max_radius)
        lines = HoughLinesP(processed_image, 1, np.pi/180,
                            40, minLineLength=200, maxLineGap=30)
        circles = np.round(circles[0, :]).astype("int")
        for x1, y1, x2, y2 in lines[0]:
            for (x, y, r) in circles:
                if ((x2-x)**2+(y2-y)**2)**0.5 < 10:
                    self.reference_x = (x2+x)/2
                    self.reference_y = (y2+y)/2
                    break

    def findDistances(self) -> List:
        self.findReference()
        circles = self.findCircles()
        for i in circles:
            circles[i][0] -= self.reference_x
            circles[i][1] -= self.reference_y
        return circles


if __name__ == "__main__":
    test = Vision(10, 10, 10)
    test.test
