const fs = require('fs');
const path = require('path');
const request = require('request-promise');

const buildPath = (filename) => path.join(__dirname, filename);

const downloadHTMLToFile = async (url, filename) => {
	const html = await request(url);
	fs.writeFileSync(buildPath(filename), html);
};

const saveAsJSON = (obj, fileName) => {
	const jsonString = JSON.stringify(obj, 0, 2);
	fs.writeFileSync(buildPath(fileName), jsonString);
};

const loadHTMLFromFile = (filename) => fs.readFileSync(buildPath(filename)).toString();

module.exports = {
	saveAsJSON,
	downloadHTMLToFile,
	loadHTMLFromFile,
};
