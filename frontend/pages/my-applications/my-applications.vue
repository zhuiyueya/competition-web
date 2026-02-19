<template>
  <view class="container">
    <view class="search-bar">
      <input 
        v-model="matchNo"
        type="text"
        placeholder="请输入参赛号查询"
        class="search-input"
      />
      <button class="search-btn" @click="searchApplications">查询</button>
    </view>

    <text class="search-hint">请使用管理员发布的参赛号查询获奖信息</text>
    
    <view class="application-list" v-if="applications.length > 0">
      <view 
        v-for="application in applications" 
        :key="application.id"
        class="application-item"
      >
        <view class="app-header">
          <text class="project-name">{{ application.category }} - {{ application.task }}</text>
          <view :class="['status-badge', getStatusClass(application.status)]">
            {{ getStatusText(application.status) }}
          </view>
        </view>
        
        <view class="app-content">
          <view class="info-row">
            <text class="info-label">学校：</text>
            <text class="info-value">{{ displayText(application.school_name) }}</text>
          </view>
          
          <view class="info-row">
            <text class="info-label">学段：</text>
            <text class="info-value">{{ displayText(application.education_level) }}</text>
          </view>
          
          <view class="info-row">
            <text class="info-label">人数：</text>
            <text class="info-value">{{ application.participant_count }}人</text>
          </view>
          
          <view class="info-row">
            <text class="info-label">联系人：</text>
            <text class="info-value">{{ displayText(application.contact_name) }}</text>
          </view>
          
          <view class="info-row">
            <text class="info-label">手机：</text>
            <text class="info-value">{{ displayText(application.contact_phone) }}</text>
          </view>
          
          <view class="info-row" v-if="application.match_no">
            <text class="info-label">参赛号：</text>
            <text class="info-value">{{ displayText(application.match_no) }}</text>
          </view>
          
          <view class="info-row" v-if="application.award_level">
            <text class="info-label">获奖：</text>
            <text class="info-value award-text">{{ displayText(application.award_level) }}</text>
          </view>
          
          <view class="participants-section" v-if="application.participants.length > 0">
            <text class="participants-title">选手名单：</text>
            <view class="participants-list">
              <text 
                v-for="participant in application.participants" 
                :key="participant.id"
                class="participant-name"
              >
                {{ participant.seq_no }}. {{ participant.participant_name }}
              </text>
            </view>
          </view>
        </view>
        
        <view class="app-footer">
          <text class="submit-time">
            提交时间：{{ formatDate(application.created_at) }}
          </text>

          <button
            class="cert-btn"
            :disabled="!canOpenCertificate(application)"
            @click="openPlayerCertificate(application)"
          >
            打开获奖证书
          </button>
        </view>
      </view>
    </view>
    
    <view class="empty-state" v-else-if="hasSearched">
      <view class="empty-icon">📭</view>
      <text class="empty-text">很遗憾，未查询到获奖信息</text>
    </view>
    
    <view class="initial-state" v-else>
      <view class="initial-icon">🔍</view>
      <text class="initial-text">请输入参赛号查询获奖信息</text>
    </view>
  </view>
</template>

<script>
import * as requestApi from '../../utils/request'
import auth from '../../utils/auth'

const request = requestApi && requestApi.default ? requestApi.default : requestApi
const BASE_URL = requestApi && requestApi.BASE_URL ? requestApi.BASE_URL : ''

