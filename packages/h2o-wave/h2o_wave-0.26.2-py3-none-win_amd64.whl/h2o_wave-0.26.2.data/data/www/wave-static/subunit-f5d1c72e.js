function a(s){return{name:"SubUnit",case_insensitive:!0,contains:[{className:"string",begin:`\\[
(multipart)?`,end:`\\]
`},{className:"string",begin:"\\d{4}-\\d{2}-\\d{2}(\\s+)\\d{2}:\\d{2}:\\d{2}.\\d+Z"},{className:"string",begin:"(\\+|-)\\d+"},{className:"keyword",relevance:10,variants:[{begin:"^(test|testing|success|successful|failure|error|skip|xfail|uxsuccess)(:?)\\s+(test)?"},{begin:"^progress(:?)(\\s+)?(pop|push)?"},{begin:"^tags:"},{begin:"^time:"}]}]}}export{a as default};
