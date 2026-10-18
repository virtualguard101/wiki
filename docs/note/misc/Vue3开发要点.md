---
date: 2026-10-18 22:29:34
title: Vue3开发要点
permalink: vue3-overview
publish: true
tags:
  - Web开发
  - 杂项学习
---

# Vue3开发要点

## 前端项目的基本结构

### 前端与后端

- **前端**负责页面, 表单, 表格, 交互和路由等用户可见部分

- **后端**负责业务规则, 数据读写和接口响应

- 前后端通过 HTTP API 交换数据. 前端提交请求并根据响应更新页面

### Vue 3 单文件组件

Vue 3 常用 `.vue` 单文件组件组织页面. 一个组件通常包含模板, 逻辑和样式:

```vue
<template>
  <button @click="count++">点击次数: {{ count }}</button>
</template>

<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>

<style scoped>
button {
  cursor: pointer;
}
</style>
```

- `<template>`描述页面结构, 展示数据并绑定事件

- `<script setup>`编写状态和交互逻辑. `ref` 创建的基本类型状态通过 `.value` 在脚本中读写, 在模板中会自动解包

- `<style scoped>`将样式限制在当前组件, 避免意外影响其他组件

- 三个区块并非每个组件都必须同时出现. 无状态展示组件可以没有 `<script>`, 不需要局部样式时也可以省略 `<style>`

Vue 3 支持 Options API 和 Composition API. 课件主要讲项目结构与页面流程, 此处的示例使用 Composition API 的 `<script setup>` 语法.

### SPA 与 MVVM

- **SPA**(Single Page Application)是单页应用. 页面首次加载后, 前端根据路由切换视图, 通常不需要为每次页面导航重新请求完整 [HTML](HTML要点.md)

- **MVVM**是组织界面与状态的一种模式. 在 Vue 中, 模板描述视图, 响应式状态保存数据, 框架负责将状态变化同步到视图

- 修改状态后由 Vue 更新界面, 不要在业务代码里手工拼接 DOM 来保持页面同步

Vue 不是严格意义上完整实现 MVVM 模式的框架, 因此将其理解为采用响应式数据驱动视图更准确.

## 创建并启动项目

### 环境与职责

- **Node.js**提供 JavaScript 运行环境

- **npm**安装和管理项目依赖, 并运行 `package.json` 中定义的脚本

- **Vite**负责开发服务器和生产构建

- **VS Code**用于编辑代码. Vue - Official 扩展提供 Vue 单文件组件的语言支持

- **Chrome**用于查看页面和调试浏览器行为

典型依赖关系:

```text
Node.js -> npm -> Vite -> Vue 项目
```

### 创建 Vite 项目

确保 Node.js 和 npm 已安装后, 在终端运行:

```bash
npm create vite@latest prj-frontend -- --template vue
cd prj-frontend
npm install
npm run dev
```

按终端提示打开开发服务器给出的地址, 常见默认地址是 `http://localhost:5173`.

常用 npm 命令:

| 命令 | 作用 |
| --- | --- |
| `node -v` | 查看 Node.js 版本 |
| `npm -v` | 查看 npm 版本 |
| `npm install` | 根据 `package.json` 安装项目依赖 |
| `npm run dev` | 启动开发服务器 |
| `npm run build` | 生成生产构建产物 |

如果 `npm run dev` 失败, 先检查当前目录是否为项目根目录, 再检查依赖安装和终端错误信息.

## 组件库与页面布局

### 安装和注册 Element Plus

Element Plus 是 Vue 3 的 UI 组件库. 以全局注册为例:

```bash
npm install element-plus
```

在应用入口 `src/main.js` 中导入组件库, 样式并注册:

```js
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.mount('#app')
```

导入样式负责组件外观, `app.use(ElementPlus)`负责注册组件, `app.mount('#app')`将 Vue 应用挂载到 `index.html` 的 `#app` 节点. 漏掉样式时组件可能没有预期外观, 漏掉注册时全局组件不可用.

小型项目可以全局注册以简化使用. 更大型的项目也可按需导入组件, 以控制依赖和构建产物.

### 组织应用布局

管理后台常见布局由顶部栏, 侧边导航栏, 主内容区和页脚组成. 主内容区使用 `<router-view />` 显示当前路由对应的页面:

```vue
<template>
  <el-container>
    <el-header>员工信息系统</el-header>
    <el-container>
      <el-aside>
        <el-menu>
          <el-menu-item index="/category">分类管理</el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>
```

