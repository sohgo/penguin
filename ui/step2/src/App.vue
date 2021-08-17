<template>
    <div>
        <router-view></router-view>
    </div>
</template>

<script>
export default {
}
</script>

<style>
body {
    /* type square font setting
    font-family:Shin Maru Go Medium,Simplon Norm,Roboto,Segoe UI,Helvetica Neue,HelveticaNeue,Arial,Noto Sans JP,Hiragino Kaku Gothic ProN,Hiragino Sans,Meiryo,sans-serif;*/
    /* adobe creative cloud font setting */
    font-family:a-otf-ud-shin-maru-go-pr6n,	Simplon Norm,Roboto,Segoe UI,Helvetica Neue,HelveticaNeue,Arial,Noto Sans JP,Hiragino Kaku Gothic ProN,Hiragino Sans,Meiryo,sans-serif;
    font-weight: 700;
    font-style: normal;
    /* end adobe creative cloud font setting */
    font-feature-settings: "palt";
    -webkit-font-smoothing: antialiased;
    font-size: 0.914rem;
}.
.entry-bg {
    background-color: #03AF7A;
}
.basefont {
    font-family: 'M PLUS Rounded 1c';
    .wf-roundedmplus1c { font-family: "M PLUS Rounded 1c"; };
    font-weight: bolder;
}
.header {
    background-color: #03AF7A;
    color:#FFF;
    font-size:1rem;
    font-weight: bold;
}
h1 {
    font-size:1.4rem;
    line-height: 1.8rem;
    border-bottom:3px solid #333;
    padding-bottom:1.3rem;
    font-weight: bold;
}
h1.entry {
    border-bottom: 3px solid #FFF;
}
h2 {
    font-size:1.14rem;
    font-weight: bold;
    background-color: #03AF7A;
    color:#FFF;
    padding:1rem;
    margin:0 -30px;
    margin-top:3rem;    
    margin-bottom:1rem; 
}
h3 {
    font-size:1rem;
    font-weight: bold;
}
.workplace-header {
    padding:6px 0px 6px 8px;
    border-left:6px solid rgb(3 175 122);
    background: rgba(3,175,122,0.1);
    margin-top:2rem;
}
.daily-input-title .v-messages {
    font-size: 0;
    min-height: 0;
}
.daily-input-section {
    font-size:1.14rem;
    font-weight: bold;
    background-color: #03AF7A;
}
h4 {
    font-size:0.95rem;
}
p {
    line-height: 180%;
    font-size: 1rem;
}

.btn-tag{
    margin-top: 8px;
    border: none;
    border-radius: 5px;
    margin-right: 0.34rem;
    background-color: #FFBBBB;
}
</style>
