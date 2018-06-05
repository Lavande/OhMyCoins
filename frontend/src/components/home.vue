<template>
  <div class="home_wrap">
    <div class="navBar">
      <span class="logo"></span>
      Oh My Coins!
    </div>
    <!-- 基本信息 -->
    <div class="block">
      <h1 class="title">持仓信息</h1>
      <div class="table_wrap">
        <table>
          <thead>
            <tr>
              <th>Token</th>
              <th>Price</th>
              <th>Amount</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="n in tableData">
              <td>{{n.Token}}</td>
              <td>{{n.Price}}</td>
              <td>{{n.Amount}}</td>
              <td>{{n.Value}}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="base_right">
        <div class="total_inf">我的身价:<span class="num">{{data.Total}}</span></div>
        <!-- 饼图 -->
        <div class="pie_pic" id="pie_pic"></div>
      </div>
    </div>
    <!-- 折线图 -->
    <div class="block">
      <h1 class="title">币价与开发进度相关信息</h1>
      <!-- 折线图1 -->
      <div class="line_pic" id="line_pic1"></div>
      <p class="line_pic_txt">相关系数：{{this.btcxs}}</p>
      <!-- 折线图2 -->
      <div class="line_pic" id="line_pic2"></div>
      <p class="line_pic_txt">相关系数：{{this.eosxs}}</p>
      <!-- 折线图3 -->
      <div class="line_pic" id="line_pic3"></div>
      <p class="line_pic_txt">相关系数：{{this.ethxs}}</p>
    </div>
    <div class="block">
      <div class="left_con">
        <div class="title">词云</div>
        <div class="word_cloud" id="word_cloud"></div>
      </div>
      <!-- <div class="right_con">
        <div class="title">情感分析</div>
      </div> -->
    </div>
  </div>
</template>

<script>
import jqcloud from 'jqcloud2';
export default {
  name: 'login',
  data () {
    return {
      data: {},
      tableData:[],
      cloudData:[],
      pieData:[],
      chartsData:[],
      btcxs:'',
      eosxs:'',
      ethxs:''
    }
  },
  mounted(){
    if(localStorage){
      this.data=JSON.parse(localStorage.getItem('data'));
      console.log(this.data)
    }
    this.setData();
    this.initAllPic();
  },
  methods:{
    setData(){
      this.tableData=this.data.Table;
      this.cloudData=this.data.Cloud;
      this.cloudData.forEach((item,index)=>{
        item.weight=item.weight*10;
      });
      this.pieData=this.data.Pie;
      this.chartsData=this.data.Charts;
      this.btcxs=this.chartsData.BTC[2];
      this.eosxs=this.chartsData.EOS[2];
      this.ethxs=this.chartsData.ETH[2];
    },
    //初始化图标
    initAllPic(){
      this.drawPie();
      this.drawLine1();
      this.drawLine2();
      this.drawLine3();
      this.wordCloud()
    },
    //饼图
    drawPie(){
      // 基于准备好的dom，初始化echarts实例
      let myChart = this.$echarts.init(document.getElementById('pie_pic'))
      // 绘制图表
      myChart.setOption({
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        series : [
            {
                name: '币种',
                type: 'pie',
                radius : '60%',
                center: ['50%', '50%'],
                data: this.pieData,
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
      });
    },
    drawLine1(){
      // 基于准备好的dom，初始化echarts实例
      let myChart = this.$echarts.init(document.getElementById('line_pic1'))
      // 绘制图表
      myChart.setOption({
        title : {
          text: 'BTC',
          left:'10'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
              type: 'cross',
              crossStyle: {
                  color: '#999'
              }
          }
        },
        legend: {
            top:'10%',
            data:['价格','代码提交次数']
        },
        grid: {
            left: '3%',
            right: '3%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            show:false
        },
        yAxis: [
          {
              type: 'value',
              name: '价格',
              axisLabel: {
                  formatter: '{value} $'
              }
          },
          {
              type: 'value',
              name: '次数',
              axisLabel: {
                  formatter: '{value} 次'
              }
          }
        ],
        series: [
            {
                name:'价格',
                type:'line',
                stack: '总量',
                data:this.chartsData.BTC[0]
            },
            {
                name:'代码提交次数',
                type:'line',
                stack: '总量',
                yAxisIndex: 1,
                data:this.chartsData.BTC[1]
            }
        ]
      });
    },
    drawLine2(){
      // 基于准备好的dom，初始化echarts实例
      let myChart = this.$echarts.init(document.getElementById('line_pic2'))
      // 绘制图表
      myChart.setOption({
        title : {
          text: 'EOS',
          left:'10'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
              type: 'cross',
              crossStyle: {
                  color: '#999'
              }
          }
        },
        legend: {
            top:'10%',
            data:['价格','代码提交次数']
        },
        grid: {
            left: '3%',
            right: '3%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            show:false
        },
        yAxis: [
          {
              type: 'value',
              name: '价格',
              axisLabel: {
                  formatter: '{value} $'
              }
          },
          {
              type: 'value',
              name: '次数',
              axisLabel: {
                  formatter: '{value} 次'
              }
          }
        ],
        series: [
            {
                name:'价格',
                type:'line',
                stack: '总量',
                data:this.chartsData.EOS[0]
            },
            {
                name:'代码提交次数',
                type:'line',
                stack: '总量',
                yAxisIndex: 1,
                data:this.chartsData.EOS[1]
            }
        ]
      });
    },
    drawLine3(){
      // 基于准备好的dom，初始化echarts实例
      let myChart = this.$echarts.init(document.getElementById('line_pic3'))
      // 绘制图表
      myChart.setOption({
        title : {
          text: 'ETH',
          left:'10'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
              type: 'cross',
              crossStyle: {
                  color: '#999'
              }
          }
        },
        legend: {
            top:'10%',
            data:['价格','代码提交次数']
        },
        grid: {
            left: '3%',
            right: '3%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            show:false
        },
        yAxis: [
          {
              type: 'value',
              name: '价格',
              axisLabel: {
                  formatter: '{value} $'
              }
          },
          {
              type: 'value',
              name: '次数',
              axisLabel: {
                  formatter: '{value} 次'
              }
          }
        ],
        series: [
            {
                name:'价格',
                type:'line',
                stack: '总量',
                data:this.chartsData.ETH[0]
            },
            {
                name:'代码提交次数',
                type:'line',
                stack: '总量',
                yAxisIndex: 1,
                data:this.chartsData.ETH[1]
            }
        ]
      });
    },
    //词云
    wordCloud(){
      let data = this.cloudData;
      $("#word_cloud").jQCloud(data,{
        autoResize: true
      });
    }
  }
}
</script>

