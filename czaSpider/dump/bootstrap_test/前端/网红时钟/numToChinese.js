let chnNumChar = ["零","壹","贰","叁","肆","伍","陆","柒","捌","玖"];
let chnUnitSection = ["","万","亿","万亿","亿亿"];
let chnUnitChar = ["","拾","佰","仟"];

function SectionToChinese(section){
    let strIns = '', chnStr = '';
    let unitPos = 0;
    let zero = true;
    while(section > 0){
        let v = section % 10;
        if(v === 0){
            if(!zero){
                zero = true;
                chnStr = chnNumChar[v] + chnStr;
            }
        }else{
            zero = false;
            strIns = chnNumChar[v];
            strIns += chnUnitChar[unitPos];
            chnStr = strIns + chnStr;
        }
        unitPos++;
        section = Math.floor(section / 10);
    }
    return chnStr;
}

function NumberToChinese(num){
    let unitPos = 0;
    let strIns = '', chnStr = '';
    let needZero = false;

    if(num === 0){
        return chnNumChar[0];
    }

    while(num > 0){
        let section = num % 10000;
        if(needZero){
            chnStr = chnNumChar[0] + chnStr;
        }
        strIns = SectionToChinese(section);
        strIns += (section !== 0) ? chnUnitSection[unitPos] : chnUnitSection[0];
        chnStr = strIns + chnStr;
        needZero = (section < 1000) && (section > 0);
        num = Math.floor(num / 10000);
        unitPos++;
    }

    return chnStr;
}