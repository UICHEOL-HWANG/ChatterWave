import { createRouter, createWebHistory } from 'vue-router';
import store from '../store';
import Login from '../components/Login.vue';
import Signup from '../components/signup.vue';
import ChatRooms from '../components/ChatRooms.vue';

const routes = [
  { path: '/login', name: 'login', component: Login },
  { path: '/signup', name: 'signup', component: Signup },
  { 
    path: '/chat', 
    name: 'chat', 
    component: ChatRooms, 
    meta: { requiresAuth: true , requiresNoBan: true }  
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(async (to, from, next) => {
  const isAuthenticated = !!store.getters.getToken;
  const isBanned = store.getters.getBanStatus; // ✅ Vuex에서 차단 여부 가져오기

  // 🔒 인증이 필요한 페이지인데 로그인 안 된 경우 → 로그인 페이지로 이동
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
    return;
  }

  // 🚫 차단된 사용자가 채팅 라우트로 접근하려는 경우 → 메인 페이지로 리디렉트
  if (to.meta.requiresNoBan && isBanned) {
    alert("🚫 차단된 사용자입니다. 채팅에 접근할 수 없습니다.");
    next('/');
    return;
  }

  next();
});

export default router;
