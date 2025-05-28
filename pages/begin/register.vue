<template>
	<view class="register-page-root">
		<view class="branding-section">
			<!-- <image class="app-logo-large" src="/static/app-logo-color.png" mode="aspectFit"></image> -->
			<text class="app-name-text">创建您的账户\n</text>
			<text class="app-subtitle-text">加入我们，开始学习新旅程</text>
		</view>

		<view class="register-form-card">
			<view class="form-input-wrapper">
				<image class="input-icon" src="/static/user-icon-gray.png"></image>
				<input class="styled-input-field" type="text" v-model="username" placeholder="请输入账号名" />
			</view>
			<view class="form-input-wrapper">
				<image class="input-icon" src="/static/lock-icon-gray.png"></image>
				<input class="styled-input-field" type="password" v-model="password" placeholder="请输入密码" />
			</view>
			<view class="form-input-wrapper">
				<image class="input-icon" src="/static/lock-check-icon-gray.png"></image>
				<input class="styled-input-field" type="password" v-model="password_2" placeholder="请再次输入密码" />
			</view>
			<button class="main-register-button" @click="register">立即注册</button>
			<view class="alternative-actions">
				<text class="action-link-text" @click="goToLogin">已有账户? 直接登录</text>
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
				password: '',
				password_2: ''
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
			});
		},
		methods: {
			async register() {
				// 校验逻辑
				if (!this.if_password_same() || !this.if_username_valid()) {
					console.log('注册失败');
					var content = '';
					if (!this.if_password_same()) {
						content = content + '两次输入的密码不一致\r\n';
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

				// 发起注册请求
				const data = {
					username: this.username,
					nickname: this.username,
					password: this.password
				};
				await myRequest({
					url: '/users',
					method: 'POST',
					data: data,
					name: '注册',
					success: (response) => {
						uni.showToast({
							title: '注册成功',
							icon: 'success'
						});
						// 注册成功后跳转到登录页面
						uni.navigateTo({
							url: '/pages/begin/login'
						});
					},
				})
			},

			if_password_same() {
				if (this.password == this.password_2) {
					return true;
				} else {
					return false;
				}
			},
			if_username_valid() {
				if (this.username == '') {
					console.log('用户名不能为空');
					return false;
				} else {
					return true;
				}
			},
			goToLogin() {
				uni.reLaunch({
					url: '/pages/begin/login'
				});
			},
		}
	};
</script>

<style scoped>
	.register-page-root {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 100vh;
		background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
		padding: 20px;
		box-sizing: border-box;
	}

	.branding-section {
		text-align: center;
		margin-bottom: 30px;
		color: #ffffff;
	}

	.app-logo-large {
		width: 90px;
		height: 90px;
		margin-bottom: 12px;
	}

	.app-name-text {
		font-size: 26px;
		font-weight: bold;
		margin-bottom: 8px;
		text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
	}

	.app-subtitle-text {
		font-size: 15px;
		opacity: 0.9;
	}

	.register-form-card {
		width: 80%;
		max-width: 400px;
		background-color: rgba(255, 255, 255, 0.95);
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
		margin-bottom: 18px;
		height: 50px;
		border: 1px solid #e0e0e0;
	}

	.form-input-wrapper:focus-within {
		border-color: #66a6ff;
		box-shadow: 0 0 0 2px rgba(102, 166, 255, 0.2);
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

	.main-register-button {
		width: 100%;
		height: 50px;
		line-height: 50px;
		margin-top: 10px;
		margin-bottom: 20px;
		background: linear-gradient(to right, #89f7fe, #66a6ff);
		color: white;
		font-size: 18px;
		font-weight: bold;
		border: none;
		border-radius: 10px;
		box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
		transition: transform 0.2s ease, box-shadow 0.2s ease;
	}

	.main-register-button:hover {
		transform: translateY(-2px);
		box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
	}

	.alternative-actions {
		text-align: center;
		margin-top: 15px;
	}

	.action-link-text {
		font-size: 14px;
		color: #66a6ff;
		cursor: pointer;
		font-weight: 500;
	}

	.action-link-text:hover {
		text-decoration: underline;
	}
</style>