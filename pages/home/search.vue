<template>
	<view class="search-page-container">
		<!-- 顶部导航栏 -->
		<view class="top-nav-bar">
			<image class="nav-back-icon" src="/static/back-arrow.png" @click="backToHome"></image>
			<!-- <text class="nav-page-title">单词搜索</text> -->
			<view class="nav-placeholder"></view> <!-- 占位使标题居中 -->
		</view>

		<!-- 搜索输入区域 -->
		<view class="search-input-area">
			<view class="search-field-wrapper">
				<image class="search-icon-prefix" src="/static/search-icon-gray.png"></image>
				<input class="main-search-input" type="text" v-model="searchQuery" placeholder="请输入要搜索的单词"
					@confirm="search" />
				<image v-if="searchQuery" class="clear-input-icon" src="/static/clear-icon-gray.png"
					@click="clearInput"></image>
			</view>
			<button class="initiate-search-button" @click="search">搜索</button>
		</view>

		<!-- 搜索结果区域 -->
		<scroll-view scroll-y class="search-results-scroll-area">
			<view v-if="isLoading" class="loading-indicator">
				<text>正在搜索中...</text> <!-- 或使用加载动画 -->
			</view>
			<view v-else-if="searchResults.length > 0" class="results-list">
				<view class="result-card-item" v-for="(item, index) in searchResults" :key="index">
					<text class="result-word">{{ item.word }} - {{ item.partOfSpeech }}</text>
					<view v-for="(def, i) in item.definitions" :key="i" class="definition-block">
						<text class="definition-text">{{ i + 1 }}. {{ def.definition }}</text>
						<text v-if="def.example" class="example-text">例句: {{ def.example }}</text>
					</view>
				</view>
			</view>
			<view v-else-if="searchedYet && searchResults.length === 0" class="no-results-found">
				<image class="empty-state-icon" src="/static/empty-search.png" mode="aspectFit"></image>
				<text class="empty-state-text">未找到与 "{{ searchQuery }}" 相关的结果</text>
			</view>
			<view v-else class="initial-empty-state">
				<image class="empty-state-icon" src="/static/search-illustration.png" mode="aspectFit"></image>
				<text class="empty-state-text">输入单词开始搜索吧！</text>
			</view>
		</scroll-view>
	</view>
</template>

<script>
	import {
			myRequest
		} from '@/utils/util.js';
	export default {
		data() {
			return {
				searchQuery: '',
				searchResults: [],
				userId: null, // 确保 userId 在 data 中声明
				isLoading: false,
				searchedYet: false
			};
		},
		onLoad() {
			console.log('页面加载');
			uni.getStorage({
				key: 'user_id',
				success: (res) => {
					this.userId = res.data;
					console.log('ID:' + this.userId);
				},
				fail: () => {
					console.log("未获取到userId，可能需要处理登录");
				}
			});
		},
		onShow() {
			// 如果需要在页面显示时再次检查登录状态或刷新数据，可以在这里处理
			if (!this.userId) {
				uni.getStorage({
					key: 'user_id',
					success: (res) => {
						this.userId = res.data;
					},
					fail: () => {
						console.log("onShow: 没有获取到userId，跳转到登录页面");
						uni.reLaunch({
							url: '/pages/begin/login'
						});
					}
				});
			}
		},
		methods: {
			async search() {
				if (!this.searchQuery.trim()) {
					uni.showToast({
						title: '请输入搜索内容',
						icon: 'none'
					});
					return;
				}
				this.isLoading = true;
				this.searchedYet = true;
				this.searchResults = []; // 清空旧结果
				await myRequest({
					url: 'https://api.dictionaryapi.dev/api/v2/entries/en/' + this.searchQuery.trim(),
					method: 'GET',
					name: '搜索',
					success: (response) => {
						let results = [];
						response.data.forEach(entry => {
							entry.meanings.forEach(meaning => {
								results.push({
									word: entry.word, // 添加单词本身
									partOfSpeech: meaning.partOfSpeech,
									definitions: meaning.definitions.map(def => ({
										definition: def.definition,
										example: def.example
									}))
								});
							});
						});
						this.searchResults = results;
						if (results.length === 0) {
							uni.showToast({
								title: '未找到释义',
								icon: 'none'
							});
						}
					},
				})
				this.isLoading = false;
			},
			clearInput() {
				this.searchQuery = '';
				this.searchResults = [];
				this.searchedYet = false; // 重置搜索状态
			},
			backToHome() {
				console.log('返回首页');
				uni.reLaunch({
					url: '/pages/home/home' // 假设home是tab页
				});
			}
		}
	};