<style lang="scss">
@import '../../node_modules/jqcloud2/dist/jqcloud.min.css';
.home_wrap{
  width: 100%;
  .navBar{
    display: flex;
    justify-content: center;
    width: 100%;
    height: 60px;
    background: rgba(255,255,255,.8);
    box-shadow: rgba(0,0,0,0.2) 0px 1px 12px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    line-height: 60px;
    .logo{
      display: inline-block;
      width: 40px;
      height: 40px;
      background: url('../assets/bitcoin.png') 0 0 no-repeat;
      background-size: cover;
      margin-right:10px;
      position: relative;
      top: 10px;
      // margin-top: 10px;
    }
  }
  .block{
    width: 1080px;
    min-height: 300px;
    background: white;
    margin: 0 auto;
    margin-top: 30px;
    border-radius: 6px;
    box-sizing: border-box;
    padding: 15px;
    overflow: hidden;
    .title{
      margin-bottom: 10px;
      line-height: 30px;
      font-size: 20px;
      color:#59718a;
    }
    //持仓信息表格
    .table_wrap{
      float: left;
      width: 55%;
      height: 500px;
      overflow-x: hidden;
      overflow-y: scroll;
      table{
				width: 100%;
				border-collapse: collapse;
			}
			td{
				padding: 6px 9px;
        text-align: center;
			}
      tr{
        border-bottom: 1px solid #e3e3e3;
        height: 36px;
      }
			thead{
				background-color: #59718a;
				color: white;
				border-bottom: 1px solid #e3e3e3;
			}
			tbody>tr:nth-child(2n){
				background-color: #eee;
			}
    }
    //右侧内容
    .base_right{
      width: 45%;
      box-sizing: border-box;
      padding: 0 20px;
      float: left;
      .total_inf{
        // position: relative;
        background: rgba(89,113,138,.7);
        border-radius: 6px;
        color: white;
        font-size: 18px;
        height: 50px;
        line-height: 50px;
        margin: 0 0 20px 0;
        box-sizing: border-box;
        padding: 0 10px;
        text-align: center;
        .num{
          font-weight: bold;
          font-size: 24px;
          line-height: 50px;
          display: inline-block;
          margin-left: 10px;
          // position: absolute;
          // left: 50%; 
          // transform: translateX(-50%);
        }
      }
      .pie_pic{
        width: 400px;
        height: 400px;
      }
    }
    //折线图
    .line_pic{
      width: 100%;
      height: 200px;
      //margin-bottom: 10px;
      margin: 10px auto;
    }
    .line_pic_txt{
      line-height: 30px;
      font-size: 16px;
      text-align: center;
      margin-bottom: 20px;
    }
    .left_con,.right_con{
      width:100%;
      // width:50%;
      height: 400px;
      float: left;
      .title{
        margin-bottom: 10px;
        line-height: 30px;
        font-size: 20px;
        color:#59718a;
      }
      .word_cloud{
        width: 800px;
        height: 300px;
        margin: 0 auto;
      }
    }
  }
}
</style>
