const moment = require('moment');
const request = require('request-promise');
const { Client } = require('@elastic/elasticsearch');
const eventCalendar = require('./eventCalendar');

const elasticUrl = process.env.ELASTICSEARCH_URL_PREFIX.split('/').slice(0,-1).join('/')
const index = process.env.ELASTICSEARCH_URL_PREFIX.split('/').slice(-1) + 'events'

console.log(`elasticUrl: ${elasticUrl}`);
console.log(`index ${index}`);

const client = new Client({ node: elasticUrl });

const buildEventUrl = (from, until, page) => {
	const fromDate = moment(from).format('DD-MM');
	const toDate = moment(until).format('DD-MM');
	let url = `https://veranstaltungen.meinestadt.de/muenster-westfalen/alle/alle/kalender/d-${fromDate}t-${toDate}?words=`;
	if (page && page > 0) {
		url = url + `&page=${page}`
	}
	return url;
};

const scrapeEventCalendar = async (html) => eventCalendar.extract(html);
const persist = (body) => client.index({ index, body, id: body.id });

const scrape = async () => {
	await scrapePage(0);
	await scrapePage(2);
	await scrapePage(3);
	await scrapePage(4);
};

const scrapePage = async (page) => {
	const today = moment();
	const tomorrow = moment().add(7, 'days');
	const url = buildEventUrl(today, tomorrow, page);
	// eslint-disable-next-line no-console
	console.log(`==> requesting ${url}`);
	const html = await request(url);
	const result = await scrapeEventCalendar(html);
	// eslint-disable-next-line no-console
	console.log(`found ${result.length} events`);

	await Promise.all(result.map(persist));

	// eslint-disable-next-line no-console
	console.log(`done indexing ${result.length} items on page ${page}\n`);
};

module.exports = scrape;
