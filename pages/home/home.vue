<template>
    <view class="home-page-wrapper">
        <!-- 顶部区域：欢迎语或Logo -->
        <view class="hero-section">
            <!-- <image class="hero-logo" src="/static/app-logo.png" mode="aspectFit"></image> -->
            <text class="welcome-text">开启您的学习之旅</text>
        </view>

        <!-- 功能卡片区域 -->
        <view class="action-cards-container">
            <view class="action-card primary" @click="goToLearn">
                <image class="card-icon" src="/static/learn-icon.png" mode="aspectFit"></image>
                <text class="card-title">每日学习</text>
                <text class="card-description">开始新的单词学习</text>
            </view>
            <view class="action-card secondary" @click="goToReviews">
                <image class="card-icon" src="/static/review-icon.png" mode="aspectFit"></image>
                <text class="card-title">单词复习</text>
                <text class="card-description">巩固已学单词</text>
            </view>
			<view class="action-card secondary" @click="goToReviewszh">
			    <image class="card-icon" src="/static/reviewzh-icon.png" mode="aspectFit"></image>
			    <text class="card-title">汉译英</text>
			    <text class="card-description">巩固已学单词</text>
			</view>
        </view>

        <!-- 底部导航栏 -->
        <view class="bottom-navigation-bar">
            <!-- <view class="nav-item" :class="{'active': activeTab === 'home'}" @click="navigateTo('home')">
                <image class="nav-icon" :src="activeTab === 'home' ? '/static/home-active.png' : '/static/home-inactive.png'"></image>
                <text class="nav-text">首页</text>
            </view> -->
            <view class="nav-item" :class="{'active': activeTab === 'search'}" @click="goToSearch">
                <image class="nav-icon" :src="activeTab === 'search' ? '/static/search-active.png' : '/static/search-inactive.png'"></image>
                <!-- <text class="nav-text">搜索</text> -->
            </view>
            <view class="nav-item" :class="{'active': activeTab === 'user'}" @click="goToUser">
                <image class="nav-icon" :src="activeTab === 'user' ? '/static/user-active.png' : '/static/user-inactive.png'"></image>
                <!-- <text class="nav-text">我的</text> -->
            </view>
        </view>
    </view>
</template>

<script>
	import {
		myRequest
	} from '@/utils/util.js';
	
    export default {
        onload() {
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
			
			console.log("关闭所有页面")
            uni.getStorage({
                key: 'user_id',
                success: (res) => {
                    console.log('ID:' + res.data);
                    this.userId = res.data; // 获取用户ID
                    console.log('修改后的userId:'+ this.userId); // 打印确认
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
            goToLearn() {
                console.log('跳转到学习页面');
                // 跳转到学习页面
                uni.navigateTo({
                    url: '/pages/word/learn'
                });
            },
            goToReviews() {
                console.log('跳转到复习页面');
                uni.navigateTo({
                    url: '/pages/word/reviews'
                });
            },
			goToReviewszh() {
			    console.log('跳转到复习页面');
			    uni.navigateTo({
			        url: '/pages/word/reviewszh'
			    });
			},
            goToSearch() {
                uni.navigateTo({
                    url: '/pages/home/search'
                });
            },
            goToUser() {
                uni.navigateTo({
                    url: '/pages/home/user'
                });
            },
            navigateTo(tabName) {
                this.activeTab = tabName;
                if (tabName === 'search') this.goToSearch();
                else if (tabName === 'user') this.goToUser();
                // 如果 tabName 是 'home'，则不需要做任何事，因为当前就是 home 页
            }
        }
    };
</script>

<style scoped>
    .home-page-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between; /* 让底部导航栏能固定在底部 */
        min-height: 100vh;
        /* background: linear-gradient(135deg, #f8defa 0%, #b7b7ff 100%); */ /* 清新活泼的渐变 */
		background: linear-gradient(135deg, #f8defa 0%, #e6edff 100%); /* 清新活泼的渐变 */
        padding: 0; /* 移除全局padding，让内容区和底部导航宽度100% */
        box-sizing: border-box;
    }

    .hero-section {
        width: 100%;
        padding: 90px 20px 40px; /* 增加顶部内边距 */
        text-align: center;
        color: #ffffff;
    }
    .hero-logo {
        width: 100px;
        height: 100px;
        margin-bottom: 15px;
    }
    .welcome-text {
		top: 10vh;
        font-size: 24px;
        font-weight: 500;
		color: #42adff;
        opacity: 0.9;
    }

    .action-cards-container {
        width: 70%;
        padding: 0 20px; /* 容器左右留白 */
        display: flex;
        flex-direction: column; /* 卡片垂直排列 */
        gap: 25px; /* 卡片之间的间距 */
        align-items: center; /* 卡片居中 */
        flex-grow: 1; /* 占据剩余空间，将底部导航推到底部 */
    }

    .action-card {
        background: linear-gradient(135deg, rgba(137,247,255,0.2) 0%, rgba(102,166,255,0.6) 100%); /* 渐变背景 */
        color: #ffffff; /* 文字颜色调整为白色以适应渐变背景 */
        border-radius: 15px; /* 圆角 */
        padding: 20px 15px; /* 调整内边距 */
        width: 90%; /* 调整宽度 */
        max-width: 350px; /* 最大宽度 */
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15); /* 轻微调整阴影 */
        text-align: center;
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease; /* 添加动画效果 */
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .action-card:hover {
        transform: translateY(-5px); /* 悬停时的动画效果 */
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2); /* 悬停阴影调整 */
    }
    
    .card-icon {
        width: 50px; /* 图标稍小一些 */
        height: 50px;
        margin-bottom: 10px; /* 图标和标题间距调整 */
        /* 如果图标是深色的，在渐变背景上可能不明显，考虑使用白色版本的图标或加描边/背景 */
    }

    .card-title {
        font-size: 20px; /* 标题字号稍小 */
        font-weight: 600;
        color: #ffffff; /* 标题颜色改为白色 */
        margin-bottom: 5px;
    }

    .card-description {
        font-size: 14px;
        color: #f0f0f0; /* 描述文字颜色改为浅白色 */
        opacity: 0.9;
    }

    /* 为不同卡片定义强调色 - 以下样式在渐变背景下可能不再需要特别区分， */
    /* 或者需要调整为改变图标颜色或添加其他视觉元素 */

    .bottom-navigation-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        display: flex;
        justify-content: space-around;
        background-color: rgba(255, 255, 255, 0.25); /* 设置为80%透明 */
        box-shadow: 0 -3px 10px rgba(0, 0, 0, 0.08);
        padding: 10px 0;
        border-top-left-radius: 20px; /* 轻微圆角 */
        border-top-right-radius: 20px;
        z-index: 1000;
    }

    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        padding: 5px 10px;
        flex: 1; /* 均匀分配空间 */
        text-align: center;
    }

    .nav-icon {
        width: 28px;
        height: 28px;
        margin-bottom: 4px;
    }

    .nav-text {
        font-size: 12px;
        color: #888888;
        transition: color 0.2s ease;
    }

    .nav-item.active .nav-text {
        /* color: #5B6FE8; */ /* 激活状态的颜色，与背景主色调协调 */
        font-weight: 600;
    }

</style>