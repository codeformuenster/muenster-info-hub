const moment = require('moment');
const request = require('request-promise');
const { Client } = require('@elastic/elasticsearch');
const eventCalendar = require('./eventCalendar');

const elasticUrl = process.env.ELASTICSEARCH_URL;
const index = 'MuensterHub';
const client = new Client({ node: elasticUrl });

const buildEventUrl = (from, until) => {
	const fromDate = moment(from).format('DD-MM');
	const toDate = moment(until).format('DD-MM');
	return `https://veranstaltungen.meinestadt.de/muenster-westfalen/alle/alle/kalender/d-${fromDate}t-${toDate}?words=`;
};

const scrapeEventCalendar = async (html) => eventCalendar.extract(html);
const persist = (body) => client.index({ index, body });

const scrape = async () => {
	const today = moment();
	const tomorrow = moment().add(7, 'days');
	const url = buildEventUrl(today, tomorrow);
	// eslint-disable-next-line no-console
	console.log(`requesting ${url}`);
	const html = await request(url);
	const result = await scrapeEventCalendar(html);
	// eslint-disable-next-line no-console
	console.log(`found ${result.length} events`);
	await Promise.all(result.map(persist));
	// eslint-disable-next-line no-console
	console.log(`done indexing ${result.length} items`);
};

module.exports = scrape;
