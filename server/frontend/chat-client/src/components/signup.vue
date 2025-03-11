<template>
  <div class="signup-container">
    <div class="signup-box">
      <h1 class="signup-title">회원가입</h1>
      <form @submit.prevent="register" class="signup-form">
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
          <label for="email">이메일</label>
          <input 
            v-model="form.email" 
            id="email" 
            type="email" 
            required 
            placeholder="이메일을 입력하세요"
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
        <div class="form-group">
          <label for="confirmPassword">비밀번호 확인</label>
          <input 
            v-model="form.confirmPassword" 
            id="confirmPassword" 
            type="password" 
            required 
            placeholder="비밀번호를 다시 입력하세요"
          />
        </div>
        <button type="submit" class="signup-button">회원가입</button>
      </form>
      <div class="login-link">
        이미 계정이 있으신가요? <router-link to="/login" class="login-button">로그인</router-link>
      </div>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  name: 'Signup',
  data() {
    return {
      form: {
        username: '',
        email: '',  // 이메일 필드 추가
        password: '',
        confirmPassword: ''
      },
      errorMessage: ''
    }
  },
  methods: {
    async register() {
      try {
        if (this.form.password !== this.form.confirmPassword) {
          this.errorMessage = '비밀번호가 일치하지 않습니다.'
          return
        }

        const response = await axios.post('http://localhost:8008/user/register', {
          username: this.form.username,
          email: this.form.email,  // 이메일 추가
          password: this.form.password
        })

        if (response.data) {
          // 회원가입 성공
          alert('회원가입이 성공적으로 완료되었습니다! 로그인 페이지로 이동합니다.')
          this.$router.push('/')

        }
      } catch (error) {
        if (error.response) {
          this.errorMessage = error.response.data.detail || '회원가입 중 오류가 발생했습니다.'
        } else {
          this.errorMessage = '서버와 통신 중 오류가 발생했습니다.'
        }
      }
    }
  }
}
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.signup-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 400px;
}

.signup-title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.signup-button {
  width: 100%;
  padding: 12px;
  background-color: #742DDD;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.signup-button:hover {
  background-color: #6021c0;
}

.login-link {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #666;
}

.login-button {
  color: #742DDD;
  text-decoration: none;
  font-weight: 600;
}

.login-button:hover {
  text-decoration: underline;
}

.error {
  color: #dc3545;
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
}
</style>
