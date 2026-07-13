const personSchema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "https://longtai.org/#person",
      "name": "LongTai Jiang",
      "alternateName": "Jiang",
      "url": "https://longtai.org",
      "image": "https://www.gravatar.com/avatar/64a851c812177321ca40d671ad3c014a",
      "description": "國立台中科技大學學生，資訊社群活躍成員，參與過 COSCUP 與 SITCON。",
      "jobTitle": "Student Developer",
      "knowsAbout": [
        "HTML",
        "CSS",
        "Python",
        "Community Management"
      ],
      "alumniOf": {
        "@type": "CollegeOrUniversity",
        "name": "國立台中科技大學"
      },
      "memberOf": [
        {
          "@type": "Organization",
          "name": "SCAICT"
        },
        {
          "@type": "Organization",
          "name": "SITCON"
        },
        {
          "@type": "Organization",
          "name": "國立台中科技大學 資訊工程科 學會"
        }
      ],
      "sameAs": [
        "https://github.com/longtai-me",
        "https://instagram.com/jiang.0925",
        "https://t.me/lcngtai"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://longtai.org/#website",
      "url": "https://longtai.org",
      "name": "LongTai Jiang | 學生開發者",
      "publisher": {
        "@id": "https://longtai.org/#person"
      }
    }
  ]
};

const script = document.createElement('script');
script.type = 'application/ld+json';
script.text = JSON.stringify(personSchema);
document.head.appendChild(script);