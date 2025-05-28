<template>
	<view class="learn-container">
		<!-- 顶部导航栏 -->
		<view class="top-nav">
			<image class="back-icon" src="/static/back-arrow.png" @click="backToHome"></image>
			<!-- <text class="nav-title">每日学习</text> -->
			<view class="placeholder-view"></view>
		</view>

		<!-- 单词及进度展示卡片 -->
		<view class="word-progress-card">
			<view class="word-header">
				<text class="word-text">{{ wordData.word }}</text>
				<image class="sound-icon" src="/static/sound-icon.png" @click="playWordSound"></image>
			</view>
			<view class="progress-bar-container">
				<view class="progress-bar-filled" :style="{ width: proficiencyPercentage + '%' }"></view>
			</view>
			<text class="proficiency-text">熟练度: {{ wordData.proficiency }} / {{ def_pro }}</text>
		</view>

		<!-- 选项列表 -->
		<view class="options-grid">
			<view v-for="(option, index) in options" :key="index" class="option-card" :class="optionClass(index)"
				@click="selectOption(index)">
				<text class="option-text">{{ option }}</text>
			</view>
		</view>

		<!-- 底部信息与操作 -->
		<view class="bottom-bar">
			<view class="progress-bar-bottom">
				<view class="progress-bar-filled-bottom" :style="{ width: (completedCount / totalCount) * 100 + '%' }">
				</view>
			</view>
			<text class="completion-info">{{ completedCount }} / {{ totalCount }}</text>
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
				wordData: {
					word_id: 0,
					word: '',
					translations: [],
					phrases: [],
					proficiency: 0,
				},
				def_pro: 0,
				// 选项数组
				options: [],
				// 完成的单词计数器
				completedCount: 0,
				// 要完成的单词数
				totalCount: 0,
				selectedOptionIndex: null,
				isAnswerCorrect: false,
				incorrectOptionIndexes: [], // 改为数组，记录所有错误选项
				soundUrl: '',
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
				}
			});
			this.userId = uni.getStorageSync('user_id');
			// 读取进度
			this.completedCount = uni.getStorageSync('completedCount');
			if (this.completedCount == '') this.completedCount = 0
		},
		
		onShow() {
			console.log('页面加载');
			uni.getStorage({
				key: 'user_id',
				success: (res) => {
					// console.log('ID:' + res.data);
					this.userId = res.data; // 获取用户ID
					// console.log('修改后的userId:', this.userId); // 打印确认
				},
				fail: (err) => {
					console.error('获取用户ID失败:', err);
					uni.showToast({
						title: '获取用户ID失败',
						icon: 'none'
					});
					// 跳转到登录页面
					uni.reLaunch({
						url: '/pages/begin/login'
					});
				}
			});
			this.completedCount = uni.getStorageSync('completedCount');
			if (this.completedCount == '') this.completedCount = 0
			// console.log(this.completedCount)
			//数据更新
			this.getUserData();
			// this.get_progress(); // 之前我们在这里调用，没得
			this.getLearnWord();
		},
		
		onHide() {
			// 页面卸载时的操作
			console.log('页面隐藏');
			// 本地保存进度
			uni.setStorage({
				key: 'completedCount',
				data: this.completedCount
			});
		},
		
		methods: {
			// 返回主页
			backToHome() {
				uni.reLaunch({
					url: '/pages/home/home'
				});
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
			// 初始化选项 
			async initOptions() {
				const correctOption = this.wordData.translations[0].translation;
				const data = {
					user_id: this.userId
				};
				this.wait_options = [correctOption]; // 清空选项数组
				while (this.wait_options.length < 4) {
					await this.getOptions();
				}
				this.options = this.shuffleArray(this.wait_options);
			},

			// 获取选项
			async getOptions() {
				await myRequest({
					url: '/get_option',
					method: 'POST',
					name: '获取选项',
					success: (response) => {
						console.log(response.data)
						if (response.data) {
							this.wait_options.push(response.data.option);
						} else {
							console.error('后端返回的数据结构不符合预期:', response.data);
							uni.showToast({
								title: '获取选项成功，但无法获取选项',
								icon: 'none'
							});
						}
					},
				})
			},

			// 选择选项
			selectOption(index) {
				if (this.options[index] === this.wordData.translations[0].translation) {
					uni.showToast({
						title: '答案正确',
						icon: 'none'
					});
					this.wordData.proficiency++;
					if (this.wordData.proficiency >= this.def_pro) {
						this.completedCount++;
						console.log("this.completedCount++;")
					}
					this.update_progress();
					uni.navigateTo({
						url: `/pages/word/word?word=${encodeURIComponent(this.wordData.word)}
                        &word_id=${encodeURIComponent(this.wordData.word_id)}
                        &totalCount=${encodeURIComponent(this.totalCount)}
                        &completedCount=${encodeURIComponent(this.completedCount)}`
					});
				} else {
					this.wordData.proficiency = 0;
					// 将错误选项添加到数组中，避免重复添加
					if (!this.incorrectOptionIndexes.includes(index)) {
						this.incorrectOptionIndexes.push(index);
					}
					uni.showToast({
						title: '答案错误',
						icon: 'none'
					});
				}
			},
			
			// 打乱数组顺序 
			shuffleArray(array) {
				// console.log('打乱')
				for (let i = array.length - 1; i > 0; i--) {
					const j = Math.floor(Math.random() * (i + 1));
					[array[i], array[j]] = [array[j], array[i]];
				}
				return array;
			},
			
			async getUserData() {
				this.userId = uni.getStorageSync('user_id');
				const data = {
					user_id: this.userId
				};
				await myRequest({
					url: '/get_user_message_by_id',
					method: 'POST',
					data: data,
					name: '获取用户信息',
					success: (response) => {
						this.totalCount = response.data.user_group_word;
						this.def_pro = response.data.user_def_learned;
					},
				})
			},
			
			async getLearnWord() {
				this.userId = uni.getStorageSync('user_id');
				const data = {
					user_id: this.userId
				};
				await myRequest({
					url: '/get_learn_word',
					method: 'POST',
					data: data,
					name: '获取正在学习单词',
					success: (response) => {
						// 将用户信息存储在本地存储中
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
					},
				})
				// 重置错误选项数组
				this.incorrectOptionIndexes = [];
				await this.get_progress();
				await this.initOptions();
				// 自动播放单词发音
				this.playWordSound();
			},
			
			async update_progress() {
				console.log("proficiency: " + this.wordData.proficiency)
				if (isNaN(this.wordData.proficiency)) {
					this.wordData.proficiency = 0;
				}
				const data = {
					user_id: this.userId,
					word_id: this.wordData.word_id,
					proficiency: this.wordData.proficiency
				};
				console.log("data: " + JSON.stringify(data))
				await myRequest({
					url: '/update_word',
					method: 'POST',
					data: data,
					name: '单词更新',
					success: (response) => {
						console.log(response.data.message);
					},
				})
			},
			
			async get_progress() {
				const data = {
					user_id: this.userId,
					word_id: this.wordData.word_id
				}
				await myRequest({
					url: '/get_word_progress',
					method: 'POST',
					data: data,
					name: '单词进度',
					success: (response) => {
						if (response.data) {
							this.wordData.proficiency = response.data.proficiency;
							console.log("proficiency: " + this.wordData.proficiency);
						} else {
							console.error('后端返回的数据结构不符合预期:', response.data);
							uni.showToast({
								title: '请求单词进度成功，但无法获取请求单词进度',
								icon: 'none'
							});
						}
					},
				})
			},
		},
		computed: {
			proficiencyPercentage() {
				if (this.def_pro > 0) {
					return (this.wordData.proficiency / this.def_pro) * 100;
				}
				return 0;
			},
			optionClass() {
				return (index) => {
					return {
						'selected': this.selectedOptionIndex === index,
						'correct': this.isAnswerCorrect && this.selectedOptionIndex === index,
						'incorrect': !this.isAnswerCorrect && this.selectedOptionIndex === index,
						'incorrect-selected': this.incorrectOptionIndexes.includes(index) // 检查索引是否在错误选项数组中
					};
				};
			}
		}
	};