将通用布局放在 `App.vue`, 将各页面放在 `src/views/`, 可避免每个页面重复实现导航和外框.

## 路由与页面导航

### 路由记录

Vue Router 将 URL 映射到 Vue 组件. 每条路由至少要清楚定义访问路径和显示的组件, 也可为路由添加名称:

```js
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/category',
    name: 'Category',
    component: () => import('../views/Category.vue'),
    meta: { requiresAuth: true },
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
```

- `path`是浏览器地址栏中的 URL 路径

- `component`是该路径对应的页面组件

- `createWebHistory()`使用 History API, URL 中不带 `#`

- 动态 `import()`可将页面拆分为异步加载的代码块

创建路由器后, 在入口文件中调用 `app.use(router)`. 在导航菜单中使用 `<router-link>`切换页面, 在内容区域放置 `<router-view />`显示页面. 导航切换的是 SPA 中的视图, 不等同于重新加载整个 HTML 文档.

使用 `createWebHistory()`时, 生产服务器需要将未匹配到静态文件的页面路径回退到 `index.html`, 否则直接刷新 `/category` 可能返回 404.

## API 与 CRUD 数据流

### 创建 Axios 实例

Axios 负责浏览器端 HTTP 请求. 将基础地址和超时设置集中到一个实例, 避免每个页面重复配置:

```js
// src/utils/request.js
import axios from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_BASE_API,
  timeout: 5000,
})

export default request
```

开发和生产环境可分别配置环境变量:

```dotenv
# .env.development
VITE_BASE_API=http://localhost:9090
```

```dotenv
# .env.production
VITE_BASE_API=https://api.example.com
```

Vite 客户端可读取的自定义环境变量默认使用 `VITE_` 前缀. 这些值会进入浏览器代码, 不能把密码, 私钥或其他秘密放在其中. 修改环境变量后通常需要重启开发服务器.

### 集中管理 API 函数

按业务模块组织请求, 让页面只调用函数, 不直接拼接 URL:

```js
// src/api/category.js
import request from '../utils/request.js'

export function listCategories(params) {
  return request.get('/category/list', { params })
}

export function saveCategory(data) {
  return request.post('/category/save', data)
}

export function updateCategory(data) {
  return request.put('/category/update', data)
}

export function deleteCategory(id) {
  return request.delete(`/category/${id}`)
}
```

具体 URL, HTTP 方法和参数格式要与后端 API 契约一致. Axios 响应对象中的 `response.data` 是服务端返回的数据载荷, 而后端约定的 `data`, `code`, `msg`, `rows`, `total` 等字段含义取决于项目接口定义.

### 新增与编辑表单

新增和编辑通常可以复用同一个表单. 新增时清空表单并进入保存分支, 编辑时将选中行回填表单并进入更新分支:

```vue
<el-form ref="formRef" :model="form" :rules="rules">
  <el-form-item label="分类名称" prop="name">
    <el-input v-model="form.name" />
  </el-form-item>
</el-form>
```

```js
import { reactive, ref } from 'vue'

const formRef = ref()
const form = reactive({ id: null, name: '' })
const rules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }],
}

async function submitForm() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  if (form.id == null) {
    await saveCategory(form)
  } else {
    await updateCategory(form)
  }
}
```

`v-model`将输入值与表单状态保持同步. `el-form-item`的 `prop`要对应 `model`中的字段名, 校验规则才能定位字段. 若后端允许 `id` 为 `0`, 使用 `form.id == null`区分新增与编辑, 不要用 `if (!form.id)`.

保存成功后给出提示, 关闭对话框并刷新列表. 请求失败时保留表单内容并提示错误, 避免将网络错误显示成保存成功.

### 表格, 加载和分页

表格页面通常需要维护列表数据, 加载状态, 页码和总数:

```js
import { onMounted, reactive, ref } from 'vue'

const rows = ref([])
const total = ref(0)
const loading = ref(false)
const query = reactive({ pageNum: 1, pageSize: 10 })

async function getList() {
  loading.value = true
  try {
    const response = await listCategories(query)
    rows.value = response.data.rows
    total.value = response.data.total
  } finally {
    loading.value = false
  }
}

onMounted(getList)
```

表格使用 `el-table-column`配置列, 使用具名插槽显示编辑, 删除等操作. 加载过程中可将 `loading`绑定到 `v-loading`, 避免用户误以为页面没有响应.

