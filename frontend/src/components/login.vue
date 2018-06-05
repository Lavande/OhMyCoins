<template>
  <div class="login_wrap">
    <div class="login_box">
      <p class="title">Oh My Coins</p>
      <div class="line">
        <div class="label">自定义币种:</div>
        <input type="text" v-model="other_bl">
      </div>
      <div class="line">
        <div class="label">地址:</div>
        <input type="text" v-model="addresses">
      </div>
      <div class="cutline">通过交易所API查询余额</div>
      <div class="line">
        <div class="label">bittrex apikey:</div>
        <input type="text" v-model="bittrex_apikey">
      </div>
      <div class="line">
        <div class="label">bittrex apisecret:</div>
        <input type="text" v-model="bittrex_apisecret">
      </div>
      <div class="line">
        <div class="label">poloniex apikey:</div>
        <input type="text" v-model="poloniex_apikey">
      </div>
      <div class="line">
        <div class="label">poloniex apisecret:</div>
        <input type="text" v-model="poloniex_apisecret">
      </div>
      <div class="line">
        <div class="label">bitfinex apikey:</div>
        <input type="text" v-model="bitfinex_apikey">
      </div>
      <div class="line">
        <div class="label">bitfinex apisecret:</div>
        <input type="text" v-model="bitfinex_apisecret">
      </div>
      <div class="line">
        <div class="label">bigone apikey:</div>
        <input type="text" v-model="bigone_apikey">
      </div>
      <div class="line">
        <div class="btn" @click="getData">走你!~</div>
      </div>
    </div>

    <!-- loading -->
    <div class="loading_wrap" v-if="showLoading">
      <div class="loading"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'login',
  data () {
    return {
      //自定义币种
      other_bl: '',
      //地址
      addresses: '',
      //通过交易所API查询余额
      bittrex_apikey: '',
      bittrex_apisecret: '',
      poloniex_apikey: '',
      poloniex_apisecret: '',
      bitfinex_apikey: '',
      bitfinex_apisecret: '',
      bigone_apikey: '',
      param:{},
      showLoading:false
    }
  },
  methods:{
    setParame(){
      this.param={
        other_bl:this.other_bl,
        addresses:this.addresses,
      };
      if(this.bittrex_apikey){
        this.param.bittrex_apikey=this.bittrex_apikey
      };
      if(this.bittrex_apisecret){
        this.param.bittrex_apisecret=this.bittrex_apisecret
      };
      if(this.poloniex_apisecret){
        this.param.poloniex_apisecret=this.poloniex_apisecret
      };
      if(this.poloniex_apisecret){
        this.param.poloniex_apisecret=this.poloniex_apisecret
      };
      if(this.bitfinex_apikey){
        this.param.bitfinex_apikey=this.bitfinex_apikey
      };
      if(this.bitfinex_apisecret){
        this.param.bitfinex_apisecret=this.bitfinex_apisecret
      };
      if(this.bigone_apikey){
        this.param.bigone_apikey=this.bigone_apikey
      };
    },
    getData(){
      this.setParame();
      console.log(this.param);
      this.showLoading=true;
      $.post("http://127.0.0.1:5050",this.param,(result)=>{
        if(result){
          console.log(result);
          this.showLoading=false;
          localStorage.setItem('data',JSON.stringify(result));
          this.goHome();
        }else{
          this.showLoading=false;
          alert("something wrong!");
        }
      });
    },
    goHome(){
      this.$router.push({path:'/home'});
    }
  }
}
</script>

<style lang="scss">
.login_wrap{
  width: 100%;
  .login_box{
    width: 550px;
    margin: 0 auto;
    margin-top: 60px;
    background: rgba(255,255,255, .6);
    padding: 20px;
    border-radius: 6px;
    box-sizing: border-box;
    .title{
      text-align: center;
      font-size: 24px;
      margin: 15px auto;
    }
    .cutline{
      height: 30px;
      margin: 20px auto;
      font-size: 16px;
      color: #5e5e5e;
      line-height: 30px;
      text-align: center;
      background: url('../assets/cutline.png') center center no-repeat;
    }
    .line{
      width: 100%;
      height: 36px;
      margin-bottom: 10px;
      &:last-child{
        margin-top: 30px;
      }
      .label{
        width: 25%;
        display: inline-block;
        text-align: right;
        line-height: 36px;
        font-size: 14px;
        margin-right: 15px;
      }
      input{
        width: 70%;
        height: 36px;
        border: none;
        border-radius: 3px;
        padding: 0 10px;
        box-sizing: border-box;
      }
      .btn{
        width: 100px;
        height: 36px;
        background: #59718a;
        text-align: center;
        line-height: 36px;
        font-size: 16px;
        margin: 0 auto;
        border-radius: 6px;
        color: white;
        cursor: pointer;
      }
    }
  }
  .loading_wrap{
    position: fixed;
    left: 0;
    top: 0;
    right:0;
    bottom: 0;
    background: rgba(0,0,0,.5);
    .loading{
      width: 64px;
      height: 64px;
      background: url('../assets/loading.gif') 0 0 no-repeat;
      background-size: cover;
      position: absolute;
      left: 50%;
      top:50%;
      margin-top: -32px;
      margin-left: -32px;
    }
    
  }
}
</style>
