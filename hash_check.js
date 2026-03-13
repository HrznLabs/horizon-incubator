const fs = require('fs');
const crypto = require('crypto');

const html = fs.readFileSync('Verticals/ridesDAO/RidesVertical_Complete_Spec.html', 'utf8');
const scripts = html.match(/<script>([\s\S]*?)<\/script>/g);

scripts.forEach((script, index) => {
    const content = script.replace(/<\/?script>/g, '');
    const hash = crypto.createHash('sha256').update(content).digest('base64');
    console.log(`Script ${index + 1}: sha256-${hash}`);
});
