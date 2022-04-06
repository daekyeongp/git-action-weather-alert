# Github Action with Python
- (1) Weather Alert Github Action
  - 케이웨더 일기예보를 이미지 기반으로, 해당 Github Issue 업로드
  - 매일 오전 8시에 업로드(한국 시간)
  - Watch 클릭시 이메일로 알람받을 수 있음
- (2) main.py 실행하는 Github Action
  - Master로 Push할 때 실행
- (3) Job에서 생성한 파일을 공유해서 사용하는 Github Action
  - [upload-artifact](https://github.com/actions/upload-artifact)와 [download-artifact](https://github.com/actions/download-artifact) 사용 예제

# Reference
- https://velog.io/@king/weather-alert
- https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- https://docs.github.com/en/actions
- https://www.actionsbyexample.com/
- https://lab.github.com/githubtraining/devops-with-github-actions