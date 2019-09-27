const moment = require('moment');
const request = require('request-promise');
const { downloadHTMLToFile, loadHTMLFromFile, saveAsJSON } = require('./../common');
const eventCalendar = require('./eventCalendar');

const fileName = 'event-calendar.html';

const buildEventUrl = (from, until) => {
	const fromDate = moment(from).format('DD-MM');
	const toDate = moment(until).format('DD-MM');
	return `https://veranstaltungen.meinestadt.de/muenster-westfalen/alle/alle/kalender/d-${fromDate}t-${toDate}?words=`;
};

const downloadEventCalendar = async (url) => {
	await downloadHTMLToFile(url, fileName);
};

const loadEventCalendar = () => loadHTMLFromFile(fileName);

const scrapeEventCalendar = async (html) => eventCalendar.extract(html);

const scrape = async () => {
	const today = moment();
	const tomorrow = moment();
	const url = buildEventUrl(today, tomorrow);
	// await downloadEventCalendar(url)

	const result = await scrapeEventCalendar(loadEventCalendar());
	saveAsJSON(result, 'result.json');
};

scrape();
