// utilities

const async_post = async function(url, body) {
    // token
    let token = document.querySelector('meta[name="X-CSRF-TOKEN"]').getAttribute('content')
    if (token === undefined) {
        throw "ERROR: token is not defined."
    }
    // body
    let json_data = JSON.stringify(body)
    if (process.env.VUE_APP_DEBUG) {
        console.log(`POST: ${url}`)
        console.log(`BODY: ${json_data}`)
    }
    // call fetch
    const result = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': token,
        },
        body: json_data,
    })
    .then(response => response.json().then(
        json_data => ({ code: response.status, data: json_data }))
    )
    .catch((error) => {
        if (process.env.VUE_APP_DEBUG) {
            window.alert('通信エラーがおきました。', error)
        }
        return { code: -1, data: { detail: `communication error: ${error}`} }
    })
    // result
    if (process.env.VUE_APP_DEBUG) {
        console.log(`RES: ${JSON.stringify(result)}`)
    }
    return result
}

const inputRequired = (v) => (!!v || '入力して下さい。')

const selectRequired = (v) => (!!v || '選択して下さい。')

const emailAddrCheck = (v) => {
    // 本気でチェックするとガチで面倒くさいので程々にやる。
    if (!v) {
        return 'メールアドレスを、入力して下さい。'
    } else if (!/^.+@.+\..+$/.test(v)) {
        return 'メールアドレスを、入力して下さい。'
    } else
        return true
}

/*
const postcodeCheck = (v) => (
    !v || /[0-9]{3}-[0-9]{4}|[0-9]{7}/.test(v) || '半角数字で入力して下さい。'
)

const yearsList = () => {
    let a = []
    for (let i = 2022; i > 1910; i--) {
        a.push({text:`${i}年`,value:`${i}`})
    }
    return a
}

const monthsList = [
    { text: '1月', value: '01' },
    { text: '2月', value: '02' },
    { text: '3月', value: '03' },
    { text: '4月', value: '04' },
    { text: '5月', value: '05' },
    { text: '6月', value: '06' },
    { text: '7月', value: '07' },
    { text: '8月', value: '08' },
    { text: '9月', value: '09' },
    { text: '10月', value: '10' },
    { text: '11月', value: '11' },
    { text: '12月', value: '12' },
]

const daysList = [
    { text: '1日', value: '01' },
    { text: '2日', value: '02' },
    { text: '3日', value: '03' },
    { text: '4日', value: '04' },
    { text: '5日', value: '05' },
    { text: '6日', value: '06' },
    { text: '7日', value: '07' },
    { text: '8日', value: '08' },
    { text: '9日', value: '09' },
    { text: '10日', value: '10' },
    { text: '11日', value: '11' },
    { text: '12日', value: '12' },
    { text: '13日', value: '13' },
    { text: '14日', value: '14' },
    { text: '15日', value: '15' },
    { text: '16日', value: '16' },
    { text: '17日', value: '17' },
    { text: '18日', value: '18' },
    { text: '19日', value: '19' },
    { text: '20日', value: '20' },
    { text: '21日', value: '21' },
    { text: '22日', value: '22' },
    { text: '23日', value: '23' },
    { text: '24日', value: '24' },
    { text: '25日', value: '25' },
    { text: '26日', value: '26' },
    { text: '27日', value: '27' },
    { text: '28日', value: '28' },
    { text: '29日', value: '29' },
    { text: '30日', value: '30' },
    { text: '31日', value: '31' },
]
*/

const is_phone = (v) => (
    !v || /^[\d+-]+$/.test(v) || '半角数字で入力して下さい。半角ハイフンがあっても構いません。'
)

const nationsList = [
    { text: '日本', value: 'Japan' },
    { text: 'Australia', value: 'Australia' },
    { text: 'Belgium', value: 'Belgium' },
    { text: 'Canada', value: 'Canada' },
    { text: 'France', value: 'France' },
    { text: 'Germany', value: 'Germany' },
    { text: 'India', value: 'India' },
    { text: 'Italy', value: 'Italy' },
    { text: 'Malaysia', value: 'Malaysia' },
    { text: 'Netherlands', value: 'Netherlands' },
    { text: 'Philippines', value: 'Philippines' },
    { text: 'Russia', value: 'Russia' },
    { text: 'Singapore', value: 'Singapore' },
    { text: 'Spain', value: 'Spain' },
    { text: 'Sweden', value: 'Sweden' },
    { text: 'Switzerland', value: 'Switzerland' },
    { text: 'Thailand', value: 'Thailand' },
    { text: 'United Kingdom', value: 'United Kingdom' },
    { text: 'United States', value: 'United States' },
    { text: 'Vietnam', value: 'Vietnam' },
    { text: '中国', value: 'China' },
    { text: '台灣', value: 'Taiwan' },
    { text: '대한민국', value: 'South Korea' },
    { text: 'United States', value: 'United States' },
    { text: 'Other', value: 'Other' },
]

const generatePastDateList = (date_string) => {
    /*
    過去14日間の日付の文字列を返す。
    date_string: YYYY-MM-DD
    return: {
        label: <YYYY-MM-DD>,
        local: <MM年DD>,
        dayWeek: <(WEEK DAY)>,
        annotate: <(n日前)>,
        }
    */
    let start_date = new Date(date_string)
    let ts = start_date.getTime()
    let dateList = []
    for (let j = 0; j < 14; j++) {
        let dto = new Date(ts)
        let yyyy = '' + dto.getFullYear()
        let mm = '' + (1 + dto.getMonth())
        if (mm.length == 1) {
            mm = '0' + mm
        }
        let dd = '' + dto.getDate()
        if (dd.length == 1) {
            dd = '0' + dd
        }
        let dw = ['日','月','火','水','木','金','土'][dto.getDay()]
        let annotate = j == 0 ? '発症日' : `${j}日前`
        dateList.push({
            label: [yyyy,mm,dd].join('-'),
            local: `${mm}月${dd}日`,
            dayWeek: `(${dw})`,
            annotate: `${annotate}`,  
            })
            ts -= 86400000
    }
    return dateList
}

export default {
    async_post,
    inputRequired,
    selectRequired,
    is_phone,
    emailAddrCheck,
    /*
    postcodeCheck,
    yearsList,
    monthsList,
    daysList,
    */
    nationsList,
    generatePastDateList,
}
