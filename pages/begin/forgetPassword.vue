<template>
  <view class="forget-password-container">
    <view class="brand-section">
      <image src="/static/app-logo-color.png" class="logo" mode="aspectFit"></image>
      <text class="title">找回密码</text>
      <text class="subtitle">请输入您的注册邮箱以重置密码</text>
    </view>
    <view class="form-card">
      <view class="input-wrapper">
        <image src="/static/email-icon-gray.png" class="input-icon" mode="aspectFit"></image>
        <input type="text" placeholder="请输入邮箱" class="input-field" v-model="email" />
      </view>
      <button class="submit-button" @tap="sendResetLink">发送重置链接</button>
    </view>
    <view class="footer-actions">
      <text class="action-link" @tap="goToLogin">返回登录</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      email: '', // 示例：确保 email 属性已定义
    };
  },
  methods: {
    sendResetLink() {
      // 处理发送重置链接的逻辑
      if (!this.email) {
        uni.showToast({ title: '请输入邮箱', icon: 'none' });
        return;
      }
      console.log('发送重置链接至:', this.email);
      // 此处应有实际的API调用来发送邮件
      // uni.request({...})
      uni.showToast({ title: '重置链接已发送，请检查邮箱', icon: 'success', duration: 2000 });
      // 可以在成功后导航回登录页面或提示用户
      // setTimeout(() => {
      //  uni.navigateTo({ url: '/pages/begin/login' });
      // }, 2000);
    },
    goToLogin() {
      uni.navigateTo({ url: '/pages/begin/login' });
    }
  }
};
</script>

<style scoped>
.forget-password-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* 从顶部开始对齐 */
  min-height: 100vh;
  background: linear-gradient(135deg, #6DD5FA, #FF758C); /* 与注册页一致的柔和渐变 */
  padding: 40rpx;
  box-sizing: border-box;
}

.brand-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 80rpx; /* 顶部留白 */
  margin-bottom: 60rpx;
}

.logo {
  width: 150rpx;
  height: 150rpx;
  margin-bottom: 30rpx;
}

.title {
  font-size: 48rpx;
  font-weight: bold;
  color: #fff;
  margin-bottom: 15rpx;
}

.subtitle {
  font-size: 28rpx;
  color: #f0f0f0; /* 稍暗的白色 */
  text-align: center;
}

.form-card {
  background-color: #ffffff;
  padding: 50rpx 40rpx;
  border-radius: 20rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 650rpx; /* 限制最大宽度 */
  box-sizing: border-box;
  margin-bottom: 40rpx;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background-color: #f7f7f7;
  border-radius: 15rpx;
  padding: 0 25rpx; /* 调整内边距 */
  margin-bottom: 40rpx; /* 增大与按钮的间距 */
  border: 1rpx solid #eee;
}

.input-icon {
  width: 36rpx;
  height: 36rpx;
  margin-right: 20rpx;
  opacity: 0.6;
}

.input-field {
  flex: 1;
  height: 90rpx; /* 增加高度 */
  font-size: 30rpx;
  color: #333;
}

.input-field::placeholder {
  color: #aaa;
}

.submit-button {
  background: linear-gradient(to right, #6DD5FA, #FF758C);
  color: white;
  font-size: 32rpx;
  font-weight: bold;
  border-radius: 15rpx;
  height: 90rpx;
  line-height: 90rpx;
  text-align: center;
  border: none;
  box-shadow: 0 5rpx 15rpx rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.submit-button:active {
  transform: scale(0.98);
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.2);
}

.footer-actions {
  margin-top: 30rpx;
  text-align: center;
}

.action-link {
  font-size: 28rpx;
  color: #ffffff; /* 白色链接，适应背景 */
  text-decoration: underline;
}
</style>