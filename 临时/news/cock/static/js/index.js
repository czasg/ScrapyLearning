$(function(){
    var
        prompt = function (message, style, time){
            style = (style === undefined) ? 'alert-success' : style;
            time = (time === undefined) ? 1200 : time;
            $('<div>')
                .appendTo('body')
                .addClass('alert_window ' + style)
                .html(message)
                .show(100)
                .delay(time)
                .fadeOut();
        },
        success_prompt = function(message, time){
            prompt(message, 'alert-success', time);  // Using Bootstrap Style
        },
        danger_prompt = function(message, time){
            prompt(message, 'alert-danger', time);
        };
    window.news_radio = true;
    $('#WebSocket-Chat-Container').on('show.bs.modal', function (e) {
        nav_top.unread = 0;
        ws_chat.model_open = true;
    });
    $('#WebSocket-Chat-Container').on('hide.bs.modal', function (e) {
        ws_chat.model_open = false;
    });
    nav_top = new Vue({
        el: '#nav-top',
        delimiters: ['[[', ']]'],
        data(){
            return {
                unread: 0,
            }
        },
    });
    ws_chat = new Vue({
        el: '#WebSocket-Chat',
        delimiters: ['[[', ']]'],
        data(){
            return {
                sock_id: '',
                content: '',
                online: 0,
                messages: [],
                model_open: false,
            }
        },
        mounted(){
			this.news_ws = new WebSocket("ws://192.168.0.223:8868/ws/api/news/data");
			this.news_ws.onmessage = (ev) => {
			    json_data = JSON.parse(ev.data);
			    if (json_data.radio && window.news_radio) {
			        success_prompt(`今日更新新闻：${json_data.count}`, 2000);
			    } else if (json_data.name) {
			        this.sock_id = json_data.name;
			    } else if (json_data.online) {
			        this.online = json_data.online;
			    } else if (json_data.from) {
			        console.log(json_data.msg);
			        this.messages.push(json_data);
			        $('#chat-content-list').parent().animate({
                        scrollTop: $('#chat-content-list').height()
                    }, 1000);
			        if (!this.model_open) {
			            nav_top.unread += 1;
			            if ((nav_top.unread % 10) === 0) {
			                danger_prompt(`您有 ${nav_top.unread} 条消息未读：`, 2000);
			            }
			        }
			    };
            };
            this.news_ws.onclose = (ev) => {
                this.messages.push({from: '数博科技', msg: 'WebSocket后台服务已关闭'});
            };
            this.news_ws.onopen = (ev) => {
                this.messages.push({from: '数博科技', msg: '欢迎来到数据组-白板报'});
                this.news_ws.send(JSON.stringify({'start': true}));
            };
        },
        methods: {
            ws_send: function(){
                if (!this.content) {
                    danger_prompt('输入不能为空~', 200);
                    return
                };
                this.news_ws.send(JSON.stringify({msg: this.content}));
                this.content = '';
            },
        },
    });
	new Vue({
		el: '#main-body-1',
		delimiters: ['[[', ']]'],
		data(){
			return {
				normal_spider_list: [],
				abnormal_spider_list: [],
				left_table_title: '新闻更新量（单位：条）',
				right_table_title: '当天未更新的任务',
				just_choose_province: '',
				is_loading: false,
				news_radio: true,
				current_day: '',
			}
		},
		watch: {
		    news_radio: function(val){
		        window.news_radio = val;
		    }
		},
		mounted(){
			this.myChart1 = echarts.init(document.getElementById('china-map'));
			this.myChart2 = echarts.init(document.getElementById('word-cloud'));
			this.myChart1.showLoading();
			this.myChart2.showLoading();
			this.choose_day(0);
		},
		methods: {
			init_pic: function(api, params){
				this.myChart1.showLoading();
				this.myChart2.showLoading();
				$.get(api, params, (api_result) => {
					this.init_table_list(api_result);
					this.init_china_map(this.myChart1, api_result);
					this.init_word_cloud(this.myChart2, api_result);
				})
			},
			choose_day: function(count){
				if (this.is_loading) {
					danger_prompt('正在加载中，请勿重复点击~', 500);
					return;
				};
				if (this.current_day === count) {
				    danger_prompt('当前数据已获取！', 500);
					return;
				};
				this.current_day = count;
				this.is_loading = true;
				var timeStamp = new Date(new Date().setHours(0, 0, 0, 0)) / 1000;
				day = timeStamp - 86400 * count;
				start_time = new Date();
				$.get('/api/get/map/data/v1', {
					day: day,
					just_choose_province: this.just_choose_province || false,
				}, (api_result) => {
					this.init_table_list(api_result);
					this.init_china_map(this.myChart1, api_result);
					this.init_word_cloud(this.myChart2, api_result);
					this.is_loading = false;
					success_prompt('Loading Success!', 500);
				})
			},
			init_table_list: function(api_result){
				this.normal_spider_list = api_result.normal_spider_list;
				this.abnormal_spider_list = api_result.abnormal_spider_list;
			},
			init_china_map: function(myChart, api_result){
				var now = new Date(),
					option = {
                        title: {
                            text: '政府新闻热度图'
                        },
                        tooltip: {
                        formatter: (params) => {
                                if (params.name) {
                                    return `<p style="font-size:18px">${params.name}：${params.value}</p><p style="font-size:14px">
                                    热度关键词：${(api_result['province_cloud_data'][params.name]).join('|') || '无'}
                                    </p>`;
                                }
                            },
                        },
                        visualMap: {
                            show: true,
                            x: 'right',
                            y: 'top',
                            splitList: api_result.bar,
                            color: ['#B71C1C', '#FFB74D', '#90CAF9', '#A5D6A7']
                        },
                        series: [
                            {
                                name: api_result.current_day,
                                type: 'map',
                                mapType: 'china',
                                selectedMode: 'multiple',
                                label: {
                                    normal: {
                                        show: true,
                                    },
                                    emphasis: {
                                        show: true,
                                    }
                                },
                                itemStyle: {
                                    normal: {
                                        borderWidth: .5,
                                    },
                                    emphasis: {
                                        borderWidth: .5,
                                        borderColor: '#4b0082',
                                        areaColor: "#ffdead",
                                    }
                                },
                                data: api_result.map_data,
                            }
                        ]
                    };
				myChart.hideLoading();
				myChart.setOption(option);
			},
			init_word_cloud: function(myChart, api_result){
				var
					data = api_result.cloud_data,
					maskImage = new Image(),
					option = {
						title: {
							text: '热度话题'
						},
						series: [{
							type: 'wordCloud',
							sizeRange: [10, 100],
							rotationRange: [-90, 90],
							rotationStep: 45,
							gridSize: 2,
							shape: 'pentagon',
							maskImage: maskImage,
							textStyle: {
								normal: {
									color: function () {
										return 'rgb(' + [
											Math.round(Math.random() * 160),
											Math.round(Math.random() * 160),
											Math.round(Math.random() * 160)
										].join(',') + ')';
									}
								}
							},
							data: data.sort(function (a, b) {
								return b.value  - a.value;
							})
						}],
					};
				maskImage.onload = function () {
					myChart.hideLoading();
					option.series[0].maskImage
					myChart.setOption(option);
				}
				maskImage.src = '../static/img/logo.png';
			},
			goto_top: function(){
			    $('html,body').animate({scrollTop: 0}, 200);
			},
		},
	});
    new Vue({
        el: '#main-body-2',
        delimiters: ['[[', ']]'],
        data(){
            return {
                is_loading: false,
                data_summary: [],
                data_statistical: [],
                data_spider_task_statistical: [],
                radio_data: '诚信数据',
                last_radio_data: '诚信数据',
                spider_tasks: ['诚信数据', '政府网站', '零碎任务', '法律', '新闻', '钢铁', '航运'],
            }
        },
        mounted(){
            var parent_width = document.getElementById('china-map').parentNode.offsetWidth;
            $('#operation-bar').css('width', parent_width - 32)
            this.myChart1 = echarts.init(document.getElementById('operation-bar'));
            this.myChart1.showLoading();
            this.init_data(this.radio_data);
        },
        methods: {
            init_data: function(task_name){
                $.get('/api/get/operation/data', {
                    task_name: task_name
                }, (api_data) => {
                    this.draw_table(api_data);
                    this.draw_bar(api_data);
                })
            },
            draw_table: function(api_data){
                this.data_summary = api_data.data_summary;
                this.data_statistical = api_data.data_statistical;
                this.data_spider_task_statistical = api_data.data_spider_task_statistical;
            },
            draw_bar: function(api_data){
                var option = {
                    tooltip : {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow',
                            label: {
                                show: true
                            }
                        }
                    },
                    toolbox: {
                        show : true
                    },
                    legend: {
                    },
                    grid: {
                        top: '12%',
                        left: '1%',
                        right: '10%',
                        containLabel: true
                    },
                    xAxis: [
                        {
                            type : 'category',
                            data : api_data.data_bar[0]
                        }
                    ],
                    yAxis: {
                        type : 'value',
                    },
                    dataZoom: [
                        {
                            show: true,
                            start: 30,
                            end: 100
                        },
                        {
                            type: 'inside',
                            start: 94,
                            end: 100
                        }
                    ],
                    series : [
                        {
                            name: '运维后废弃',
                            type: 'bar',
                            data: api_data.data_bar[1],
                            barWidth: 20,
                        },
                        {
                            name: '运维异常',
                            type: 'bar',
                            data: api_data.data_bar[2],
                            barWidth: 20,
                        },
                        {
                            name: '运维总数',
                            type: 'bar',
                            data: api_data.data_bar[3],
                            barWidth: 20,
                        }
                    ]
                };
                this.myChart1.hideLoading();
                this.myChart1.setOption(option);
                if (this.is_loading) {
                    this.is_loading = false;
                    this.last_radio_data = this.radio_data;
                    success_prompt('Loading Success!', 500);
                };
            },
            choose_task: function(){
                if (this.is_loading) {
                    danger_prompt('正在加载中，请勿重复点击~', 500);
                } else if (this.radio_data === this.last_radio_data) {
                    danger_prompt('当前数据已获取！', 500);
                } else {
                    this.is_loading = true;
                    this.init_data(this.radio_data);
                }
            }
        },
    });
})