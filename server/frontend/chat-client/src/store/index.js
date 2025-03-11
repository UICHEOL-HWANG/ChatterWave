import { createStore } from 'vuex';

export default createStore({
  state: {
    token: localStorage.getItem('access_token') || null,
    isAuthenticated: !!localStorage.getItem('access_token'),
    username: localStorage.getItem('username') || null,
    isBanned: localStorage.getItem('is_banned') === "true" // 차단 상태
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token;
      state.isAuthenticated = !!token;
      if (token) {
        localStorage.setItem('access_token', token);
      } else {
        localStorage.removeItem('access_token');
        localStorage.removeItem('username');
      }
    },
    SET_USERNAME(state, username) {
      state.username = username;
      if (username) {
        localStorage.setItem('username', username);
      } else {
        localStorage.removeItem('username');
      }
    },
    SET_BAN_STATUS(state, isBanned) { // ✅ 차단 상태 업데이트
      state.isBanned = isBanned;
      localStorage.setItem('is_banned', isBanned ? "true" : "false");
    }
  },
  actions: {
    setToken({ commit }, token) {
      commit('SET_TOKEN', token);
    },
    setUsername({ commit }, username) {
      commit('SET_USERNAME', username);
    },
    setBanStatus({ commit }, isBanned) { // ✅ 차단 상태 업데이트 액션 추가
      commit('SET_BAN_STATUS', isBanned);
    },
    logout({ commit }) {
      commit('SET_TOKEN', null);
      commit('SET_USERNAME', null);
      commit('SET_BAN_STATUS', false); // ✅ 로그아웃 시 차단 상태 초기화
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    getToken: state => state.token,
    getUsername: state => state.username,
    getBanStatus: state => state.isBanned // ✅ 차단 상태 getter 추가
  }
});
