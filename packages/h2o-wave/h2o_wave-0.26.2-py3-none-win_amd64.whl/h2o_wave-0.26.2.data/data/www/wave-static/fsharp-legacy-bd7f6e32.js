!function(){function n(n){return function(n){if(Array.isArray(n))return e(n)}(n)||function(n){if("undefined"!=typeof Symbol&&null!=n[Symbol.iterator]||null!=n["@@iterator"])return Array.from(n)}(n)||function(n,t){if(!n)return;if("string"==typeof n)return e(n,t);var r=Object.prototype.toString.call(n).slice(8,-1);"Object"===r&&n.constructor&&(r=n.constructor.name);if("Map"===r||"Set"===r)return Array.from(n);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return e(n,t)}(n)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function e(n,e){(null==e||e>n.length)&&(e=n.length);for(var t=0,r=new Array(e);t<e;t++)r[t]=n[t];return r}function t(n){return t="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(n){return typeof n}:function(n){return n&&"function"==typeof Symbol&&n.constructor===Symbol&&n!==Symbol.prototype?"symbol":typeof n},t(n)}System.register([],(function(e,r){"use strict";return{execute:function(){function r(n){return new RegExp(n.replace(/[-/\\^$*+?.()|[\]{}]/g,"\\$&"),"m")}function i(n){return n?"string"==typeof n?n:n.source:null}function o(n){return a("(?=",n,")")}function a(){for(var n=arguments.length,e=new Array(n),t=0;t<n;t++)e[t]=arguments[t];var r=e.map((function(n){return i(n)})).join("");return r}function c(n){var e=n[n.length-1];return"object"===t(e)&&e.constructor===Object?(n.splice(n.length-1,1),e):{}}function s(){for(var n=arguments.length,e=new Array(n),t=0;t<n;t++)e[t]=arguments[t];var r=c(e),o="("+(r.capture?"":"?:")+e.map((function(n){return i(n)})).join("|")+")";return o}e("default",(function(e){var t={scope:"keyword",match:/\b(yield|return|let|do|match|use)!/},i=["bool","byte","sbyte","int8","int16","int32","uint8","uint16","uint32","int","uint","int64","uint64","nativeint","unativeint","decimal","float","double","float32","single","char","string","unit","bigint","option","voption","list","array","seq","byref","exn","inref","nativeptr","obj","outref","voidptr","Result"],c={keyword:["abstract","and","as","assert","base","begin","class","default","delegate","do","done","downcast","downto","elif","else","end","exception","extern","finally","fixed","for","fun","function","global","if","in","inherit","inline","interface","internal","lazy","let","match","member","module","mutable","namespace","new","of","open","or","override","private","public","rec","return","static","struct","then","to","try","type","upcast","use","val","void","when","while","with","yield"],literal:["true","false","null","Some","None","Ok","Error","infinity","infinityf","nan","nanf"],built_in:["not","ref","raise","reraise","dict","readOnlyDict","set","get","enum","sizeof","typeof","typedefof","nameof","nullArg","invalidArg","invalidOp","id","fst","snd","ignore","lock","using","box","unbox","tryUnbox","printf","printfn","sprintf","eprintf","eprintfn","fprintf","fprintfn","failwith","failwithf"],"variable.constant":["__LINE__","__SOURCE_DIRECTORY__","__SOURCE_FILE__"]},l={variants:[e.COMMENT(/\(\*(?!\))/,/\*\)/,{contains:["self"]}),e.C_LINE_COMMENT_MODE]},u={scope:"variable",begin:/``/,end:/``/},f=/\B('|\^)/,p={scope:"symbol",variants:[{match:a(f,/``.*?``/)},{match:a(f,e.UNDERSCORE_IDENT_RE)}],relevance:0},d=function(e){var t;t=e.includeEqual?"!%&*+-/<=>@^|~?":"!%&*+-/<>@^|~?";var i=Array.from(t),c=a.apply(void 0,["["].concat(n(i.map(r)),["]"])),l=s(c,/\./),u=a(l,o(l)),f=s(a(u,l,"*"),a(c,"+"));return{scope:"operator",match:s(f,/:\?>/,/:\?/,/:>/,/:=/,/::?/,/\$/),relevance:0}},y=d({includeEqual:!0}),b=d({includeEqual:!1}),m=function(n,t){return{begin:a(n,o(a(/\s*/,s(/\w/,/'/,/\^/,/#/,/``/,/\(/,/{\|/)))),beginScope:t,end:o(s(/\n/,/=/)),relevance:0,keywords:e.inherit(c,{type:i}),contains:[l,p,e.inherit(u,{scope:null}),b]}},g=m(/:/,"operator"),h=m(/\bof\b/,"keyword"),v={begin:[/(^|\s+)/,/type/,/\s+/,/[a-zA-Z_](\w|')*/],beginScope:{2:"keyword",4:"title.class"},end:o(/\(|=|$/),keywords:c,contains:[l,e.inherit(u,{scope:null}),p,{scope:"operator",match:/<|>/},g]},E={scope:"computation-expression",match:/\b[_a-z]\w*(?=\s*\{)/},A={begin:[/^\s*/,a(/#/,s.apply(void 0,["if","else","endif","line","nowarn","light","r","i","I","load","time","help","quit"])),/\b/],beginScope:{2:"meta"},end:o(/\s|$/)},S={variants:[e.BINARY_NUMBER_MODE,e.C_NUMBER_MODE]},_={scope:"string",begin:/"/,end:/"/,contains:[e.BACKSLASH_ESCAPE]},w={scope:"string",begin:/@"/,end:/"/,contains:[{match:/""/},e.BACKSLASH_ESCAPE]},C={scope:"string",begin:/"""/,end:/"""/,relevance:2},O={scope:"subst",begin:/\{/,end:/\}/,keywords:c},x={scope:"string",begin:/\$"/,end:/"/,contains:[{match:/\{\{/},{match:/\}\}/},e.BACKSLASH_ESCAPE,O]},R={scope:"string",begin:/(\$@|@\$)"/,end:/"/,contains:[{match:/\{\{/},{match:/\}\}/},{match:/""/},e.BACKSLASH_ESCAPE,O]},k={scope:"string",begin:/\$"""/,end:/"""/,contains:[{match:/\{\{/},{match:/\}\}/},O],relevance:2},N={scope:"string",match:a(/'/,s(/[^\\']/,/\\(?:.|\d{3}|x[a-fA-F\d]{2}|u[a-fA-F\d]{4}|U[a-fA-F\d]{8})/),/'/)};return O.contains=[R,x,w,_,N,t,l,u,g,E,A,S,p,y],{name:"F#",aliases:["fs","f#"],keywords:c,illegal:/\/\*/,classNameAliases:{"computation-expression":"keyword"},contains:[t,{variants:[k,R,x,C,w,_,N]},l,u,v,{scope:"meta",begin:/\[</,end:/>\]/,relevance:2,contains:[u,C,w,_,N,S]},h,g,E,A,S,p,y]}}))}}}))}();
