<template>
	<view class="word-detail-container">
		<!-- 顶部导航栏 -->
		<view class="top-nav">
			<image class="back-icon" src="/static/back-arrow.png" @click="goBack"></image>
			<!-- <text class="nav-title">单词详情</text> -->
			<view class="placeholder-view"></view>
		</view>

		<!-- 单词显示卡片 -->
		<view class="word-display-card">
			<view class="word-header">
				<text class="word-text">{{ wordData.word }}</text>
				<image class="sound-icon" src="/static/sound-icon.png" @click="playWordSound"></image>
			</view>
		</view>

		<!-- 释义卡片 -->
		<view class="info-card">
			<view class="card-header">
				<text class="card-title">释义</text>
			</view>
			<scroll-view scroll-y class="translations-scroll">
				<view v-for="(trans, index) in wordData.translations" :key="index" class="translation-item">
					<text class="translation-type">{{ trans.type }}</text>
					<text class="translation-text">{{ trans.translation }}</text>
				</view>
			</scroll-view>
		</view>

		<!-- 短语卡片 -->
		<view class="info-card">
			<view class="card-header">
				<text class="card-title">相关短语</text>
			</view>
			<scroll-view scroll-y class="phrases-scroll">
				<view v-for="(phrase, index) in wordData.phrases" :key="index" class="phrase-item">
					<text class="phrase-en">{{ phrase.phrase }}</text>
					<text class="phrase-cn">{{ phrase.translation }}</text>
				</view>
			</scroll-view>
		</view>

		<!-- 底部操作区域 -->
		<view class="bottom-actions">
			<button @click="goBack" class="action-button">继续学习</button>
		</view>
	</view>
</template>

<script>
	import {
		myRequest
	} from '@/utils/util.js'; // 引入请求函数
	export default {
		data() {
			return {
				wordData: {
					word_id: 0,
					word: '',
					translations: [],
					phrases: [],
				},
				completedCount: 0,
				totalCount: 0,
				def_pro: 0,
				soundUrl: '',
			};
		},
		onLoad(options) {
			// 页面加载时获取数据
			console.log('页面加载');
			uni.getStorage({
				key: 'user_id',
				success: (res) => {
					console.log('ID:' + res.data);
					this.userId = res.data; // 获取用户ID
					console.log('修改后的userId:', this.userId); // 打印确认
				},
				fail: (err) => {
					console.error('获取用户ID失败:', err);
					uni.showToast({
						title: '获取用户ID失败',
						icon: 'none'
					});
					// 跳转到登录页面
					uni.navigateTo({
						url: '/pages/login/login'
					});
				}
			});
			this.userId = uni.getStorageSync('user_id');
			this.wordData.word_id = parseInt(options.word_id);
			this.completedCount = parseInt(options.completedCount);
			this.totalCount = parseInt(options.totalCount);
			this.wordData.proficiency = parseInt(options.proficiency);
			this.def_pro = parseInt(options.def_pro);

			this.updata();
		},
		onShow() {
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
		},
		methods: {
			async updata() {
				const data = {
					word_id: this.wordData.word_id,
				};
				await myRequest({
					url: '/get_word_by_id',
					method: 'POST',
					data: data,
					name: '单词',
					success: (response) => {
						this.wordData = {
							word_id: response.data.word_id,
							word: response.data.word,
							translations: response.data.translations.map((translation) => ({
								translation: translation.translation,
								type: translation.type
							})),
							phrases: response.data.phrases.map((phrase) => ({
								phrase: phrase.phrase,
								translation: phrase.translation
							}))
						};
						// 自动播放单词发音
						this.playWordSound();
					},
				})
			},
			goBack() {
				if (this.completedCount < this.totalCount || this.totalCount <= 0) {
					// 返回上一个页面，并传递参数 refresh=true
					uni.navigateBack({
						delta: 1
					});
				} else {
					// 返回首页
					uni.navigateTo({
						url: '/pages/word/completed'
					});
				}

			},
			show_translations() {
				// 显示单词释义
				// 遍历 translations 数组，拼接释义
				let translations = this.wordData.translations.map((item) => {
					return `${item.type}: ${item.translation}`;
				});
				return translations.join('\n');
			},
			show_phases() {
				// 显示短语释义
				// 遍历 phrases 数组，拼接前五个释义
				let phrases = this.wordData.phrases.map((item) => {
					return `${item.phrase}: ${item.translation}`;
				});
				return phrases.slice(0, 5).join('\n');

			},
			// 播放单词发音
			playWordSound() {
				if (this.wordData.word) {
					this.soundUrl = `https://dict.youdao.com/dictvoice?type=0&audio=${this.wordData.word}`;
					const innerAudioContext = uni.createInnerAudioContext();
					innerAudioContext.src = this.soundUrl;
					innerAudioContext.autoplay = true;
					innerAudioContext.onError((res) => {
						console.error('音频播放失败：', res.errMsg);
						uni.showToast({
							title: '音频播放失败',
							icon: 'none'
						});
					});
				}
			},
		}
	};
