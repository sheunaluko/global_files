//file for synth stuff

var ctx = new AudioContext()


export function osc(type , freq, gainVal){
    var _osc = ctx.createOscillator()
    _osc.frequency.value = freq
    var gain = ctx.createGain()
    _osc.type = type
    gain.connect(ctx.destination)
    gain.gain.value = gainVal
    _osc.connect(gain)
    _osc.start()
    return _osc 
} 













