<template>
	<view class="user-profile-page">
		<!-- 顶部背景和返回按钮 -->
		<view class="header-background">
			<image class="back-arrow-icon" src="/static/back-arrow.png" @click="backToHome"></image>
			<!-- <text class="page-header-title">个人中心</text> -->
		</view>

		<!-- 用户信息卡片 -->
		<view class="user-info-card">
			<view class="avatar-section" @click="changeAvatar">
				<image class="avatar-image" :src="avatarUrl || '/static/default-avatar.png'" mode="aspectFill"></image>
			</view>
			<text class="username-text" @click="showModal('nickname')">{{ nickname }}</text>
			<!-- 可以加入用户ID或其他简短信息 -->
			<text class="user-id-text">USER NAME: {{ username || '未登录' }}</text>
			<text class="user-id-text">ID: {{ userId || '未登录' }}</text>
		</view>

		<!-- 设置列表 -->
		<view class="settings-list">
			<view class="setting-item" @click="showModal('book')">
				<view class="item-content">
					<image class="item-icon" src="/static/book-icon.png"></image>
					<text class="item-label">当前词书</text>
				</view>
				<text class="item-value">{{ bookName || '暂未设置' }}</text>
				<image class="arrow-right-icon" src="/static/arrow-right.png"></image>
			</view>
			<view class="setting-item">
				<view class="item-content">
					<image class="item-icon" src="/static/stats-icon.png"></image>
					<text class="item-label">学习统计</text>
				</view>
			</view>
			<view class="sub-setting-item">
				<text class="sub-item-label">总词汇量:</text>
				<text class="sub-item-value">{{ tolearnNum }}</text>
			</view>
			<!-- <view class="sub-setting-item">
                <text class="sub-item-label">学习中:</text>
                <text class="sub-item-value">{{ studiedNum }}</text>
            </view> -->
			<view class="sub-setting-item">
				<text class="sub-item-label">已掌握:</text>
				<text class="sub-item-value">{{ masteredNum }}</text>
			</view>

			<view class="setting-item" @click="showModal('wordsPerGroup')">
				<view class="item-content">
					<image class="item-icon" src="/static/settings-icon.png"></image>
					<text class="item-label">每组单词数</text>
				</view>
				<text class="item-value">{{ wordsPerGroup }}</text>
				<image class="arrow-right-icon" src="/static/arrow-right.png"></image>
			</view>
			<view class="setting-item" @click="showModal('proficiency')">
				<view class="item-content">
					<image class="item-icon" src="/static/target-icon.png"></image>
					<text class="item-label">掌握熟练度</text>
				</view>
				<text class="item-value">{{ proficiency }}</text>
				<image class="arrow-right-icon" src="/static/arrow-right.png"></image>
			</view>
		</view>

		<!-- 退出登录按钮 -->
		<view class="logout-button-container">
			<button class="logout-button" @click="logout">退出登录</button>
		</view>

		<!-- 输入模态框 -->
		<view v-if="showInput" class="custom-modal-overlay">
			<view class="custom-modal-content">
				<text class="modal-title">{{ inputTitle }}</text>
				<input class="modal-input-field" type="text" v-model="inputValue" :placeholder="请输入"
					style="pointer-events: auto;" />
				<view class="modal-actions">
					<button class="modal-button cancel" @click="cancelInput">取消</button>
					<button class="modal-button confirm" @click="confirmInput">确定</button>
				</view>
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
				userId: null,
				username: '用户名',
				nickname: '昵称',
				bookName: 'CET4',
				tolearnNum: 200,
				studiedNum: 50,
				masteredNum: 30,
				wordsPerGroup: 10,
				proficiency: '0',
				showInput: false,
				inputTitle: '',
				inputValue: '',
				inputKey: '',
				avatarUrl: '',
			};
		},
		onLoad() {
			// 页面加载时获取数据
			console.log('页面加载');
			uni.getStorage({
				key: 'user_id',
				success: (res) => {
					console.log('ID:' + res.data);
					this.userId = res.data; // 获取用户ID
					console.log('修改后的userId:', this.userId); // 打印确认
				},
				fail() {
					console.log("没有获取到userId，跳转到登录页面")
					uni.reLaunch({
						url: '/pages/begin/login'
					});
				}
			});
			//数据更新
			this.userId = uni.getStorageSync('user_id');
			this.getUserData();

		},
		onShow() {
			uni.getStorage({
				key: 'user_id',
				success: (res) => {
					// console.log('ID:' + res.data);
					this.userId = res.data; // 获取用户ID
					// console.log('修改后的userId:', this.userId); // 打印确认
				},
				fail() {
					console.log("没有获取到userId，跳转到登录页面")
					uni.reLaunch({
						url: '/pages/begin/login'
					});
				}
			});
		},
		onUnload() {
			// 清除数据或执行其他操作
			console.log('页面卸载');
		},
		methods: {
			showModal(key) {
				this.showInput = true;
				this.inputKey = key;
				switch (key) {
					case 'nickname':
						this.inputTitle = '更改昵称';
						this.inputValue = this.nickname;
						break;
					case 'book':
						this.inputTitle = '更改单词书';
						this.inputValue = this.bookName;
						break;
					case 'wordsPerGroup':
						this.inputTitle = '设置每组单词数量';
						this.inputValue = this.wordsPerGroup.toString();
						break;
					case 'proficiency':
						this.inputTitle = '设置熟练度';
						this.inputValue = this.proficiency;
						break;
					default:
						break;
				}

			},
			async confirmInput() {
				console.log("Click Confirm")
				console.log(this.inputKey)
				console.log(this.inputValue)
				if (this.inputKey) {
					switch (this.inputKey) {
						case 'wordsPerGroup':
							this.wordsPerGroup = parseInt(this.inputValue);
							break;
						case 'proficiency':
							this.proficiency = this.inputValue;
							break;
						case 'nickname':
							this.nickname = this.inputValue;
							break;
						case 'book':
							this.bookName = this.inputValue;
							break;
						default:
							break;
					}
					await this.upDate();
					await this.getUserData();
				}
				this.showInput = false;
			},
			cancelInput() {
				this.showInput = false;
			},
			backToHome() {
				// 返回主页的逻辑
				uni.navigateTo({
					url: '/pages/home/home'
				});
			},
			async getUserData() {
				const data = {
					user_id: this.userId
				};
				await myRequest({
					url: '/get_user_message_by_id',
					method: 'POST',
					data: data,
					name: '获取用户信息',
					success: (response) => {
						if (response.data) {
							// 将用户信息存储在本地存储中
							this.username = response.data.username;
							this.nickname = response.data.nickname;
							this.studiedNum = response.data.learn_num;
							this.masteredNum = response.data.learned_num;
							this.wordsPerGroup = response.data.user_group_word;
							this.proficiency = response.data.user_def_learned;
							this.tolearnNum = response.data.word_num;
						} else {
							console.error('后端返回的数据结构不符合预期:', response.data);
							uni.showToast({
								title: '获取用户信息成功，但无法获取用户信息',
								icon: 'none'
							});
						}
					},
				})
			},
			async upDate() {
				const data = {
					user_id: this.userId,
					nickname: this.nickname,
					group_word: this.wordsPerGroup,
					def_learned: this.proficiency,
				};
				console.log('userId:', this.userId);
				await myRequest({
					url: '/update_message',
					method: 'POST',
					data: data,
					name: '登录',
					success: (response) => {
						uni.showToast({
							title: '更新成功',
							icon: 'success'
						});
					},
				})
			},
			logout() {
				// 清除本地存储的用户信息
				uni.removeStorage({
					key: 'user_id',
					success: () => {
						console.log('用户信息已清除');
						// 跳转到登录页面
						uni.reLaunch({
							url: '/pages/begin/login'
						});
					},
					fail: () => {
						console.error('清除用户信息失败');
					}
				});
			}
		}
	};
