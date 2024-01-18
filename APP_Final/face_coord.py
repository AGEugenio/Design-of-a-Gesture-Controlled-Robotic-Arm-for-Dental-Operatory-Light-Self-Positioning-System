import cv2
import depthai as dai
import time
import blobconverter
import dlib 


class CheckCoord():
    def coord_info(self,inDet, FRAME_SIZE):
        if inDet is not None:
            detections = inDet.detections
            # if face is detected
            if len(detections) != 0:
                detection = detections[0]

                # Correct bounding box
                xmin = max(0, detection.xmin)
                ymin = max(0, detection.ymin)
                xmax = min(detection.xmax, 1)
                ymax = min(detection.ymax, 1)

                x = int(xmin*FRAME_SIZE[0])
                y = int(ymin*FRAME_SIZE[1])
                w = int(xmax*FRAME_SIZE[0]-xmin*FRAME_SIZE[0])
                h = int(ymax*FRAME_SIZE[1]-ymin*FRAME_SIZE[1])

                bbox = (x, y, w, h)
                
                x2= x+w
                y2= y+h
                
                # Get spacial coordinates
                coord_x = detection.spatialCoordinates.x
                coord_y = detection.spatialCoordinates.y
                coord_z = detection.spatialCoordinates.z

                coordinates = (coord_x, coord_y, coord_z)
                
                #coordinates to be used for shape_predictor()
                face=dlib.rectangle(int(x),int(y),int(x2),int(y2))

                return coordinates, bbox, face
        else:
            return None,None,None
    # Display FUnction

    def display_info(self, frame, bbox, coordinates, status, status_color, fps):
        # Display bounding box
        cv2.rectangle(frame, bbox, status_color[status], 2)

        # Display coordinates
        if coordinates is not None:
            coord_x, coord_y, coord_z = coordinates
            cv2.putText(frame, f"X: {int(coord_x)} mm", (
                bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.putText(frame, f"Y: {int(coord_y)} mm", (
                bbox[0] + 10, bbox[1] + 35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.putText(frame, f"Z: {int(coord_z)} mm", (
                bbox[0] + 10, bbox[1] + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)

        # Create background for showing details
        cv2.rectangle(frame, (5, 5, 175, 100), (50, 0, 0), -1)

        # Display authentication status on the frame
        cv2.putText(frame, status, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color[status])

        # Display instructions on the frame
        cv2.putText(frame, f'FPS: {fps:.2f}', (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255))


def main():
    depth = detectDepth()

    # Define Frame size
    FRAME_SIZE = (640, 360)

    # Define the NN model name and input size
    DET_INPUT_SIZE = (300, 300)
    model_name = "face-detection-retail-0004"
    zoo_type = "depthai"
    blob_path = None

    pipeline = dai.Pipeline()

    cam = pipeline.createColorCamera()
    cam.setPreviewSize(FRAME_SIZE[0], FRAME_SIZE[1])
    cam.setInterleaved(False)
    cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    cam.setBoardSocket(dai.CameraBoardSocket.RGB)
    cam.setFps(35)
		
    #Define mono camera sources for stereo depth
    mono_left = pipeline.createMonoCamera()
    mono_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    mono_left.setBoardSocket(dai.CameraBoardSocket.LEFT)
    mono_right = pipeline.createMonoCamera()
    mono_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    mono_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    
    #Create stereo node
    stereo = pipeline.createStereoDepth()
    
    #Linking mono cam outputs to stereo node
    
    mono_left.out.link(stereo.left)
    mono_right.out.link(stereo.right)
    
    #Use blobconverter to get the blob of the required model
    if model_name is not None:
        blob_path = blobconverter.from_zoo(
        name=model_name,
        #The ‘shaves’ argument in blobconverter determines the number of SHAVE cores used to compile the neural network. The higher the value, the faster network can run.
        shaves=6,
        zoo_type=zoo_type
        ) 
    		
    #Define face detection NN node   
    face_spac_det_nn = pipeline.createMobileNetSpatialDetectionNetwork()
    face_spac_det_nn.setConfidenceThreshold(0.75)
    face_spac_det_nn.setBlobPath(blob_path)
    face_spac_det_nn.setDepthLowerThreshold(100)
    face_spac_det_nn.setDepthUpperThreshold(5000)
    
    #Define face detection input config
    face_det_manip = pipeline.createImageManip()
    face_det_manip.initialConfig.setResize(DET_INPUT_SIZE[0], DET_INPUT_SIZE[1])
    face_det_manip.initialConfig.setKeepAspectRatio(False)

    # Linking
    cam.preview.link(face_det_manip.inputImage)
    face_det_manip.out.link(face_spac_det_nn.input)
    stereo.depth.link(face_spac_det_nn.inputDepth)

    # Preview Output
    x_preview_out = pipeline.createXLinkOut()
    x_preview_out.setStreamName("preview")
    cam.preview.link(x_preview_out.input)

    # Detection Output
    det_out = pipeline.createXLinkOut()
    det_out.setStreamName('det_out')
    face_spac_det_nn.out.link(det_out.input)

    # Frame count
    frame_count = 0

    # Placeholder fps value
    fps = 0

    # Used to record the time when we processed last frames
    prev_frame_time = 0

    # Used to record the time at which we processed current frames
    new_frame_time = 0

    # Set status colors
    status_color = {
        'Face Detected': (0, 255, 0),
        'No Face Detected': (0, 0, 255)}

    # Start pipeline
    with dai.Device(pipeline) as device:

        # Output queue will be used to get the right camera frames from the outputs defined above
        q_cam = device.getOutputQueue(
            name="preview", maxSize=1, blocking=False)

        # Output queue will be used to get nn data from the video frames.
        q_det = device.getOutputQueue(
            name="det_out", maxSize=1, blocking=False)

        # # Output queue will be used to get nn data from the video frames.
        # q_bbox_depth_mapping = device.getOutputQueue(name="bbox_depth_mapping_out", maxSize=4, blocking=False)

        while True:

            # Get right camera frame
            in_cam = q_cam.get()
            frame = in_cam.getCvFrame()

            bbox = None
            coordinates = None

            inDet = q_det.tryGet()

            #Get Coordinates  
            result = depth.getCoordinates(inDet, FRAME_SIZE)
            if result is not None:
                coordinates, bbox = result
            

            # Check if a face was detected in the frame
            if bbox:
                # Face detected
                status = 'Face Detected'
            else:
                # No face detected
                status = 'No Face Detected'
            
            # Display info on frame
            depth.display_info(frame, bbox, coordinates,
                               status, status_color, fps)

            # Calculate average fps
            if frame_count % 10 == 0:
                # Time when we finish processing last 100 frames
                new_frame_time = time.time()

                # Fps will be number of frame processed in one second
                fps = 1 / ((new_frame_time - prev_frame_time)/10)
                prev_frame_time = new_frame_time

            # Capture the key pressed
            key_pressed = cv2.waitKey(1) & 0xff

            # Stop the program if Esc key was pressed
            if key_pressed == ord('q'):
                break

            # Display the final frame
            cv2.imshow("Face Cam", frame)

            # Increment frame count
            frame_count += 1

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
