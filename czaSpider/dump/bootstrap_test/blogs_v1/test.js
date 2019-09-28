class User {
    constructor({name, age}){
        this.name = name;
        this.age = age;
    }
}


$(function(){
    new Vue({
        el: '#TEST',
        data(){
            return {
                chat_msg: [
                    {
                        user_image: 'static/img/user.png',
                        user_name: 'cza',
                        user_say: 'hello world',
                        is_master: false,
                    },
                    {
                        user_image: 'static/img/user.png',
                        user_name: 'xiaoming',
                        user_say: 'welcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChatwelcome to WebChat',
                        is_master: true,
                    },
                    {
                        user_image: 'static/img/user.png',
                        user_name: 'lihong',
                        user_say: 'This is a Test Chat',
                        is_master: false,
                    },
                    {
                        user_image: 'static/img/user.png',
                        user_name: 'lihong',
                        user_say: 'Are You OK!',
                        is_master: false,
                    }
                ],
                sayingWord: ''
            }
        },
        methods: {
            saying: function(){
                if (!this.sayingWord) {
                    alert('输入不能为空');
                    return
                }
                this.chat_msg.push({
                    user_image: 'static/img/user.png',
                    user_name: 'lihong',
                    user_say: this.sayingWord,
                    is_master: true,
                });
                this.sayingWord = '';
                $('#chat-media-list').parent().animate({
                    scrollTop: $('#chat-media-list').height()
                }, 1000);
            }
        }
    })
})