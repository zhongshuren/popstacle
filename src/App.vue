<template>
  <div id="app">
    <div style="position: absolute;top:0;width:100%;height:240px;background-color: #e7ebef;z-index:1000"></div>
    <div
        style="position: absolute;top:240px;width:100%;height:60px;background-image:linear-gradient(180deg, rgba(231,235,239,1), rgba(231,235,239,0));z-index:1000"></div>
    <div style="position: absolute;top:40px;left:20px;z-index: 1000">
      <span style="font-size: 36px;color: #bdc9d5">popstacle</span>
    </div>
    <div style="position: absolute;top:40px;right: 20px;z-index:1001">
      <span style="font-size: 36px;color: #bdc9d5" @click="showTips=!showTips"><i class="el-icon-more"></i></span>
    </div>
    <div id="bottom-buttons" style="position: absolute;bottom: 0;width:100%;z-index: 1100">
      <div class="op-button" v-for="(item, id) in operations" :key="id"
           :style="`display: inline-block;width: 20%;height: 80px;background-color: ${item.color};`"
           @click="sendOpcode(item.code, item.enabled)" @touchstart="changeColor(item, item.enabled, 1)"
           @touchend="changeColor(item, item.enabled, 0)"/>
    </div>
    <div class="info-wrap" style="position:absolute;top:100px;width:100%;z-index: 1200;color:#838c95">
      <div class="info-wrap-horizontal" style="margin: auto">
        <div style="font-size: 48px">{{ `${fillZero(Math.floor(seconds / 60))}:${fillZero(seconds % 60)}` }}</div>
      </div>
    </div>
    <transition name="info-box">
      <div v-if="gameEnded" class="info-wrap"
           style="position:absolute;top:300px;width:100%;z-index: 1400;color:#838c95">
        <div class="info-wrap-horizontal"
             style="padding:20px;margin: auto;font-size: 60px;width:60%;background-color: #e7ebef;border-radius: 5px;box-shadow:0 5px 10px #838c95;">
          {{ getResult() }}
          <br>
          <el-button @click="reset">play again</el-button>
        </div>
      </div>
    </transition>
    <transition name="info-box">
      <div v-if="showTips" class="info-wrap" style="position:absolute;top:100px;width:100%;z-index: 1400;color:#838c95">
        <div class="info-wrap-horizontal"
             style="padding:20px;margin: auto;text-align: left;width:80%;height:300px;overflow: scroll;background-color: #e7ebef;border-radius: 5px;box-shadow:0 5px 10px #838c95;">
          <h2>游戏规则：</h2>
          <p>每个回合，双方可以选择一种颜色，对应一种操作：</p>
          <p><span class="green">绿色</span>、<span class="blue">蓝色</span>是加入操作，自己底部加入一个相应颜色的方块。</p>
          <p><span class="yellow">黄色</span>、<span class="orange">橙色</span>、<span class="purple">紫色</span>是消除操作，分别会消耗自己底部的一个、两个、三个<span
              class="green">绿色</span>方块，而对方的底部在遇到<span class="blue">蓝色</span>方块之前最多能被消除两倍于自己的方块。</p>
          <p>消除操作的执行需要自己底部拥有足够数量的连续<span class="green">绿色</span>方块。</p>
          <p>如果双方都选择了对应消除效果的颜色，则只有消耗量较大的一方产生效果。如果双方的消耗量相等，则跳过这个回合，不执行任何操作。</p>
          <p>最终<span class="green">绿色</span>方块数量较多的一方获胜。</p>
        </div>
      </div>
    </transition>
    <transition name="info-box">
      <div v-if="showTips" class="info-wrap" style="position:absolute;top:460px;width:100%;z-index: 1400;color:#838c95">
        <div class="info-wrap-horizontal"
             style="padding:20px;margin: auto;text-align: left;width:80%;height:100px;background-color: #e7ebef;border-radius: 5px;box-shadow:0 5px 10px #838c95;">
          <h2>Star me on github</h2>
          还不知道地址。。。
        </div>
      </div>
    </transition>
    <div class="info-wrap" style="position:absolute;top:160px;width: 100%;z-index:1200;color:#838c95">
      <div class="info-wrap-horizontal" style="margin: auto">
        <div style="display: inline-block;vertical-align: bottom;width:30%;margin:0 1% 0 1%">
          <div>P1</div>
          <div style="font-size: 32px;color:#BDC9D5">{{ myId }}</div>
        </div>
        <div v-if="!gameStarted" style="display: inline-block;vertical-align: bottom;width:30%;margin:0 1% 0 1%">
          <div>P2</div>
          <el-input pattern="number" type="number" style="font-size: 32px;width: 100%;height:100%;margin:0;padding:0"
                    @input="turnDown()" v-model="opId"/>
        </div>
        <div v-else style="display: inline-block;vertical-align: bottom;width:30%;margin:0 1% 0 1%">
          <div>P2</div>
          <div style="font-size: 32px;color:#BDC9D5">{{ opId }}</div>
        </div>
      </div>
      <div v-if="!gameStarted" class="info-wrap-horizontal" style="margin: 20px auto">
        <el-button v-if="!invited" @click="invite" style="width: 62%">invite</el-button>
        <el-button v-else @click="accept" style="width: 62%">accept</el-button>
      </div>
      <div v-if="gameStarted" class="info-wrap-horizontal" style="margin: auto">
        <div style="display: inline-block;vertical-align: bottom;width:30%;margin:0 1% 0 1%">
          <div style="font-size: 48px">{{ allCount1 }}</div>
        </div>
        <div style="display: inline-block;vertical-align: bottom;width:30%;margin:0 1% 0 1%">
          <div style="font-size: 48px">{{ allCount2 }}</div>
        </div>
      </div>
    </div>
    <div class="stack-wrap" style="position: absolute;bottom:100px;width: 100%;">
      <div class="stack-wrap-horizontal">
        <div class="stack">
          <transition-group name="stack-trans" tag="p">
            <div class="stack-item" v-for="item in stackVisual1" :key="item.id"
                 :style="`background-color: ${color[item.code]};width:auto;height:38px;margin-top:2px`"/>
          </transition-group>
        </div>
        <div class="stack">
          <transition-group name="stack-trans" tag="p">
            <div class="stack-item" v-for="item in stackVisual2" :key="item.id"
                 :style="`background-color: ${color[item.code]};width:auto;height:38px;margin-top:2px`"/>
          </transition-group>
        </div>
      </div>
    </div>
    <div class="stack-wrap" style="position: absolute;bottom:80px;width: 100%;">
      <div class="stack-wrap-horizontal">
        <div style="display: inline-block;vertical-align: bottom;width:30%;margin:0 1% 0 1%;background-color: gray">
          <div class="op-show" :style="`background-color: ${color[op1]};height:10px;`"/>
          <div style="background-color: #e7ebef;height:30px;"/>
        </div>
        <div style="display: inline-block;vertical-align: bottom;width:30%;margin:0 1% 0 1%;background-color: gray">
          <div class="op-show" :style="`background-color: ${color[op2]};height:10px;`"/>
          <div style="background-color: #e7ebef;height:30px;"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  components: {},
  mounted() {
    axios.get('/getId').then(
        (res) => {
          console.log(res.data)
          this.myId = res.data.id_code
          this.$socket.emit('initRoom', this.myId)
        }
    ).catch(
        (res) => {
          console.log(res)
        }
    )
  },
  data() {
    return {
      myId: '',
      opId: '',//这里的op是opponent的意思，而另一些地方的op是operation的意思，命名鬼才
      gameStarted: false,
      gameEnded: false,
      showTips: false,
      invited: false,
      seconds: 60,//后续的更新会让玩家自定义时长
      color: [
        //普通颜色，对应操作0，1，2，3，4。
        '#42b983',
        '#1f9cb1',
        '#efd340',
        '#e38c5d',
        '#d05293',
        //背景色
        '#bdc9d5',
        '#ffffff',
        //稍微暗一点的颜色
        '#299a67',
        '#0c7080',
        '#ba9f16',
        '#b4673e',
        '#a82e6d',
        //被禁止的颜色
        '#b3b0a4',
        '#908884',
        '#827a7c',
      ],
      operations: [
        {
          code: 0,
          color: '#42b983',
          enabled: true,
        },
        {
          code: 1,
          color: '#1f9cb1',
          enabled: true,
        },
        {
          code: 2,
          color: '#efd340',
          enabled: false,
        },
        {
          code: 3,
          color: '#e38c5d',
          enabled: false,
        },
        {
          code: 4,
          color: '#d05293',
          enabled: false,
        }
      ],
      stack1: [],
      stack2: [],
      stackVisual1: [],
      stackVisual2: [],
      stackItemId1: 0,
      stackItemId2: 0,
      allCount1: 0,
      allCount2: 0,
      op1: 5,
      op2: 5,
      result: 0,
      countDown: '',
    }
  },
  sockets: {
    recvInvitation: function (data) {
      console.log(data)
      this.opId = data
      this.invited = true
    },
    startGame: function () {
      this.gameStarted = true
      this.stack1 = []
      this.stack2 = []
      this.stackVisual1 = []
      this.stackVisual2 = []
      this.stackItemId1 = 0
      this.stackItemId2 = 0
      this.allCount1 = 0
      this.allCount2 = 0
      this.countDown = setInterval(() => {
        if (this.seconds === 0) {
          this.op1 = 5
          this.op2 = 5
          clearInterval(this.countDown)
          //结算两方胜负
          this.calcResult(this.stack1, this.stack2)
        } else {
          this.seconds -= 1
        }
      }, 1000)
    },
    recvOpcode: function (data) {
      let code1 = data.code1
      let code2 = data.code2
      let id1 = data.id1
      if (id1 !== this.myId) {
        let t = code1
        code1 = code2
        code2 = t
      }
      this.operateStack(code1, code2)
    },
    startShortCountDown: function (data) {
      console.log(data, this.myId)
      if (data !== this.myId) {
        this.op2 = 6
        console.log('the opponent has chosen the operation')
      }
    },
  },
  methods: {
    invite: function () {
      if (this.opId.length === 4) {
        this.$socket.emit('invite', {myId: this.myId, opId: this.opId})
      }
    },
    accept: function () {
      this.$socket.emit('accept', {myId: this.myId, opId: this.opId})
    },
    turnDown: function () {
      this.invited = false
    },
    sendOpcode: function (code, enabled) {
      if (!this.gameStarted) return
      if (!enabled) return
      let xc = this.getTopCount(this.stack1)
      if (code > xc + 1) return
      this.op1 = code
      this.$socket.emit('sendOpcode', {code: code, room: (this.invited ? this.opId : this.myId), myId: this.myId})
    },
    calcResult: function (stack1, stack2) {
      if (this.getAllCount(stack1) > this.getAllCount(stack2)) {
        this.result = 1
      } else if (this.getAllCount(stack1) < this.getAllCount(stack2)) {
        this.result = -1
      } else {
        this.result = 0
      }
      this.gameEnded = true
    },
    getResult: function () {
      if (this.result === 1) return 'You win'
      if (this.result === -1) return 'You lose'
      return 'Tie'
    },
    reset: function () {
      this.seconds = 60
      this.stack1 = []
      this.stack2 = []
      this.stackVisual1 = []
      this.stackVisual2 = []
      this.gameEnded = false
      this.$socket.emit('reset', {room: (this.invited ? this.opId : this.myId), myId: this.myId})
    },
    changeColor: function (item, enabled, down) {
      if (!enabled) return
      if (down) item.color = this.color[item.code + 7]
      else item.color = this.color[item.code]
    },
    popStack: function (stack, op, num) {
      for (let i = stack.length - 1; i >= Math.max(stack.length - num, 0); --i) {
        stack[i] = op
      }
      for (let i = 1; i <= num; ++i) {
        stack.pop()
      }
    },
    //utility
    fillZero: function (x) {
      if (('' + x).length === 1) return '0' + x
      return x
    },
    //visual part
    popStackVisual: function (stackVisual, op, num, stack) {
      for (let i = stackVisual.length - 1; i >= Math.max(stackVisual.length - num, 0); --i) {
        stackVisual[i].code = op
      }
      stackVisual.push(1)
      stackVisual.pop()
      let id_temp = []
      for (let i = 0; i < stackVisual.length; ++i) {
        id_temp.push(stackVisual[i].id)
      }
      setTimeout(() => {
        stackVisual.length = 0
        for (let i = 0; i < stack.length; ++i) {
          stackVisual.push({code: stack[i], id: id_temp[i]})
        }
        console.log(stackVisual)
      }, 500)
    },
    getTopCount: function (stack) {
      let ret = 0
      for (let i = stack.length - 1; i >= 0; --i) {
        if (stack[i] === 1) break
        ret++
      }
      return ret
    },
    getAllCount: function (stack) {
      let ret = 0
      for (let i = 0; i < stack.length; ++i) {
        if (stack[i] === 0) {
          ret++
        }
      }
      return ret
    },
    operateStack: function (code, code2) {
      //用于测试的随机数
      //let code2 = Math.floor(Math.random() * 5)
      /*let xc = this.getTopCount(this.stack1)
      let yc = this.getTopCount(this.stack2)
      console.log(code, code2, xc, yc)
      if (code > xc + 1) {
        return
      }*/
      /*if (code2 > yc + 1) {
        code2 = 0
      }*/
      this.op2 = code2
      if (code === 0) {
        this.stack1.push(0)
        this.stackVisual1.push({code: 0, id: this.stackItemId1})
        this.stackItemId1++;
      }
      if (code === 1) {
        this.stack1.push(1)
        this.stackVisual1.push({code: 1, id: this.stackItemId1})
        this.stackItemId1++;
      }
      if (code2 === 0) {
        this.stack2.push(0)
        this.stackVisual2.push({code: 0, id: this.stackItemId2})
        this.stackItemId2++;
      }
      if (code2 === 1) {
        this.stack2.push(1)
        this.stackVisual2.push({code: 1, id: this.stackItemId2})
        this.stackItemId2++;
      }
      let xc = this.getTopCount(this.stack1)
      let yc = this.getTopCount(this.stack2)
      console.log(code, code2, xc, yc)
      if (code >= 2 && code <= 4 && code > code2) {
        let n = code - 1
        this.popStack(this.stack1, code, n)
        this.popStackVisual(this.stackVisual1, code, n, this.stack1)
        this.popStack(this.stack2, code, Math.min(n * 2, yc + 1))
        this.popStackVisual(this.stackVisual2, code, Math.min(n * 2, yc + 1), this.stack2)
      }
      if (code2 >= 2 && code2 <= 4 && code2 > code) {
        let n = code2 - 1
        this.popStack(this.stack2, code2, n)
        this.popStackVisual(this.stackVisual2, code2, n, this.stack2)
        this.popStack(this.stack1, code2, Math.min(n * 2, xc + 1))
        this.popStackVisual(this.stackVisual1, code2, Math.min(n * 2, xc + 1), this.stack1)
      }
      xc = this.getTopCount(this.stack1)
      this.allCount1 = this.getAllCount(this.stack1)
      this.allCount2 = this.getAllCount(this.stack2)
      this.operations[2].enabled = xc >= 1
      this.operations[3].enabled = xc >= 2
      this.operations[4].enabled = xc >= 3
      this.operations[2].color = this.color[xc >= 1 ? 2 : 12]
      this.operations[3].color = this.color[xc >= 2 ? 3 : 13]
      this.operations[4].color = this.color[xc >= 3 ? 4 : 14]
    }
  }
}
</script>

<style>
.green {
  color: #42b983;
}

.blue {
  color: #1f9cb1;
}

.yellow {
  color: #efd340;
}

.orange {
  color: #e38c5d;
}

.purple {
  color: #d05293;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.stack-wrap-horizontal {
  margin: auto;
}

.stack {
  display: inline-block;
  vertical-align: bottom;
  width: 30%;
  margin: 0 1% 0 1%;
}

.stack-trans-enter {
  transform: translateY(40px);
}

.stack-trans-leave-active {
  position: absolute;
}

.stack-item {
  transition: all 0.5s;
}

.op-button {
  transition: all 0.2s;
}

.op-show {
  transition: all 0.2s;
}

.info-box-enter {
  opacity: 0;
}

.info-box-leave-to {
  opacity: 0;
}

.info-wrap {
  transition: all 0.5s;
}

</style>