</script>

<style scoped>
	.search-page-container {
		display: flex;
		flex-direction: column;
		height: 100vh;
		/* background-color: #f4f6f8; */
		background: linear-gradient(135deg, #f8defa 0%, #e6edff 100%);
		/* 清新活泼的渐变 */
	}

	.top-nav-bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0 15px;
		/* 调整padding，确保垂直居中 */
		/* background-color: #ffffff; */
		background-color: rgba(255, 255, 255, 0.0);
		/* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); */
		height: 70px;
		box-sizing: border-box;
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		z-index: 1000;
	}

	.nav-back-icon {
		width: 24px;
		margin-top: 3vh;
		height: 24px;
		cursor: pointer;
	}

	.nav-page-title {
		font-size: 18px;
		margin-top: 3vh;
		font-weight: 600;
		color: #333333;
		/* 通过flex: 1和text-align: center实现更可靠的居中 */
		flex: 1;
		text-align: center;
	}

	.nav-placeholder {
		width: 24px;
	}

	.search-input-area {
		display: flex;
		align-items: center;
		padding: 15px;
		margin-top: 80px;
		/* background-color: #ffffff; */
		background-color: rgba(255, 255, 255, 0);
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
		/* margin-top: 50px; */
		position: sticky;
		/* 使搜索栏在滚动时固定在导航栏下方 */
		top: 50px;
		/* 与导航栏高度一致 */
		z-index: 999;
		/* 确保在内容之上 */
	}

	.search-field-wrapper {
		flex-grow: 1;
		display: flex;
		align-items: center;
		background-color: #f0f2f5;
		border-radius: 20px;
		padding: 0 12px;
		height: 40px;
	}

	.search-icon-prefix {
		width: 18px;
		height: 18px;
		margin-right: 8px;
		opacity: 0.6;
	}

	.main-search-input {
		flex-grow: 1;
		font-size: 16px;
		color: #333;
		height: 100%;
		background-color: transparent;
		border: none;
	}

	.main-search-input::placeholder {
		color: #999999;
	}

	.clear-input-icon {
		width: 18px;
		height: 18px;
		cursor: pointer;
		opacity: 0.6;
		margin-left: 8px;
	}

	.initiate-search-button {
		margin-left: 10px;
		padding: 0 20px;
		height: 40px;
		line-height: 40px;
		background-color: #007bff;
		color: white;
		border: none;
		border-radius: 20px;
		font-size: 16px;
		font-weight: 500;
		cursor: pointer;
		transition: background-color 0.2s ease;
	}

	.initiate-search-button:hover {
		background-color: #0056b3;
	}

	.search-results-scroll-area {
		flex-grow: 1;
		padding: 15px;
		overflow-y: auto;
	}

	.loading-indicator,
	.no-results-found,
	.initial-empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		text-align: center;
		padding-top: 50px;
		color: #888888;
	}

	.empty-state-icon {
		width: 100px;
		/* 调整图标大小 */
		height: 100px;
		margin-bottom: 20px;
		opacity: 0.7;
	}

	.empty-state-text {
		font-size: 16px;
	}

	.results-list {
		margin-top: 10%;
		display: flex;
		flex-direction: column;
		gap: 17px;
	}

	.result-card-item {
		/* background-color: #ffffff; */
		background-color: rgba(255, 255, 255, 0.6);
		width: 85%;
		border-radius: 10px;
		padding: 15px;
		box-shadow: 0 3px 10px rgba(0, 0, 0, 0.07);
	}

	.result-word {
		font-size: 18px;
		font-weight: bold;
		color: #007bff;
		margin-bottom: 10px;
		display: block;
	}

	.definition-block {
		margin-bottom: 10px;
	}

	.definition-block:last-child {
		margin-bottom: 0;
	}

	.definition-text {
		font-size: 16px;
		color: #333333;
		line-height: 1.5;
		margin-bottom: 5px;
	}

	.example-text {
		font-size: 14px;
		color: #777777;
		font-style: italic;
	}
</style>