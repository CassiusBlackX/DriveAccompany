# 前端部分说明

## ./helpServer/ 文件夹
负责连接后端与前端，需要先启动。
在helpServer文件夹内执行下列指令：
```
npm install

node Server.js

node AlertServer.js
```

## Front-end Project setup
```
说版本不一样时
npm uninstall node-sass
npm install sass --save-dev
```
清除 npm 缓存：
```
npm cache clean --force
```
Windows 用户：手动删除 node_modules 文件夹和 package-lock.json 文件。

```
npm install
```

## ./FrontEnd 文件夹
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

这个项目是一个基于 Vue.js 的前端项目，以下是它的组织结构和功能说明：

---

### **项目的组织结构**
#### 1. **根文件**
- **`vue.config.js`**  
  配置文件，用于自定义 Vue CLI 的默认配置，比如代理、路径别名等。

- **`package.json`**  
  定义项目的依赖、脚本命令（如 `npm run serve`）、项目名称等。是项目的核心配置文件。

- **`public/index.html`**  
  这是项目的 HTML 模板文件，Vue.js 会将编译后的内容插入到 `<div id="app"></div>` 中。  
  - `<title>` 标签定义了网页在浏览器标签页上的名字（如 "倦旅智鉴"）。
  - `<link rel="icon">` 设置了网页的图标。

---

#### 2. **核心文件**
- **`src/main.js`**  
  项目的入口文件，负责初始化 Vue 实例并挂载到 `#app` 上。  
  - 引入了 App.vue，作为整个应用的根组件。
  - 引入了 `router`，用于管理页面路由。
  - 定义了全局事件总线 `$eventBus`。

- **`src/App.vue`**  
  根组件，所有页面和组件都嵌套在这里。  
  - 包含了 `<HeaderComp>`（头部组件）和 `<router-view>`（路由占位符，用于动态加载页面组件）。

---

#### 3. **路由管理**
- **`src/router/index.js`**  
  定义了页面路由。  
  - 例如，`/` 路径加载 VideoPage.vue，`/about` 路径加载 `AboutIndex.vue`。

---

#### 4. **页面组件**
- **`src/components/views/VideoPage/VideoPage.vue`**  
  负责视频页面的布局和功能。  
  - 包含子组件：`ButtonBar`（按钮栏）、`VideoContent`（视频内容）、`InfoContent`（信息内容）、`AlertBar`（警告栏）。

- **`src/components/views/About/Index.vue`**  
  负责 "关于" 页面。

---

#### 5. **子组件**
- **`src/components/layout/HeaderComp.vue`**  
  头部组件，显示标题（如 "倦旅智鉴"）和菜单。

- **`src/components/views/VideoPage/ButtonBar.vue`**  
  按钮栏组件，处理按钮点击事件和 WebSocket 消息。

- **`src/components/views/VideoPage/VideoContent.vue`**  
  视频内容组件，负责显示视频帧，并通过 WebSocket 接收视频流。

---

### **项目的运行流程**
1. **`npm run serve` 的作用**  
   - 执行 `vue-cli-service serve`，启动一个开发服务器。
   - 读取 package.json 中的依赖，加载项目文件。
   - 编译 Vue 文件（`.vue`）和其他资源（如 SCSS、图片）。
   - 将编译后的内容注入到 index.html 的 `<div id="app"></div>` 中。
   - 启动一个本地服务器（默认端口为 8080），并监听文件变化，支持热更新。

2. **项目的加载流程**
   - **入口文件**：`src/main.js` 初始化 Vue 实例。
   - **根组件**：`App.vue` 加载头部组件和路由占位符。
   - **路由管理**：根据 URL 加载对应的页面组件（如 VideoPage.vue）。
   - **页面组件**：加载子组件（如 ButtonBar.vue、`VideoContent.vue`）。
   - **功能实现**：通过 WebSocket、事件总线等实现交互。

---

### **总结**
- **最根本的组织文件**：`src/main.js`，它初始化了 Vue 实例并加载根组件。
- **页面的入口点**：`public/index.html`，是 HTML 模板文件。
- **路由管理**：`src/router/index.js`，定义了页面的切换逻辑。
- **组件的组织**：`App.vue` 是根组件，其他组件通过嵌套方式组织起来。

通过 `npm run serve`，项目会启动一个开发服务器，加载这些文件并运行整个应用。