<template>
  <view class="container">
    <view class="header">
      <image class="logo" src="/static/logo.png" mode="aspectFit"></image>
      <text class="title" @click="handleTitleTap">竞赛报名系统</text>
      <text class="subtitle">在线报名，便捷高效</text>
    </view>
    
    <view class="quick-actions">
      <view class="action-item" @click="goToRegister">
        <view class="action-icon">📝</view>
        <text class="action-title">立即报名</text>
        <text class="action-desc">填写报名信息</text>
      </view>

      <view class="action-item" @click="goToApplicationQuery">
        <view class="action-icon">🔎</view>
        <text class="action-title">报名查询</text>
        <text class="action-desc">按手机号查询</text>
      </view>
      
      <view class="action-item" @click="goToMyApplications">
        <view class="action-icon">📋</view>
        <text class="action-title">获奖查询</text>
        <text class="action-desc">按参赛号查询</text>
      </view>

      <view class="action-item" @click="goToCoachAward">
        <view class="action-icon">🏅</view>
        <text class="action-title">优秀辅导员</text>
        <text class="action-desc">证书查询</text>
      </view>
    </view>
    
    <view class="info-section">
      <view class="info-title">
        <text class="info-title-text">竞赛项目</text>
      </view>
      <view class="project-list">
        <view 
          v-for="(projects, category) in competitionRules" 
          :key="category"
          class="project-category"
        >
          <text class="category-name">{{ category }}</text>
          <view class="task-list">
            <view 
              v-for="(rule, task) in projects" 
              :key="task"
              class="task-item"
            >
              <text class="task-name">{{ task }}</text>
              <text class="task-info">{{ rule.participant_count }}人 | {{ rule.allowed_levels.join('、') }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import * as requestApi from '../../utils/request'
import auth from '../../utils/auth'

const request = requestApi && requestApi.default ? requestApi.default : requestApi

export default {
  data() {
    return {
      competitionRules: {},
      _titleTapCount: 0,
      _titleTapTimer: null
    }
  },
  
  onLoad() {
    this.loadCompetitionRules()
  },

  async onShow() {
    await auth.requireUserLoginOrRedirect('/pages/index/index')
  },
  
  methods: {
    handleTitleTap() {
      try {
        if (this._titleTapTimer) clearTimeout(this._titleTapTimer)
      } catch (e) {}

      this._titleTapCount += 1
      this._titleTapTimer = setTimeout(() => {
        this._titleTapCount = 0
      }, 800)

      if (this._titleTapCount >= 7) {
        this._titleTapCount = 0
        uni.navigateTo({
          url: '/pages/admin-login/admin-login'
        })
      }
    },
    async loadCompetitionRules() {
      try {
        const data = await request.get('/api/competition-rules')
        if (data.success) {
          this.competitionRules = data.data
        }
      } catch (error) {
        console.error('加载竞赛规则失败:', error)
      }
    },
    
    goToRegister() {
      uni.switchTab({
        url: '/pages/register/register'
      })
    },
    
    goToMyApplications() {
      uni.switchTab({
        url: '/pages/my-applications/my-applications'
      })
    },

    goToApplicationQuery() {
      uni.navigateTo({
        url: '/pages/application-query/application-query'
      })
    },

    goToCoachAward() {
      uni.navigateTo({
        url: '/pages/coach-award/coach-award'
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
}

.header {
  text-align: center;
  padding: 40px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  margin-bottom: 30px;
  color: white;
}

.logo {
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
}

.title {
  display: block;
  font-size: 28px;
  margin-bottom: 10px;
}

.subtitle {
  display: block;
  font-size: 16px;
  opacity: 0.8;
}

.quick-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
}

.action-item {
  background-color: #fff;
  padding: 18px 12px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.action-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.action-title {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.action-desc {
  display: block;
  font-size: 14px;
  color: #666;
}

.info-section {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.info-title {
  border-bottom: 2px solid #007aff;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.info-title-text {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.project-category {
  margin-bottom: 25px;
}

.category-name {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: #007aff;
  margin-bottom: 15px;
}

.task-list {
  padding-left: 15px;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 10px;
}

.task-name {
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

.task-info {
  font-size: 14px;
  color: #666;
}
</style>
