<template>
  <div class="about" v-html="renderedMarkdown"></div>
</template>

<script>
import MarkdownIt from 'markdown-it';
export default {
  name: "AboutIndex",
  data() {
    return {
markdown: '**倦旅智鉴**\n' 
+ '倦旅智鉴是一个基于深度学习的图像处理工具，旨在帮助用户快速、准确地处理和分析图像数据。我们致力于为用户提供高效、便捷的图像处理解决方案。\n'
+ '我们提供了多种图像处理功能，包括图像分类、目标检测、图像分割等。用户可以通过简单的操作，快速完成复杂的图像处理任务。\n',
          
      renderedMarkdown: ''
    };
  },
  mounted() {
    this.renderMarkdown();
  },
  methods: {
    renderMarkdown() {
      const md = new MarkdownIt();
      this.renderedMarkdown = md.render(this.markdown);
    }
  }
}
</script>

<style scoped>
.about{
  width: 70%;
  margin: 0 auto;
}
</style>