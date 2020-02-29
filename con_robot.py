# -*- coding: utf-8 -*-

import cv2
import pyrealsense2 as rs
import numpy as np
import random
import time
from tqdm import tqdm

def setup_robot():
    
    print("Connecting to Robots...")

    for _ in tqdm(range(100)):
        time.sleep(0.01)

    print("Conection Success!")
    
    batterry = 100
    
    direction = random.randint(0,360)
    roll = 0
    pitch = 0
    
    speed = 0
    f_or_b = True

    status = "Safety..."    

    return batterry,direction,roll,pitch,speed,f_or_b,status

def display_img(batterry,direction,roll,pitch,speed,f_or_b,status):
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)    

    while True:
        
        robot_img = cv2.imread("./robot.jpg")
        back_img = cv2.imread("./white.jpg")
    
        oh,ow = robot_img.shape[:2]
        back_img[100:oh + 100, 280:ow + 280] = robot_img

        try:        
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
             
            oh,ow = depth_colormap.shape[:2]
            depth_colormap = cv2.resize(depth_colormap,(int(ow/2),int(oh/2)))
            color_image = cv2.resize(color_image,(int(ow/2),int(oh/2)))

            oh,ow = depth_colormap.shape[:2]
            back_img[50:oh + 50, 950:ow + 950] = color_image
            back_img[350:oh + 350, 950:ow + 950] = depth_colormap
            
            print("Make Mask!")
                 
        except:
            print("Error!")

             
        robot_img = back_img
        
                
        cv2.putText(robot_img,"Status:"+status,(60,100),font,2,(0,255,0),3) 
        cv2.putText(robot_img,"Speed:"+str(speed),(60,200),font,1,(255,0,0),2) 
        cv2.putText(robot_img,"COLOR IMAGE",(1000,45),font,1,(255,244,0),2) 
        cv2.putText(robot_img,"3D IMAGE",(1030,345),font,1,(255,244,0),2) 
        cv2.putText(robot_img,"Direction:"+str(direction),(60,270),font,1,(255,0,0),2) 
        cv2.putText(robot_img,"Roll:"+str(roll),(60,340),font,1,(255,0,0),2) 
        cv2.putText(robot_img,"Pitch:"+str(pitch),(60,410),font,1,(255,0,0),2) 
        cv2.putText(robot_img,"Batterry:"+str(int(batterry))+"%",(60,500),font,1,(255,0,0),2) 
         
        batterry_x = int(batterry * 2)
        cv2.rectangle(robot_img,(60,510),(batterry_x + 60,530),(255,0,0),-1) 
         
        cv2.rectangle(robot_img,(60,510),(260,530),(0,255,0),3)
        
        cv2.imshow("Dream Walker Control System",robot_img)
        

        k = cv2.waitKey(1)

        if k == ord('u'):
            
            for i in range(100):
                k = cv2.waitKey(1)
                print("Key:",k)
                if k == ord('l'):
                    status = "Waiting..."
                    break
 
        elif k == ord('w'):
            if speed >= -100 and speed < 100 and status != "Safety...":
                speed += 1
        elif k == ord('s'):
            if speed > -100 and speed <= 100 and status != "Safety...":
                speed -= 1
        elif k == ord('p'):
            speed = 0
            status = "Safety..."

        elif k == ord('q'):
            break

        if speed >= 1:
            status = "Moving Forward"
        elif speed <= -1:
            status = "Moving Behind" 

        
        batterry -= 0.01

    cv2.destroyAllWindows()


def main():

    batterry,direction,roll,pitch,speed,f_or_b,status = setup_robot()
    display_img(batterry,direction,roll,pitch,speed,f_or_b,status)

if __name__ == "__main__":
    main()
