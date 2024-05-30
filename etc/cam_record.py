import cv2
import os

# 동영상을 녹화할 파일명과 확장자 지정
video_filename = 'recorded_video.mp4'

# OpenCV VideoWriter 객체 생성
# cv2.VideoWriter_fourcc(*'mp4v')는 mp4 형식으로 저장하기 위한 코덱
# (원하는 코덱을 사용할 수 있습니다)
# 마지막 파라미터는 프레임 레이트와 화면 크기 설정
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_filename, fourcc, 30.0, (1280, 720))  # 프레임 레이트와 화면 크기는 조정 가능

# 웹캠에서 영상을 읽어오기 위한 VideoCapture 객체 생성
cap = cv2.VideoCapture(0)  # 여러 개의 카메라가 있을 경우 인덱스를 변경하여 선택

# VideoCapture 객체 초기화 확인
if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

# 프레임을 저장할 폴더 생성
dataset_folder = 'dataset'
os.makedirs(dataset_folder, exist_ok=True)

# 영상 녹화 및 프레임 저장 루프
frame_count = 0
while True:
    # 웹캠에서 프레임 읽기
    ret, frame = cap.read()

    # 프레임 읽기에 실패하면 종료
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # 읽어온 프레임을 동영상에 쓰기
    out.write(frame)

    # 화면에 프레임 출력
    cv2.imshow('frame', frame)

    # 프레임을 파일로 저장
    frame_filename = os.path.join(dataset_folder, f'frame_{frame_count}.jpg')
    cv2.imwrite(frame_filename, frame)

    # 프레임 카운트 증가
    frame_count += 1

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 모든 작업이 끝나면 객체들 해제
cap.release()
out.release()
cv2.destroyAllWindows()
