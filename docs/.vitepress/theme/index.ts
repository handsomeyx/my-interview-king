import DefaultTheme from 'vitepress/theme'
import { h, onMounted } from 'vue'
import { useRoute } from 'vitepress'
import InteractiveParticles from './InteractiveParticles.vue'
import ReadingProgress from './ReadingProgress.vue'
import SearchPanel from './SearchPanel.vue'
import StudyTracker from './StudyTracker.vue'
import ArticleActions from './ArticleActions.vue'
import ContinueReading from './ContinueReading.vue'
import LearningPath from './LearningPath.vue'
import RelatedProblems from './RelatedProblems.vue'
import Breadcrumbs from './Breadcrumbs.vue'
import NotFound from './NotFound.vue'
import FeedbackButton from './FeedbackButton.vue'
import SiteStats from './SiteStats.vue'
import MyProgressPanel from './MyProgressPanel.vue'
import ProblemLinker from './ProblemLinker.vue'
import ThinkingLinks from './ThinkingLinks.vue'
import AlgorithmPath from './AlgorithmPath.vue'
import JavaPath from './JavaPath.vue'
import DistributedPath from './DistributedPath.vue'
import AiPath from './AiPath.vue'
import ProjectsPath from './ProjectsPath.vue'
import AlgorithmCross from './AlgorithmCross.vue'
import JavaCross from './JavaCross.vue'
import DistributedCross from './DistributedCross.vue'
import AiCross from './AiCross.vue'
import ProjectsCross from './ProjectsCross.vue'
import AlgorithmStar from './AlgorithmStar.vue'
import JavaStar from './JavaStar.vue'
import DistributedStar from './DistributedStar.vue'
import AiStar from './AiStar.vue'
import ProjectsStar from './ProjectsStar.vue'
import './custom.css'

// 为代码块添加复制按钮
function CodeBlock(props) {
  return h(DefaultTheme.Content, null, {
    code: (_, { slots }) => {
      const code = slots.default()[0]
      if (code.type !== 1 || code.props?.class !== 'language-') return code
      
      const codeContent = code.children?.[0]?.children || ''
      
      const copyButton = h('button', {
        class: 'copy-button',
        onClick: () => {
          navigator.clipboard.writeText(codeContent)
          const button = event.target
          button.textContent = '已复制!'
          setTimeout(() => {
            button.textContent = '复制'
          }, 2000)
        }
      }, '复制')
      
      return h('div', { class: 'code-block-wrapper' }, [
        code,
        copyButton
      ])
    }
  })
}

export default {
  extends: DefaultTheme,
  NotFound,
  Layout: () => {
    const route = useRoute()
    const getPageKey = () => {
      const path = route.path || ''
      return path.replace(/^\//, '').replace(/\.html$/, '')
    }
    return h(DefaultTheme.Layout, null, {
      'layout-top': () => [h(ReadingProgress), h(SearchPanel), h(StudyTracker), h(ArticleActions), h(FeedbackButton), h(ProblemLinker)],
      'doc-before': () => h(Breadcrumbs),
      'doc-after': () => h(ThinkingLinks, { pageKey: getPageKey() }),
      // 使用插槽将粒子背景放入布局底部
      'layout-bottom': () => h(InteractiveParticles)
    })
  },
  enhanceApp({ app }) {
    app.component('ContinueReading', ContinueReading)
    app.component('LearningPath', LearningPath)
    app.component('SiteStats', SiteStats)
    app.component('MyProgressPanel', MyProgressPanel)
    app.component('AlgorithmPath', AlgorithmPath)
    app.component('JavaPath', JavaPath)
    app.component('DistributedPath', DistributedPath)
    app.component('AiPath', AiPath)
    app.component('ProjectsPath', ProjectsPath)
    app.component('AlgorithmCross', AlgorithmCross)
    app.component('JavaCross', JavaCross)
    app.component('DistributedCross', DistributedCross)
    app.component('AiCross', AiCross)
    app.component('ProjectsCross', ProjectsCross)
    app.component('AlgorithmStar', AlgorithmStar)
    app.component('JavaStar', JavaStar)
    app.component('DistributedStar', DistributedStar)
    app.component('AiStar', AiStar)
    app.component('ProjectsStar', ProjectsStar)
  },
  setup() {
    onMounted(() => {
      const openImageModal = (src) => {
        const modal = document.createElement('div')
        modal.className = 'image-modal'
        const enlarged = document.createElement('img')
        enlarged.src = src
        enlarged.className = 'enlarged-image'
        const closeBtn = document.createElement('span')
        closeBtn.className = 'close-button'
        closeBtn.textContent = '×'
        modal.append(enlarged, closeBtn)
        document.body.appendChild(modal)
        const dismiss = () => document.body.removeChild(modal)
        closeBtn.addEventListener('click', dismiss)
        modal.addEventListener('click', (e) => { if (e.target === modal) dismiss() })
      }
      // 事件委托：一次绑定，SPA 路由切换后新渲染的元素同样生效
      document.addEventListener('click', (e) => {
        const img = e.target.closest('.vp-doc img')
        if (img && img.src) {
          openImageModal(img.src)
          return
        }
        const title = e.target.closest('.outline-title')
        if (title) {
          title.classList.toggle('collapsed')
          const links = title.nextElementSibling
          if (links) {
            links.classList.toggle('collapsed')
            links.classList.toggle('expanded')
          }
        }
      })
    })
  }
}