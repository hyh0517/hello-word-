<script>
	import {
		myRequest
	} from './utils/util'
	import silenceUpdate from '@/uni_modules/rt-uni-update/js_sdk/silence-update.js' //引入静默更新


	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')

			// #ifdef APP

			// 获取本地应用资源版本号
			plus.runtime.getProperty(plus.runtime.appid, (inf) => {
				console.log(JSON.stringify(inf))
				//获取服务器的版本号
				const data = {
					ver: inf.versionCode
				}
				myRequest({
					url: '/check_update',
					method: 'GET',
					data: data,
					name: '检查更新',
					success: (res) => {
						//判断后台返回版本号是否大于当前应用版本号
						if (Number(res.data.edition_number) > Number(inf.versionCode)) {
							//如果是wgt升级，并且是静默更新 （注意！！！ 如果是手动检查新版本，就不用判断静默更新，请直接跳转更新页，不然点击检查新版本后会没反应）
							if (res.data.package_type == 1 && res.data.edition_silence == 1) {
								//调用静默更新方法 传入下载地址
								silenceUpdate(res.data.edition_url)
							} else {
								//跳转更新页面 （注意！！！如果pages.json第一页的代码里有一打开就跳转其他页面的操作，下面这行代码最好写在setTimeout里面设置延时3到5秒再执行）
								uni.navigateTo({
									url: '/uni_modules/rt-uni-update/components/rt-uni-update/rt-uni-update?obj=' +
										JSON.stringify(res.data)
								});
							}
						}
					}

				})

			});

			// #endif

		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
	/*每个页面公共css */
</style>