function g(e){const n={variants:[e.COMMENT("--","$"),e.COMMENT(/\{-/,/-\}/,{contains:["self"]})]},t={className:"meta",begin:/\{-#/,end:/#-\}/},c={className:"meta",begin:"^#",end:"$"},i={className:"type",begin:"\\b[A-Z][\\w']*",relevance:0},a={begin:"\\(",end:"\\)",illegal:'"',contains:[t,c,{className:"type",begin:"\\b[A-Z][\\w]*(\\((\\.\\.|,|\\w+)\\))?"},e.inherit(e.TITLE_MODE,{begin:"[_a-z][\\w']*"}),n]},l={begin:/\{/,end:/\}/,contains:a.contains},s="([0-9]_*)+",o="([0-9a-fA-F]_*)+",r="([01]_*)+",d="([0-7]_*)+",b={className:"number",relevance:0,variants:[{match:`\\b(${s})(\\.(${s}))?([eE][+-]?(${s}))?\\b`},{match:`\\b0[xX]_*(${o})(\\.(${o}))?([pP][+-]?(${s}))?\\b`},{match:`\\b0[oO](${d})\\b`},{match:`\\b0[bB](${r})\\b`}]};return{name:"Haskell",aliases:["hs"],keywords:"let in if then else case of where do module import hiding qualified type data newtype deriving class instance as default infix infixl infixr foreign export ccall stdcall cplusplus jvm dotnet safe unsafe family forall mdo proc rec",contains:[{beginKeywords:"module",end:"where",keywords:"module where",contains:[a,n],illegal:"\\W\\.|;"},{begin:"\\bimport\\b",end:"$",keywords:"import qualified as hiding",contains:[a,n],illegal:"\\W\\.|;"},{className:"class",begin:"^(\\s*)?(class|instance)\\b",end:"where",keywords:"class family instance where",contains:[i,a,n]},{className:"class",begin:"\\b(data|(new)?type)\\b",end:"$",keywords:"data family type newtype deriving",contains:[t,i,a,l,n]},{beginKeywords:"default",end:"$",contains:[i,a,n]},{beginKeywords:"infix infixl infixr",end:"$",contains:[e.C_NUMBER_MODE,n]},{begin:"\\bforeign\\b",end:"$",keywords:"foreign import export ccall stdcall cplusplus jvm dotnet safe unsafe",contains:[i,e.QUOTE_STRING_MODE,n]},{className:"meta",begin:"#!\\/usr\\/bin\\/env runhaskell",end:"$"},t,c,{scope:"string",begin:/'(?=\\?.')/,end:/'/,contains:[{scope:"char.escape",match:/\\./}]},e.QUOTE_STRING_MODE,b,i,e.inherit(e.TITLE_MODE,{begin:"^[_a-z][\\w']*"}),n,{begin:"->|<-"}]}}export{g as default};
