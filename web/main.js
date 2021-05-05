async function spectro(){

    var input_file = document.getElementById("input").files[0].name
    let newTable = document.createElement("table")
    const img_id = document.getElementById('output_image')
    const div_id = document.getElementById('spl_table')
    const title_id = document.createElement('H2')
    var title = document.createTextNode("SPL Data Table");
    title_id.appendChild(title)
    console.log('creating spectrogram from file ' + input_file +  '...')
    // put stream fucntion here
    var h =  eel.SPL_Table(input_file)()
    console.log(h)
    newTable.innerHTML = await eel.SPL_Table(input_file)()
    document.body.insertBefore(newTable, img_id)
    div_id.appendChild(title_id)
    div_id.appendChild(newTable)
    console.log('created SPL Table')

    //loop through to calculate snps and add them to columns
    //loop through blocks and append spectrogram data to file_bytes
    console.log('Creating Spectrogram')
    eel.spectrogram(input_file)(image)
    console.log('Done')
}
function image(file_bytes){
    document.getElementById('output').src = "data:image/jpg;base64," + file_bytes
}
