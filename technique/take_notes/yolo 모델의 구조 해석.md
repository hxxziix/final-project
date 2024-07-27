# ex) yolov9s

| from | n | params | module | arguments |
|------|---|--------|--------|-----------|
| -1   | 1 | 928    | ultralytics.nn.modules.conv.Conv | [3, 32, 3, 2] |
| -1   | 1 | 18560  | ultralytics.nn.modules.conv.Conv | [32, 64, 3, 2] |
| -1   | 1 | 31104  | ultralytics.nn.modules.block.ELAN1 | [64, 64, 64, 32] |
| -1   | 1 | 73984  | ultralytics.nn.modules.block.AConv | [64, 128] |
| -1   | 1 | 258432 | ultralytics.nn.modules.block.RepNCSPELAN4 | [128, 128, 128, 64, 3] |
| -1   | 1 | 221568 | ultralytics.nn.modules.block.AConv | [128, 192] |
| -1   | 1 | 579648 | ultralytics.nn.modules.block.RepNCSPELAN4 | [192, 192, 192, 96, 3] |
| -1   | 1 | 442880 | ultralytics.nn.modules.block.AConv | [192, 256] |
| -1   | 1 | 1028864 | ultralytics.nn.modules.block.RepNCSPELAN4 | [256, 256, 256, 128, 3] |
| -1   | 1 | 164608 | ultralytics.nn.modules.block.SPPELAN | [256, 256, 128] |
| -1   | 1 | 0      | torch.nn.modules.upsampling.Upsample | [None, 2, 'nearest'] |
| [-1, 6] | 1 | 0   | ultralytics.nn.modules.conv.Concat | [1] |
| -1   | 1 | 628800 | ultralytics.nn.modules.block.RepNCSPELAN4 | [448, 192, 192, 96, 3] |
| -1   | 1 | 0      | torch.nn.modules.upsampling.Upsample | [None, 2, 'nearest'] |
| [-1, 4] | 1 | 0   | ultralytics.nn.modules.conv.Concat | [1] |
| -1   | 1 | 283008 | ultralytics.nn.modules.block.RepNCSPELAN4 | [320, 128, 128, 64, 3] |
| -1   | 1 | 110784 | ultralytics.nn.modules.block.AConv | [128, 96] |
| [-1, 12] | 1 | 0  | ultralytics.nn.modules.conv.Concat | [1] |
| -1   | 1 | 598080 | ultralytics.nn.modules.block.RepNCSPELAN4 | [288, 192, 192, 96, 3] |

- **from**: 모듈이 구성 중인 위치를 나타냅니다.
- **n**: 해당 모듈의 인덱스를 나타냅니다.
- **params**: 해당 모듈의 파라미터 수를 나타냅니다.
- **module**: 사용된 모듈의 유형을 나타냅니다.
- **arguments**: 모듈에 전달된 인수(argument)들을 설명합니다.

구체적으로, 각 줄은 다음을 나타냅니다:

## Layer
- **Convolutional Layer**: 입력 채널이 3이고 출력 채널이 32이며, 커널 크기가 3x3이고 스트라이드가 2인 Convolutional Layer입니다.
- **Convolutional Layer**: 입력 채널이 32이고 출력 채널이 64이며, 커널 크기가 3x3이고 스트라이드가 2인 Convolutional Layer입니다.
- **ELAN1 Block**: 입력 채널이 64이고, 내부적으로 64 채널을 가지는 ELAN1 Block입니다.
- **AConv Block**: 입력 채널이 64이고 출력 채널이 128인 AConv Block입니다.
- **RepNCSPELAN4 Block**: 입력 채널이 128이고, 각각 128, 128, 64 채널을 가지며 3개의 Convolutional Layer를 포함하는 RepNCSPELAN4 Block입니다.
- **AConv Block**: 입력 채널이 128이고 출력 채널이 192인 AConv Block입니다.
- **RepNCSPELAN4 Block**: 입력 채널이 192이고, 각각 192, 192, 96 채널을 가지며 3개의 Convolutional Layer를 포함하는 RepNCSPELAN4 Block입니다.
- **AConv Block**: 입력 채널이 192이고 출력 채널이 256인 AConv Block입니다.
- **RepNCSPELAN4 Block**: 입력 채널이 256이고, 각각 256, 256, 128 채널을 가지며 3개의 Convolutional Layer를 포함하는 RepNCSPELAN4 Block입니다.
- **SPPELAN Block**: 입력 채널이 256이고, 내부적으로 256, 256, 128 채널을 가지는 SPPELAN Block입니다.
- **Upsample Layer**: 이미지 크기를 2배로 업샘플링하는 Upsample Layer입니다.
- **Concat Layer**: 특정 차원에 대해 Concatenation을 수행하는 Concat Layer입니다.
- **RepNCSPELAN4 Block**: 입력 채널이 448이고, 각각 192, 192, 96 채널을 가지며 3개의 Convolutional Layer를 포함하는 RepNCSPELAN4 Block입니다.
- **Upsample Layer**: 이미지 크기를 2배로 업샘플링하는 Upsample Layer입니다.
- **Concat Layer**: 특정 차원에 대해 Concatenation을 수행하는 Concat Layer입니다.
- **RepNCSPELAN4 Block**: 입력 채널이 320이고, 각각 128, 128, 64 채널을 가지며 3개의 Convolutional Layer를 포함하는 RepNCSPELAN4 Block입니다.
- **AConv Block**: 입력 채널이 128이고 출력 채널이 96인 AConv Block입니다.
- **Concat Layer**: 특정 차원에 대해 Concatenation을 수행하는 Concat Layer입니다.
- **RepNCSPELAN4 Block**: 입력 채널이 288이고, 각각 192, 192, 96 채널을 가지며 3개의 Convolutional Layer를 포함하는 RepNCSPELAN4 Block입니다.
