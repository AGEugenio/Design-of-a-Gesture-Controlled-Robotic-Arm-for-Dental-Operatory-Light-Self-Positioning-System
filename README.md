# Design-of-a-Gesture-Controlled-Robotic-Arm-for-Dental-Operatory-Light-Self-Positioning-System

<p align= "justify">
In the world of healthcare, especially in orthodontics, lighting systems play a crucial role. Currently, the process of manually handling and adjusting dental lights poses challenges during operations and raises concerns about possible contamination. Recognizing these issues, our project aims to provide a solution—a robotic arm for dental operatory light equipped with a self-positioning system. This innovation is capable of adjusting the dental light's position to lighten the patient's mouth, ensuring not just efficiency but a genuine commitment to the well-being of both practitioners and patients in the dental setting.
<br>
<br>
</p>

<p align="center"width="100%">
<img src="https://github.com/AGEugenio/Design-of-a-Gesture-Controlled-Robotic-Arm-for-Dental-Operatory-Light-Self-Positioning-System/assets/113889259/89759b97-fed6-446c-b659-b18897494041" width="50%" /> 
<br> 

This is the final design of the device. The robotic arm was designed using Fusion 360 and sliced using CURA slicer. The sliced components were 3D printed using PLA Filaments. This arm holds the dental light and it can adjust the position of the light based on the given hand gesture and detected mouth position. It is equipped with a camera that serves as its eye, it captures the image of hand and face. This captured image is going to be processed and analyzed. Also for better user interaction, it has an LCD which displays the UI where the user may see a live preview of the camera feed, along with real-time detection of the face and hand.
  
<br>
</p>

<p align="center"width="100%">
<img src="https://github.com/AGEugenio/Design-of-a-Gesture-Controlled-Robotic-Arm-for-Dental-Operatory-Light-Self-Positioning-System/assets/113889259/5a8b4973-56d0-49b2-8f64-102036937959" width="40%" />
<img src="https://github.com/AGEugenio/Design-of-a-Gesture-Controlled-Robotic-Arm-for-Dental-Operatory-Light-Self-Positioning-System/assets/113889259/238e8762-6d0c-4243-bb82-b011413ede3f" width="40%" />
<img src="https://github.com/AGEugenio/Design-of-a-Gesture-Controlled-Robotic-Arm-for-Dental-Operatory-Light-Self-Positioning-System/assets/113889259/f63ee641-f4fe-4e82-927f-da0056aea15c" width="40%" />
<img src="https://github.com/AGEugenio/Design-of-a-Gesture-Controlled-Robotic-Arm-for-Dental-Operatory-Light-Self-Positioning-System/assets/113889259/05c4b4e2-753a-4185-9d4d-49f5783ede6b" width="40%" />
<img src="https://github.com/AGEugenio/Design-of-a-Gesture-Controlled-Robotic-Arm-for-Dental-Operatory-Light-Self-Positioning-System/assets/113889259/8d49a437-abdc-4e05-bc9e-e2334a9f5cd8" width="40%" />
<br>

These are some of the screenshot of the project's Graphical User Interface (GUI). This GUI is developed using Python programming language with the PyQt5 toolkit.
  
<br>
</p>

<p align="center"width="100%">
<img src="https://github.com/AGEugenio/Design-of-a-Gesture-Controlled-Robotic-Arm-for-Dental-Operatory-Light-Self-Positioning-System/assets/113889259/83982304-bc88-4379-b7ba-3f0e64351ff6" width="40%" />
<img src="https://github.com/AGEugenio/Design-of-a-Gesture-Controlled-Robotic-Arm-for-Dental-Operatory-Light-Self-Positioning-System/assets/113889259/c54f73d6-0951-4918-9bd9-805b2f58b178" width="40%"  />
<br>
<span style="font-size:5px;"><em>The blurring of faces was not part of the software's output</em></span>
  
These pictures show the real-time detection of the face and hand in the software. Here, an Open-Source Computer Vision (OpenCV) library was used for the reading and processing of the captured image in the system. Also, pre-built models from Mediapipe and OpenVINO were used for the face and hand detection. Moreover, the mouth landmarks in dlib’s 68-point model were used for mouth location.
 

</p>




