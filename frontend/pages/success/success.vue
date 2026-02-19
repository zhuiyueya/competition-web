<template>
  <view class="container">
    <view class="success-card">
      <view class="success-icon">✅</view>
      <text class="success-title">报名成功！</text>
      <text class="success-message">您的报名信息已提交，请等待审核</text>
      
      <view class="next-steps">
        <text class="steps-title">后续步骤：</text>
        <view class="step-item">
          <text class="step-number">1</text>
          <text class="step-text">等待管理员审核报名信息</text>
        </view>
        <view class="step-item">
          <text class="step-number">2</text>
          <text class="step-text">审核通过后分配参赛号</text>
        </view>
        <view class="step-item">
          <text class="step-number">3</text>
          <text class="step-text">比赛结束后可查询获奖情况</text>
        </view>
      </view>
      
      <view class="action-buttons">
        <button class="btn-secondary" @click="viewMyApplications">查看我的报名</button>
        <button class="btn-primary" @click="goHome">返回首页</button>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  methods: {
    viewMyApplications() {
      uni.navigateTo({
        url: '/pages/application-query/application-query'
      })
    },
    
    goHome() {
      uni.switchTab({
        url: '/pages/index/index'
      })
    }
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.success-card {
  background-color: white;
  border-radius: 20px;
  padding: 40px 30px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  max-width: 350px;
  width: 100%;
}

.success-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.success-title {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.success-message {
  display: block;
  font-size: 16px;
  color: #666;
  margin-bottom: 30px;
  line-height: 1.5;
}

.next-steps {
  text-align: left;
  background-color: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
}

.steps-title {
  display: block;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

.step-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.step-item:last-child {
  margin-bottom: 0;
}

.step-number {
  width: 24px;
  height: 24px;
  background-color: #007aff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  margin-right: 12px;
  flex-shrink: 0;
}

.step-text {
  font-size: 14px;
  color: #555;
  line-height: 1.4;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-primary {
  background-color: #007aff;
  color: white;
  border: none;
  border-radius: 25px;
  padding: 15px 30px;
  font-size: 16px;
  font-weight: bold;
}

.btn-secondary {
  background-color: transparent;
  color: #007aff;
  border: 2px solid #007aff;
  border-radius: 25px;
  padding: 13px 30px;
  font-size: 16px;
}
</style>
