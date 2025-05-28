<template>
    <view class="index-page-container">
        <!-- 顶部装饰或Logo区域 -->
        <view class="header-decoration">
            <text class="page-title">单词挑战</text>
        </view>

        <!-- 单词卡片 -->
        <view class="word-card-main">
            <text class="current-word-text">{{ currentWord.english }}</text>
        </view>

        <!-- 选项网格 -->
        <view class="options-grid-container">
            <view v-for="(option, index) in options" :key="index" class="option-button-card"
                @click="selectOption(index)">
                <text class="option-button-text">{{ option }}</text>
            </view>
        </view>

        <!-- 完整释义模态框 -->
        <view v-if="showDefinition" class="modal-overlay" @click.self="closeDefinition"> <!-- 点击遮罩层关闭 -->
            <view class="modal-content-box">
                <view class="modal-header-section">
                    <text class="modal-title-text">{{ currentWord.english }}</text>
                    <image class="close-modal-icon" src="/static/close-icon.png" @click="closeDefinition" />
                </view>
                <scroll-view scroll-y class="modal-body-scroll">
                    <text class="definition-text-block">{{ currentWord.definition }}</text>
                </scroll-view>
                <view class="modal-footer-actions">
                    <button class="modal-action-button primary" @click="proceedToNext">继续挑战</button>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            // 当前单词
            currentWord: {
                english: 'example',
                definition: 'A thing characteristic of a group, idea, or class.',
                options: ['示例', '定义', '解释', '示例']
            },
            // 选项数组
            options: [],
            // 是否显示完整释义
            showDefinition: false
        };
    },
    methods: {
        // 初始化选项
        initOptions() {
            const correctOption = this.currentWord.definition.split('.')[0];
            const allOptions = ['示例', '定义', '解释', correctOption];
            this.options = this.shuffleArray(allOptions);
        },
        // 选择选项
        selectOption(index) {
            if (this.options[index] === this.currentWord.definition.split('.')[0]) {
                this.showDefinition = true;
            } else {
                uni.showToast({
                    title: '答案错误',
                    icon: 'none'
                });
            }
        },
        // 关闭完整释义
        closeDefinition() {
            this.showDefinition = false;
            // 更新单词
            this.updateWord();
        },
        // 更新单词
        updateWord() {
            // 这里可以调用 API 获取下一个单词
            this.currentWord = {
                english: 'nextWord',
                definition: 'Next word definition.',
                options: ['示例', '定义', '解释', '示例']
            };
            this.initOptions();
        },
        // 打乱数组顺序
        shuffleArray(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }
            return array;
        },
        proceedToNext() {
            this.closeDefinition(); // 调用已有的 closeDefinition 包含更新单词的逻辑
        }
    },
    mounted() {
        this.initOptions();
    }
};
</script>

<style scoped>
    .index-page-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start; /* 从顶部开始排列 */
        min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* 更活泼的渐变背景 */
        padding: 20px;
        box-sizing: border-box;
    }

    .header-decoration {
        width: 100%;
        padding: 20px 0;
        text-align: center;
        margin-bottom: 20px;
    }

    .page-title {
        font-size: 28px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    .word-card-main {
        background-color: rgba(255, 255, 255, 0.9); /* 半透明白色背景 */
        padding: 30px 25px;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        text-align: center;
        margin-bottom: 30px;
        width: 100%;
        max-width: 450px;
    }

    .current-word-text {
        font-size: 36px;
        font-weight: bold;
        color: #333;
    }

    .options-grid-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        width: 100%;
        max-width: 450px;
        margin-bottom: 30px;
    }

    .option-button-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        text-align: center;
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .option-button-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }

    .option-button-text {
        font-size: 18px;
        color: #555;
        font-weight: 500;
    }

    /* 模态框样式 */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.6); /* 加深遮罩 */
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 2000;
        padding: 20px; /* 避免内容贴边 */
        box-sizing: border-box;
    }

    .modal-content-box {
        background-color: #ffffff;
        padding: 0; /* 内部通过section控制padding */
        border-radius: 12px;
        width: 100%;
        max-width: 400px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        overflow: hidden; /* 确保子元素在圆角内 */
        display: flex;
        flex-direction: column;
    }

    .modal-header-section {
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e9ecef;
    }

    .modal-title-text {
        font-size: 20px;
        font-weight: 600;
        color: #333;
    }

    .close-modal-icon {
        width: 20px;
        height: 20px;
        cursor: pointer;
        opacity: 0.7;
        transition: opacity 0.2s ease;
    }
    .close-modal-icon:hover {
        opacity: 1;
    }

    .modal-body-scroll {
        padding: 20px;
        max-height: 60vh; /* 限制最大高度，使其可滚动 */
        line-height: 1.6;
    }

    .definition-text-block {
        font-size: 16px;
        color: #555;
        white-space: pre-wrap; /* 保留换行和空格 */
    }

    .modal-footer-actions {
        padding: 15px 20px;
        border-top: 1px solid #e9ecef;
        display: flex;
        justify-content: flex-end; /* 按钮靠右 */
    }

    .modal-action-button {
        padding: 10px 25px;
        font-size: 16px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: background-color 0.2s ease, box-shadow 0.2s ease;
        font-weight: 500;
    }

    .modal-action-button.primary {
        background-color: #007bff;
        color: white;
        box-shadow: 0 2px 5px rgba(0,123,255,0.3);
    }
    .modal-action-button.primary:hover {
        background-color: #0056b3;
        box-shadow: 0 4px 8px rgba(0,123,255,0.4);
    }

    /* 移除或调整原有的全局 button 样式，如果它与新样式冲突 */
    /* button { ... } */
</style>