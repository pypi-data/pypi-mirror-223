System.register([],(function(e,n){"use strict";return{execute:function(){e("default",(function(e){var s=l(e),c=n,r=["any","void","number","boolean","string","object","never","symbol","bigint","unknown"],d={beginKeywords:"namespace",end:/\{/,excludeEnd:!0,contains:[s.exports.CLASS_REFERENCE]},b={beginKeywords:"interface",end:/\{/,excludeEnd:!0,keywords:{keyword:"interface extends",built_in:r},contains:[s.exports.CLASS_REFERENCE]},u={$pattern:n,keyword:a.concat(["type","namespace","interface","public","private","protected","implements","declare","abstract","readonly","enum","override"]),literal:t,built_in:o.concat(r),"variable.language":i},g={className:"meta",begin:"@"+c},m=function(e,n,a){var t=e.contains.findIndex((function(e){return e.label===n}));if(-1===t)throw new Error("can not find mode to replace");e.contains.splice(t,1,a)};return Object.assign(s.keywords,u),s.exports.PARAMS_CONTAINS.push(g),s.contains=s.contains.concat([g,d,b]),m(s,"shebang",e.SHEBANG()),m(s,"use_strict",{className:"meta",relevance:10,begin:/^\s*['"]use strict['"]/}),s.contains.find((function(e){return"func.def"===e.label})).relevance=0,Object.assign(s,{name:"TypeScript",aliases:["ts","tsx","mts","cts"]}),s}));var n="[A-Za-z$_][0-9A-Za-z$_]*",a=["as","in","of","if","for","while","finally","var","new","function","do","return","void","else","break","catch","instanceof","with","throw","case","default","try","switch","continue","typeof","delete","let","yield","const","class","debugger","async","await","static","import","from","export","extends"],t=["true","false","null","undefined","NaN","Infinity"],s=["Object","Function","Boolean","Symbol","Math","Date","Number","BigInt","String","RegExp","Array","Float32Array","Float64Array","Int8Array","Uint8Array","Uint8ClampedArray","Int16Array","Int32Array","Uint16Array","Uint32Array","BigInt64Array","BigUint64Array","Set","Map","WeakSet","WeakMap","ArrayBuffer","SharedArrayBuffer","Atomics","DataView","JSON","Promise","Generator","GeneratorFunction","AsyncFunction","Reflect","Proxy","Intl","WebAssembly"],c=["Error","EvalError","InternalError","RangeError","ReferenceError","SyntaxError","TypeError","URIError"],r=["setInterval","setTimeout","clearInterval","clearTimeout","require","exports","eval","isFinite","isNaN","parseFloat","parseInt","decodeURI","decodeURIComponent","encodeURI","encodeURIComponent","escape","unescape"],i=["arguments","this","super","console","window","document","localStorage","sessionStorage","module","global"],o=[].concat(r,s,c);function l(e){var l=e.regex,d=n,b="<>",u="</>",g={begin:/<[A-Za-z0-9\\._:-]+/,end:/\/[A-Za-z0-9\\._:-]+>|\/>/,isTrulyOpeningTag:function(e,n){var a=e[0].length+e.index,t=e.input[a];if("<"!==t&&","!==t){var s;">"===t&&(function(e,n){var a=n.after,t="</"+e[0].slice(1);return-1!==e.input.indexOf(t,a)}(e,{after:a})||n.ignoreMatch());var c=e.input.substring(a);(c.match(/^\s*=/)||(s=c.match(/^\s+extends\s+/))&&0===s.index)&&n.ignoreMatch()}else n.ignoreMatch()}},m={$pattern:n,keyword:a,literal:t,built_in:o,"variable.language":i},E="[0-9](_?[0-9])*",y="\\.(".concat(E,")"),A="0|[1-9](_?[0-9])*|0[0-7]*[89][0-9]*",f={className:"number",variants:[{begin:"(\\b(".concat(A,")((").concat(y,")|\\.)?|(").concat(y,"))")+"[eE][+-]?(".concat(E,")\\b")},{begin:"\\b(".concat(A,")\\b((").concat(y,")\\b|\\.)?|(").concat(y,")\\b")},{begin:"\\b(0|[1-9](_?[0-9])*)n\\b"},{begin:"\\b0[xX][0-9a-fA-F](_?[0-9a-fA-F])*n?\\b"},{begin:"\\b0[bB][0-1](_?[0-1])*n?\\b"},{begin:"\\b0[oO][0-7](_?[0-7])*n?\\b"},{begin:"\\b0[0-7]+n?\\b"}],relevance:0},p={className:"subst",begin:"\\$\\{",end:"\\}",keywords:m,contains:[]},N={begin:"html`",end:"",starts:{end:"`",returnEnd:!1,contains:[e.BACKSLASH_ESCAPE,p],subLanguage:"xml"}},_={begin:"css`",end:"",starts:{end:"`",returnEnd:!1,contains:[e.BACKSLASH_ESCAPE,p],subLanguage:"css"}},v={begin:"gql`",end:"",starts:{end:"`",returnEnd:!1,contains:[e.BACKSLASH_ESCAPE,p],subLanguage:"graphql"}},h={className:"string",begin:"`",end:"`",contains:[e.BACKSLASH_ESCAPE,p]},S={className:"comment",variants:[e.COMMENT(/\/\*\*(?!\/)/,"\\*/",{relevance:0,contains:[{begin:"(?=@[A-Za-z]+)",relevance:0,contains:[{className:"doctag",begin:"@[A-Za-z]+"},{className:"type",begin:"\\{",end:"\\}",excludeEnd:!0,excludeBegin:!0,relevance:0},{className:"variable",begin:d+"(?=\\s*(-)|$)",endsParent:!0,relevance:0},{begin:/(?=[^\n])\s/,relevance:0}]}]}),e.C_BLOCK_COMMENT_MODE,e.C_LINE_COMMENT_MODE]},w=[e.APOS_STRING_MODE,e.QUOTE_STRING_MODE,N,_,v,h,{match:/\$\d+/},f];p.contains=w.concat({begin:/\{/,end:/\}/,keywords:m,contains:["self"].concat(w)});var R,x=[].concat(S,p.contains),k=x.concat([{begin:/\(/,end:/\)/,keywords:m,contains:["self"].concat(x)}]),O={className:"params",begin:/\(/,end:/\)/,excludeBegin:!0,excludeEnd:!0,keywords:m,contains:k},C={variants:[{match:[/class/,/\s+/,d,/\s+/,/extends/,/\s+/,l.concat(d,"(",l.concat(/\./,d),")*")],scope:{1:"keyword",3:"title.class",5:"keyword",7:"title.class.inherited"}},{match:[/class/,/\s+/,d],scope:{1:"keyword",3:"title.class"}}]},I={relevance:0,match:l.either(/\bJSON/,/\b[A-Z][a-z]+([A-Z][a-z]*|\d)*/,/\b[A-Z]{2,}([A-Z][a-z]+|\d)+([A-Z][a-z]*)*/,/\b[A-Z]{2,}[a-z]+([A-Z][a-z]+|\d)*([A-Z][a-z]*)*/),className:"title.class",keywords:{_:[].concat(s,c)}},T={variants:[{match:[/function/,/\s+/,d,/(?=\s*\()/]},{match:[/function/,/\s*(?=\()/]}],className:{1:"keyword",3:"title.function"},label:"func.def",contains:[O],illegal:/%/},M={match:l.concat(/\b/,(R=[].concat(r,["super","import"]),l.concat("(?!",R.join("|"),")")),d,l.lookahead(/\(/)),className:"title.function",relevance:0},B={begin:l.concat(/\./,l.lookahead(l.concat(d,/(?![0-9A-Za-z$_(])/))),end:d,excludeBegin:!0,keywords:"prototype",className:"property",relevance:0},Z={match:[/get|set/,/\s+/,d,/(?=\()/],className:{1:"keyword",3:"title.function"},contains:[{begin:/\(\)/},O]},z="(\\([^()]*(\\([^()]*(\\([^()]*\\)[^()]*)*\\)[^()]*)*\\)|"+e.UNDERSCORE_IDENT_RE+")\\s*=>",D={match:[/const|var|let/,/\s+/,d,/\s*/,/=\s*/,/(async\s*)?/,l.lookahead(z)],keywords:"async",className:{1:"keyword",3:"title.function"},contains:[O]};return{name:"JavaScript",aliases:["js","jsx","mjs","cjs"],keywords:m,exports:{PARAMS_CONTAINS:k,CLASS_REFERENCE:I},illegal:/#(?![$_A-z])/,contains:[e.SHEBANG({label:"shebang",binary:"node",relevance:5}),{label:"use_strict",className:"meta",relevance:10,begin:/^\s*['"]use (strict|asm)['"]/},e.APOS_STRING_MODE,e.QUOTE_STRING_MODE,N,_,v,h,S,{match:/\$\d+/},f,I,{className:"attr",begin:d+l.lookahead(":"),relevance:0},D,{begin:"("+e.RE_STARTERS_RE+"|\\b(case|return|throw)\\b)\\s*",keywords:"return throw case",relevance:0,contains:[S,e.REGEXP_MODE,{className:"function",begin:z,returnBegin:!0,end:"\\s*=>",contains:[{className:"params",variants:[{begin:e.UNDERSCORE_IDENT_RE,relevance:0},{className:null,begin:/\(\s*\)/,skip:!0},{begin:/\(/,end:/\)/,excludeBegin:!0,excludeEnd:!0,keywords:m,contains:k}]}]},{begin:/,/,relevance:0},{match:/\s+/,relevance:0},{variants:[{begin:b,end:u},{match:/<[A-Za-z0-9\\._:-]+\s*\/>/},{begin:g.begin,"on:begin":g.isTrulyOpeningTag,end:g.end}],subLanguage:"xml",contains:[{begin:g.begin,end:g.end,skip:!0,contains:["self"]}]}]},T,{beginKeywords:"while if switch catch for"},{begin:"\\b(?!function)"+e.UNDERSCORE_IDENT_RE+"\\([^()]*(\\([^()]*(\\([^()]*\\)[^()]*)*\\)[^()]*)*\\)\\s*\\{",returnBegin:!0,label:"func.def",contains:[O,e.inherit(e.TITLE_MODE,{begin:d,className:"title.function"})]},{match:/\.\.\./,relevance:0},B,{match:"\\$"+d,relevance:0},{match:[/\bconstructor(?=\s*\()/],className:{1:"title.function"},contains:[O]},M,{relevance:0,match:/\b[A-Z][A-Z_0-9]+\b/,className:"variable.constant"},C,Z,{match:/\$[(.]/}]}}}}}));
