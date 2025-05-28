<template>
	<view class="review-container">
		<!-- 顶部导航栏 -->
		<view class="top-nav">
			<image class="back-icon" src="/static/back-arrow.png" @click="backToHome"></image>
			<!-- <text class="nav-title">单词复习</text> -->
			<view class="placeholder-view"></view> <!-- 用于占位，使标题居中 -->
		</view>

		<!-- 单词卡片 -->
		<view class="word-card">
			<view class="word-header">
				<text class="word-text">{{ wordData.word }}</text>
				<image class="sound-icon" src="/static/sound-icon.png" @click="playWordSound"></image>
			</view>
		</view>

		<!-- 选项列表 -->
		<view class="options-grid">
			<view v-for="(option, index) in options" :key="index" class="option-card" :class="optionClass(index)"
				@click="selectOption(index)">
				<text class="option-text">{{ option }}</text>
			</view>
		</view>

		<!-- 底部信息 -->
		<view class="bottom-info">
			<text class="progress-text">未复习单词数：{{ totalCount }}</text>
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
					word: 'aaaa',
					translations: [],
					phrases: [],
					proficiency: 0,
				},
				// 选项数组
				options: [],
				// 完成的单词计数器
				completedCount: 0,
				// 要完成的单词数
				totalCount: 0,
				selectedOptionIndex: null,
				isAnswerCorrect: false,
				incorrectOptionIndexes: [], // 记录所有错误选项
				attempts: 0,
				wait_options: [],
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
				fail() {
					console.log("没有获取到userId，跳转到登录页面")
					uni.reLaunch({
						url: '/pages/begin/login'
					});
				}
			});
			this.get_totalCount();
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

			// 打乱数组顺序
			shuffleArray(array) {
				for (let i = array.length - 1; i > 0; i--) {
					const j = Math.floor(Math.random() * (i + 1));
					[array[i], array[j]] = [array[j], array[i]];
				}
				return array;
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
					}
					// 更新progress到后端
					this.update_progress();
					// 跳转到完整释义页面
					uni.navigateTo({
						url: `/pages/word/word?word=${encodeURIComponent(this.wordData.word)}
                        &word_id=${encodeURIComponent(this.wordData.word_id)}
                        &totalCount=${encodeURIComponent(this.totalCount)}
                        &completedCount=${encodeURIComponent(this.completedCount)}`
					});
				} else {
					if (!this.incorrectOptionIndexes.includes(index)) {
						this.incorrectOptionIndexes.push(index);
					}
					uni.showToast({
						title: '答案错误',
						icon: 'none'
					});
					this.back_to_learning();
				}
			},
			async getLearnWord() {
				const data = {
					user_id: this.userId
				};
				await myRequest({
					url: '/get_reviews_word',
					method: 'POST',
					data: data,
					name: '获取复习单词',
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
					},
				})
				// 重置错误选项数组
				this.incorrectOptionIndexes = [];
				await this.initOptions();
				// 自动播放单词发音
				this.playWordSound();
			},
			// 更新单词
			async updateWord() {
				await this.getLearnWord();
				// this.initOptions();
			},
			async get_totalCount() {
				const data = {
					user_id: this.userId
				};
				await myRequest({
					url: '/get_learned_word_num',
					method: 'POST',
					data: data,
					name: '获取复习单词数量',
					success: (response) => {
						this.totalCount = response.data.learned_word_num;
						console.log('获取到的单词数:', this.totalCount);
						if (this.totalCount == 0) {
						    uni.showToast({
						        title: '没有要复习的单词',
						        icon: 'none'
						    });
						    this.backToHome();
						} else this.getLearnWord();
					},
				});

			},
			async update_progress() {
				const data = {
					user_id: this.userId,
					word_id: this.wordData.word_id,
				};
				await myRequest({
					url: '/add_learned_word_to_have_learned',
					method: 'POST',
					data: data,
					name: '更新复习单词',
					success: (response) => {
						console.log(response.data.message)
					},
				});
			},
			async back_to_learning() {
				const data = {
					user_id: this.userId,
					word_id: this.wordData.word_id,
				};
				await myRequest({
					url: '/back_have_learned_to_learning',
					method: 'POST',
					data: data,
					name: '更新复习单词回到学习中',
					success: (response) => {
						console.log(response.data.message)
					},
				});
			}
		},
		computed: {
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
	.review-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		height: 100vh;
		/* background-color: #f0f2f5; */
		/* 淡雅的背景色 */
		background: linear-gradient(135deg, #f8defa 0%, #e6edff 100%);
		/* 清新活泼的渐变 */
	}

	.top-nav {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		display: flex;
		align-items: center;
		/* justify-content: space-between; */
		/* 让标题文本能更好地居中 */
		padding: 15px 20px;
		/* background-color: #ffffff; */
		background-color: rgba(255, 255, 255, 0.0);
		/* 半透明背景 */
		/* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); */
		z-index: 1000;
		height: 50px;
		/* 固定导航栏高度 */
	}

	.back-icon {
		margin-top: 3vh;
		width: 24px;
		height: 24px;
		cursor: pointer;
	}

	.nav-title {
		margin-top: 3vh;
		margin-left: 30vw;
		font-size: 18px;
		font-weight: 600;
		/* 使用数字字重 */
		color: #333333;
	}

	.placeholder-view {
		/* 此元素用于平衡布局，如果标题本身能通过flex居中则可移除 */
		width: 24px;
		/* 与图标宽度一致，帮助对称 */
	}

	.word-card {
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

	.bottom-info {
		position: fixed;
		bottom: 0;
		left: 0;
		width: 100%;
		/* padding: 15px 15px; */
		background-color: rgba(255, 255, 255, 0.0);
		box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
		height: 50px;
		/* 增加高度以适应进度条 */
	}

	.progress-text {
		/* margin-left: 25vw; */
		font-size: 16px;
		color: #555555;
	}
</style>