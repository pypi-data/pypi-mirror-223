function a(e){const n={className:"variable",variants:[{begin:/\$[\w\d#@][\w\d_]*/},{begin:/\$\{(.*?)\}/}]},r="BEGIN END if else while do for in break continue delete next nextfile function func exit|10",i={className:"string",contains:[e.BACKSLASH_ESCAPE],variants:[{begin:/(u|b)?r?'''/,end:/'''/,relevance:10},{begin:/(u|b)?r?"""/,end:/"""/,relevance:10},{begin:/(u|r|ur)'/,end:/'/,relevance:10},{begin:/(u|r|ur)"/,end:/"/,relevance:10},{begin:/(b|br)'/,end:/'/},{begin:/(b|br)"/,end:/"/},e.APOS_STRING_MODE,e.QUOTE_STRING_MODE]};return{name:"Awk",keywords:{keyword:r},contains:[n,i,e.REGEXP_MODE,e.HASH_COMMENT_MODE,e.NUMBER_MODE]}}export{a as default};
