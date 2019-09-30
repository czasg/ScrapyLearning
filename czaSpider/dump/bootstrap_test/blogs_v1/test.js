/*
维护users字典，存储用户的图片信息
*/
class User {
    constructor({user_image, user_name, is_master, snow_key, unreadInfo=0}){
        this.user_image = user_image;
        this.user_name = user_name;
        this.is_master = is_master;
        this.snow_key = snow_key;
        this.unreadInfo = unreadInfo;  // 定义未读信息
    }
}

$(function(){
    test = new Vue({
        el: '#TEST',
        data(){
            return {
                sayingWord: '',
                users: {},  // snow_key : User
                messages: {},
                sessions: [],
                current_chat: '',
            }
        },
        mounted(){
            var users_info = [
                    {
                        user_image: 'static/img/user.png',
                        user_name: 'big_home',
                        user_say: 'hello world',
                        is_master: false,
                        snow_key: '1234567890',
                        to: 'big_home',
                    },{
                        user_image: 'static/img/user.png',
                        user_name: 'big_home',
                        user_say: 'are you ok',
                        is_master: false,
                        snow_key: '1234567890',
                        to: 'big_home',
                    },{
                        user_image: 'static/img/user.png',
                        user_name: 'xiaoming',
                        user_say: 'i am very ok',
                        is_master: true,
                        snow_key: '123456',
                        to: '1234567890',
                    },{
                        user_image: 'static/img/user.png',
                        user_name: 'cza',
                        user_say: 'hello world',
                        is_master: false,
                        snow_key: '123',
                        to: '123456',
                    },{
                        user_image: 'static/img/user.png',
                        user_name: 'xiaoming',
                        user_say: 'welcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChat',
                        is_master: true,
                        snow_key: '123456',
                        to: '123',
                    },{
                        user_image: 'static/img/user.png',
                        user_name: 'xiaoming',
                        user_say: 'welcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChat',
                        is_master: true,
                        snow_key: '123456',
                        to: '123',
                    },{
                        user_image: 'static/img/user.png',
                        user_name: 'lihong',
                        user_say: 'This is a Test Chat',
                        is_master: false,
                        snow_key: '123123',
                        to: '123456',
                    },{
                        user_image: 'static/img/user.png',
                        user_name: 'lihong',
                        user_say: 'Are You OK!',
                        is_master: false,
                        snow_key: '123123',
                        to: '123456',
                    }
                ];
            users_info.forEach(user_info => {
                if (!user_info.is_master) {
                    if (this.sessions.indexOf(user_info.snow_key) === -1) {
                        this.sessions.push(user_info.snow_key);
                    }
                }
                if (this.users[user_info.snow_key] === undefined) {
                    this.users[user_info.snow_key] = new User(user_info);  //这里存的数据太多了
                    this.messages[user_info.snow_key] = [];
                }
                if (user_info.is_master) {
                    this.messages[user_info.to].push(user_info);
                } else {
                    this.messages[user_info.snow_key].push(user_info);
                    this.users[user_info.snow_key].unreadInfo += 1;
                }
            })
        },
        methods: {
            saying: function(){
                if (!this.sayingWord) {
                    alert('输入不能为空');
                    return
                }
                this.messages[this.current_chat].push({
                    user_image: 'static/img/user.png',
                    user_name: 'lihong',
                    user_say: this.sayingWord,
                    is_master: true,
                });
                this.sayingWord = '';
                $('#chat-media-list').parent().animate({
                    scrollTop: $('#chat-media-list').height()
                }, 1000);
            },
            choose_session: function(snow_key){
                this.current_chat = snow_key;
                this.users[snow_key].unreadInfo = 0;
            }
        }
    })
})