分页组件发出页码变化事件后, 更新 `pageNum`并重新调用列表 API. 改变每页条数时一般要重置到第一页. 请求参数名称, 返回字段和总数含义应以实际 API 为准.

### 删除确认

删除是不可逆操作时, 先确认再发请求; 取消时不发送请求:

```js
import { ElMessage, ElMessageBox } from 'element-plus'

async function removeCategory(id) {
  try {
    await ElMessageBox.confirm('确认删除该分类吗?', '提示', {
      type: 'warning',
    })
    await deleteCategory(id)
    ElMessage.success('删除成功')
    await getList()
  } catch (error) {
    if (error === 'cancel' || error === 'close') return
    ElMessage.error('删除失败')
    throw error
  }
}
```

如果项目提供统一的错误处理器, 应按项目约定避免重复提示. 不要把所有异常都当成用户取消, 也不要吞掉真实的网络或服务端错误.

## 登录, Token 与访问控制

### 登录流程

登录表单通常包含用户名和密码, 用 `v-model`绑定输入, 用 `rules`做前端必填校验. 前端校验用于改善交互, 不能代替后端校验:

1. 校验表单字段

2. 调用登录 API

3. 根据后端响应保存必要的登录状态

4. 跳转到应用页面

5. 后续请求按接口约定携带凭证

课件示例将响应写入 `localStorage`, 需先序列化:

```js
localStorage.setItem('user', JSON.stringify(response.data))
const user = JSON.parse(localStorage.getItem('user'))
```

实际项目应只保存必要数据, 并处理缺失或格式错误的存储值. `localStorage`会在浏览器会话之间保留数据; 使用它保存可读 Token 时, 同源脚本一旦发生 [XSS](Web安全要点.md#10-XSS-跨站脚本) 就可能读取该 Token. 是否采用 `localStorage`, `sessionStorage`或 `HttpOnly` Cookie, 应根据认证设计和后端能力决定. 不要把密码长期存入浏览器存储.

### Axios 请求携带凭证

若后端采用 Bearer Token, 可通过请求拦截器统一添加请求头:

```js
request.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

响应拦截器可统一处理未授权响应, 但应避免对同一错误重复弹窗或无限重试. Token 刷新, 过期和退出登录的行为应与服务端接口协同设计.

### 路由守卫

在 `router.beforeEach`中根据目标路由和认证状态决定是否放行. 通过 `meta.requiresAuth`显式标记需要登录的页面:

```js
router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !token) {
    return { name: 'Login' }
  }
  if (to.name === 'Login' && token) {
    return { name: 'Home' }
  }
})
```

路由守卫只控制前端导航, 不能保护服务端资源. API 必须在服务端验证 Token 和用户权限. 退出登录时清理本地凭证并跳转到登录页. Token 是否过期也应依据可信的服务端机制判断, 不能仅以浏览器中存在字符串作为授权依据.

## 构建与部署

### 生产构建

```bash
npm run build
```

Vite 将源码编译和打包到 `dist/`. `src/`和 `.vue`文件是开发源码, 发布时应提供构建后的静态文件, 而不是把源码目录直接交给 Nginx.

### Nginx 静态部署

部署时将 `dist/` 内容放入[Nginx](反向代理.md#Nginx)网站根目录, 并为 SPA 配置路由回退:

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/app/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

同时确认以下事项:

- 生产环境的 API 地址已在构建时正确配置

- Nginx `root`指向包含 `index.html`的 `dist/`目录

- 前端路由刷新能回退到 `index.html`

- API 服务可从部署环境访问, 且 CORS 和 HTTPS 配置符合实际架构

- 防火墙, 安全组和 DNS 已按部署环境开放相应访问

前端项目与后端服务是两部分. Nginx 提供前端静态文件, 不会因此自动启动或代理后端 API.

## 开发检查清单

-  使用 Vite 创建并启动 Vue 3 项目

-  确认 Element Plus 组件和样式都已引入

-  路由记录, 菜单和页面组件对应正确

-  API 请求集中管理, 开发与生产环境地址分离

-  表单有校验, 表格有加载状态, 分页会重新请求数据

-  新增, 编辑, 删除分别走正确的 API 分支

-  删除前确认, 取消删除不会发出请求

-  登录状态, Token 携带, 退出登录和路由守卫逻辑一致

-  关键权限由后端验证, 不仅依赖前端路由

-  `npm run build`成功, 并验证 Nginx 的 SPA 路由回退
