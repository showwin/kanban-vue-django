Vue.use(VueWebsocket, "ws://localhost:8000");

var card = Vue.component('card', {
  props: ['task'],
  template: `<div>
              <h3 class="title dd-handle" >{{ task.title }}</h3>
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
    tasks: []
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
  },
  created: function () {
    this.$http.get('/tasks').then(response => {
      this.tasks = response.body;
    });
  }
})

var wc = new Vue({
  methods: {
    add() {
      this.$socket.emit("add", { a: 5, b: 3 });
    }
  },
  socket: {
		events: {
			// Similar as this.$socket.on("changed", (msg) => { ... });
			// If you set `prefix` to `/counter/`, the event name will be `/counter/changed`
			//
			changed(msg) {
				console.log("Something changed: " + msg);
			},

			connect() {
				console.log("Websocket connected to " + this.$socket.nsp);
			},

			disconnect() {
				console.log("Websocket disconnected from " + this.$socket.nsp);
			},

			error(err) {
				console.error("Websocket error!", err);
			}
		}
	}
})
