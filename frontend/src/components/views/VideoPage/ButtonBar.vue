<!-- <template>
  <div class="button-bar">
    <div
      v-for="(buttonEl, index) in buttonEls"
      :key="index"
      class="button-container"
      :class="isButtonColor[index] ? buttonEl.color : 'white'"
    >
      <img :src="buttonEl.image" class="buttonImg" alt="button image" />
    </div>
  </div>
</template>

<script>
import { closedEyes, headTurn, phoneWatch, yawnEmoji } from "../../../assets/images/button";

export default {
  name: 'ButtonBar',
  data() {
    return {
      buttonEls: [
        {
          type: 'closed-eyes',
          image: closedEyes,
          color: "pink_message",
        },
        {
          type: "yawn-emoji",
          image: yawnEmoji,
          color: "purple_message",
        },
        {
          type: 'head-turn',
          image: headTurn,
          color: "light_blue_message",
        },
        {
          type: "phone-watch",
          image: phoneWatch,
          color: "grass_green_message",
        }
      ],
      isButtonColor: [false, false, false, false], // 记录每个按钮的颜色状态
    };
  },
  mounted() {
    // 监听来自 AlertBar 的 WebSocket 消息
    this.$eventBus.$on('websocket-message', this.handleWebSocketMessage);
  },
  methods: {
    handleWebSocketMessage(message) {
      // 如果 message 是 0，则不执行任何操作
      if (message === 0) return;

      // message 从 1 开始，对应的按钮索引应该是 message-1
      const buttonIndex = message - 1;

      if (buttonIndex >= 0 && buttonIndex < this.buttonEls.length) {
        // 切换对应按钮的颜色
        this.toggleButtonColor(buttonIndex);

        // 设置 2 秒后恢复按钮颜色为白色
        setTimeout(() => {
          this.resetButtonColor(buttonIndex);
        }, 2000);
      }
    },
    toggleButtonColor(index) {
      // 切换指定按钮的颜色状态为激活状态
      this.$set(this.isButtonColor, index, true);
    },
    resetButtonColor(index) {
      // 将按钮颜色状态恢复为白色
      this.$set(this.isButtonColor, index, false);
    }
  },
  beforeDestroy() {
    // 组件销毁时，移除事件监听器
    this.$eventBus.$off('websocket-message', this.handleWebSocketMessage);
  }
};
</script>

