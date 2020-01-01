
function highlight(elem){
                elem.style.color = "red";
                elem.parentElement.parentElement.style.transform="scale(1.5)";
                setTimeout(function(){
                    elem.style.color="";
                    elem.parentElement.parentElement.style.transform="scale(1)";
                },300);
            }
