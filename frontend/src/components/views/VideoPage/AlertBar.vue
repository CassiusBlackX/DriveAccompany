<template>
  <div class="alert-bar">
    <div class="alert-count"></div>
    <div v-for="(alert, index) in alertlist" :key="index" class="alert">
      <img :src="alert.image" class="alert-icon" />
      <span class="alert-type" :class="alert.type">{{ alert.title }}:</span>
      {{ alert.message }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlertBar',
  data() {
    return {
      alertlist: [
        {
          type: 'None',
          title: 'None',
          message: 'No alert',
        },
      ],
      alerts: [
        {
          type: 'normal',
          title: 'Normal',
          message: 'User is not showing any signs of drowsiness',
        },
        {
          type: 'closed-eyes',
          title: 'Closed Eyes',
          message: 'User is closing their eyes for too long',
        },
        {
          type: 'yawn-emoji',
          title: 'Yawning',
          message: 'User is yawning too much',
        },
        {
          type: 'head-turn',
          title: 'Head Turn',
          message: 'User is turning their head away',
        },
        // {
        //   type: 'phone',
        //   title: 'Phone',
        //   message: 'User is using their phone',
        // },
        
      ],
    };
  },
  mounted() {
    // WebSocket 连接到服务器
    //this.ws = new WebSocket('ws://localhost:6868');
    this.ws = new WebSocket('ws://192.168.124.38:6868?client_id=client2');
    this.ws.onmessage = this.handleMessage;
  },
  methods: {
    handleMessage(event) {
      // 收到数字代表是几个 alert
      const message = parseInt(event.data, 10); // 将消息转换为整数
      if (message >= 0 && message <= 4) {
        this.alertlist.push(this.alerts[message]);

        // 保持 alertlist 的长度最大为 14
        if (this.alertlist.length > 14) {
          this.alertlist.shift();
        }

        // 通过事件总线将消息广播给其他组件
        this.$eventBus.$emit('websocket-message', message);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../../../assets/scss/index.scss";
.alert-bar {
  color: white;
  background-color: dimgray;
  opacity: 0.8;
  padding: 10px;
  font-family: $default_font_family;
}

.alert {
  display: inline-block;
  margin-bottom: 5px;
  padding: 8px;
  border-radius: 5px;
  font-size: 14px;
  line-height: 1.4;
  width: 90%;
}

.alert-type {
  font-weight: 550;
}

.normal {
  color: #9999;
}

.yawn-emoji {
  color: $purple_message;
}

// .phone {
//   color: $grass_green_message;
// }

.closed-eyes {
  color: $pink_message;
}

.head-turn {
  color: $light_blue_message;
}

/* Add more styles for different alert types */
</style>
