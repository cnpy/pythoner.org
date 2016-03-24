$(document).ready(function(){
    $('.topic-content img').each(function(i,d){
        var html = showImg(this.src);
        $(this).after(html);
        $(this).remove(); // 移除原来的img标签
    });

    // show image
    function showImg(url) {
            var frameid = 'frameimg' + Math.random();
            window.img = '<img id="img" src=\''+url+'?'+Math.random()+'\' /><script>window.onload = function() { parent.document.getElementById(\''+frameid+'\').height = document.getElementById(\'img\').height+\'px\'; }<'+'/script>';
            var new_img = '<iframe id="'+frameid+'" src="javascript:parent.img;" frameBorder="0" scrolling="no" width="100%"></iframe>';
            // document.write(new_img);
            return new_img;
    }

});
