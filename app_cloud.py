from AvengersEnsemble import *
from Draw import *
from streamlit_webrtc import webrtc_streamer
import av

def transform(frame: av.VideoFrame):
    # 프레임을 RGB로 변환
    img = frame.to_ndarray(format="bgr24")

    # 예측 수행
    boxes, confidences, labels = ensemble_predict(img)

    # 예측 결과를 프레임에 그리기
    output_image = draw_with_pil(img, boxes, confidences, labels)
    
    return av.VideoFrame.from_ndarray(output_image, format="bgr24")

# WebRTC 연결 설정: STUN/TURN 서버 설정
rtc_configuration = {
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}] # STUN 서버
    # TURN 서버: 선택사항
}

# 스트리밍 ui
webrtc_streamer(key="streamer", video_frame_callback=transform, rtc_configuration=rtc_configuration, sendback_audio=False)