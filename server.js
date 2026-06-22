const express = require('express');
const _ = require('lodash');                    // 4.17.4 - CVE-2019-10744 prototype pollution
const serialize = require('serialize-javascript'); // 1.6.1 - CVE-2019-16769 RCE
const marked = require('marked');               // 0.3.6 - CVE-2022-21680 ReDoS + XSS

const app = express();
app.use(express.json());

// VULNERABILITY: Prototype pollution via lodash.merge
// Attack: {"__proto__": {"admin": true}} or {"constructor": {"prototype": {"admin": true}}}
app.post('/api/merge', (req, res) => {
    const base = {};
    const userInput = req.body;
    _.merge(base, userInput);   // CVE-2019-10744
    res.json({ merged: base, isAdmin: ({}).admin });
});

// VULNERABILITY: serialize-javascript with user data causes XSS/RCE
app.post('/api/serialize', (req, res) => {
    const data = req.body;
    const serialized = serialize(data);   // CVE-2019-16769
    res.send(`<script>var appData = ${serialized};</script>`);
});

// VULNERABILITY: marked XSS + ReDoS with user-supplied markdown
app.post('/api/render_markdown', (req, res) => {
    const markdown = req.body.content;
    const html = marked(markdown);   // CVE-2022-21680, older versions allow XSS
    res.send(html);
});

// VULNERABILITY: minimist prototype pollution
app.get('/api/parse_args', (req, res) => {
    const minimist = require('minimist');   // 1.2.0 - CVE-2020-7598
    const args = minimist(req.query.args ? req.query.args.split(' ') : []);
    res.json({ parsed: args, isAdmin: ({}).admin });
});

app.listen(3000, '0.0.0.0', () => console.log('Server on :3000'));
