const cheerio = require('cheerio');
const moment = require('moment');

const createEvent = (cEvent) => ({
	id: `${cEvent.name}-${cEvent.start_date}`,
	title: cEvent.name,
	is_top_event: true,
	source: 'meinestadt.de',
	description: cEvent.description,
	// FIXME https://momentjs.com/timezone/
	start_date: moment.utc(cEvent.startDate, "ddd MMM D HH:mm:ss ZZ YYYY").toISOString(),
	end_date: moment.utc(cEvent.endDate, "ddd MMM D HH:mm:ss ZZ YYYY").toISOString(),
	link: cEvent.url,
	location_name: cEvent.location.name,
	location_plz: cEvent.location.address.postalCode,
	images: [
		{
			image_url: cEvent.image,
		},
	],

});

const extractJSONLD = (html) => Object.values(cheerio.load(html, {
	decodeEntities: false,
	normalizeWhitespace: true,
})('.ms-resultlist-items script[type="application/ld+json"]'))
	.map((entry) => entry.children)
	.filter((item) => Array.isArray(item))
	.reduce((p, c) => [...p, ...c], [])
	.map((item) => item.data)
	.filter((item) => !!item)
	.filter((item) => item.includes('{'))
	.map(JSON.parse)
	.map(createEvent);


const extractMetaInfo = (html) => {
	const $ = cheerio.load(html, {
		decodeEntities: false,
		normalizeWhitespace: true,
	});
	const events = $('.ms-result-item.ms-result-item-event.ms-link-area-basin').map((i, item) => {
		const category = $(item).find('.ms-result-item-pre-headline a').text()
			.replace('\n', '')
			.trim();

		const title = $(item).find('.ms-result-item-headline a').data().mst.mslayer_element_text;
		const tickets = !!$(item).find('.ms-bem-button.ms-float-right.ms-link-area-swimming-link.js-mstItem.ms-bem-button--primary').data();
		const addressFormFields = $(item).find('.ms-event-form.js-dbForm').children().get()
			.map((field) => field.attribs)
			.reduce((p, c) => {
				const n = { ...p };
				n[c.name] = c.value;
				return n;
			}, {});
		const address = `${addressFormFields.street}|${addressFormFields.city}`;
		return {
			category,
			title,
			pre_booking: tickets,
			location_address: address,
		};
	});
	return events.get();
};

const extract = (html) => {
	const json = extractJSONLD(html);
	const metaInfo = extractMetaInfo(html);
	return json.map((item) => {
		const match = metaInfo.find((meta) => item.title === meta.title);
		return { ...item, ...match };
	});
};

module.exports = { extract };
