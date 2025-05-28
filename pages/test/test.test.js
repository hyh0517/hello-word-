import { shallowMount } from '@vue/test-utils'
import Login from '@/pages/login.vue'

describe('Login Component', () => {
  let wrapper

  beforeEach(() => {
    wrapper = shallowMount(Login)
  })

  // 测试页面加载时的逻辑
  it('should check onShow logic', async () => {
    // 模拟 uni.getStorage
    uni.getStorage = jest.fn((options) => {
      if (options.key === 'user_id') {
        options.success({ data: 'mock_user_id' })
      }
    })

    // 模拟 uni.getProvider
    uni.getProvider = jest.fn((options) => {
      if (options.service === 'oauth') {
        options.success({ provider: ['weixin', 'univerify'] })
      }
    })

    await wrapper.vm.onShow()
    expect(uni.getStorage).toHaveBeenCalled()
    expect(uni.getProvider).toHaveBeenCalled()
    expect(wrapper.vm.showPhoneLogin).toBe(true)
  })

  // 测试登录逻辑
  it('should login with correct credentials', async () => {
    // 模拟输入用户名和密码
    wrapper.setData({ username: 'test_user', password: 'test_password' })

    // 模拟 myRequest
    const myRequestMock = jest.fn((options) => {
      if (options.url === '/login') {
        return Promise.resolve({
          statusCode: 201,
          data: { user_id: 'mock_user_id' }
        })
      }
    })
    wrapper.vm.myRequest = myRequestMock

    // 模拟 uni.showToast
    uni.showToast = jest.fn()

    // 模拟 uni.setStorageSync
    uni.setStorageSync = jest.fn()

    // 模拟 uni.reLaunch
    uni.reLaunch = jest.fn()

    await wrapper.vm.login()
    expect(myRequestMock).toHaveBeenCalled()
    expect(uni.showToast).toHaveBeenCalledWith({
      title: '登入成功',
      icon: 'success'
    })
    expect(uni.setStorageSync).toHaveBeenCalledWith('user_id', 'mock_user_id')
    expect(uni.reLaunch).toHaveBeenCalledWith({ url: '/pages/home/home' })
  })

  // 测试微信登录
  it('should login with WeChat', async () => {
    // 模拟 uni.login
    uni.login = jest.fn((options) => {
      if (options.provider === 'weixin') {
        options.success({
          code: 'mock_code',
          authResult: { openid: 'mock_openid' }
        })
      }
    })

    // 模拟 uni.getUserInfo
    uni.getUserInfo = jest.fn((options) => {
      if (options.provider === 'weixin') {
        options.success({
          userInfo: { nickName: 'mock_nickname' }
        })
      }
    })

    // 模拟 myRequest
    const myRequestMock = jest.fn((options) => {
      if (options.url === '/get_id_by_username') {
        return Promise.resolve({ statusCode: 201, data: { user_id: 'mock_user_id' } })
      }
      if (options.url === '/users') {
        return Promise.resolve({ data: { user: { id: 'mock_user_id' } } })
      }
    })
    wrapper.vm.myRequest = myRequestMock

    // 模拟 uni.setStorageSync
    uni.setStorageSync = jest.fn()

    // 模拟 uni.reLaunch
    uni.reLaunch = jest.fn()

    await wrapper.vm.wechatLogin()
    expect(uni.login).toHaveBeenCalled()
    expect(uni.getUserInfo).toHaveBeenCalled()
    expect(myRequestMock).toHaveBeenCalled()
    expect(uni.setStorageSync).toHaveBeenCalledWith('user_id', 'mock_user_id')
    expect(uni.reLaunch).toHaveBeenCalledWith({ url: '/pages/home/home' })
  })

  // 测试手机号登录
  it('should login with phone', async () => {
    // 模拟 uni.login
    uni.login = jest.fn((options) => {
      if (options.provider === 'univerify') {
        options.success({
          authResult: { openid: 'mock_openid' }
        })
      }
    })

    // 模拟 myRequest
    const myRequestMock = jest.fn((options) => {
      if (options.url === '/get_id_by_username') {
        return Promise.resolve({ statusCode: 201, data: { user_id: 'mock_user_id' } })
      }
      if (options.url === '/users') {
        return Promise.resolve({ data: { user: { id: 'mock_user_id' } } })
      }
    })
    wrapper.vm.myRequest = myRequestMock

    // 模拟 uni.setStorageSync
    uni.setStorageSync = jest.fn()

    // 模拟 uni.reLaunch
    uni.reLaunch = jest.fn()

    await wrapper.vm.phoneLogin()
    expect(uni.login).toHaveBeenCalled()
    expect(myRequestMock).toHaveBeenCalled()
    expect(uni.setStorageSync).toHaveBeenCalledWith('user_id', 'mock_user_id')
    expect(uni.reLaunch).toHaveBeenCalledWith({ url: '/pages/home/home' })
  })
})