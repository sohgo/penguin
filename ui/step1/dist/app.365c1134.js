(function(t){function e(e){for(var l,n,i=e[0],o=e[1],u=e[2],v=0,d=[];v<i.length;v++)n=i[v],Object.prototype.hasOwnProperty.call(r,n)&&r[n]&&d.push(r[n][0]),r[n]=0;for(l in o)Object.prototype.hasOwnProperty.call(o,l)&&(t[l]=o[l]);c&&c(e);while(d.length)d.shift()();return s.push.apply(s,u||[]),a()}function a(){for(var t,e=0;e<s.length;e++){for(var a=s[e],l=!0,i=1;i<a.length;i++){var o=a[i];0!==r[o]&&(l=!1)}l&&(s.splice(e--,1),t=n(n.s=a[0]))}return t}var l={},r={app:0},s=[];function n(e){if(l[e])return l[e].exports;var a=l[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,n),a.l=!0,a.exports}n.m=t,n.c=l,n.d=function(t,e,a){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},n.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(n.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var l in t)n.d(a,l,function(e){return t[e]}.bind(null,l));return a},n.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="/1/";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],o=i.push.bind(i);i.push=e,i=i.slice();for(var u=0;u<i.length;u++)e(i[u]);var c=o;s.push([0,"chunk-vendors"]),a()})({0:function(t,e,a){t.exports=a("56d7")},"034f":function(t,e,a){"use strict";a("85ec")},"199c":function(t,e){},"23be":function(t,e,a){"use strict";var l=a("199c"),r=a.n(l);e["default"]=r.a},"3dfd":function(t,e,a){"use strict";var l=a("ea4a"),r=a("23be"),s=(a("034f"),a("2877")),n=Object(s["a"])(r["default"],l["a"],l["b"],!1,null,null,null);e["default"]=n.exports},"56d7":function(t,e,a){"use strict";a.r(e);var l=a("2b0e"),r=a("3dfd"),s=a("f309");l["a"].use(s["a"]);var n=new s["a"]({}),i=a("8c4f"),o=a("77ef"),u=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-app",[a("v-app-bar",{staticClass:"basefont white--text text-center",attrs:{color:"#03AF7A",elevation:"0",dense:"",app:""}},[a("v-btn",{attrs:{icon:"",to:"/"}},[a("v-icon",{staticClass:"white--text",attrs:{link:""}},[t._v("mdi-arrow-left")])],1),a("v-spacer"),a("v-app-bar-title",[t._v(" 個人情報の設定 ")]),a("v-spacer")],1),a("v-main",{staticClass:"white"},[a("div",{staticClass:"ma-3"},[a("h3",{staticClass:"my-3"},[t._v(" あなたの氏名、誕生月日、"),a("br"),t._v(" 好みの色を入力して下さい。 ")]),a("v-divider",{attrs:{id:"hr-balck"}}),a("v-form",{ref:"baseform",staticClass:"mx-3",attrs:{"lazy-validation":""},model:{value:t.valid,callback:function(e){t.valid=e},expression:"valid"}},[a("v-text-field",{staticClass:"mt-3",attrs:{label:"氏名",rules:t.inputRequired,required:""},model:{value:t.formData.name,callback:function(e){t.$set(t.formData,"name",e)},expression:"formData.name"}}),a("v-text-field",{attrs:{label:"ふりがな",rules:t.kanaRules,required:""},model:{value:t.formData.kana,callback:function(e){t.$set(t.formData,"kana",e)},expression:"formData.kana"}}),a("v-row",[a("v-col",{staticClass:"mt-3"},[t._v("誕生月日")]),a("v-col",[a("v-select",{attrs:{label:"月",items:t.birthMList,rules:t.selectRequired,required:""},model:{value:t.formData.birthM,callback:function(e){t.$set(t.formData,"birthM",e)},expression:"formData.birthM"}})],1),a("v-col",[a("v-select",{attrs:{label:"日",items:t.birthDList,rules:t.selectRequired,required:""},model:{value:t.formData.birthD,callback:function(e){t.$set(t.formData,"birthD",e)},expression:"formData.birthD"}})],1)],1),a("v-text-field",{staticClass:"mt-3",attrs:{label:"メールアドレス",rules:t.emailAddrRules,required:""},model:{value:t.formData.emailAddr,callback:function(e){t.$set(t.formData,"emailAddr",e)},expression:"formData.emailAddr"}}),a("v-select",{staticClass:"mb-3",attrs:{label:"好みの色",items:t.favColorsList,rules:t.selectRequired,required:""},model:{value:t.formData.favColor,callback:function(e){t.$set(t.formData,"favColor",e)},expression:"formData.favColor"}})],1),a("v-btn",{staticClass:"pa-5",attrs:{color:"#03AF7A",block:""},on:{click:t.submitData}},[a("span",{staticClass:"pa-2 white--text font-large"},[t._v(" 登録する ")])])],1)])],1)},c=[];const v=async function(t,e){let a=document.querySelector('meta[name="X-CSRF-TOKEN"]').getAttribute("content");if(void 0===a)throw"ERROR: token is not defined.";let l=JSON.stringify(e);console.log("POST: "+t),console.log("BODY: "+l);const r=await fetch(t,{method:"POST",headers:{"Content-Type":"application/json","X-CSRF-TOKEN":a},body:l}).then(t=>t.json().then(e=>({code:t.status,data:e}))).catch(t=>(window.alert("通信エラーがおきました。",t),{code:-1,data:{}}));return console.log("RES: "+JSON.stringify(r)),r},d=t=>!!t||"入力して下さい。",p=t=>!!t||"選択して下さい。",f=t=>t?!!_(t)||"ひらがなで入力して下さい。":"ふりがなを、入力して下さい。",m=t=>t&&!!/^.+@.+\..+$/.test(t)||"メールアドレスを、入力して下さい。",x=t=>!t||/[0-9]{3}-[0-9]{4}|[0-9]{7}/.test(t)||"半角数字で入力して下さい。",b=()=>{let t=[];for(let e=2022;e>1910;e--)t.push({text:e+"年",value:""+e});return t},h=[{text:"1月",value:"01"},{text:"2月",value:"02"},{text:"3月",value:"03"},{text:"4月",value:"04"},{text:"5月",value:"05"},{text:"6月",value:"06"},{text:"7月",value:"07"},{text:"8月",value:"08"},{text:"9月",value:"09"},{text:"10月",value:"10"},{text:"11月",value:"11"},{text:"12月",value:"12"}],y=[{text:"1日",value:"01"},{text:"2日",value:"02"},{text:"3日",value:"03"},{text:"4日",value:"04"},{text:"5日",value:"05"},{text:"6日",value:"06"},{text:"7日",value:"07"},{text:"8日",value:"08"},{text:"9日",value:"09"},{text:"10日",value:"10"},{text:"11日",value:"11"},{text:"12日",value:"12"},{text:"13日",value:"13"},{text:"14日",value:"14"},{text:"15日",value:"15"},{text:"16日",value:"16"},{text:"17日",value:"17"},{text:"18日",value:"18"},{text:"19日",value:"19"},{text:"20日",value:"20"},{text:"21日",value:"21"},{text:"22日",value:"22"},{text:"23日",value:"23"},{text:"24日",value:"24"},{text:"25日",value:"25"},{text:"26日",value:"26"},{text:"27日",value:"27"},{text:"28日",value:"28"},{text:"29日",value:"29"},{text:"30日",value:"30"},{text:"31日",value:"31"}],C=[{text:"あか",value:"red"},{text:"あお",value:"blue"},{text:"みどり",value:"green"},{text:"きいろ",value:"yellow"},{text:"オレンジ",value:"orange"},{text:"みずいろ",value:"cyan"},{text:"しろ",value:"white"},{text:"くろ",value:"black"}],_=t=>!!t&&(!!t.length&&(" "!=t&&/^[ぁ-ゔー\s\u3000・]*$/.test(t))),D=[{text:"日本",value:"Japan"},{text:"Australia",value:"Australia"},{text:"Belgium",value:"Belgium"},{text:"Canada",value:"Canada"},{text:"France",value:"France"},{text:"Germany",value:"Germany"},{text:"India",value:"India"},{text:"Italy",value:"Italy"},{text:"Malaysia",value:"Malaysia"},{text:"Netherlands",value:"Netherlands"},{text:"Philippines",value:"Philippines"},{text:"Russia",value:"Russia"},{text:"Singapore",value:"Singapore"},{text:"Spain",value:"Spain"},{text:"Sweden",value:"Sweden"},{text:"Switzerland",value:"Switzerland"},{text:"Thailand",value:"Thailand"},{text:"United Kingdom",value:"United Kingdom"},{text:"United States",value:"United States"},{text:"Vietnam",value:"Vietnam"},{text:"中国",value:"China"},{text:"台灣",value:"Taiwan"},{text:"대한민국",value:"South Korea"},{text:"United States",value:"United States"},{text:"Other",value:"Other"}];var w={async_post:v,inputRequired:d,selectRequired:p,is_kana:_,postcodeCheck:x,emailAddrCheck:m,kanaRequired:f,yearsList:b,monthsList:h,daysList:y,colorsList:C,nationsList:D},S={components:{},data(){return{valid:!1,birthYList:w.yearsList(),birthMList:w.monthsList,birthDList:w.daysList,favColorsList:w.colorsList,inputRequired:[w.inputRequired],selectRequired:[w.selectRequired],kanaRules:[w.kanaRequired],emailAddrRules:[w.emailAddrCheck],formData:{name:"",kana:"",birthM:"",birthD:"",emailAddr:"",favColor:""}}},methods:{submitData:async function(){if(this.$refs.baseform.validate()){let t="/1",e=await w.async_post(t,this.formData);201==e.code&&e.data.xpath?(this.$store.state.formData.xpath=e.data.xpath,this.$router.push("/Step1End")):(this.$store.commit("updateResponseData",e),this.$router.push("/Error"))}}},mounted:function(){this.formData=this.$store.state.formData}},g=S,k=a("2877"),R=a("6544"),O=a.n(R),V=a("7496"),$=a("40dc"),A=a("bb78"),q=a("8336"),E=a("62ad"),M=a("ce7e"),j=a("4bd4"),L=a("132d"),T=a("f6c4"),P=a("0fd9"),F=a("b974"),I=a("2fa4"),B=a("8654"),N=Object(k["a"])(g,u,c,!1,null,null,null),U=N.exports;O()(N,{VApp:V["a"],VAppBar:$["a"],VAppBarTitle:A["a"],VBtn:q["a"],VCol:E["a"],VDivider:M["a"],VForm:j["a"],VIcon:L["a"],VMain:T["a"],VRow:P["a"],VSelect:F["a"],VSpacer:I["a"],VTextField:B["a"]});var J=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-app",[a("v-main",{staticClass:"pa-5 basecolor basefont"},[a("h2",{staticClass:"pb-5"},[t._v(" 初期情報を登録いたしました。"),a("br"),t._v(" ご協力ありがとうございます。 ")]),a("v-divider",{attrs:{id:"hr-white"}}),a("div",{staticClass:"py-3"},[a("div",{staticClass:"my-3"},[t._v(" 次に個人情報"),a("br"),t._v(" を入力して頂きます。 ")]),a("div",{staticClass:"my-3"},[t._v(" ご登録頂いたメールアドレスに"),a("br"),t._v(" 入力フォームを送らせて頂きましたので、"),a("br"),t._v(" 後から入力することも可能でございます。"),a("br")]),a("div",{staticClass:"my-3"},[t._v(" ご確認下さい。 ")])]),a("v-btn",{staticClass:"pa-5",attrs:{color:"white",block:""},on:{click:t.toDetailInput}},[a("span",{staticClass:"black--text font-large"},[t._v("次にすすむ")])])],1)],1)},K=[],z={methods:{toDetailInput:function(){let t=this.$store.state.formData.xpath,e="/2/x/"+t;location.href=e}}},G=z,X=Object(k["a"])(G,J,K,!1,null,null,null),Y=X.exports;O()(X,{VApp:V["a"],VBtn:q["a"],VDivider:M["a"],VMain:T["a"]});var H=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-app",[a("v-main",{staticClass:"pa-5 basecolor basefont"},[a("h2",{staticClass:"pb-5"},[t._v(" エラーが起きました。"),a("br"),t._v(" "+t._s(this.$store.state.responseData.code)+" ")])])],1)},Q=[],W={beforeEach(t,e){console.log(`to:${t.name} from:${e.name}`)}},Z=W,tt=Object(k["a"])(Z,H,Q,!1,null,null,null),et=tt.exports;O()(tt,{VApp:V["a"],VMain:T["a"]});var at=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-app",[a("v-main",{staticClass:"pa-5 basecolor basefont"},[a("h2",{staticClass:"pb-5"},[t._v(" URLに誤りがあります。 ")])])],1)},lt=[],rt={beforeEach(t,e){console.log(`to:${t.name} from:${e.name}`)}},st=rt,nt=Object(k["a"])(st,at,lt,!1,null,null,null),it=nt.exports;O()(nt,{VApp:V["a"],VMain:T["a"]}),l["a"].use(i["a"]);const ot=[{path:"/",name:"Beginning",component:o["default"]},{path:"/Step1Input",name:"Step1Input",component:U},{path:"/Step1End",name:"Step1End",component:Y},{path:"/Error",name:"Error",component:et},{path:"/:pathMatch(.*)*",name:"NotFound",component:it}],ut=new i["a"]({mode:"hash",routes:ot});var ct=ut,vt=a("2f62");l["a"].use(vt["a"]);var dt=new vt["a"].Store({state:{formData:{},responseData:{}},mutations:{updateFormData(t,e){t.formData=e},updateResponseData(t,e){t.responseData=e}},actions:{},modules:{}});l["a"].config.productionTip=!1,new l["a"]({vuetify:n,router:ct,store:dt,render:t=>t(r["default"])}).$mount("#app")},"77ef":function(t,e,a){"use strict";var l=a("cc30"),r=a("dbf4"),s=a("2877"),n=a("6544"),i=a.n(n),o=a("7496"),u=a("8336"),c=a("ce7e"),v=a("f6c4"),d=Object(s["a"])(r["default"],l["a"],l["b"],!1,null,null,null);e["default"]=d.exports,i()(d,{VApp:o["a"],VBtn:u["a"],VDivider:c["a"],VMain:v["a"]})},"85ec":function(t,e,a){},cc30:function(t,e,a){"use strict";a.d(e,"a",(function(){return l})),a.d(e,"b",(function(){return r}));var l=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-app",[a("v-main",{staticClass:"pa-5 basecolor basefont"},[a("h2",{staticClass:"pb-5"},[t._v(" 積極的疫学調査"),a("br"),t._v(" にご協力ください。 ")]),a("v-divider",{attrs:{id:"hr-white"}}),a("div",{staticClass:"py-3"},[a("div",{staticClass:"my-3"},[t._v(" このたびは新型コロナウイルス感染症に罹患され、 大変ご不安だと思います。 ")]),a("div",{staticClass:"my-3"},[t._v(" このアプリではあなたがこれまでにどのような方と 接触してきたのか、また、毎日の体調について 共有して頂くためのインタフェースを提供しています。 ")]),a("div",{staticClass:"my-3"},[t._v(" アプリを使い始める前に、 "),a("div",{staticClass:"ma-2"},[t._v(" 1. あなたの住所などの情報"),a("br"),t._v(" 2. 基礎疾患に関する情報"),a("br")]),t._v(" について登録をお願いします。 ")]),a("div",{staticClass:"my-3"},[t._v(" その後、過去14日間の行動履歴について、 このアプリに登録をして頂きます。 ")]),a("div",{staticClass:"my-3"},[t._v(" 少し時間のかかる作業ではありますが、 新型コロナウイルス感染症の拡大を防止 するために必要ですので、休憩を取りながら、 できるだけ正確な情報の登録を お願いします。 ")]),a("div",{staticClass:"my-3"},[t._v(" よろしくお願いいたします。 ")])]),a("v-btn",{staticClass:"pa-5",attrs:{color:"white",block:"",to:"/Step1Input"}},[a("span",{staticClass:"black--text font-large"},[t._v("はじめる")])])],1)],1)},r=[]},d3a8:function(t,e){},dbf4:function(t,e,a){"use strict";var l=a("d3a8"),r=a.n(l);e["default"]=r.a},ea4a:function(t,e,a){"use strict";a.d(e,"a",(function(){return l})),a.d(e,"b",(function(){return r}));var l=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("router-view")],1)},r=[]}});
//# sourceMappingURL=app.365c1134.js.map