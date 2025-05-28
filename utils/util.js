// request.js
// 定义基础 URL，你可以根据需要在不同的环境配置中设置不同的值
const BASE_URL = '';// 如果你在生产环境中使用，可以设置为你的服务器地址
// const BASE_URL = 'http://127.0.0.1:5000';

export function myRequest(options) {
	// 克隆 options 对象，避免修改传入的对象
	const requestOptions = {
		...options
	};

	// 如果传入的是 uri，则拼接基础 URL
	if (requestOptions.url && !requestOptions.url.startsWith('http')) {
		requestOptions.url = BASE_URL + requestOptions.url;
	}

	return new Promise((resolve, reject) => {
		const {
			url,
			data = {},
			method = 'POST',
			header = {},
			name = '',
			success,
			fail
		} = requestOptions;

		uni.request({
			url,
			data,
			method,
			header,
			success: (res) => {
				console.log(name + '请求成功:', res);
				// 状态码 201 表示成功
				if (res.statusCode == 201 || res.statusCode == 200) {
					// 如果有 success 回调，执行它
					if (typeof success === 'function') {
						success(res);
					}
				} else {
					console.error(name + '失败:', res);
					uni.showToast({
						title: name + '失败' + res.statusCode,
						icon: 'none'
					});
					fail(res);
				}
				resolve(res.data);
			},
			fail: (err) => {
				console.error(name + '请求失败:', err);
				// 如果有 fail 回调，执行它
				if (typeof fail === 'function') {
					fail(err);
				}
				uni.showToast({
					title: name + '请求失败',
					icon: 'none'
				});
				reject(err);
			}
		});
	});
}