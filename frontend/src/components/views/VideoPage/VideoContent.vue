<template>
  <div class="video-container">
    <!-- <canvas ref="videoCanvas" class="video-content" :src="currentFrame"> -->
    <img ref="image" :src="currentFrame" alt="Video" class="video-content"/>
    <!-- </canvas> -->
    <div class="button-bar-container">
    <div class="button-bar">
      <button @click="startVideo" class="but"><img :src="playimg" class="buttonImg"/></button>
      <button @click="stopVideo" class="but"><img :src="stopimg" class="buttonImg"/></button>
      <button @click="saveVideo" class="but"><img :src="saveimg" class="buttonImg"/></button>
    </div>
    </div>
  </div>
</template>
  
  <script>
  // import JSMpeg from '../../../assets/server/jsmpeg.min.js';
  // import WebSocket from 'ws';
  export default {
    name: 'VideoContent',
    data() {
      return {
        ws: null,
        currentFrame: '',
        isPlaying: false,
          playimg: require('../../../assets/images/button/play.png'),
          saveimg: require('../../../assets/images/button/save.png'),
          stopimg: require('../../../assets/images/button/stop.png'),
      };
    },

    mounted() {
  //this.ws = new WebSocket('ws://localhost:7979'); // 替换成 videohelp_server 的地址
  this.ws = new WebSocket('ws://192.168.124.38:7979?client_id=client2');//换成绝对IP。在其他主机上也能连接到我本地。
  this.ws.onmessage = this.handleMessage;
  this.ws.onclose = (event) => {
    console.log('WebSocket closed:', event);
    
    //alert("服务器已断开连接！");
  };
  this.ws.onerror = (error) => {
    console.log('WebSocket error:', error);
  };
},

  methods: {
    startVideo() {
      if (!this.isPlaying) {
        this.isPlaying = true;
        this.ws.send('start'); 
      }
    },
    stopVideo() {
      if (this.isPlaying) {
        this.isPlaying = false;
        this.ws.send('stop');
      }
    },
    saveVideo() {
      this.ws.send('save');
    },


    handleMessage(event) {
      const message = event.data;
      if(message==-1){
        alert("后端已断开连接！");
      }
      const blob = new Blob([message], { type: 'image/jpg' });
      const url = URL.createObjectURL(blob);

      this.currentFrame = url
    }

  }
};
    

  </script>
  
  <style lang="scss" scoped>
  @import "../../../assets/scss/index.scss";
  .video-container {
    width: 100%;
    height: 100%;
    position: relative;
    background-color: black;
  }
  .video-content {    
    width: 100%;
    height: 90%;
  }

  .but{
    opacity: 0.8;
    background-color: #ffff;
    border-radius: 5px;
    border: #ffff;
    &:hover {
      background-color: rgba(#ffff, 0.7);
    }
    &:active {
      // active时，背景色变浅，且与focus，hover做区分
      background-color: darken($color: #ffff, $amount: 10%)
    }
  }
  .button-bar-container{
      width:100%;
      opacity: 0.7;
      background-color: #9999;
      display: flex;
      position: absolute;
      left: 0%;
      bottom: 0%;

  }
    .button-bar{
      width: 80px;
      display:flex;
      border-radius: 5px;
      flex-direction: row;
      justify-content: space-between;
    }

  .buttonImg{
    // background-color: #ffff;
    width: 100%;
    height: 100%;
    max-width: 15px;
    max-height: 15px;
  }

  </style>
  