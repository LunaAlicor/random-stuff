import cv2


def extract_frames(video, output):
    cap = cv2.VideoCapture(video)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        frame_filename = f"{output}/frame_{frame_count}.jpg"
        cv2.imwrite(frame_filename, frame)

    cap.release()


video_path = ":)"
output_path = r":)"
extract_frames(video_path, output_path)
