function spectro(){

    var input_file = document.getElementById("input").files[0].name
    var output_fn = document.getElementById("filename").value
    
    console.log('creating spectrogram from file ' + input_file +  '...')
    eel.spectrogram(input_file, output_fn)(image)
}
function image(file_bytes){
    document.getElementById('output').src = "data:image/jpg;base64," + file_bytes
}