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
.basefont {
    font-family: 'M PLUS Rounded 1c';
    .wf-roundedmplus1c { font-family: "M PLUS Rounded 1c"; };
    font-weight: bolder;
}
.font-large {
    font-size: 200%;
}
.basecolor {
    background-color: #03AF7A;
    color: white;
}
.subcolor {
    background-color: white;
    color: black;
}
#hr-white {
    border-width: 3px 0 0 0;
    border-color: white;
    border-radius: 2px 2px 2px 2px;
}
#hr-black {
    border-width: 3px 0 0 0;
    border-color: black;
    border-radius: 2px 2px 2px 2px;
}
</style>
