<template>
  <view class="container">
    <view class="card">
      <text class="title">微信授权登录</text>
      <text class="desc">进入系统前需要完成微信授权登录，用于报名与证书查询</text>

      <button class="btn" @click="handleLogin">微信授权登录</button>

      <text v-if="errorMsg" class="error">{{ errorMsg }}</text>
    </view>
  </view>
</template>

<script>
import auth from '../../utils/auth'

export default {
  data() {
    return {
      errorMsg: ''
    }
  },

  methods: {
    async handleLogin() {
      this.errorMsg = ''
      const ok = await auth.loginWithWeChatProfile()
      if (!ok) {
        this.errorMsg = '授权或登录失败，请重试'
        return
      }

      const redirect = uni.getStorageSync('post_login_redirect')
      if (redirect) {
        try { uni.removeStorageSync('post_login_redirect') } catch (e) {}
        if (String(redirect).startsWith('/pages/register/')) {
          uni.switchTab({ url: '/pages/register/register' })
          return
        }
        if (String(redirect).startsWith('/pages/my-applications/')) {
          uni.switchTab({ url: '/pages/my-applications/my-applications' })
          return
        }
        uni.reLaunch({ url: String(redirect) })
        return
      }

      uni.switchTab({ url: '/pages/index/index' })
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
}

.card {
  width: 100%;
  background-color: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  box-sizing: border-box;
}

.title {
  display: block;
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.desc {
  display: block;
  font-size: 14px;
  color: #666;
  line-height: 20px;
  margin-bottom: 18px;
}

.btn {
  background-color: #07c160;
  color: #fff;
  border-radius: 8px;
}

.error {
  display: block;
  margin-top: 12px;
  color: #e74c3c;
  font-size: 12px;
}
</style>
