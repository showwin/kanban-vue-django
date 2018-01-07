var card = Vue.component('card', {
  props: ['task'],
  template: `<div>
              <h3 class="title dd-handle" >{{ task.name }}</h3>
              <div class="text">{{ task.content }}</div>
              <hr>
              <table class="status-button">
                <tr>
                  <td><button v-on:click="task.status -= 1">◀︎</button></td>
                  <td><button v-on:click="task.status += 1">▶︎</button></td>
                </tr>
              </table>
            </div>`
})

var filters = {
  open: function (tasks) {
    return tasks.filter(task => task.status === 1)
  },
  progress: function (tasks) {
    return tasks.filter(task => task.status === 2)
  },
  done: function (tasks) {
    return tasks.filter(task => task.status === 3)
  }
}

board = new Vue({
  el: '#board',
  data: {
    tasks: [
      { name: '料理する', content: '今日の昼ごはん作る', status: 1 },
      { name: 'お皿洗う', content: '昨日の分も合わせてお皿洗う', status: 1 },
      { name: 'ゲームする', content: '早くおわらせてXCOM 2やるで〜', status: 2 }
    ]
  },
  computed: {
    tasksOpen: function () {
      return filters.open(this.tasks)
    },
    tasksProgress: function () {
      return filters.progress(this.tasks)
    },
    tasksDone: function () {
      return filters.done(this.tasks)
    }
  }
})
