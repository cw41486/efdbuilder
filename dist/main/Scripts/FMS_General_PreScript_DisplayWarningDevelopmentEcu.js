// javascript

// FMS_General_PreScript_DisplayWarningDevelopmentEcu.js

// This script is a general script that just displays a warning dialog to the
// user explaining that the ECU is still in development.

{/////////////////////////
// internationalization //
//////////////////////////
var strings = {
    "attention" : {
        en: "ATTENTION: This EFD file should be used for development purposes only. Flash support for this ECU has not been completed.",
        fr: "ATTENTION: Ce fichier EFD doit \u00EAtre utilis\u00E9 \u00E0 fins de recherches uniquement. Le support technique du Flash pour cet ECU n\'a pas \u00E9t\u00E9 achev\u00E9.",
        it: "ATTENZIONE:  Questo file EFD deve essere utilizzato solo per scopi di sviluppo.  Il supporto FLASH  per questa centralina (ECU) non \u00E8 stata completata.",
        de: "ACHTUNG: Diese EFD-Datei sollte nur f\u00FCr Entwicklungszwecke verwendet werden. Flash-Support f\u00FCr diesen ECU ist noch nicht fertiggestellt.",
        es: "ATENCI\u00D3N: Este archivo EFD debe solamente ser utilizado con fines de desarollo. El soporte de flash para este ECU no fue completado.",
        pt: "ATEN\u00C7\u00C3O: Este arquivo EFD deve ser usado somente com o prop\u00F3sito de desenvolvimento. O suporte de flash para este ECU n\u00E3o foi completo.",
        zh: "\u6CE8\u610F\uFF1A\u8FD9EFD\u7684\u6587\u4EF6\u5E94\u4EC5\u7528\u4E8E\u5F00\u53D1\u76EE\u7684\u3002\u6B64ECU\u7684\u6A21\u584A\u652F\u6301\u5C1A\u672A\u5B8C\u6210\u3002",
        pl: "Uwaga: EFD plik powinien by\u0107 stosowany wy\u0142\u0105cznie w celu opracowywania/zbudowania. Wsparcie/programowanie Flash dla tego ECU nie zosta\u0142o zako\u0144czone.",
        hr: "PA\u017DNJA: Ova EFD datoteka treba koristiti za razvoj svrhe. Flash podr\u0161ka za ovaj ECU nije zavr\u0161ena.",
        cs: "Upozorn\u011Bn\u00ED: Tento soubor EFD by m\u011Bl b\u00FDt pou\u017E\u00EDv\u00E1n pouze pro \u00FA\u010Dely v\u00FDvoje. Flash podporu pro tento ECU nebyla dokon\u010Dena.\n",
        da: "OBS: Dette EFD fil b\u00F8r anvendes til udviklingsform\u00E5l alene. Flash-st\u00F8tte til denne ECU er ikke afsluttet.",
        el: "\u03A0\u03A1\u039F\u03A3\u039F\u03A7\u0397: \u0391\u03C5\u03C4\u03AE \u03B7 EFD \u03B1\u03C1\u03C7\u03B5\u03AF\u03BF \u03B8\u03B1 \u03C0\u03C1\u03AD\u03C0\u03B5\u03B9 \u03BD\u03B1 \u03C7\u03C1\u03B7\u03C3\u03B9\u03BC\u03BF\u03C0\u03BF\u03B9\u03B5\u03AF\u03C4\u03B1\u03B9 \u03BC\u03CC\u03BD\u03BF \u03B3\u03B9\u03B1 \u03C3\u03BA\u03BF\u03C0\u03BF\u03CD\u03C2 \u03B1\u03BD\u03AC\u03C0\u03C4\u03C5\u03BE\u03B7\u03C2. Flash \u03C5\u03C0\u03BF\u03C3\u03C4\u03AE\u03C1\u03B9\u03BE\u03B7 \u03B3\u03B9\u03B1 \u03C4\u03B7\u03BD \u03B5\u03BD \u03BB\u03CC\u03B3\u03C9 \u03BC\u03BF\u03BD\u03AC\u03B4\u03B1 \u03B4\u03B5\u03BD \u03AD\u03C7\u03B5\u03B9 \u03BF\u03BB\u03BF\u03BA\u03BB\u03B7\u03C1\u03C9\u03B8\u03B5\u03AF.",
        iw: "\u05E9\u05D9\u05DD \u05DC\u05D1: \u05E7\u05D5\u05D1\u05E5 \u05D6\u05D4 EFD \u05D0\u05DE\u05D5\u05E8 \u05DC\u05E9\u05DE\u05E9 \u05DC\u05DE\u05D8\u05E8\u05D5\u05EA \u05E4\u05D9\u05EA\u05D5\u05D7 \u05D1\u05DC\u05D1\u05D3. \u05EA\u05DE\u05D9\u05DB\u05D4 \u05E2\u05D1\u05D5\u05E8 Flash ECU \u05D6\u05D5 \u05DC\u05D0 \u05D4\u05D5\u05E9\u05DC\u05DE\u05D4.",
        hu: "FIGYELEM: Ez az EFD f\u00E1jlt kell haszn\u00E1lni fejleszt\u00E9si c\u00E9lokra. Flash t\u00E1mogat\u00E1s ezen ECU nem fejez\u0151d\u00F6tt be.",
        ja: "\u6CE8\u610F\uFF1A\u3053\u306EEFD\u30D5\u30A1\u30A4\u30EB\u306F\u3001\u958B\u767A\u76EE\u7684\u306B\u4F7F\u7528\u3055\u308C\u308B\u3079\u304D\u3067\u3042\u308B\u3002\u3053\u306EECU\u306E\u30D5\u30E9\u30C3\u30B7\u30E5\u306E\u30B5\u30DD\u30FC\u30C8\u304C\u5B8C\u4E86\u3057\u3066\u3044\u307E\u305B\u3093\u3002",
        ru: "\u0412\u041D\u0418\u041C\u0410\u041D\u0418\u0415: \u042D\u0442\u043E\u0442 EFD \u0444\u0430\u0439\u043B \u0434\u043E\u043B\u0436\u0435\u043D \u0431\u044B\u0442\u044C \u0438\u0441\u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u043D \u0434\u043B\u044F \u0440\u0430\u0437\u0432\u0438\u0442\u0438\u044F \u0446\u0435\u043B\u044F\u0445. \u0424\u043B\u044D\u0448 \u043F\u043E\u0434\u0434\u0435\u0440\u0436\u043A\u0443 \u044D\u0442\u043E\u0433\u043E ECU \u043D\u0435 \u0431\u044B\u043B\u0430 \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043D\u0430.",
        sl: "POZOR: Ta EFD datoteka je treba uporabljati za razvojne namene. Flash podporo za ta ECU \u0161e ni kon\u010Dan.",
        sv: "VARNING: Denna EFD fil b\u00F6r anv\u00E4ndas f\u00F6r utveckling syfte. Flash-st\u00F6d f\u00F6r denna ecu, har inte slutf\u00F6rts.",
        tr: "D\u0130KKAT: Bu \u200B\u200BEFD dosya sadece geli\u015Ftirme amac\u0131yla kullan\u0131lmal\u0131d\u0131r. Bu ECU i\u00E7in Flash deste\u011Fi hen\u00FCz tamamlanmam\u0131\u015Ft\u0131r."
    } ,
    "ok": {
        en: "OK",
        fr: "ok",
        it: "OK",
        de: "Ok",
        es: "Aceptar",
        pt: "OK",
        zh: "\u201C\u786E\u5B9A\u201D",
        pl: "OK",
        hr: "OK",
        cs: "OK",
        da: "OK",
        el: "OK",
        iw: "\u05D1\u05E1\u05D3\u05E8",
        hu: "OK",
        ja: "[OK]",
        ru: "Ok",
        sl: "OK",
        sv: "OK",
        tr: "Tamam"
    }
};
var language = typeof locale === 'undefined' ? "en" : locale.getLanguage();
function getString(key) {
    var s = strings[key][language];
    return s == undefined ? strings[key]["en"] : s;
}
}/////////////////////////

log.log(FlashLogLevel.MANAGEMENT, "User Dialog: ATTENTION: This EFD file should be used for development purposes only. Flash support for this ECU has not been completed.");
status.displaySelection(getString("attention"), [getString("ok")] );
log.log(FlashLogLevel.MANAGEMENT, "User Selection: ok");