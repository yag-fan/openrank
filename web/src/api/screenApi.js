import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器：打印请求信息
api.interceptors.request.use(
  (config) => {
    console.log('[API 请求]', config.method?.toUpperCase(), config.url, 'params=', config.params, 'data=', config.data)
    return config
  },
  (error) => {
    console.error('[API 请求错误]', error)
    return Promise.reject(error)
  }
)

// 响应拦截器：打印响应信息
api.interceptors.response.use(
  (response) => {
    console.log('[API 响应]', response.config.url, 'status=', response.status, 'data=', response.data)
    return response
  },
  (error) => {
    if (error.response) {
      console.error('[API 响应错误]', error.config?.url, 'status=', error.response.status, 'data=', error.response.data)
    } else {
      console.error('[API 网络错误]', error.message)
    }
    return Promise.reject(error)
  }
)

// 获取大屏核心数据
export const getCoreData = () => {
  return api.get('/screen/core-data')
}

// 获取PR详情
export const getPrDetail = (prId) => {
  return api.get(`/screen/pr-detail/${prId}`)
}

// 获取时序趋势数据
export const getTimeTrend = () => {
  return api.get('/screen/time-trend')
}

export default api

