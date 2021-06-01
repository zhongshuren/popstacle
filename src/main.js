import Vue from 'vue'
import App from './App.vue'
import VueSocketIO from "vue-socket.io";
import SocketIO from 'socket.io-client'
import axios from "axios";
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

axios.defaults.baseURL = '/api'

Vue.config.productionTip = false
Vue.use(new VueSocketIO({
    debug: false,
    connection: SocketIO('/socket.io'),
}))
Vue.use(ElementUI)

new Vue({
    render: h => h(App),
}).$mount('#app')
