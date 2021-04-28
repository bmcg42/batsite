function spectro(){
    //var f = eel.spectrogram(document.getElementById("input").files[0])
    //image(f)
    output_filename(document.getElementById("filename").value)
}

function image(filename){
    document.getElementById("output").src=filename
}
