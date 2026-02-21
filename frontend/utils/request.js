// API请求封装
const _storageBaseUrl = (
  (typeof uni !== 'undefined' && uni && typeof uni.getStorageSync === 'function')
    ? String(uni.getStorageSync('base_url') || '').trim()
    : ''
)

const _h5LocalBaseUrl = (() => {
  try {
    if (typeof location === 'undefined' || !location) return ''
    const hostname = String(location.hostname || '').trim()
    if (hostname === 'localhost' || hostname === '127.0.0.1') return 'http://127.0.0.1:5001'
    return ''
  } catch (e) {
    return ''
  }
})()

export const BASE_URL = _storageBaseUrl || 'http://127.0.0.1:5001'

const request = (options) => {
  return new Promise((resolve, reject) => {
    const url = options.url || ''
    const isAdminApi = typeof url === 'string' && url.startsWith('/api/admin/')
    const tokenKey = isAdminApi ? 'admin_token' : 'user_token'
    const token = uni.getStorageSync(tokenKey) || ''

    uni.request({
      url: BASE_URL + url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options.header
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
          return
        }

        const payload = res && res.data ? res.data : {}
        if (payload && typeof payload === 'object') {
          resolve({
            success: false,
            statusCode: res.statusCode,
            ...payload
          })
          return
        }

        resolve({
          success: false,
          statusCode: res.statusCode,
          message: '请求失败'
        })
      },
      fail: (error) => {
        reject(error)
      }
    })
  })
}

export default {
  get: (url, data, options = {}) => {
    return request({
      url,
      method: 'GET',
      data,
      ...options
    })
  },
  
  post: (url, data, options = {}) => {
    return request({
      url,
      method: 'POST',
      data,
      ...options
    })
  },
  
  put: (url, data, options = {}) => {
    return request({
      url,
      method: 'PUT',
      data,
      ...options
    })
  },
  
  delete: (url, data, options = {}) => {
    return request({
      url,
      method: 'DELETE',
      data,
      ...options
    })
  }
}
