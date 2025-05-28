<template>
	<view class="login-page-root">
		<view class="branding-section">
			<!-- <image class="app-logo-large" src="/static/app-logo-color.png" mode="aspectFit"></image> -->
			<text class="app-name-text">欢迎回来\n</text>
			<text class="app-subtitle-text">登录以继续您的学习之旅</text>
		</view>

		<view class="login-form-card">
			<view class="form-input-wrapper">
				<image class="input-icon" src="/static/user-icon-gray.png"></image>
				<input class="styled-input-field" type="text" v-model="username" placeholder="请输入账号名" />
			</view>
			<view class="form-input-wrapper">
				<image class="input-icon" src="/static/lock-icon-gray.png"></image>
				<input class="styled-input-field" type="password" v-model="password" placeholder="请输入密码" />
			</view>
			<button class="main-login-button" @click="login">立即登录</button>
			<view class="alternative-actions">
				<text class="action-link-text" @click="goToForgetPassword">忘记密码?</text>
				<text class="action-link-text" @click="goToRegister">创建账户</text>
			</view>
		</view>

		<view class="third-party-login-section">
			<text class="divider-text">或使用其他方式登录</text>
			<view class="social-buttons-container">
				<button class="social-button wechat" @click="wechatLogin">
					<image src="/static/wechat-logo.png"></image>
				</button>
				<button v-if="showPhoneLogin" class="social-button wechat" @click="phoneLogin">
					<image src="/static/smartphone.png"></image>
				</button>
			</view>
		</view>
	</view>
</template>

