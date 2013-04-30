/*
Helper.js
=========
These javascript snippets were used to gather data in order to setup the
links scripts.  The script, data gathered, and date the script was run are
given.
*/


/* Languages - based on ISO 639-1 standard
 * ============================================================ */

/*
gtlds
------------------------------------------------------------
This function can be run on http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
to get information about the language codes which can then be used in other
programs.
*/
function printLangStructures() {
  console.log(JSON.stringify(getLangInfo()));
  console.log(JSON.stringify(getLangCodesToInfo()));
  console.log(JSON.stringify(getLangFamilyToInfo()));
}


/* lang helper functions
------------------------------------------------------------ */
function getLangInfo() {
  var langs = [];
  
  $($(".wikitable")[0]).find("tbody tr").each(function(i, elem) {
    langs.push({
      'family': $($(this).find("td")[1]).text().trim(),
      'name': $($(this).find("td")[2]).text().trim(),
      'localname': $($(this).find("td")[3]).text().trim(),
      'code': $($(this).find("td")[4]).text().trim()
    });
  });

  return langs;
}

function getLangCodesToInfo() {
  var langCodes = {};
  var langInfo = getLangInfo();

  for (var i = 0; i < langInfo.length; i++) {
    var code = langInfo[i].code;
    langCodes[code] = langInfo[i];
  }

  return langCodes;
}

function getLangFamilyToInfo() {
  var langFamilies = {};
  var langInfo = getLangInfo();

  for (var i = 0; i < langInfo.length; i++) {
    var family = langInfo[i].family;
    if (!(family in langFamilies)) {
      langFamilies[family] = [];
    }
    langFamilies[family].push(langInfo[i]);
  }

  return langFamilies;
}
