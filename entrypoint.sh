export ENV=prod
uvicorn app.main:app --host 0.0.0.0 --port $PORT
# 도커 파일이 실행될 때, entrypoint.sh 파일이 실행되면서, ENV 환경변수를 prod로 설정하고, uvicorn을 실행한다.
