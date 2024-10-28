function checkDevice(){//もしPCだったらtrue, タッチ式のスマホやタブレット、ipadだったらfalse
    if(navigator.userAgent.match(/(iPhone|iPad|iPod|Android)/i)){
        return false
    }else{
        return true
    }
}