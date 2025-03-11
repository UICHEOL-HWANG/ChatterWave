FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /api_app

# pip 업데이트
RUN pip install --upgrade pip

# requirements.txt 파일 복사 후 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY . .

CMD ["python", "main.py"]