<script>
	import {
		myRequest
	} from '@/utils/util.js';

	export default {
		data() {
			return {
				username: '',
				nickname: '',
				password: '',
				showPhoneLogin: false
			};
		},
		onShow() {
			uni.getStorage({
				key: 'user_id',
				success: (res) => {
					console.log("获取到userId，跳转到主页")
					uni.reLaunch({
						url: '/pages/home/home'
					});
				},
				fail() {

				}
			});

			uni.getProvider({
				service: 'oauth',
				success: (res) => {
					console.log(res.provider);
					this.showPhoneLogin = res.provider.includes('univerify');

					// uni.preLogin({
					// 	provider: 'univerify',
					// 	success() { //预登录成功
					// 		console.log("预登录成功")
					// 	},
					// 	fail(err) { // 预登录失败
					// 		console.log(JSON.stringify(err))
					// 	}
					// })
				}
			});
		},
		methods: {
			async login() {
				// 校验逻辑
				if (!this.if_password_vaild() || !this.if_username_valid()) {
					console.log('注册失败');
					var content = '';
					if (!this.if_password_same()) {
						content = content + '密码不能为空\r\n';
					}
					if (!this.if_username_valid()) {
						content = content + '用户名不能为空\r\n';
					}

					uni.showToast({
						title: content,
						icon: 'none'
					});
					return;
				}
				// 登录逻辑
				console.log('登录');
				console.log('账号:', this.username);
				console.log('密码:', this.password);
				const data = {
					username: this.username,
					password: this.password
				};
				await myRequest({
					url: '/login',
					method: 'POST',
					data: data,
					name: '登录',
					success: (response) => {
						uni.showToast({
							title: '登入成功',
							icon: 'success'
						});
						// 将用户信息存储在本地存储中
						// 检查 response.data 的结构
						if (response.data) {
							// 将用户信息存储在本地存储中
							uni.setStorageSync('user_id', response.data.user_id);
							console.log('登录成功，用户信息已存储:', response.data.user_id);
						} else {
							console.error('后端返回的数据结构不符合预期:', response.data);
							uni.showToast({
								title: '登录成功，但无法获取用户信息',
								icon: 'none'
							});
						}
						uni.reLaunch({
							url: '/pages/home/home'
						});
					},
				});
			},
			async wechatLogin() {
				console.log("wechatLogin")
				uni.login({
					provider: 'weixin',
					success: async (loginRes) => {
						console.log("11111111111111111111")
						console.log(JSON.stringify(loginRes))
						// console.log(loginRes.authResult.openid)
						// 登录成功
						
						uni.showToast({
							title: '登入成功',
							icon: 'success'
						});
						
						await new Promise((resolve, reject) => {
							uni.getUserInfo({
								provider: 'weixin',
								success: (info) => {
									console.log(JSON.stringify(info.userInfo))
									console.log(info.userInfo.nickName);
									this.nickname = info.userInfo.nickName;
									resolve(); // 解析 Promise，表示 success 回调执行完成
								},
								fail: (err) => {
									reject(err); // 拒绝 Promise，处理失败情况
								}
							});
						});
						if (loginRes.authResult === undefined) {
							const data = {
								code: loginRes.code
							}
							myRequest({
								url: "/get_openid",
								data: data,
								name: "获取openid",
								method: "POST",
								success: async (res) => {
									console.log(JSON.stringify(res))
									console.log("------------------------")
									console.log(res.data.openid)
									const data = {
										username: res.data.openid,
									};
									await myRequest({
										url: '/get_id_by_username',
										method: 'POST',
										data: data,
										name: '尝试获取用户id',
										success: async (response) => {
											if (response.statusCode == 201) {
												uni.setStorageSync('user_id',
													response
													.data.user_id);
												console.log('登录成功，用户信息已存储:',
													response
													.data.user_id);
											} else {
												// 用户不存在，注册用户
												const regdata = {
													username: res.data.openid,
													nickname: this.nickname,
													password: res.data.openid
												};
												console.log(regdata)
												await myRequest({
													url: '/users',
													method: 'POST',
													data: regdata,
													name: '注册',
													success: (
														regresponse
														) => {
														uni.setStorageSync(
															'user_id',
															regresponse
															.data
															.user
															.id);
														console.log(
															'登录成功，用户信息已存储:',
															regresponse
															.data
															.user
															.id);
													},
												})
											}
											uni.reLaunch({
												url: '/pages/home/home'
											});
										},
									});
								}
							})
						} else {
							const data = {
								username: loginRes.authResult.openid
							}
							await myRequest({
								url: '/get_id_by_username',
								method: 'POST',
								data: data,
								name: '尝试获取用户id',
								success: async (response) => {
									if (response.statusCode == 201) {
										uni.setStorageSync('user_id', response
											.data.user_id);
										console.log('登录成功，用户信息已存储:', response
											.data.user_id);
									} else {
										// 用户不存在，注册用户
										const regdata = {
											username: loginRes.authResult.openid,
											nickname: this.nickname,
											password: loginRes.authResult.openid
										};
										console.log(regdata)
										await myRequest({
											url: '/users',
											method: 'POST',
											data: regdata,
											name: '注册',
											success: (regresponse) => {
												uni.setStorageSync('user_id',
													regresponse.data.user.id);
												console.log('登录成功，用户信息已存储:',
													regresponse.data.user.id);
											},
										})
									}
									uni.reLaunch({
										url: '/pages/home/home'
									});
								},
							});
						}
					},
					fail: function(err) {
						// 登录授权失败
						console.log(JSON.stringify(err))
					}
				});
			},
			async phoneLogin() {
				console.log("phoneLogin")
				uni.login({
					provider: 'univerify',
					univerifyStyle: { // 自定义登录框样式
						//参考`univerifyStyle 数据结构`
					},
					success: async(res) => { // 登录成功
						console.log(res.authResult); // {openid:'登录授权唯一标识',access_token:'接口返回的 token'}
						const data = {
							username: res.authResult.openid,
						};
						await myRequest({
							url: '/get_id_by_username',
							method: 'POST',
							data: data,
							name: '尝试获取用户id',
							success: async (response) => {
								if (response.statusCode == 201) {
									uni.setStorageSync('user_id',response.data.user_id);
									console.log('登录成功，用户信息已存储:',response.data.user_id);
								} else {
									// 用户不存在，注册用户
									const regdata = {
										username: res.authResult.openid,
										nickname: "手机用户请及时更改昵称",
										password: res.authResult.openid
									};
									console.log(regdata)
									await myRequest({
										url: '/users',
										method: 'POST',
										data: regdata,
										name: '注册',
										success: (
											regresponse) => {
											uni.setStorageSync('user_id',regresponse.data.user.id);
											console.log('登录成功，用户信息已存储:',regresponse.data.user.id);
										},
									})
								}
								uni.reLaunch({
									url: '/pages/home/home'
								});
							},
						});

						uni.closeAuthView()
					},
					fail(res) { // 登录失败
						console.log(res.errCode)
						console.log(res.errMsg)
					}
				})

			},
			goToForgetPassword() {
				// 跳转到忘记密码页面
				uni.navigateTo({
					url: '/pages/begin/forgetPassword'
				});
			},
			goToRegister() {
				// 跳转到注册页面
				uni.navigateTo({
					url: '/pages/begin/register'
				});
			},
			if_username_valid() {
				// 检查用户名是否有效
				return this.username !== '';
			},
			if_password_vaild() {
				// 检查密码是否有效
				return this.password !== '';
			},
		}
	};
