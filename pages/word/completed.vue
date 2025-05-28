<template>
    <view class="container">
        <view class="completed-card">
            <image class="completed-icon" src="/static/completed-icon.png" mode="aspectFit"></image>
            <text class="completed-header">恭喜您</text>
            <text class="completed-body">已完成今日背诵任务</text>
            <button class="back-button" @click="goBack">返回首页</button>
        </view>
    </view>
</template>

<script>
    export default {
        onLoad() {
            this.userId = uni.getStorageSync('user_id');
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
			uni.setStorageSync("completedCount", 0);
        },
        methods: {
            goBack() {
                uni.reLaunch({
                    url: '/pages/home/home'
                });
            }
        }
    };
</script>

<style scoped>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        background: linear-gradient(135deg, #f8defa 0%, #e6edff 100%); /* 清新活泼的渐变 */
        padding: 20px;
    }

    .completed-card { /* 将 completed-content 重命名为 completed-card 并调整样式 */
        /* background-color: #ffffff; */
		background-color: rgba(255,255,255,0.5);
        padding: 40px 30px; /* 增加内边距 */
        border-radius: 15px; /* 更大的圆角 */
        width: 85%;
        max-width: 400px; /* 限制最大宽度 */
        text-align: center;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15); /* 更明显的阴影 */
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .completed-icon { /* 新增图标样式 */
        width: 80px;
        height: 80px;
        margin-bottom: 25px;
    }

    .completed-header {
        font-size: 26px; /* 调整字号 */
        font-weight: bold;
        color: #333; /* 深色文字，对比更清晰 */
        margin-bottom: 15px; /* 调整间距 */
    }

    .completed-body {
        font-size: 18px;
        color: #555; /* 调整文字颜色 */
        margin-bottom: 30px; /* 调整间距 */
    }

    .back-button {
        width: 100%; /* 按钮宽度充满卡片 */
        max-width: 280px; /* 限制按钮最大宽度 */
        height: 45px; /* 调整按钮高度 */
        background-color: #007bff; /* 使用更通用的蓝色主题 */
        color: #ffffff;
        font-size: 16px;
        border: none;
        border-radius: 8px; /* 调整按钮圆角 */
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease; /* 增加过渡效果 */
        box-shadow: 0 4px 8px rgba(0, 123, 255, 0.2); /* 按钮阴影 */
    }

    .back-button:hover {
        background-color: #0056b3; /* 悬停时颜色加深 */
        transform: translateY(-2px); /* 轻微上浮效果 */
    }
</style>