var express = require('express');
var router = express.Router();
const execSync = require('child_process').execSync;
var path = require('path');

router.get('/', function(req, res, next) {
    res.render('home', {
        x_len: 7,
        y_len: 7,
    });
});

async function run_auto_gui(x,y,board) {
    py_run_filepath = path.resolve(__dirname, "..", "..", "run", "run_py.sh")

    let code = execSync("/bin/sh "+ py_run_filepath+" " +x +" "+  y + " " + String(board)).toString();

    console.log(code)

    code = code.split("\n")
    code = code[code.length - 2]
    console.log("------------", code)
    code = await JSON.parse(code)

    return code
}


router.get('/tmp/:i/:j/:board', function(req, res){

    let y = req.params.i;
    let x = req.params.j;
    let board = req.params.board;

    (async () => {
    
        ret_s  = await run_auto_gui(x,y, board);

        res.json({
            statusCode: "done", 
            value: "historical_vals",
            x: ret_s["x"],
            y: ret_s["y"],
            status: ret_s["status"]
           });
       
    })();

});

module.exports = router;