</script>

<style scoped>
	.learn-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		min-height: 100vh;
		/* background-color: #f0f2f5; */
		/* background: linear-gradient(135deg, #f8defa 0%, #b7b7ff 100%); /* 清新活泼的渐变 */
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
		/* justify-content: space-between; */
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
		margin-left: 30vw;
		margin-top: 3vh;
		font-size: 18px;
		font-weight: 600;
		color: #333333;
	}

	.placeholder-view {
		width: 24px;
	}

	.word-progress-card {
		/* background-color: #ffffff; */
		background-color: rgba(255, 255, 255, 0.6);
		padding: 25px 20px;
		border-radius: 12px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
		text-align: center;
		margin-top: 120px;
		margin-bottom: 30px;
		width: 75%;
		max-width: 500px;
	}

	.word-header {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.word-text {
		font-size: 32px;
		font-weight: bold;
		color: #007aff;
		/* 主题蓝色 */
	}

	.sound-icon {
		width: 24px;
		height: 24px;
		margin-left: 10px;
		cursor: pointer;
	}

	.progress-bar-container {
		width: 100%;
		height: 15px;
		/* 增加高度 */
		background-color: #e9ecef;
		border-radius: 5px;
		overflow: hidden;
		margin-bottom: 8px;
		margin-top: 10px;
	}

	.progress-bar-filled {
		height: 100%;
		background-color: #007aff;
		border-radius: 5px;
		transition: width 0.3s ease;
	}

	.proficiency-text {
		font-size: 14px;
		color: #555555;
	}

	.options-grid {
		display: grid;
		grid-template-columns: 1fr;
		/* 修改为每行一个选项 */
		gap: 15px;
		width: 85%;
		max-width: 500px;
		margin-bottom: 20px;
		margin-top: 30px;
	}

	.option-card {
		/* background-color: #ffffff; */
		background-color: rgba(255, 255, 255, 0.6);
		padding: 20px 15px;
		border-radius: 10px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
		text-align: center;
		cursor: pointer;
		transition: all 0.2s ease-in-out;
		border: 2px solid transparent;
		/* For selection border */
	}

	.option-card:hover {
		transform: translateY(-3px);
		box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
	}

	.option-card.selected {
		border-color: #007aff;
		box-shadow: 0 0 0 2px rgba(0, 123, 255, .25);
	}

	.option-card.correct {
		background-color: #d4edda;
		/* Light green for correct */
		border-color: #c3e6cb;
	}

	.option-card.incorrect {
		background-color: #f8d7da;
		/* Light red for incorrect */
		border-color: #f5c6cb;
	}

	.option-card.incorrect-selected {
		background-color: #f8d7da;
		/* Light red for incorrect */
		border-color: #f5c6cb;
		border-width: 2px;
		box-shadow: 0 0 8px rgba(220, 53, 69, 0.5);
		/* 添加红色阴影效果 */
	}

	.option-text {
		font-size: 16px;
		color: #333333;
	}

	.bottom-bar {
		position: fixed;
		bottom: 0;
		left: 0;
		width: 100%;
		/* padding: 15px 15px; */
		background-color: rgba(255, 255, 255, 0.0);
		box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
		display: flex;
		/* justify-content: center; */
		align-items: center;
		z-index: 1000;
		height: 50px;
		/* 增加高度以适应进度条 */
	}

	.progress-bar-bottom {
		width: 60vw;
		height: 15px;
		/* 增加高度 */
		background-color: rgba(205, 198, 235, 0.6);
		border-radius: 10px;
		box-shadow: 0px 0px 4px rgba(0, 0, 0, 0.2);
		overflow: hidden;
		margin-bottom: 8px;
		margin-left: 10vw;
	}

	.progress-bar-filled-bottom {
		height: 100%;
		background-color: #9bccff;
		border-radius: 5px;
		transition: width 0.3s ease;
	}

	.completion-info {
		margin-left: 5vw;
		/* 贴着进度条5vw */
		font-size: 16px;
		margin-bottom: 8px;
		color: #555555;
		font-weight: 500;
	}
</style>