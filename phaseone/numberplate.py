import cv2 as cv

cvNet = cv.dnn.readNetFromTensorflow('models/Number_plate_Model/frozen_inference_graph.pb', 'models/Number_plate_Model/NuPlate_model.pbtxt')

cap1 = cv.VideoCapture("rtsp://admin:admin0864@121.6.207.205:8081/cam/realmonitor?channel=1&subtype=1")



while True:
	ret,img = cap1.read()
	if ret == True:
		rows = img.shape[0]
		cols = img.shape[1]
		cvNet.setInput(cv.dnn.blobFromImage(img, 1.0/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False))
		cvOut = cvNet.forward()
		for detection in cvOut[0,0,:,:]:
			score = float(detection[2])
			if score > 0.9:
				left = detection[3] * cols
				top = detection[4] * rows
				right = detection[5] * cols
				bottom = detection[6] * rows
				cv.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)

		cv.imshow('img', img)
		if cv.waitKey(1) and 0xFF==ord('q'):
			break