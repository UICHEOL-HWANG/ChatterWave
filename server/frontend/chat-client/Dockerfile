# Node.js 이미지 사용
FROM node:18-alpine

# 작업 디렉토리 설정
WORKDIR /front

# package.json과 package-lock.json 복사 후 의존성 설치
COPY package*.json ./
RUN npm install

# 애플리케이션 소스 코드 복사
COPY . .

# 애플리케이션 빌드
RUN npm run build

# http-server 설치
RUN npm install -g http-server

# 8080 포트 열기
EXPOSE 8080

# 빌드된 파일을 http-server로 서빙
CMD ["http-server", "dist", "-p", "8080"]