</script>

<style scoped>
	.user-profile-page {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		/* background-color: #f4f6f8; */
		/* 淡雅的背景色 */
		background: linear-gradient(135deg, #f8defa 0%, #e6edff 100%);
		/* 清新活泼的渐变 */
	}

	.header-background {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		display: flex;
		align-items: center;
		/* justify-content: space-between; */
		padding: 15px 20px;
		/* background-color: #ffffff; */
		background-color: rgba(255, 255, 255, 0.0);
		/* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); */
		z-index: 1000;
		height: 50px;
	}

	.back-arrow-icon {
		width: 24px;
		margin-top: 3vh;
		height: 24px;
		cursor: pointer;
	}

	.page-header-title {
		font-size: 20px;
		font-weight: 600;
	}

	.user-info-card {
		background-color: rgba(255, 255, 255, 0.6);
		border-radius: 15px;
		box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
		margin: 90px 20px 20px;
		/* 向上移动，产生层叠效果 */
		padding: 20px;
		text-align: center;
		position: relative;
		z-index: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.avatar-section {
		margin-bottom: 10px;
	}

	.avatar-image {
		width: 80px;
		height: 80px;
		border-radius: 50%;
		border: 3px solid white;
		/* 头像描边 */
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
		background-color: #e0e0e0;
		/* 默认头像背景 */
	}

	.username-text {
		font-size: 20px;
		font-weight: bold;
		color: #333;
		margin-bottom: 5px;
	}

	.user-id-text {
		font-size: 14px;
		color: #888;
	}

	.settings-list {
		background-color: rgba(255, 255, 255, 0.7);
		border-radius: 10px;
		margin: 0 20px 20px;
		padding: 0 0;
		/* 移除内部padding，由item控制 */
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
	}

	.setting-item,
	.sub-setting-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 15px 20px;
		border-bottom: 1px solid #f0f0f0;
		cursor: pointer;
		transition: background-color 0.2s ease;
	}

	.setting-item:hover {
		background-color: #f9f9f9;
	}

	.setting-item:last-child {
		border-bottom: none;
	}

	.item-content {
		display: flex;
		align-items: center;
	}

	.item-icon {
		width: 22px;
		height: 22px;
		margin-right: 15px;
		opacity: 0.7;
	}

	.item-label {
		font-size: 16px;
		color: #333;
	}

	.item-value {
		font-size: 16px;
		color: #888;
	}

	.arrow-right-icon {
		width: 16px;
		height: 16px;
		opacity: 0.5;
	}

	.sub-setting-item {
		padding-left: 57px;
		/* 与带图标的item对齐 */
		cursor: default;
	}

	.sub-setting-item:hover {
		background-color: transparent;
	}

	.sub-item-label {
		font-size: 12px;
		color: #6f6f6f;
	}

	.sub-item-value {
		font-size: 12px;
		color: #333;
		font-weight: 500;
	}

	.logout-button-container {
		margin: 20px 20px;
	}

	.logout-button {
		width: 90%;
		padding: 12px;
		background-color: rgba(127, 63, 217, 0.3);
		/* 醒目的红色 */
		color: white;
		border: none;
		border-radius: 8px;
		font-size: 16px;
		font-weight: 500;
		cursor: pointer;
		text-align: center;
		box-shadow: 0 2px 5px rgba(255, 77, 79, 0.3);
		transition: background-color 0.2s ease;
	}

	.logout-button:hover {
		background-color: rgba(217, 54, 62, 0.3);
	}

	/* 输入模态框样式 */
	.custom-modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 2000;
		padding: 20px;
		box-sizing: border-box;
	}

	.custom-modal-content {
		background-color: white;
		padding: 25px;
		border-radius: 12px;
		width: 100%;
		max-width: 380px;
		box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
		display: flex;
		flex-direction: column;
	}

	.modal-title {
		font-size: 18px;
		font-weight: 600;
		color: #333;
		margin-bottom: 20px;
		text-align: center;
	}

	.modal-input-field {
		/* width: 100%; */
		height: 50px;
		/* padding: 12px 15px; */
		border: 5px solid #e5e5e6;
		border-radius: 8px;
		font-size: 26px;
		margin-bottom: 25px;
		box-sizing: border-box;
	}

/* 	.modal-input-field:focus {
		border-color: #5A8DFF;
		outline: none;
		box-shadow: 0 0 0 2px rgba(90, 141, 255, 0.2);
	} */

	.modal-actions {
		display: flex;
		justify-content: space-between;
		gap: 15px;
		/* 按钮间距 */
	}

	.modal-button {
		flex: 1;
		/* 让按钮平分宽度 */
		padding: 10px;
		border-radius: 8px;
		font-size: 20px;
		font-weight: 500;
		cursor: pointer;
		transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
		border: 1px solid transparent;
	}

	.modal-button.cancel {
		background-color: #f0f2f5;
		color: #555;
		border-color: #dcdfe6;
	}

	.modal-button.cancel:hover {
		background-color: #e4e7ed;
		border-color: #c0c4cc;
	}

	.modal-button.confirm {
		background-color: #5A8DFF;
		color: white;
	}

	.modal-button.confirm:hover {
		background-color: #4075E8;
	}
</style>