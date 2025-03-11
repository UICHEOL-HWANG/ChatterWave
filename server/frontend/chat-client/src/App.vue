<template>
  <div id="app">
    <NavBar />
    <main class="main-content">
      <router-view v-if="$route.path !== '/'"></router-view>
      <div v-else class="home">
        <section class="hero">
          <div class="hero-content">
            <h1>실시간 채팅으로<br>소통을 시작하세요</h1>
            <p>안전하고 빠른 실시간 채팅 서비스를 경험해보세요</p>
            <div class="hero-buttons">
              <router-link
                :to="isAuthenticated ? '/chat' : '/login'"
                class="btn btn-primary"
              >
                무료로 시작하기</router-link>
              <router-link to="/login" class="btn btn-secondary">로그인</router-link>
            </div>
          </div>
        </section>

        <section class="features">
          <div class="feature-container">
            <div class="feature-item">
              <div class="feature-icon">🚀</div>
              <h3>빠른 시작</h3>
              <p>간단한 회원가입으로<br>즉시 채팅을 시작하세요</p>
            </div>
            <div class="feature-item">
              <div class="feature-icon">🔒</div>
              <h3>보안 중심</h3>
              <p>안전한 채팅을 위한<br>최고 수준의 보안</p>
            </div>
            <div class="feature-item">
              <div class="feature-icon">💬</div>
              <h3>실시간 소통</h3>
              <p>끊김 없는 실시간<br>메시지 전송</p>
            </div>
          </div>
        </section>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue'
import Login from './components/Login.vue'
import Signup from './components/signup.vue'


export default {
  name: 'App',
  components: {
    NavBar,
    Footer,
    Login,
    Signup,

  },
  computed: {
    ...mapGetters(['isAuthenticated']), // Vuex에서 인증 상태를 가져옵니다.
  },
}
</script>

<style>




/* ... 기존 스타일 유지 ... */

/* 모바일 반응형 스타일 */
@media (max-width: 768px) {
  .hero {
    padding: 40px 20px;
  }

  .hero h1 {
    font-size: 2rem;
    line-height: 1.3;
    margin-bottom: 15px;
  }

  .hero p {
    font-size: 1rem;
    margin-bottom: 30px;
    padding: 0 20px;
  }

  .hero-buttons {
    flex-direction: column;
    gap: 15px;
  }

  .btn {
    width: 100%;
    max-width: 280px;
    padding: 12px 20px;
    font-size: 1rem;
  }

  .features {
    padding: 40px 20px;
  }

  .feature-container {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .feature-item {
    padding: 30px 20px;
  }

  .feature-icon {
    font-size: 2.5rem;
    margin-bottom: 15px;
  }

  .feature-item h3 {
    font-size: 1.3rem;
    margin-bottom: 10px;
  }

  .feature-item p {
    font-size: 0.9rem;
  }
}

/* 더 작은 모바일 화면 */
@media (max-width: 480px) {
  .hero h1 {
    font-size: 1.8rem;
  }

  .hero p {
    font-size: 0.9rem;
  }

  .btn {
    max-width: 240px;
    padding: 10px 15px;
  }

  .feature-item {
    padding: 25px 15px;
  }
}

/* 가로 모드 대응 */
@media (max-height: 600px) and (orientation: landscape) {
  .hero {
    padding: 30px 20px;
  }

  .hero h1 {
    font-size: 1.8rem;
    margin-bottom: 10px;
  }

  .feature-container {
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
}

/* ... 다른 스타일들은 유지 ... */

.feature-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 80px; /* 40px에서 80px로 증가 */
  padding: 0 40px; /* 좌우 패딩 추가 */
}

/* 모바일 대응을 위한 미디어 쿼리 */
@media (max-width: 768px) {
  .feature-container {
    grid-template-columns: 1fr;
    gap: 40px; /* 모바일에서는 간격을 좁게 */
    padding: 0 20px; /* 모바일에서는 패딩을 좁게 */
  }

}
#app {
  font-family: 'Noto Sans KR', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh; /* 최소 높이 설정 */
  display: flex; /* flex 레이아웃으로 설정 */
  flex-direction: column; /* 상단부터 아래로 배치 */
  padding: 0;
  margin: 0 auto; /* 화면 중앙 정렬 */
}

.main-content {
  flex: 1; /* 남은 공간을 차지하도록 설정 */
  max-width: 1200px; /* 최대 너비 설정 */
  margin: 65px auto; /* 중앙 정렬 */
  padding: 20px; /* 내부 여백 추가 */
  display: flex;
  flex-direction: column; /* 세로 레이아웃 */
  background-color: #ffffff; /* 배경색 */
}

.home {
  width: 100%;
}

.hero {
  padding: 80px 20px;
  background: linear-gradient(135deg, #742DDD 0%, #9754FF 100%);
  color: white;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero h1 {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  line-height: 1.2;
}

.hero p {
  font-size: 1.25rem;
  margin-bottom: 40px;
  color: rgba(255, 255, 255, 0.9);
}

.hero-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.btn {
  padding: 15px 30px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  text-decoration: none;
  transition: transform 0.2s;
}

.btn:hover {
  transform: translateY(-2px);
}

.btn-primary {
  background-color: white;
  color: #742DDD;
}

.btn-secondary {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid white;
}

.features {
  padding: 80px 20px;
  background-color: white;
}

.feature-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.feature-item {
  text-align: center;
  padding: 40px 20px;
  border-radius: 12px;
  background-color: #f8f9fa;
  transition: transform 0.2s;
}

.feature-item:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.feature-item h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 15px;
}

.feature-item p {
  color: #666;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 2.5rem;
  }

  .feature-container {
    grid-template-columns: 1fr;
  }

  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }

  .btn {
    width: 100%;
    max-width: 300px;
    text-align: center;
  }
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background-color: #f5f5f5;
  margin: 0;
  padding: 0;
  min-height: 100vh;
}
</style>
