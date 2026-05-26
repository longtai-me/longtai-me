const personSchema = {
      "@context": "https://schema.org",
      "@type": "Person",
      "name": "LongTai Jiang",
      "alternateName": "Jiang",
      "url": "https://longtai.org",
      "image": "https://www.gravatar.com/avatar/64a851c812177321ca40d671ad3c014a",
      "description": "國立台中科技大學學生，資訊社群活躍成員，參與過 COSCUP 與 SITCON。",
      "jobTitle": "Student Developer",
      "affiliation": {
        "@type": "Organization",
        "name": "國立台中科技大學"
      },
      "sameAs": [
        "https://github.com/longtai-me",
        "https://instagram.com/jiang.0925",
        "https://t.me/lcngtai"
      ]
    };

const script = document.createElement('script');
script.type = 'application/ld+json';
script.text = JSON.stringify(personSchema);
document.head.appendChild(script);