<style lang="scss" scoped>
@import "../../../assets/scss/index.scss";
.button-bar {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.button-container {
  height: 0;
  padding: 50% 0%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px black solid;
  border-radius: 8px;
  margin: 5px 0px;

  @media only screen and (max-width: $md_window_size) {
    padding: 12% 5%;
    flex: 1;
  }
}

.button-container:hover {
  cursor: pointer;
}

.buttonImg {
  max-width: 40px;
  max-height: 40px;

  @media only screen and (min-width: $md_window_size) and (max-width: $lg_window_size) {
    max-width: 32px;
    max-height: 32px;
  }

  @media only screen and (max-width: $md_window_size) {
    max-width: 40px;
    max-height: 40px;
  }
}

.purple_message {
  background-color: $purple_message;
}

.pink_message {
  background-color: $pink_message;
}

.light_blue_message {
  background-color: $light_blue_message;
}

.grass_green_message {
  background-color: $grass_green_message;
}
</style> -->


<!-- <template>
  <div class="button-bar">
    <div
      v-for="(buttonEl, index) in buttonEls"
      :key="index"
      class="button-container"
      :class="isButtonColor[index] ? buttonEl.color : 'white'"
      @click="handleButtonClick(index + 1)"  
    >
      <img :src="buttonEl.image" class="buttonImg" alt="button image" />
    </div>
  </div>
</template>

<script>
import { closedEyes, headTurn, phoneWatch, yawnEmoji } from "../../../assets/images/button";
import audioPlayer from '../../../components/views/VideoPage/audioPlayer.js'; // 导入音频播放工具

export default {
  name: 'ButtonBar',
  data() {
    return {
      buttonEls: [
        {
          type: 'closed-eyes',
          image: closedEyes,
          color: "pink_message",
        },
        {
          type: "yawn-emoji",
          image: yawnEmoji,
          color: "purple_message",
        },
        {
          type: 'head-turn',
          image: headTurn,
          color: "light_blue_message",
        },
        {
          type: "phone-watch",
          image: phoneWatch,
          color: "grass_green_message",
        }
      ],
      isButtonColor: [false, false, false, false], // 记录每个按钮的颜色状态
    };
  },
  mounted() {
    // 监听来自 AlertBar 的 WebSocket 消息
    this.$eventBus.$on('websocket-message', this.handleWebSocketMessage);
  },
  methods: {
    handleWebSocketMessage(message) {
      // 如果 message 是 0，则不执行任何操作
      if (message === 0) return;

      // message 从 1 开始，对应的按钮索引应该是 message-1
      const buttonIndex = message - 1;

      if (buttonIndex >= 0 && buttonIndex < this.buttonEls.length) {
        // 切换对应按钮的颜色
        this.toggleButtonColor(buttonIndex);

        // 播放音频
        // const audioFiles = [
        //   "C:/Users/10210/Desktop/Jetson/Code/vuertsp-master - 副本/src/assets/audio/closed_eyes.wav",
        //   "C:/Users/10210/Desktop/Jetson/Code/vuertsp-master - 副本/src/assets/audio/yawn.wav",
        //   "C:/Users/10210/Desktop/Jetson/Code/vuertsp-master - 副本/src/assets/audio/head_turn.wav",
        //   "C:/Users/10210/Desktop/Jetson/Code/vuertsp-master - 副本/src/assets/audio/phone_watch.wav"
        // ];

        const audioFiles = [
        "/closed_eyes.wav",
        "/yawn.wav",
        "/head_turn.wav",
        "/phone_watch.wav"
        ];


        // 确保用户点击后播放音频
        this.$nextTick(() => {
          audioPlayer.enqueueAudio(audioFiles[buttonIndex]);
        });

        // 设置 2 秒后恢复按钮颜色为白色
        setTimeout(() => {
          this.resetButtonColor(buttonIndex);
        }, 2000);
      }
    },
    handleButtonClick(index) {
      // 这里可以处理按钮的点击逻辑，比如添加额外的交互
      console.log(`Button ${index} clicked`); // 记录点击
    },
    toggleButtonColor(index) {
      // 切换指定按钮的颜色状态为激活状态
      this.$set(this.isButtonColor, index, true);
    },
    resetButtonColor(index) {
      // 将按钮颜色状态恢复为白色
      this.$set(this.isButtonColor, index, false);
    }
  },
  beforeDestroy() {
    // 组件销毁时，移除事件监听器
    this.$eventBus.$off('websocket-message', this.handleWebSocketMessage);
  }
};
</script>

<style lang="scss" scoped>
@import "../../../assets/scss/index.scss";
.button-bar {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.button-container {
  height: 0;
  padding: 50% 0%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px black solid;
  border-radius: 8px;
  margin: 5px 0px;

  @media only screen and (max-width: $md_window_size) {
    padding: 12% 5%;
    flex: 1;
  }
}

.button-container:hover {
  cursor: pointer;
}

.buttonImg {
  max-width: 40px;
  max-height: 40px;

  @media only screen and (min-width: $md_window_size) and (max-width: $lg_window_size) {
    max-width: 32px;
    max-height: 32px;
  }

  @media only screen and (max-width: $md_window_size) {
    max-width: 40px;
    max-height: 40px;
  }
}

.purple_message {
  background-color: $purple_message;
}

.pink_message {
  background-color: $pink_message;
}

.light_blue_message {
  background-color: $light_blue_message;
}

.grass_green_message {
  background-color: $grass_green_message;
}
</style> -->


<template>
  <div class="button-bar">
    <div
      v-for="(buttonEl, index) in buttonEls"
      :key="index"
      class="button-container"
      :class="isButtonColor[index] ? buttonEl.color : 'white'"
      @click="handleButtonClick(index + 1)"  
    >
      <img :src="buttonEl.image" class="buttonImg" alt="button image" />
    </div>
  </div>
</template>

<script>
import { closedEyes, headTurn, yawnEmoji } from "../../../assets/images/button";
import audioPlayer from '../../../components/views/VideoPage/audioPlayer.js'; // 导入音频播放工具

export default {
  name: 'ButtonBar',
  data() {
    return {
      buttonEls: [
        {
          type: 'closed-eyes',
          image: closedEyes,
          color: "pink_message",
        },
        {
          type: "yawn-emoji",
          image: yawnEmoji,
          color: "purple_message",
        },
        {
          type: 'head-turn',
          image: headTurn,
          color: "light_blue_message",
        }
        // ,
        // {
        //   type: "phone-watch",
        //   image: phoneWatch,
        //   color: "grass_green_message",
        // }
      ],
      // isButtonColor: [false, false, false, false], // 记录每个按钮的颜色状态
      isButtonColor: [false, false, false],
    };
  },
  mounted() {
    // 监听来自 AlertBar 的 WebSocket 消息
    this.$eventBus.$on('websocket-message', this.handleWebSocketMessage);
  },
  methods: {
    handleWebSocketMessage(message) {
      // 如果 message 是 0，则不执行任何操作
      if (message === 0) return;

      // message 从 1 开始，对应的按钮索引应该是 message-1
      const buttonIndex = message - 1;

      if (buttonIndex >= 0 && buttonIndex < this.buttonEls.length) {
        // 切换对应按钮的颜色
        this.toggleButtonColor(buttonIndex);

        // 播放音频
        const audioFiles = [
          "/closed_eyes.wav",
          "/yawn.wav",
          "/head_turn.wav",
          //"/phone_watch.wav"
        ];

        // 确保用户点击后播放音频
        if (!audioPlayer.isPlaying) { // 检查是否正在播放
          this.$nextTick(() => {
            audioPlayer.enqueueAudio(audioFiles[buttonIndex]);
          });
        }

        // 设置 2 秒后恢复按钮颜色为白色
        setTimeout(() => {
          this.resetButtonColor(buttonIndex);
        }, 2000);
      }
    },
    handleButtonClick(index) {
      // 这里可以处理按钮的点击逻辑，比如添加额外的交互
      console.log(`Button ${index} clicked`); // 记录点击
    },
    toggleButtonColor(index) {
      // 切换指定按钮的颜色状态为激活状态
      this.$set(this.isButtonColor, index, true);
    },
    resetButtonColor(index) {
      // 将按钮颜色状态恢复为白色
      this.$set(this.isButtonColor, index, false);
    }
  },
  beforeDestroy() {
    // 组件销毁时，移除事件监听器
    this.$eventBus.$off('websocket-message', this.handleWebSocketMessage);
  }
};
</script>

<style lang="scss" scoped>
@import "../../../assets/scss/index.scss";
.button-bar {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.button-container {
  height: 0;
  padding: 50% 0%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px black solid;
  border-radius: 8px;
  margin: 5px 0px;

  @media only screen and (max-width: $md_window_size) {
    padding: 12% 5%;
    flex: 1;
  }
}

.button-container:hover {
  cursor: pointer;
}

.buttonImg {
  max-width: 40px;
  max-height: 40px;

  @media only screen and (min-width: $md_window_size) and (max-width: $lg_window_size) {
    max-width: 32px;
    max-height: 32px;
  }

  @media only screen and (max-width: $md_window_size) {
    max-width: 40px;
    max-height: 40px;
  }
}

.purple_message {
  background-color: $purple_message;
}

.pink_message {
  background-color: $pink_message;
}

.light_blue_message {
  background-color: $light_blue_message;
}

.grass_green_message {
  background-color: $grass_green_message;
}
</style>
