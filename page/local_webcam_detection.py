from AvengersEnsemble import *
from Draw import *

# 로컬 웹캠 열기
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("오류: 웹캠이 열려있지 않음.")
    exit()

detected_labels = set()  # 탐지된 라벨을 저장할 집합(set)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("오류: 프레임을 읽을 수 없음.")
        break

    # 앙상블 예측 수행
    boxes, confidences, labels = ensemble_predict(frame)

    # 예측 결과를 프레임에 그리기 및 집합에 라벨 추가
    draw(frame, boxes, confidences, labels)

    for label in labels:
        detected_labels.add(label)
            
    print("\n탐지된 라벨 기록:")
    print(detected_labels)
    print('\n' + '==' * 50)

    # 프레임 출력
    cv2.imshow('YOLO Ensemble Detection', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()