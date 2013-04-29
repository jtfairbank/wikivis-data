/*
Helper.js
=========
These javascript snippets were used to gather data in order to setup the
links scripts.  The script, data gathered, and date the script was run are
given.
*/


/* TLDS
 * ============================================================ */

/*
gtlds
------------------------------------------------------------
This function can be run on http://en.wikipedia.org/wiki/List_of_Internet_top-level_domains
to get a json array of the gtlds and their enitity / meaning.  The
array can then be copied into other programs.

**Requires:**

 * jquery

**Last Run:** 4/27/13

**Output:**

    {"aero":["air-transport industry"],"asia":["Asia-Pacific region"],"biz":["business"],"cat":["Catalan"],"com":["commercial"],"coop":["cooperatives"],"info":["information"],"int":["international organizations"],"jobs":["companies"],"mobi":["mobile devices"],"museum":["museums"],"name":["individuals, by name"],"net":["network"],"org":["organization"],"post":["postal services"],"pro":["professions"],"tel":["Internet communication services"],"travel":["travel and tourism industry related sites"],"xxx":["adult entertainment"]}
*/
function printGtlds() {
  var gtlds = getTldsToEntity(0); // magic# is the index of the gtld table in a list of tables on this page

  console.log(JSON.stringify(gtlds));

  return gtlds;
}

/*
ctlds
------------------------------------------------------------
This function can be run on http://en.wikipedia.org/wiki/List_of_Internet_top-level_domains
to get a json array of country tlds and their enitity / meaning.  The
array can then be copied into other programs.

**Requires:**

 * jquery

**Last Run:** 4/27/13

**Output:**

    {"gtlds":[{"name":"xxx.","entity":"adult entertainment"},{"name":"orea.","entity":"air-transport industry"},{"name":"aisa.","entity":"Asia-Pacific region"},{"name":"zib.","entity":"business"},{"name":"tac.","entity":"Catalan"},{"name":"moc.","entity":"commercial"},{"name":"sboj.","entity":"companies"},{"name":"pooc.","entity":"cooperatives"},{"name":"eman.","entity":"individuals, by name"},{"name":"ofni.","entity":"information"},{"name":"tni.","entity":"international organizations"},{"name":"let.","entity":"Internet communication services"},{"name":"ibom.","entity":"mobile devices"},{"name":"muesum.","entity":"museums"},{"name":"ten.","entity":"network"},{"name":"gro.","entity":"organization"},{"name":"tsop.","entity":"postal services"},{"name":"orp.","entity":"professions"},{"name":"levart.","entity":"travel and tourism industry related sites"}]}
*/
function printCtlds() {
  var ctlds = getTldsToEntity(2); // magic# is the index of the ctld table in a list of tables on this page
  var moreUsTlds = getTldsToEntity(1); // magic# is the index of other us ctlds table in a list of tables on this page

  // set the US entities to be the same and add them to the ctlds list
  for (var key in moreUsTlds) {
    if (moreUsTlds.hasOwnProperty(key)) {
      moreUsTlds[key] = "United States of America";
      ctlds[key] = moreUsTlds[key];
    }
  }

  console.log(JSON.stringify(ctlds));

  return ctlds;
}


/* tld helper functions
------------------------------------------------------------ */
function getTlds(tableNum) {
  var tlds = [];
  
  $($(".wikitable")[tableNum]).find("tbody tr").each(function(i, elem) {
    tlds.push({
      'name': $($(this).find("td")[0]).text().replace('.', '').replace('\n', ' ').trim(),
      'entity': $($(this).find("td")[1]).text().trim()
    });
  });

  return tlds;
}

function getTldsToEntity(tableNum) {
  var tlds = {};
  var tldsList = getTlds(tableNum);

  for (var i = 0; i < tldsList.length; i++) {
    var name = tldsList[i].name;
    var entity = tldsList[i].entity;
    tlds[name] = entity;
  }

  return tlds;
}
