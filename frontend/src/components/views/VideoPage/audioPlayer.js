// audioPlayer.js
class AudioPlayer {
    constructor() {
      this.audio = null; // 当前播放的音频
      this.queue = []; // 音频队列
      this.isPlaying = false; // 当前是否正在播放
    }
  
    // 将音频添加到队列
    enqueueAudio(src) {
      this.queue.push(src);
      this.playNext(); // 尝试播放下一个音频
    }
  
    // 播放队列中的下一个音频
    playNext() {
      if (this.isPlaying || this.queue.length === 0) return; // 如果正在播放或队列为空，退出
  
      const nextAudioSrc = this.queue.shift(); // 获取下一个音频源
      this.audio = new Audio(nextAudioSrc); // 创建音频对象
      this.isPlaying = true; // 设置为正在播放

      
      
      // 绑定音频播放结束事件
      this.audio.onended = () => {
        this.isPlaying = false; // 播放结束，设置为未播放状态
        this.playNext(); // 尝试播放下一个音频
      };
  
      this.audio.play().catch((error) => {
        console.error("Audio playback failed:", error); // 处理播放错误
        this.isPlaying = false; // 如果播放失败，设置为未播放状态
        this.playNext(); // 尝试播放下一个音频
      });
    }
  }
  
  const audioPlayer = new AudioPlayer();
  export default audioPlayer;
  