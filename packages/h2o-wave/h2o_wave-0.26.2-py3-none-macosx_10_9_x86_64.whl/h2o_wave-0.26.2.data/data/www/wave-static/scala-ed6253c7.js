function E(e){const s=e.regex,i={className:"meta",begin:"@[A-Za-z]+"},a={className:"subst",variants:[{begin:"\\$[A-Za-z0-9_]+"},{begin:/\$\{/,end:/\}/}]},c={className:"string",variants:[{begin:'"""',end:'"""'},{begin:'"',end:'"',illegal:"\\n",contains:[e.BACKSLASH_ESCAPE]},{begin:'[a-z]+"',end:'"',illegal:"\\n",contains:[e.BACKSLASH_ESCAPE,a]},{className:"string",begin:'[a-z]+"""',end:'"""',contains:[a],relevance:10}]},n={className:"type",begin:"\\b[A-Z][A-Za-z0-9_]*",relevance:0},t={className:"title",begin:/[^0-9\n\t "'(),.`{}\[\]:;][^\n\t "'(),.`{}\[\]:;]+|[^0-9\n\t "'(),.`{}\[\]:;=]/,relevance:0},r={className:"class",beginKeywords:"class object trait type",end:/[:={\[\n;]/,excludeEnd:!0,contains:[e.C_LINE_COMMENT_MODE,e.C_BLOCK_COMMENT_MODE,{beginKeywords:"extends with",relevance:10},{begin:/\[/,end:/\]/,excludeBegin:!0,excludeEnd:!0,relevance:0,contains:[n]},{className:"params",begin:/\(/,end:/\)/,excludeBegin:!0,excludeEnd:!0,relevance:0,contains:[n]},t]},o={className:"function",beginKeywords:"def",end:s.lookahead(/[:={\[(\n;]/),contains:[t]},l={begin:[/^\s*/,"extension",/\s+(?=[[(])/],beginScope:{2:"keyword"}},d={begin:[/^\s*/,/end/,/\s+/,/(extension\b)?/],beginScope:{2:"keyword",4:"keyword"}},g=[{match:/\.inline\b/},{begin:/\binline(?=\s)/,keywords:"inline"}],b={begin:[/\(\s*/,/using/,/\s+(?!\))/],beginScope:{2:"keyword"}};return{name:"Scala",keywords:{literal:"true false null",keyword:"type yield lazy override def with val var sealed abstract private trait object if then forSome for while do throw finally protected extends import final return else break new catch super class case package default try this match continue throws implicit export enum given transparent"},contains:[e.C_LINE_COMMENT_MODE,e.C_BLOCK_COMMENT_MODE,c,n,o,r,e.C_NUMBER_MODE,l,d,...g,b,i]}}export{E as default};
