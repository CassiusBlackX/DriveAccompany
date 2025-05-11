import Vue from 'vue';
import App from './App.vue';
import router from './router';

Vue.prototype.$eventBus = new Vue(); // 定义全局事件总线

new Vue({
  router,  // Add this line
  render: (h) => h(App),
}).$mount('#app');

