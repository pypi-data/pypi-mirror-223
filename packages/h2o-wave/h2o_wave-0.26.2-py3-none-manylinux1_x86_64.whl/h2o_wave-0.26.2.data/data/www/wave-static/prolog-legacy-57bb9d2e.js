System.register([],(function(n,e){"use strict";return{execute:function(){n("default",(function(n){var e={begin:/\(/,end:/\)/,relevance:0},a={begin:/\[/,end:/\]/},i={className:"comment",begin:/%/,end:/$/,contains:[n.PHRASAL_WORDS_MODE]},s={className:"string",begin:/`/,end:/`/,contains:[n.BACKSLASH_ESCAPE]},t=[{begin:/[a-z][A-Za-z0-9_]*/,relevance:0},{className:"symbol",variants:[{begin:/[A-Z][a-zA-Z0-9_]*/},{begin:/_[A-Za-z0-9_]*/}],relevance:0},e,{begin:/:-/},a,i,n.C_BLOCK_COMMENT_MODE,n.QUOTE_STRING_MODE,n.APOS_STRING_MODE,s,{className:"string",begin:/0'(\\'|.)/},{className:"string",begin:/0'\\s/},n.C_NUMBER_MODE];return e.contains=t,a.contains=t,{name:"Prolog",contains:t.concat([{begin:/\.$/}])}}))}}}));
