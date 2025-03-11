<template>
  <div class="login-container">
    <div class="login-box">
      <h1 class="login-title">로그인</h1>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="username">아이디</label>
          <input 
            v-model="form.username" 
            id="username" 
            type="text" 
            required 
            placeholder="아이디를 입력하세요"
          />
        </div>
        <div class="form-group">
          <label for="password">비밀번호</label>
          <input 
            v-model="form.password" 
            id="password" 
            type="password" 
            required 
            placeholder="비밀번호를 입력하세요"
          />
        </div>
        <button type="submit" class="login-button">로그인</button>
      </form>
      <div class="signup-link">
        계정이 없으신가요? <router-link to="/signup">회원가입</router-link>
      </div>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';  // 세미콜론 추가

export default {
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      errorMessage: ''
    };  // 세미콜론 추가
  },
  methods: {
    async login() {
      try {
        const params = new URLSearchParams();  // 세미콜론 추가
        params.append('username', this.form.username);  // 세미콜론 추가
        params.append('password', this.form.password);  // 세미콜론 추가
        params.append('scope', '');  // 세미콜론 추가
        params.append('grant_type', 'password');  // 세미콜론 추가
        params.append('client_id', 'string');  // 세미콜론 추가
        params.append('client_secret', 'string');  // 세미콜론 추가

        const response = await axios.post('http://localhost:8008/user/login', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });  // 세미콜론 추가

        if (response.data && response.data.access_token) {
          localStorage.setItem('access_token', response.data.access_token);  // 세미콜론 추가
          localStorage.setItem('username', this.form.username);  // 세미콜론 추가

          this.$store.dispatch('setBanStatus', response.data.is_banned);
          
          this.$store.dispatch('setToken', response.data.access_token);  // 세미콜론 추가
          alert('로그인이 완료되었습니다!');  // 세미콜론 추가
          this.$router.push('/');  // 세미콜론 추가
        }
      } catch (error) {
        this.errorMessage = '로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.';  // 세미콜론 추가
        console.error('Login error:', error);  // 세미콜론 추가
      }
    }
  }
};  // 세미콜론 추가
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 400px;
}
.signup-link {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #666;
}

.signup-text {
  color: #742DDD;
  text-decoration: none;
  font-weight: 600;
  margin-left: 5px;
}

.signup-text:hover {
  text-decoration: underline;
}

.login-title {
  font-size: 24px;
  color: #1a1a1a;
  margin-bottom: 30px;
  text-align: center;
  font-weight: 600;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
  text-align: left;
}

.form-group input {
  padding: 12px;
  border: 1px solid #e1e1e1;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #742DDD;
}

.login-button {
  background-color: #742DDD;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #6425c4;
}

.error {
  color: #ff4b4b;
  font-size: 14px;
  margin-top: 16px;
  text-align: center;
}
</style>