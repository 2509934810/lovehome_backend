
sendreq = {
    'get': function(args){
        args['method'] = "get"
        axios({
            args
        })
    },
    "post": function(args){
        axios({
            args
        })
    }
}