export default {
  data() {
    return {
      matchNo: '',
      applications: [],
      hasSearched: false
    }
  },

  async onShow() {
    await auth.requireUserLoginOrRedirect('/pages/my-applications/my-applications')
  },

  onHide() {
    this.resetPage()
  },

  onUnload() {
    this.resetPage()
  },
  
  methods: {
    resetPage() {
      this.matchNo = ''
      this.applications = []
      this.hasSearched = false
    },

    canOpenCertificate(application) {
      return !!(application && !this.isBlankText(application.award_level))
    },

    isBlankText(v) {
      const s = String(v == null ? '' : v).trim()
      if (!s) return true
      const low = s.toLowerCase()
      return low === 'nan' || low === 'none' || low === 'null' || low === 'undefined'
    },

    displayText(v) {
      return this.isBlankText(v) ? '无' : String(v).trim()
    },

    openPlayerCertificate(application) {
      if (!this.canOpenCertificate(application)) return

      const id = application.id
      const url = `${BASE_URL}/api/certificate/generate/${id}`
      const token = String(uni.getStorageSync('user_token') || '').trim()
      uni.showLoading({ title: '打开中...' })

      uni.downloadFile({
        url,
        header: token ? { Authorization: `Bearer ${token}` } : {},
        success: (res) => {
          uni.hideLoading()
          if (!res || res.statusCode !== 200) {
            const sc = res && typeof res.statusCode !== 'undefined' ? String(res.statusCode) : ''
            uni.showModal({
              title: '下载失败',
              content: sc ? `HTTP ${sc}` : '下载失败',
              showCancel: false
            })
            return
          }
          const tempFilePath = res && res.tempFilePath
          if (!tempFilePath) {
            uni.showModal({
              title: '下载失败',
              content: '未获取到临时文件路径',
              showCancel: false
            })
            return
          }
          uni.openDocument({
            filePath: tempFilePath,
            showMenu: true,
            fail: (e) => {
              const msg = (e && e.errMsg) ? String(e.errMsg) : '打开失败'
              uni.showModal({
                title: '打开失败',
                content: msg,
                showCancel: false
              })
            }
          })
        },
        fail: (e) => {
          uni.hideLoading()
          const msg = (e && e.errMsg) ? String(e.errMsg) : '下载失败'
          uni.showModal({
            title: '下载失败',
            content: msg,
            showCancel: false
          })
        }
      })
    },
    async searchApplications() {
      const ok = await auth.requireUserLoginOrRedirect('/pages/my-applications/my-applications')
      if (!ok) return

      if (!this.matchNo || !String(this.matchNo).trim()) {
        uni.showToast({
          title: '请输入参赛号',
          icon: 'error'
        })
        return
      }
      
      try {
        uni.showLoading({
          title: '查询中...'
        })

        const data = await request.get('/api/my-applications', {
          match_no: String(this.matchNo).trim()
        })

        uni.hideLoading()

        if (data.success) {
          this.applications = data.data
          this.hasSearched = true
        } else {
          uni.showModal({
            title: '查询失败',
            content: data.message || '查询失败，请重试',
            showCancel: false
          })
        }
      } catch (error) {
        uni.hideLoading()
        uni.showToast({
          title: '网络错误',
          icon: 'error'
        })
      }
    },
    
    getStatusClass(status) {
      const statusMap = {
        'pending': 'status-pending',
        'approved': 'status-approved',
        'rejected': 'status-rejected'
      }
      return statusMap[status] || 'status-default'
    },
    
    getStatusText(status) {
      const statusMap = {
        'pending': '待审核',
        'approved': '已通过',
        'rejected': '已拒绝'
      }
      return statusMap[status] || '未知'
    },
    
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
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

.search-bar {
  display: flex;
  margin-bottom: 20px;
  background-color: white;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.search-hint {
  display: block;
  margin-top: -10px;
  margin-bottom: 20px;
  font-size: 12px;
  color: #666;
  padding: 0 5px;
}

.search-input {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 6px;
  height: 42px;
  line-height: 42px;
  padding: 0 12px;
  font-size: 16px;
  margin-right: 10px;
  box-sizing: border-box;
}

.search-btn {
  background-color: #007aff;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0 20px;
  font-size: 16px;
  height: 42px;
  line-height: 42px;
}

.application-list {
  margin-bottom: 20px;
}

.application-item {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.project-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.status-badge {
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: bold;
}

.status-pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-approved {
  background-color: #d4edda;
  color: #155724;
}

.status-rejected {
  background-color: #f8d7da;
  color: #721c24;
}

.status-default {
  background-color: #e2e3e5;
  color: #383d41;
}

.app-content {
  margin-bottom: 15px;
}

.info-row {
  display: flex;
  margin-bottom: 8px;
}

.info-label {
  width: 80px;
  color: #666;
  font-size: 14px;
}

.info-value {
  flex: 1;
  color: #333;
  font-size: 14px;
}

.cert-btn {
  margin-top: 10px;
  background-color: #007aff;
  color: white;
  border-radius: 20px;
  padding: 8px 18px;
  font-size: 14px;
}
.award-text {
  color: #ff6b35;
  font-weight: bold;
}

.participants-section {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.participants-title {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.participants-list {
  display: flex;
  flex-wrap: wrap;
}

.participant-name {
  background-color: #f8f9fa;
  padding: 5px 10px;
  border-radius: 15px;
  margin-right: 8px;
  margin-bottom: 5px;
  font-size: 12px;
  color: #333;
}

.app-footer {
  text-align: right;
}

.submit-time {
  font-size: 12px;
  color: #999;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.empty-text {
  display: block;
  font-size: 16px;
  color: #666;
  margin-bottom: 30px;
}

.go-register-btn {
  background-color: #007aff;
  color: white;
  border: none;
  border-radius: 25px;
  padding: 12px 30px;
  font-size: 16px;
}

.initial-state {
  text-align: center;
  padding: 100px 20px;
}

.initial-icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.initial-text {
  display: block;
  font-size: 16px;
  color: #666;
}
</style>
