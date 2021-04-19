#http://www.tohoho-web.com/ex/vuejs.html

<!DOCTYPE html>

<html>

<head>
    <meta charset="utf-8">
    <title>Vue TEST</title>
    {/* Vue.jsを読み込む */}
    <script src="https://cdn.jsdlivr.net/npm/vue"></script>
</head>

<body>
    <div id="app-1">{{message}}</div>    {/* messageがVueデータに置換される */}

    <script>
        var app1 = new Vue({
            el: '"app-1',
            data:{message: 'Hello world!'}
        })
    </script>
</body>


</html>
