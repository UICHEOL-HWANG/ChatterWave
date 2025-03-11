<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="nav-logo">
        <span class="material-icons">message</span>
        <span class="logo-text">Chatter Wave</span>
      </router-link>
      <div class="nav-links">
        <template v-if="isAuthenticated">
          <span class="welcome-message">{{ username }}님 반갑습니다</span>
          <router-link to="/chat" class="nav-link">채팅</router-link>
          <button @click="handleLogout" class="nav-link logout-btn">로그아웃</button>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link">로그인</router-link>
          <router-link to="/signup" class="nav-link">회원가입</router-link>
        </template>
      </div>
    </div> 
  </nav>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'NavBar',
  computed: {
    ...mapGetters(['isAuthenticated', 'getUsername']),
    username() {
      return localStorage.getItem('username') || '사용자';
    }
  },
  methods: {
    ...mapActions(['logout']),
    handleLogout() {
      this.logout();
      localStorage.removeItem('access_token');
      localStorage.removeItem('username');
      this.$router.push('/login');
    }
  },
  created() {
    // 컴포넌트가 생성될 때 로그인 상태 체크
    const token = localStorage.getItem('access_token');
    if (token) {
      this.$store.dispatch('setToken', token);
    }
  },
  mounted() {
    if (this.isAuthenticated && this.$refs.userMenuTrigger) {
      tippy(this.$refs.userMenuTrigger, {
        content: `
          <div class="menu-container">
            <div class="menu-item" onclick="this._tippy.hide()">
              <span class="material-icons">chat</span>
              채팅 시작
            </div>
            <div class="menu-item" onclick="this._tippy.hide()">
              <span class="material-icons">person</span>
              회원 정보
            </div>
            <div class="menu-divider"></div>
            <div class="menu-item" onclick="document.dispatchEvent(new CustomEvent('logout'))">
              <span class="material-icons">logout</span>
              로그아웃
            </div>
          </div>
        `,
        allowHTML: true,
        interactive: true,
        theme: 'light',
        placement: 'bottom-end',
        trigger: 'click',
        arrow: true
      });

      // 로그아웃 이벤트 리스너
      document.addEventListener('logout', this.handleLogout);
    }
  },
  beforeUnmount() {
    document.removeEventListener('logout', this.handleLogout);
  }
};
</script>

<style scoped>

.nav-logo {
  display: flex;
  align-items: center;
  gap: 6px;  /* 간격 미세 조정 */
  font-size: 20px;
  font-weight: 600;
  color: #2D8DDD;
  text-decoration: none;
  height: 40px;  /* 고정 높이 설정 */
}

.nav-logo .material-icons {
  font-size: 24px;
  color: #2D8DDD;
  display: flex;
  align-items: center;
  margin-top: 1px;  /* 미세 상단 조정 */
}

.logo-text {
  display: flex;
  align-items: center;
  height: 100%;
  padding-top: 1px;  /* 텍스트 미세 상단 조정 */
}


.navbar {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-logo {
  font-size: 20px;
  font-weight: bold;
  color: #742DDD;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-link {
  color: #333;
  text-decoration: none;
  font-size: 14px;
  padding: 8px 12px;
  border-radius: 4px;
  transition: all 0.2s;
}

.nav-link:hover {
  background-color: #f5f5f5;
}

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #333;
  padding: 8px 12px;
}

.logout-btn:hover {
  color: #742DDD;
  background-color: #f5f5f5;
  border-radius: 4px;
}

/* Tippy 메뉴 스타일 */
.menu-container {
  padding: 0.5rem;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
  color: #333;
}

.menu-item:hover {
  background: #f5f5f5;
}

.menu-divider {
  height: 1px;
  background: #eee;
  margin: 0.5rem 0;
}

.menu-item .material-icons {
  font-size: 1.2rem;
}
</style>