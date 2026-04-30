const personSchema = [
  {
    "img": "public/images/events/SITCON_2026.svg",
    "alt": "SITCON 2026",
    "title": "SITCON 2026",
    "desc": "個人贊助"
  },
  {
    "img": "public/images/events/SITCON_2026.svg",
    "alt": "SITCON 2026",
    "title": "SITCON 2026",
    "desc": "個人贊助"
  },
  {
    "img": "public/images/events/SCAICT.png",
    "alt": "SCAICT",
    "title": "SCAICT",
    "subtitle": "SITCON 2026",
    "desc": "社群攤位設備支援"
  }
];

const script = document.createElement('script');
script.type = 'application/ld+json';
script.text = JSON.stringify(personSchema);
document.head.appendChild(script);