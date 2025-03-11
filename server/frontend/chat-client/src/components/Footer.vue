<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-section">
        <h3>ChatApp</h3>
        <p>실시간 채팅 서비스</p>
      </div>
      <div class="footer-section">
        <h4>링크</h4>
        <ul>
          <li><router-link to="/about">소개</router-link></li>
          <li><router-link to="/privacy">개인정보처리방침</router-link></li>
          <li><router-link to="/terms">이용약관</router-link></li>
        </ul>
      </div>
      <div class="footer-section">
        <h4>문의</h4>
        <ul>
          <li>이메일: support@chatapp.com</li>
          <li>전화: 02-1234-5678</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2024 ChatApp. All rights reserved.</p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background-color: #1a1a1a;
  color: white;
  padding: 40px 0 20px;
  position: relative;
  width: 100vw;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  box-sizing: border-box;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.footer-section h3 {
  font-size: 20px;
  margin-bottom: 15px;
}

.footer-section h4 {
  font-size: 16px;
  margin-bottom: 10px;
}

.footer-section ul {
  list-style: none;
}

.footer-section ul li {
  margin-bottom: 8px;
}

.footer-section a {
  color: #fff;
  text-decoration: none;
}

.footer-section a:hover {
  text-decoration: underline;
}

.footer-bottom {
  text-align: center;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #333;
}
</style> 