</script>

<style scoped>
	.login-page-root {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		/* 上下居中主要内容 */
		min-height: 100vh;
		/* background: linear-gradient(135deg, #6DD5FA 0%, #FF758C 100%); */
		background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);

		/* 清新活泼的渐变 */
		padding: 20px;
		box-sizing: border-box;
	}

	.branding-section {
		text-align: center;
		margin-bottom: 40px;
		color: #ffffff;
	}

	.app-logo-large {
		width: 100px;
		height: 100px;
		margin-bottom: 15px;
	}

	.app-name-text {
		font-size: 28px;
		font-weight: bold;
		margin-bottom: 8px;
		text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
	}

	.app-subtitle-text {
		font-size: 16px;
		opacity: 0.9;
	}

	.login-form-card {
		width: 80%;
		max-width: 400px;
		background-color: rgba(255, 255, 255, 0.55);
		/* 轻微透明增加质感 */
		padding: 30px 25px;
		border-radius: 15px;
		box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
	}

	.form-input-wrapper {
		display: flex;
		align-items: center;
		background-color: #f7f7f7;
		border-radius: 10px;
		padding: 0 15px;
		margin-bottom: 20px;
		height: 50px;
		border: 1px solid #e0e0e0;
	}

	.form-input-wrapper:focus-within {
		border-color: #FF758C;
		/* 渐变色中的一个强调色 */
		box-shadow: 0 0 0 2px rgba(255, 117, 140, 0.2);
	}

	.input-icon {
		width: 20px;
		height: 20px;
		margin-right: 10px;
		opacity: 0.6;
	}

	.styled-input-field {
		flex-grow: 1;
		font-size: 16px;
		color: #333;
		height: 100%;
		background-color: transparent;
		border: none;
	}

	.main-login-button {
		width: 100%;
		height: 50px;
		line-height: 50px;
		margin-bottom: 20px;
		background: linear-gradient(to right, #89f7fe, #66a6ff);
		/* 与背景呼应的渐变 */
		color: white;
		font-size: 18px;
		font-weight: bold;
		border: none;
		border-radius: 10px;
		box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
		transition: transform 0.2s ease, box-shadow 0.2s ease;
	}

	.main-login-button:hover {
		transform: translateY(-2px);
		box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
	}

	.alternative-actions {
		display: flex;
		justify-content: space-between;
		margin-top: 15px;
	}

	.action-link-text {
		font-size: 14px;
		color: #FF758C;
		/* 使用主题强调色 */
		cursor: pointer;
		font-weight: 500;
	}

	.action-link-text:hover {
		text-decoration: underline;
	}

	/* 可选的第三方登录样式，默认注释掉 */

	.third-party-login-section {
		width: 100%;
		max-width: 400px;
		text-align: center;
		margin-top: 30px;
	}

	.divider-text {
		font-size: 14px;
		color: #ffffff;
		opacity: 0.8;
		margin-bottom: 15px;
		position: relative;
		display: inline-block;
	}

	.divider-text::before,
	.divider-text::after {
		content: '';
		position: absolute;
		top: 50%;
		width: 60px;
		height: 1px;
		background-color: rgba(255, 255, 255, 0.5);
	}

	.divider-text::before {
		right: 100%;
		margin-right: 15px;
	}

	.divider-text::after {
		left: 100%;
		margin-left: 15px;
	}

	.social-buttons-container {
		display: flex;
		justify-content: center;
		gap: 20px;
	}

	.social-button {
		background-color: rgba(255, 255, 255, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.3);
		color: white;
		padding: 3px 3px;
		border-radius: 8px;
		font-size: 14px;
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.social-button image {
		width: 40px;
		height: 40px;
	}
</style>