</script>

<style scoped>
	.word-detail-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		min-height: 100vh;
		/* background-color: #f0f2f5; */
		background: linear-gradient(135deg, #f8defa 0%, #e6edff 100%);
		/* 清新活泼的渐变 */
		box-sizing: border-box;
	}

	.top-nav {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 15px 20px;
		/* background-color: #ffffff; */
		background-color: rgba(255, 255, 255, 0.0);
		/* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); */
		z-index: 1000;
		height: 50px;
	}

	.back-icon {
		width: 24px;
		margin-top: 3vh;
		height: 24px;
		cursor: pointer;
	}

	.nav-title {
		margin-top: 3vh;
		font-size: 18px;
		font-weight: 600;
		color: #333333;
	}

	.placeholder-view {
		width: 24px;
	}

	.word-display-card {
		/* background-color: #ffffff; */
		background-color: rgba(255, 255, 255, 0.6);
		padding: 25px 20px;
		border-radius: 12px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
		text-align: center;
		margin-top: 120px;
		margin-bottom: 20px;
		width: 70%;
		max-width: 500px;
	}

	.word-header {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.word-text {
		font-size: 30px;
		font-weight: bold;
		color: #007aff;
	}

	.sound-icon {
		width: 24px;
		height: 24px;
		cursor: pointer;
		margin-left: 10px;
	}

	.info-card {
		/* background-color: #ffffff; */
		background-color: rgba(255, 255, 255, 0.6);
		border-radius: 12px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
		margin-bottom: 20px;
		width: 90%;
		max-width: 500px;
		overflow: hidden;
		/* 确保子元素不会溢出圆角 */
	}

	.card-header {
		padding: 15px 20px;
		/* background-color: #f8f9fa; */
		background-color: rgba(255, 255, 255, 0.6);
		border-bottom: 1px solid #e9ecef;
	}

	.card-title {
		font-size: 18px;
		font-weight: 600;
		color: #333333;
	}

	.translations-scroll,
	.phrases-scroll {
		max-height: 200px;
		/* 限制滚动区域高度 */
		padding: 15px 20px;
	}

	.translation-item,
	.phrase-item {
		margin-bottom: 12px;
	}

	.translation-item:last-child,
	.phrase-item:last-child {
		margin-bottom: 0;
	}

	.translation-type {
		font-size: 14px;
		color: #888888;
		margin-right: 8px;
		font-style: italic;
	}

	.translation-text {
		font-size: 16px;
		color: #333333;
		line-height: 1.5;
	}

	.phrase-en {
		font-size: 16px;
		color: #007aff;
		font-weight: 500;
		display: block;
		/* 让英文和中文释义各占一行 */
		margin-bottom: 4px;
	}

	.phrase-cn {
		font-size: 14px;
		color: #555555;
		line-height: 1.5;
	}

	.bottom-actions {
		position: fixed;
		bottom: 0;
		left: 0;
		width: 100%;
		/* padding: 15px 15px; */
		height: 70px;
		/* 增加高度以适应进度条 */
		/* background-color: #ffffff; */
		background-color: rgba(255, 255, 255, 0.0);
		box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
		display: flex;
		justify-content: center;
		z-index: 1000;
	}

	.action-button {
		width: 70%;
		max-width: 300px;
		height: 45px;
		line-height: 45px;
		/* 确保文字垂直居中 */
		background-color: #007aff;
		color: #ffffff;
		font-size: 16px;
		font-weight: 500;
		border: none;
		/* margin-left: 10vw; */
		margin-top: 10px;
		border-radius: 8px;
		text-align: center;
		transition: background-color 0.3s ease;
	}

	.action-button:hover {
		background-color: #0056b3;
	}
</style>