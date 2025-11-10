def get_angebot_template():
    """
    Retrieves the html structure for formatting the offer.
    """

    template = """<!DOCTYPE html>
    <html lang="de">
    <head>
    <meta charset="UTF-8">
    <style>
    @page {
    size: A4;
    margin: 30mm 20mm 30mm 20mm;
    font-size: 8px;
    font-family: Helvetica, sans-serif; 

    @bottom {
        content: "";
        border-top: 1px solid #ccc;
        height: 1px;
        margin-top: 2mm;
    }

    @bottom-left {
        content: "────────────────────────────────────────────" "\A"
                "Bankverbindung" "\A"
                "Volksbank Schnathorst" "\A"
                "IBAN: DE96 4926 2364 0070 4710 00" "\A"
                "BIC: GENODEM1SNA";
        white-space: pre;
    }

    @bottom-center {
        content: "──────────────────────────────────────────────" "\A" 
                "T.P.O." "\A"
                "Inh. Daniela Gross" "\A"
                "In den Fichten 34" "\A"
                "32584 Löhne";
        white-space: pre;
    }

    @bottom-right {
        content: "────────────────────────────────────────────" "\A"
                "Tel: 05731 755 13 11" "\A"
                "Fax: 05731 755 13 12" "\A"
                "Mail: tpo-gross@outlook.com" "\A"
                "UST-IdNr.: DE31 8295 117";
        white-space: pre;
    }
    }
    html {
    font-size: 8px;
    line-height: 1.5;
    }

    body {
        font-family: Helvetica, sans-serif;
        margin: 0;
        padding: 0;
        color: #222;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin: 30px 0px 0 0px;
    }

    .customer-info {
        max-width: 65%;
    }

    .logo {
        width: 170px;
        height: auto;
    }
    .logo img {
        width: 100%;
        height: auto;
    }

    /* Struktur */
    h2 {
        margin: 30px 30px 5px 30px;
        font-size: 11px;
    }
    p, th {
        font-size: 9px;
        margin: 0 30px;
    }

    table.content-table td {
        margin: 0 30px;
    }

    td {
        font-size: 9px;
        margin: 0; /* Kein globales margin mehr auf <td>! */
    }
    table {
        border-collapse: separate;
        border-spacing: 0 5px;
        margin: 18px 0px 0 0px;
        width: 100%;
    }
    th {
        background-color: #f0f0f0;
        text-align: left;
        padding: 4px;
        border-bottom: 1px solid #ccc;
    }
    td {
        background-color: #ffffff;
        padding: 4px;
        vertical-align: top;
        border: 1px solid #e0e0e0;
        border-top: none;
    }
    tr.no-split {
        page-break-inside: avoid;
    }
    .product-img {
        display: block;              /* Makes margin auto work */
        margin: 0 auto;              /* Center horizontally */
        max-width: 100%;
        max-height: 3.5cm;             /* or another fixed value */
        height: auto;
        object-fit: contain;
    }
    .totals-box {
        margin: 35px 30px 0 auto;
        width: 40%;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 8px 10px;
        font-size: 9px;
        background-color: #f9f9f9;
        page-break-inside: avoid;
    }
    .totals-box .row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
    }
    .totals-box .row.total {
        font-weight: bold;
        border-top: 1px solid #ccc;
        padding-top: 4px;
        margin-top: 6px;
    }

    td.product-description {
    padding: 2px 4px;
    line-height: 1.3;
    }

    .product-title {
    font-weight: bold;
    font-size: 9px;
    margin: 0;
    padding: 0;
    line-height: 1.2;
    }
    .product-alternative {
    font-weight: bold;
    font-size: 10px;
    line-height: 1.2;
    color: #B22222;
    }

    .product-text {
    font-size: 9px;
    margin: 0;
    padding: 0;
    line-height: 1.3;
    white-space: pre-wrap;
    }


    /* Customer block */
    .customer-block {
        font-size: 9px;            /* Make it bigger */
        line-height: 1.2;           /* Improve readability */
        margin-left: 0px;          /* Align exactly with table */
        margin-right: 30px;
        margin-bottom: 15px;
    }

    .customer-block p {
        font-size: 9px;
        line-height: 1.3;
        margin: 0;
    }

    .anschreiben {
        line-height: 1.6;
    }

    .anschreiben p {
        font-size: 9px;
        line-height: 1.6;
        margin: 0;
        padding: 0;
        text-indent: 0;
    }

    .angebot-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0;
        padding: 0;
        text-indent: 0;
    }

    .angebot-title {
        font-size: 16px;
        font-weight: bold;
    }

    .angebot-datum {
        font-size: 11px;
        color: #444;
    }

    /* Restlicher Text */
    .hinweise-block {
        font-size: 10px;
        margin-left: 0;
        line-height: 1.6;
    }

    .hinweise-block ol {
        font-size: 9px;
        padding-left: 2;
    }

    .hinweise-block li {
        font-size: 9px;
        margin-bottom: 4px;
        padding-left: 14px;
    }
    .AGB {
        font-size: 9px;
        margin-right: 0px;
        margin-bottom: 10px;
    }

    .AGB p {
        font-size: 9px;
        margin: 0 30px;
        margin-bottom: 10px;
        text-align: justify;
    }

    .agb-text {
        margin-top: 4px;
    }

    .unterschrift {
        margin-top: 15mm;
        text-align: right;
        font-size: 9px;
    }

    .unterschrift .line {
        border-top: 1px solid #000;
        width: 200px;
        margin-bottom: 2mm;
        float: right;
    }

    .unterschrift {
        margin-top: 15mm;
        font-size: 9px;
        text-align: right;
    }

    .line-with-label {
        display: inline-block;
        text-align: center;
    }

    .line {
        border-top: 1px solid #000;
        width: 200px;
        margin: 0 auto 2mm auto;
    }

    .label {
        width: 200px;
        text-align: center;
    }

    /* Footer wird durch diese Box "nach unten gedrückt" */
    .footer-push {
        height: 100px;
    }
    </style>
    </head>
    <body>

    <div class="header">
    <div class="customer-block">
        <p style="font-size: 13px;"><strong>{{ kunde['Firma'] }}</strong></p>
        <p>{{ kunde['Anrede'] }} {{ kunde['Vorname'] }} {{ kunde['Nachname'] }}</p>
        <p>{{ kunde['Adresse'] }}</p>
        <p>{{ kunde['PLZ'] }} {{ kunde['Ort'] }}</p>
        <p>Tel.: {{ kunde['Telefonnummer'] }}</p>
        <p>E-Mail: {{ kunde['E_Mail'] }}</p>
    </div>
    <div class="logo">
        <img src="{{ logo_base64 }}" alt="Logo">
    </div>
    </div>

    <div class="angebot-row">
    <div class="angebot-title" style="font-size: 13px;">Angebot: {{ angebot_id }}</div>
    <div class="angebot-datum">{{ aktuelles_datum }}</div>
    </div>

    <div class="anschreiben">
    {% if kunde['Anrede'] == 'Herr' %}
    <p>Sehr geehrter Herr {{ kunde['Nachname'] }},</p>
    {% elif kunde['Anrede'] == 'Frau' %}
    <p>Sehr geehrte Frau {{ kunde['Nachname'] }},</p>
    {% else %}
    <p>Sehr geehrte Damen und Herren,</p>
    {% endif %}
    <p>für Ihre Anfrage und Ihr Interesse an unseren Produkten und Dienstleistungen dürfen wir uns bedanken.</p> 
    <p>Gerne bieten wir Ihnen wie folgt an.</p>
    <p>Unser Angebot hat eine Gültigkeit von 4 Wochen.</p>
    <p>Bei Fragen stehen wir Ihnen gerne jeder Zeit zur Verfügung.</p>
    </div>
    <table>
    <colgroup>
        <col style="width: 5%;">
        <col style="width: 25%;">
        <col style="width: 43%;">
        <col style="width: 5%;">
        <col style="width: 12%;">
        <col style="width: 10%;">
    </colgroup>
    <thead>
    <tr>
    <th>Pos.</th>
    <th>Abbildungen ähnlich</th>
    <th>Bezeichnung</th>
    <th>Menge</th>
    <th>Preis/st netto</th>
    <th>Gesamtpreis</th>
    </tr>
    </thead>
    <tbody>
    {% for row in products %}
    <tr class="product-row{% if loop.index > 1 %} no-split{% endif %}">
    <td><strong>{{ row['Positionsbezeichnung'] }}</strong></td>
    <td>{% if row['image'] %}<img src="{{ row['image'] }}" class="product-img">{% endif %}</td>
    <td class="product-description">
    {% if row['Alternative'] == True %}
        <div class="product-alternative">Alternativ-Option</div>
    {% endif %}
    {% if row['Titel'] %}
        <div class="product-title">{{ row['Titel'] }}</div>
    {% endif %}
    <div class="product-text">{{ row['Beschreibung'] or ''}}</div>
    </td>
    <td>
    {% if not row.Alternative and row.Menge is not none %}
        {% if row.Menge == row.Menge|int %}
            {{ row.Menge|int }}
        {% else %}
            {% set formatted = "%.2f"|format(row.Menge) %}
            {{ formatted.replace('.', ',') }}
        {% endif %}
    {% endif %}
    </td>
    <td>{{ row.Preis | german_currency }} €</td>
    <td>
    {% if not row.Alternative %}
        {% if row.Menge is not none %}
        {{ row.Gesamtpreis | german_currency }} €
        {% else %}
        {{ row.Preis | german_currency }} €
        {% endif %}
    {% endif %}
    {% endfor %}
    </tbody>
    </table>

    <div class="totals-box">
    <div class="row">
        <div>Netto Gesamt:</div>
        <div>{{ netto | german_currency }} €</div>
    </div>

    {% if rabatt != 0 %}
    <div class="row">
        <div>{{ rabatt|replace('.', ',') }}% Rabatt:</div>
        <div>-{{ rabatt_num | german_currency }} €</div>
    </div>
    {% endif %}

    {% if if_mwst == True %}
    <div class="row">
        <div>19% MwSt:</div>
        <div>{{ mwst | german_currency }} €</div>
    </div>
    {% endif %}

    {% if if_mwst == False %}
    <div class="row">
        <div>ATU-Nummer:</div>
        <div>{{atu}}</div>
    </div>
    {% endif %}

    <div class="row total">
        <div>Brutto Gesamt:</div>
        <div>{{ brutto | german_currency }} €</div>
    </div>
    </div>

    <div class="hinweise-block" style="page-break-before: always;">
    <p><strong>Montagekostenpauschale</strong><br>
    Konzessionspflichtige Anschlüsse sowie Maurer- und Stemmarbeiten sind nicht im Preis enthalten und müssen bauseits erstellt werden.</p>

    <p>Zusätzliche Arbeiten, Wartezeiten, Verkleidungsbleche, Montage- und Anschlussmaterial werden nach tatsächlichem Aufwand berechnet.</p>

    <p>Um Mehrkosten zu vermeiden, sorgen Sie bitte dafür:</p>
    <ol>
        <li>dass der Aufstellungsort frei zugänglich ist</li>
        <li>dass das Gerät ohne Umstände eintransportiert werden kann (Türbreite etc.)</li>
        <li>dass der Ablaufanschluss in Gerätenähe zugänglich ist</li>
        <li>dass der Wasseranschluss in der Nähe (max. 2m) zugänglich ist und ein Absperrhahn versehen ist</li>
        <li>dass der Stromanschluss in Gerätenähe und idealerweise mit Steckdose ausgerüstet ist,<br>wahlweise auch mit einer Festanschlussdose.
        <br>(bei Festanschluss müssen die Sicherungen oder Schalter zugänglich sein)</li>
    </ol>

    <p><strong><em>Alle Leitungen müssen Unterputz verlegt werden!</em></strong></p>

    <p>Bitte beachten Sie, dass über Gas-Geräte eine Dunstabzugshaube bauseits vorhanden sein muss.</p>
    <p>Der Gas-Anschluß des Gerätes an die Versorgungsleitungen darf nur durch einen konzessionierten Fachbetrieb vorgenommen werden.</p>

    <p class="agb-text"><strong>Zu- und Abluftbauseits</strong></p>

    <p class="agb-text">
        Der Vertrag wird unter Verwendung unserer Allgemeinen Geschäftsbedingungen, sowie den unten stehenden Zahlungsbedingungen geschlossen.
        Diese werden Ihnen auf Wunsch kostenlos übersandt und sind im Internet unter www.tpo-gross.de einzusehen. 
        Konzessionspflichtige Anschlüsse sowie Maurer- und Stemmarbeiten sind nicht im Preis enthalten und müssen bauseits erstellt werden. 
        Zu evtl. weiteren Entgeltminderungen verweisen wir auf die getroffenen Vereinbarungen.
    </p>

    <p style="margin-top: 4mm;"><strong>Zahlungsbedingungen:</strong><br>Vorkasse</p>

    <div class="unterschrift">
    <div class="line-with-label">
        <div class="line"></div>
        <div class="label">Datum, Unterschrift</div>
    </div>
    </div>
    <div class="AGB" style="page-break-before: always;">
    <p><strong>Durch die nachfolgenden Allgemeinen Geschäftsbedingungen (AGB) werden die vertraglichen Beziehungen
    zwischen der TPO (nachfolgend TPO) und dem Kunden geregelt. TPO verkauft Gastronomiebedarf an gewerbliche Kunden.</strong></p>
        <p><strong>1. Allgemeines</strong></p>
        <p>1.1 Alle Lieferungen und Leistungen erfolgen ausschließlich auf Grundlage dieser AGB. Diese sind Bestandteil aller
        Verträge, die TPO mit den Kunden schließt. Sie gelten auch für alle zukünftigen Verträge mit den Kunden, auch
        wenn sie nicht nochmals gesondert vereinbart wurden.</p>
        <p>1.2 Geschäftsbedingungen der Kunden oder Dritter finden keine Anwendung, auch wenn TPO ihrer Geltung im
        Einzelfall nicht gesondert widerspricht.</p>
        <p>1.3 Der Kunde versichert durch seine Anmeldung dass er Unternehmer i.S. d. § 14 BGB und der europarechtlichen
        Vorschriften ist und die Waren ausschließlich zu unternehmerischen Zwecken nutzt.</p>
        <p>1.4 TPO prüft regelmäßig bei Vertragsabschlüssen und in bestimmten Fällen, in denen ein berechtigtes Interesse
        vorliegt, Ihre Bonität. Dazu arbeiten wir mit der Creditreform Herford & Minden Dorff GmbH & Co. KG, Krellstraße
        68, 32584 Löhne zusammen, von der wir die dazu benötigten Daten erhalten. Zu diesem Zweck übermitteln wir
        Ihren Namen und Ihre Kontaktdaten an die Creditreform. Weitere Informationen zur Datenverarbeitung bei
        Creditreform erhalten Sie in dem ausführlichen Merkblatt „Creditreform-Informationen gem. Art. 14 EU-DSGVO
        oder unter <a href="www.creditreform-ORT.de/EU-DSGVO" target="_blank".>www.creditreform-ORT.de/EU-DSGVO</a>.</p>
        <p>1.5 TPO behält sich vor, bei unvorhersehbaren Änderungen, die TPO nicht veranlasst hat und auf die TPO auch
        keinen Einfluss hat und durch die das bei Vertragsschluss vorhandene Äquivalenzverhältnis in nicht
        unbedeutendem Maße gestört wurde, diese AGB zu ändern, soweit dies dem Kunden zumutbar ist. Die Kunden
        werden über die Änderungen umgehend informiert. Hierbei werden dem Kunden die geänderten AGB unter
        Hervorhebung der abgeänderten Passagen übersandt. Dies kann auch per Email erfolgen. Sollte der Kunde nicht
        innerhalb von sechs Wochen seit der Mitteilung den geänderten AGB widersprechen, so gelten diese als genehmigt
        und finden auch auf bereits bestehende Verträge Anwendung. Hierauf wird der Kunde bei der Mitteilung über die
        Änderung besonders hingewiesen.</p>
        <p><strong>2. Angebot und Vertragsschluss</strong></p>
        <p>2.1 Alle Angebote von TPO sind freibleibend und unverbindlich, es sei denn sie sind ausdrücklich als verbindlich
        gekennzeichnet. Sie verstehen sich lediglich als Aufforderung an den Kunden, ein Angebot gegenüber TPO
        abzugeben. Angaben von TPO über Maße, Gewichte, technische Daten usw. sowie Darstellungen und Abbildungen
        insbesondere auf den Internetseiten von TPO oder in Katalogen sind ebenfalls unverbindlich, soweit nicht die
        Verwendbarkeit zum vertraglichen vereinbarten Zweck eine genaue Übereinstimmung voraussetzt. Sie stellen
        keine Beschaffenheitsgarantie dar, sondern dienen lediglich der Beschreibung oder Kennzeichnung.
        Handelsübliche Abweichungen und solche, die auf grundrechtlicher Vorschriften erfolgen oder technische
        Verbesserungen darstellen sind zulässig soweit sie die Verwendbarkeit zum vertraglich vereinbarten Zweck nicht
        beeinträchtigen und dem Kunden zumutbar sind. Gleiches gilt für die Ersetzung von Bauteilen durch technisch
        mindestens Gleichwertige.</p>
        <p>2.2 Der Vertrag kommt folgendermaßen zu Stande: Der auf der Website dargestellte Warenkatalog stellt kein
        Angebot im juristischen Sinne dar. Mit der Bestellung erklärt der Kunde verbindlich sein Vertragsangebot.
        Eingabefehler können vor Absenden der Bestellung mittels der üblichen Tastatur- und Mausfunktionen berichtigt
        werden. Mit Mausklick auf den Bestellbutton unterbreitet der Kunde ein verbindliches Kaufangebot. Nach Eingang
        des Angebots des Kunden bei TPO erhält der Kunde eine automatisch generierte E-Mail, die den Eingang der
        Bestellung deren Einzelheiten aufführt. Diese Bestätigung stellt keine Annahme des Angebots durch den Verkäufer
        dar. Eine Bestellung des Kunden wird ausdrücklich durch Übersendung einer entsprechenden Auftragsbestätigung
        oder konkludent durch Ausführung der Lieferung oder Leistung angenommen.</p>
        <p>2.3 TPO behält sich das Eigentum oder Urheberrecht an allen abgegebenen Angeboten und Kostenvoranschlägen
        sowie sonstigen Unterlagen vor, die dem Kunden zur Verfügung gestellt wurden, sofern keine
        Eigentumsübertragung oder Übertragung von entsprechenden Rechten vereinbart wurde. Der Kunde darf diese
        Unterlagen nicht ohne Zustimmung von TPO Dritten zugänglich machen, vervielfältigen, bekanntgeben, selbst oder
        durch Dritte nutzen. Der Kunde ist verpflichtet diese Unterlagen auf Aufforderung an TPO herauszugeben und
        angefertigte Kopien zu vernichten, wenn diese im Rahmen der Geschäftsbeziehung nicht mehr benötigt werden.</p>
        <p>2.4 Der Vertragstext wird von uns nicht gespeichert.</p>
        <p><strong>3. Preise und Zahlung</strong></p>
        <p>3.1 Alle Preise verstehen sich in EUR ab Werk zuzüglich Verpackung, der gesetzlichen Umsatzsteuer, bei
        Exportlieferungen zuzüglich Zoll sowie Gebühren und anderer öffentlicher Abgaben. Für Lieferungen innerhalb
        Deutschlands fallen keine zusätzlichen Versandkosten an (bei Inseln und Bergstationen frei Station
        Festland/Talstation). Die Versandkosten für andere europäische Länder können Sie der Versandkostentabelle in
        den Lieferbedingungen entnehmen.</p>
        <p>3.2 Liegt der Liefertermin mehr als vier Monate nach dem Vertragsschluss, ist TPO berechtigt die Preise
        angemessen zu erhöhen und die Preise an veränderte Preisgrundlagen (Material, Löhne usw.) anzupassen. Es
        gelten dann die am Liefertag gültigen Preise.</p>
        <p>3.3 Die Zahlung erfolgt wahlweise per Kreditkarte, Sofortüberweisung, Leasing, Rechnung oder Vorkasse.</p>
        <p>3.4 Bei Auswahl der Zahlungsart Vorkasse nennen wir Ihnen unsere Bankverbindung in der Auftragsbestätigung
        bzw. im Anschluss. Der Rechnungsbetrag ist binnen 5 Tagen auf unser Konto zu überweisen. Die Belastung Ihres
        Kreditkartenkontos sowie der Bankeinzug erfolgen mit Abschluss der Bestellung.</p>
        <p>3.5 Kommen Sie in Zahlungsverzug, so ist der Kaufpreis während des Verzuges in Höhe von 5% über dem
        Basiszinssatz zu verzinsen. Wir behalten uns vor, einen höheren Verzugsschaden nachzuweisen und geltend zu
        machen. Mit Erhalt der 2. Mahnung wird eine zusätzliche Gebühr von 7,50 EUR berechnet.</p>
        <p>3.6 Eine Aufrechnung mit Zahlungsansprüchen des Kunden oder die Zurückbehaltung von Zahlungen wegen
        solcher Ansprüche ist nur mit unbestrittenen oder rechtskräftig festgestellten Forderungen zulässig.</p>
        <p>3.7 Werden nach Vertragsschluss Umstände bekannt, die geeignet sind die Kreditwürdigkeit des Kunden
        wesentlich herabzusetzen und durch die die Bezahlung der noch offenen Forderungen aus dem jeweiligen
        Vertragsverhältnis gefährdet wird so ist TPO berechtigt, die noch ausstehenden Lieferungen und Leistungen nur
        gegen Vorauszahlung oder Sicherheitsleistung zu erbringen.</p>
        <p><strong>4. Erfüllungsort, Versand</strong></p>
        <p>4.1 Soweit die Parteien nichts anderes bestimmen, ist der Erfüllungsort für alle Verpflichtungen aus dem
        Vertragsverhältnis der Sitz von TPO.</p>
        <p>4.2 Die Versandart und die Verpackung unterstehen dem pflichtgemäßen Ermessen von TPO .</p>
        <p>4.3 Mit Übergabe des Liefergegenstandes an den Spediteur, Frachtführer oder an eine sonstige zur Ausführung
        der Versendung bestimmten Dritten geht die Gefahr auf den Kunden über. Dies gilt auch, wenn Teillieferungen
        erfolgen oder der Verkäufer noch andere Leistungen (z. B. Installation) übernommen hat. Verzögert sich der
        Versand durch Umstände die der Kunde zu vertreten hat, so geht die Gefahr mit dem Zeitpunkt auf den Kunden
        über, mit dem TPO versandbereit ist und dies dem Kunden angezeigt hat.</p>
        <p>4.4 Lagerkosten nach Gefahrübergang trägt der Kunde. Erfolgt die Lagerung durch TPO so betragen die
        Lagerkosten 0,25% des Rechnungsbetrages der zu lagernden Liefergegenstände pro abgelaufener Woche. Die
        Geltendmachung und der Nachweis weiterer oder geringerer Lagerkosten bleiben vorbehalten.</p>
        <p><strong>5. Lieferung</strong></p>
        <p>5.1 Lieferungen erfolgen ab Werk (EXW) gemäß Incoterms 2010. Es wird ausdrücklich vereinbart, dass die
        Lieferung durch ein vom Verkäufer ausgesuchtes und beauftragtes Transportunternehmen vorgenommen wird. Es
        wird ausdrücklich vereinbart, dass das Transportunternehmen nur bis zur Bordsteinkante liefert.</p>
        <p>5.2 Unbeschadet ihrer Rechte aus Verzug des Kunden, kann TPO eine Verlängerung der Liefer- und
        Leistungsfristen um den Zeitraum verlangen, in dem der Kunden seinen vertraglichen Pflichten nicht nachkommt.
        Kann oder will der Kunde die Ware zum vereinbarten Zeitpunkt nicht abnehmen, kann TPO sämtliche durch den
        Annahmeverzug entstehenden Mehrkosten dem Kunden gesondert in Rechnung stellen. Bei Nichtdurchführung
        des Auftrags aus vom Kunden zu vertretenden Gründen gelten 30% der Auftragssumme als Schadensersatz
        vereinbart. Dem Kunden bleibt das Recht vorbehalten, nachzuweisen, dass uns durch die Nichtdurchführung kein
        oder ein wesentlich geringerer Schaden entstanden ist.</p>
        <p>5.3 TPO haftet nicht für die Unmöglichkeit der Lieferung oder Leistung oder für Lieferverzögerungen, soweit diese
        durch höhere Gewalt oder sonstige, zum Zeitpunkt des Vertragsschlusses nicht vorhersehbare Ereignisse die TPO
        nicht zu vertreten hat, verursacht worden sind. Erschweren solche Ereignisse TPO die Lieferung oder Leistung
        wesentlich oder machen sie unmöglich und ist die Behinderung nicht nur von vorübergehender Dauer, ist TPO zum
        Rücktritt vom Vertrag berechtigt.
        Bei Behinderungen von nur vorübergehender Dauer verlängern sich die Liefer- oder Leistungsfristen oder
        verschieben sich die Liefer- oder Leistungstermine um den Zeitraum der Behinderung zuzüglich einer
        angemessenen Anlauffrist.</p>
        <p>5.4 Soweit dem Kunden durch die Verzögerung die Abnahme der Lieferung oder Leistung nicht zuzumuten ist,
        kann er durch unverzügliche schriftliche Erklärung gegenüber TPO vom Vertrag zurück treten.</p>
        <p>5.5 TPO ist zu Teillieferungen berechtigt, soweit dem Kunden hierdurch kein erheblicher Mehraufwand und/oder
        zusätzliche Kosten entstehen, die Teillieferung für den Kunden im Rahmen des vertraglichen Bestimmungszweckes
        verwendbar ist und die Lieferung der restlichen bestellten Waren gesichert ist.</p>
        <p>5.6 Der Kunde ist verpflichtet, sich erkennbare Transportschäden sofort beim Empfang vom Transportunternehmer
        bescheinigen zu lassen um Ersatzforderungen an das Transportunternehmen geltend zu machen. TPO ist bemüht,
        dem Kunden bei der Abwicklung von Transportschäden behilflich zu sein. Äußerlich nicht erkennbare Schäden
        müssen nach Kenntnis telefonisch und schriftlich beim Transporteur angezeigt werden. Für die Einhaltung der Frist
        und Abwicklung des Transportschadens ist der Kunde alleinverantwortlich. Der Kunde ist als Empfänger zur
        Geltendmachung von Ansprüchen gegen das Transportunternehmen aus dem Frachtvertrag gemäß § 421 HGB im
        eigenen Namen berechtigt.</p>
        <p><strong>6. Gewährleistung</strong></p>
        <p>6.1 Die Gewährleistungsfrist beträgt ein Jahr ab Lieferung.</p>
        <p>6.2 Die gelieferten Gegenstände sind gem. § 377 HGB unverzüglich nach Ablieferung an den Kunden oder an den
        von ihm bestimmten Dritten sorgfältig zu untersuchen. Sie gelten als genehmigt, wenn TPO nicht eine Mängelrüge
        hinsichtlich offensichtlicher oder anderer Mängel, die bei einer unverzüglichen und sorgfältigen Untersuchung
        erkennbar waren, unverzüglich nach Ablieferung des Liefergegenstandes oder ansonsten unverzüglich nach der
        Entdeckung des Mangels oder dem Zeitpunkt in dem der Mangel für den Kunden bei normaler Verwendung des
        Liefergegenstandes ohne nähere Untersuchung erkennbar war, in Textform zugegangen ist.</p>
        <p>6.3 Auf Verlangen von TPO ist der beanstandete Gegenstand frachtfrei an diese zurück zu senden. Bei berechtigter
        Mängelrüge vergütet TPO die Kosten des günstigsten Versandweges. Dies gilt nicht, wenn die Kosten sich erhöhen,
        weil der Gegenstand sich an einem anderem Ort als dem Ort des bestimmungsgemäßen Gebrauchs befindet.</p>
        <p>6.4 Bei Sachmängeln ist TPO zur Nacherfüllung nach seiner Wahl zunächst zur Nachbesserung oder
        Ersatzlieferung verpflichtet und berechtigt. Eine Nacherfüllung gilt nach dem zweiten erfolglosen Versuch als
        fehlgeschlagen. Im Falle des Fehlschlagens, der Unmöglichkeit, Unzumutbarkeit, Verweigerung oder
        unangemessenen Verzögerung der Nachbesserung oder Ersatzlieferung, kann der Kunde vom Vertrag
        zurücktreten oder den Kaufpreis angemessen mindern. Ergibt sich bei einer im Rahmen der Mängelrüge
        durchgeführten Prüfung der Ware, dass die Mängelrüge zu Unrecht erfolgt ist, sind wir berechtigt, eine
        verkehrsübliche Vergütung für die Prüfung der Ware sowie die Kosten für den Versand zu berechnen.</p>
        <p>6.5 Der Gewährleistungsanspruch entfällt, wenn der Kunde den Kaufgegenstand ohne ausdrückliche Zustimmung
        von TPO ändert oder durch Dritte ändern lässt und die Mängelbeseitigung hierdurch unmöglich oder unzumutbar
        erschwert wird. In jedem Fall hat der Kunde die durch die Änderungen entstehenden Mehrkosten der
        Mängelbeseitigung zu tragen.</p>
        <p>6.6 Ein etwa erforderlicher Anschluss an die Versorgungsleitungen (Strom, Wasser, Dampf, Abwasser,
        Heißwasser, Gas, etc.) ist vom Käufer auf seine Kosten zu veranlassen, und darf nur von konzessionierten örtlichen
        Elektrofachleuten bzw. Installateuren vorgenommen werden. Ist ein Mangel auf eine nicht fachgerechte Installation
        zurückzuführen, entfällt der Gewährleistungsanspruch gegen TPO.</p>
        <p>6.7 Die Lieferung gebrauchter Gegenstände erfolgt unter Ausschluss jeglicher Gewährleistung.</p>
        <p>6.8 Sollte durch den Hersteller des Liefergegenstandes eine längere Gewährleistungsfrist oder eine Garantie
        eingeräumt werden, so treten wir unsere Rechte hieraus bereits mit dem Kauf an den Besteller/Käufer ab.</p>
        <p>6.9 Im Übrigen gilt Ziffer 7 dieses Vertrages.</p>
        <p><strong>7. Haftung</strong></p>
        <p>7.1 Für Schäden, die an anderen Rechtsgütern als dem Leben, Körper oder Gesundheit entstehen ist die Haftung
        ausgeschlossen, soweit die Schäden nicht auf vorsätzlichem oder grob fahrlässigem Verhalten der TPO, eines von
        deren gesetzlichen Vertretern oder eines von deren Erfüllungsgehilfen beruhen und das Verhalten auch keine
        Verletzung von vertragswesentlichen Pflichten ist. Wesentliche Vertragspflichten sind solche Pflichten, deren
        Erfüllung die ordnungsgemäße Durchführung des Vertrages überhaupt erst ermöglicht und auf deren Einhaltung
        der Nutzer regelmäßig vertrauen darf.</p>
        <p>7.2 In jedem Fall ist der Nutzer ebenfalls zur Schadensbegrenzung verpflichtet. Dies beinhaltet die rechtzeitige
        Anzeige von Schäden im Rahmen der weiteren Schadensminimierung.</p>
        <p>7.3 Haftet TPO für den Verlust von Daten, die der Kunde auf der Webseite hinterlegt hat, so gilt, dass TPO nur
        insoweit haftet, soweit der Kunde alle erforderlichen und zumutbaren Datensicherungsvorkehrungen getroffen und
        sichergestellt hat, dass die Daten aus Datenmaterial, das in maschinenlesbarer Form bereitgehalten wird, mit
        vertretbarem Aufwand rekonstruiert werden können.</p>
        <p>7.4 Die vorgenannten Haftungsausschlüsse und Beschränkungen gelten außerdem nicht im Fall der Übernahme
        ausdrücklicher Garantien durch TPO sowie bei Ansprüchen wegen fehlender zugesicherter Eigenschaften oder
        Ansprüchen aus dem Produkthaftungsgesetz.</p>
        <p><strong>8. Eigentumsvorbehalt</strong></p>
        <p>8.1 Die von TPO an den Kunden gelieferte Ware bleibt bis zur vollständigen Bezahlung aller gesicherten
        Forderungen Eigentum von TPO. Die Ware sowie die nach dieser Klausel an ihre Stelle tretende, vom
        Eigentumsvorbehalt erfasste Ware wird nachfolgend Vorbehaltsware genannt.</p>
        <p>8.2 Der Kunde verwahrt die Vorbehaltsware unentgeltlich für TPO.</p>
        <p>8.3 Der Kunde ist berechtigt, die Vorbehaltsware bis zum Eintritt des Verwertungsfalls im ordnungsgemäßen
        Geschäftsverkehr zu verarbeiten und zu veräußern. Verpfändungen und Sicherungsübereignungen sind
        unzulässig.</p>
        <p>8.4 Wird die Vorbehaltsware vom Kunde verarbeitet, so erfolgt die Verarbeitung im Namen und für Rechnung von
        TPO und TPO erwirbt unmittelbar das Eigentum oder – wenn die Verarbeitung aus Stoffen mehrerer Eigentümer
        erfolgt oder der Wert der verarbeiteten Sache höher ist als der Wert der Vorbehaltsware – das Miteigentum
        (Bruchteilseigentum) an der neu geschaffenen Sache im Verhältnis des Werts der Vorbehaltsware zum Wert der
        neu geschaffenen Sache erwirbt. Für den Fall, dass kein solcher Eigentumserwerb bei TPO eintreten sollte,
        überträgt der Kunde bereits jetzt sein künftiges Eigentum oder – im o.g. Verhältnis – Miteigentum an der neu
        geschaffenen Sache zur Sicherheit an TPO. Wird die Vorbehaltsware mit anderen Sachen zu einer einheitlichen
        Sache verbunden oder untrennbar vermischt und ist eine der anderen Sachen als Hauptsache anzusehen, so
        überträgt TPO, soweit die Hauptsache ihr gehört, dem Kunde anteilig das Miteigentum an der einheitlichen Sache
        in dem in Satz 1 genannten Verhältnis.</p>
        <p>8.5 Im Fall der Weiterveräußerung der Vorbehaltsware tritt der Kunde bereits jetzt sicherungshalber die hieraus
        entstehende Forderung gegen den Erwerber – bei Miteigentum von TPO an der Vorbehaltsware anteilig
        entsprechend dem Miteigentumsanteil – an TPO ab. Gleiches gilt für sonstige Forderungen, die an die Stelle der
        Vorbehaltsware treten oder sonst hinsichtlich der Vorbehaltsware entstehen, wie z.B. Versicherungsansprüche
        oder Ansprüche aus unerlaubter Handlung bei Verlust oder Zerstörung. TPO ermächtigt den Kunde widerruflich,
        die an TPO abgetretenen Forderungen in eigenem Namen für Rechnung von TPO einzuziehen. TPO darf diese
        Einzugsermächtigung nur im Verwertungsfall widerrufen.</p>
        <p>8.6 Greifen Dritte auf die Vorbehaltsware zu, insbesondere durch Pfändung, wird der Kunde sie unv erzüglich auf
        das Eigentum von TPO hinweisen und TPO hierüber informieren, um ihr die Durchsetzung ihrer Eigentumsrechte
        zu ermöglichen. Sofern der Dritte nicht in der Lage ist, TPO die in diesem Zusammenhang entstehenden
        gerichtlichen oder außergerichtlichen Kosten zu erstatten, haftet hierfür der Kunde gegenüber TPO.</p>
        <p>8.7 TPO wird die Vorbehaltsware sowie die an ihre Stelle tretenden Sachen oder Forderungen auf Verlangen nach
        ihrer Wahl freigeben, soweit ihr Wert die Höhe der gesicherten Forderungen um mehr als 10 % übersteigt.</p>
        <p>8.8 Tritt TPO bei vertragswidrigem Verhalten des Kunden– insbesondere Zahlungsverzug – vom Vertrag zurück
        (Verwertungsfall), ist TPO berechtigt, die Vorbehaltsware heraus zu verlangen.</p>
        <p><strong>9. Schadensersatzansprüche</strong></p>
        <p>9.1 Falls TPO ausdrücklich in die Aufhebung eines verbindlich erteilten Auftrages einwilligt, hat der Kunde 30 %
        der Auftragssumme zu zahlen, auch wenn wir dies bei der Aufhebung nicht ausdrücklich wiederholen. Dasselbe
        gilt, wenn der Kunde den Vertrag nicht erfüllt und bei Rücktritt. Ist der Lieferungsgegenstand bereits geliefert, erhöht
        sich der Pauschalbetrag um die Kosten Transportes sowie die Kosten der Aufarbeitung. Die Geltendmachung eines
        höheren Schadens ist nicht ausgeschlossen. Der Kunde ist berechtigt nachzuweisen, dass uns ein geringerer
        Schaden entstanden ist.</p>
        <p><strong>10. Schlussbestimmungen</strong></p>
        <p>10.1 Die rechtlichen Beziehungen zwischen dem Kunden und TPO unterliegen ausschließlich dem Recht der
        Bundesrepublik Deutschland unter Ausschluss der Bestimmungen des UN-Kaufrechts. Daneben gelten die
        Incoterms 2024 der internationalen Handelskammer Paris.</p>
        <p>10.2 Die TPO darf den Kunden nach Vertragsabschluss als Referenzkunden benennen. TPO hat das Recht, den
        Kundennamen als Referenz zu Werbezwecken zu nutzen. Dies gilt auch für die Werbung im Internet.
        Pressemitteilungen bedürfen darüber hinaus der einverständlichen Abstimmung des Texts.</p>
        <p>10.3 Erfüllungsort und ausschließlicher Gerichtsstand für alle Streitigkeiten aus der Geschäftsbeziehung zwischen
        TPO und dem Kunden ist Dortmund.</p>
        <p>10.4 Sollten einzelne Regelungen dieser AGB unwirksam sein oder werden, wird die Wirksamkeit der übrigen AGB
        davon nicht berührt.</p>
        <p>Die Allgemeinen Geschäftsbedingungen gelten für unseren gesamten Geschäftsverkehr mit unseren Kunden.
        Der Anwendung sämtlicher anders lautender Einkaufs- und Lieferbedingungen des Kunden wird hiermit ausdrücklich
        widersprochen, es sei denn, dass wir sie im Einzelfall explizit anerkannt haben. Die AGB werden von den Kunden mit
        Auftragserteilung anerkannt und gelten für die gesamte Dauer der Geschäftsverbindung, auch wenn wir auf die AGB bei
        der Annahme einzelner Aufträge nicht mehr Bezug nehmen. Sie gelten auch für künftige Geschäfte. Kunden sind sowohl
        juristische als auch natürliche Personen.</p>

        </div>
    </div>
    </body>
    </html>"""
    return template

def get_auftrag_template():
    """
    Retrieves the html structure for formatting the offer.
    """
    template = """<!DOCTYPE html>
    <html lang="de">
    <head>
    <meta charset="UTF-8">
    <style>
    @page {
    size: A4;
    margin: 30mm 20mm 30mm 20mm;
    font-size: 8px;
    font-family: Helvetica, sans-serif; 

    @bottom {
        content: "";
        border-top: 1px solid #ccc;
        height: 1px;
        margin-top: 2mm;
    }

    @bottom-left {
        content: "────────────────────────────────────────────" "\A"
                "Bankverbindung" "\A"
                "Volksbank Schnathorst" "\A"
                "IBAN: DE96 4926 2364 0070 4710 00" "\A"
                "BIC: GENODEM1SNA";
        white-space: pre;
    }

    @bottom-center {
        content: "──────────────────────────────────────────────" "\A" 
                "T.P.O." "\A"
                "Inh. Daniela Gross" "\A"
                "In den Fichten 34" "\A"
                "32584 Löhne";
        white-space: pre;
    }

    @bottom-right {
        content: "────────────────────────────────────────────" "\A"
                "Tel: 05731 755 13 11" "\A"
                "Fax: 05731 755 13 12" "\A"
                "Mail: tpo-gross@outlook.com" "\A"
                "UST-IdNr.: DE31 8295 117";
        white-space: pre;
    }
    }
    html {
    font-size: 8px;
    line-height: 1.5;
    }

    body {
        font-family: Helvetica, sans-serif;
        margin: 0;
        padding: 0;
        color: #222;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin: 30px 0px 0 0px;
    }

    .customer-info {
        max-width: 65%;
    }

    .logo {
        width: 170px;
        height: auto;
    }
    .logo img {
        width: 100%;
        height: auto;
    }

    /* Struktur */
    h2 {
        margin: 30px 30px 5px 30px;
        font-size: 11px;
    }
    p, th {
        font-size: 9px;
        margin: 0 30px;
    }

    table.content-table td {
        margin: 0 30px;
    }

    td {
        font-size: 9px;
        margin: 0; /* Kein globales margin mehr auf <td>! */
    }
    table {
        border-collapse: separate;
        border-spacing: 0 5px;
        margin: 18px 0px 0 0px;
        width: 100%;
    }
    th {
        background-color: #f0f0f0;
        text-align: left;
        padding: 4px;
        border-bottom: 1px solid #ccc;
    }
    td {
        background-color: #ffffff;
        padding: 4px;
        vertical-align: top;
        border: 1px solid #e0e0e0;
        border-top: none;
    }
    tr.no-split {
        page-break-inside: avoid;
    }
    .product-img {
        display: block;              /* Makes margin auto work */
        margin: 0 auto;              /* Center horizontally */
        max-width: 100%;
        max-height: 3.5cm;             /* or another fixed value */
        height: auto;
        object-fit: contain;
    }
    .totals-box {
        margin: 35px 30px 0 auto;
        width: 40%;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 8px 10px;
        font-size: 9px;
        background-color: #f9f9f9;
        page-break-inside: avoid;
    }
    .totals-box .row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
    }
    .totals-box .row.total {
        font-weight: bold;
        border-top: 1px solid #ccc;
        padding-top: 4px;
        margin-top: 6px;
    }

    td.product-description {
    padding: 2px 4px;
    line-height: 1.3;
    }

    .product-title {
    font-weight: bold;
    font-size: 9px;
    margin: 0;
    padding: 0;
    line-height: 1.2;
    }
    .product-alternative {
    font-weight: bold;
    font-size: 10px;
    line-height: 1.2;
    color: #B22222;
    }

    .product-text {
    font-size: 9px;
    margin: 0;
    padding: 0;
    line-height: 1.3;
    white-space: pre-wrap;
    }


    /* Customer block */
    .customer-block {
        font-size: 9px;            /* Make it bigger */
        line-height: 1.2;           /* Improve readability */
        margin-left: 0px;          /* Align exactly with table */
        margin-right: 30px;
        margin-bottom: 15px;
    }

    .customer-block p {
        font-size: 9px;
        line-height: 1.3;
        margin: 0;
    }

    .anschreiben {
        margin: 0;
        line-height: 1.6;
    }

    .anschreiben p {
        font-size: 9px;
        line-height: 1.6;
        margin: 0;
        padding: 0;
        text-indent: 0;
    }

    .angebot-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0;
        padding: 0;
        text-indent: 0;
    }

    .angebot-title {
        font-size: 16px;
        font-weight: bold;
    }

    .angebot-datum {
        font-size: 11px;
        color: #444;
    }

    /* Restlicher Text */
    .hinweise-block {
        font-size: 10px;
        margin-left: 0;
        line-height: 1.6;
    }

    .hinweise-block ol {
        font-size: 9px;
        padding-left: 2;
    }

    .hinweise-block li {
        font-size: 9px;
        margin-bottom: 4px;
        padding-left: 14px;
    }
    .AGB {
        font-size: 9px;
        margin-right: 0px;
        margin-bottom: 10px;
    }

    .AGB p {
        font-size: 9px;
        margin: 0 30px;
        margin-bottom: 10px;
        text-align: justify;
    }

    .agb-text {
        margin-top: 4px;
    }

    .unterschrift {
        margin-top: 15mm;
        text-align: right;
        font-size: 9px;
    }

    .unterschrift .line {
        border-top: 1px solid #000;
        width: 200px;
        margin-bottom: 2mm;
        float: right;
    }

    .unterschrift {
        margin-top: 15mm;
        font-size: 9px;
        text-align: right;
    }

    .line-with-label {
        display: inline-block;
        text-align: center;
    }

    .line {
        border-top: 1px solid #000;
        width: 200px;
        margin: 0 auto 2mm auto;
    }

    .label {
        width: 200px;
        text-align: center;
    }

    /* Footer wird durch diese Box "nach unten gedrückt" */
    .footer-push {
        height: 100px;
    }
    </style>
    </head>
    <body>

    <div class="header">
    <div class="customer-block">
        <p style="font-size: 13px;"><strong>{{ kunde['Firma'] }}</strong></p>
        <p>{{ kunde['Anrede'] }} {{ kunde['Vorname'] }} {{ kunde['Nachname'] }}</p>
        <p>{{ kunde['Adresse'] }}</p>
        <p>{{ kunde['PLZ'] }} {{ kunde['Ort'] }}</p>
        <p>Tel.: {{ kunde['Telefonnummer'] }}</p>
        <p>E-Mail: {{ kunde['E_Mail'] }}</p>
    </div>
    <div class="logo">
        <img src="{{ logo_base64 }}" alt="Logo">
    </div>
    </div>

    <div class="angebot-row">
    <div class="angebot-title" style="font-size: 13px;">Auftragsbestätigung: {{ angebot_id }}</div>
    <div class="angebot-datum">{{ aktuelles_datum }}</div>
    </div>

    <div class="anschreiben">
    {% if kunde['Anrede'] == 'Herr' %}
    <p>Sehr geehrter Herr {{ kunde['Nachname'] }},</p>
    {% elif kunde['Anrede'] == 'Frau' %}
    <p>Sehr geehrte Frau {{ kunde['Nachname'] }},</p>
    {% else %}
    <p>Sehr geehrte Damen und Herren,</p>
    {% endif %}
    <p>für Ihren Auftrag und Ihr Interesse an unseren Produkten und Dienstleistungen dürfen wir uns bedanken.</p> 
    <p>Gerne bestätigen wir Ihnen wie folgt.</p>
    <p>Für Fragen stehen wir Ihnen gerne jeder Zeit zur Verfügung.</p>
    </div>
    <table>
    <colgroup>
        <col style="width: 5%;">
        <col style="width: 25%;">
        <col style="width: 43%;">
        <col style="width: 5%;">
        <col style="width: 12%;">
        <col style="width: 10%;">
    </colgroup>
    <thead>
    <tr>
    <th>Pos.</th>
    <th>Abbildungen ähnlich</th>
    <th>Bezeichnung</th>
    <th>Menge</th>
    <th>Preis/st netto</th>
    <th>Gesamtpreis</th>
    </tr>
    </thead>
    <tbody>
    {% for row in products %}
        {% if not row['Alternative'] %}
        <tr class="product-row{% if loop.index > 1 %} no-split{% endif %}">
            <td><strong>{{ row['Positionsbezeichnung'] }}</strong></td>
            <td>
                {% if row['image'] %}
                    <img src="{{ row['image'] }}" class="product-img">
                {% endif %}
            </td>
            <td class="product-description">
                {% if row['Titel'] %}
                    <div class="product-title">{{ row['Titel'] }}</div>
                {% endif %}
                <div class="product-text">{{ row['Beschreibung'] or '' }}</div>
            </td>
            <td>
                {% if row.Menge is not none %}
                    {% if row.Menge == row.Menge|int %}
                        {{ row.Menge|int }}
                    {% else %}
                        {% set formatted = "%.2f"|format(row.Menge) %}
                        {{ formatted.replace('.', ',') }}
                    {% endif %}
                {% endif %}
            </td>
            <td>{{ row.Preis | german_currency }} €</td>
            <td>
                {% if row.Menge is not none %}
                    {{ row.Gesamtpreis | german_currency }} €
                {% else %}
                    {{ row.Preis | german_currency }} €
                {% endif %}
            </td>
        </tr>
        {% endif %}
    {% endfor %}

    </tbody>
    </table>

    <div class="totals-box">
    <div class="row">
        <div>Netto Gesamt:</div>
        <div>{{ netto | german_currency }} €</div>
    </div>

    {% if rabatt != 0 %}
    <div class="row">
        <div>{{ rabatt|replace('.', ',') }}% Rabatt:</div>
        <div>-{{ rabatt_num | german_currency }} €</div>
    </div>
    {% endif %}

    {% if if_mwst == True %}
    <div class="row">
        <div>19% MwSt:</div>
        <div>{{ mwst | german_currency }} €</div>
    </div>
    {% endif %}
    {% if if_mwst == False %}
    <div class="row">
        <div>ATU-Nummer:</div>
        <div>{{atu}}</div>
    </div>
    {% endif %}
    <div class="row total">
        <div>Brutto Gesamt:</div>
        <div>{{ brutto | german_currency }} €</div>
    </div>
    </div>

    <div class="hinweise-block" style="page-break-before: always;">
    <p><strong>Montagekostenpauschale</strong><br>
    Konzessionspflichtige Anschlüsse sowie Maurer- und Stemmarbeiten sind nicht im Preis enthalten und müssen bauseits erstellt werden.</p>

    <p>Zusätzliche Arbeiten, Wartezeiten, Verkleidungsbleche, Montage- und Anschlussmaterial werden nach tatsächlichem Aufwand berechnet.</p>

    <p>Um Mehrkosten zu vermeiden, sorgen Sie bitte dafür:</p>
    <ol>
        <li>dass der Aufstellungsort frei zugänglich ist</li>
        <li>dass das Gerät ohne Umstände eintransportiert werden kann (Türbreite etc.)</li>
        <li>dass der Ablaufanschluss in Gerätenähe zugänglich ist</li>
        <li>dass der Wasseranschluss in der Nähe (max. 2m) zugänglich ist und ein Absperrhahn versehen ist</li>
        <li>dass der Stromanschluss in Gerätenähe und idealerweise mit Steckdose ausgerüstet ist,<br>wahlweise auch mit einer Festanschlussdose.
        <br>(bei Festanschluss müssen die Sicherungen oder Schalter zugänglich sein)</li>
    </ol>

    <p><strong><em>Alle Leitungen müssen Unterputz verlegt werden!</em></strong></p>

    <p>Bitte beachten Sie, dass über Gas-Geräte eine Dunstabzugshaube bauseits vorhanden sein muss.</p>
    <p>Der Gas-Anschluß des Gerätes an die Versorgungsleitungen darf nur durch einen konzessionierten Fachbetrieb vorgenommen werden.</p>

    <p class="agb-text"><strong>Zu- und Abluftbauseits</strong></p>

    <p class="agb-text">
        Der Vertrag wird unter Verwendung unserer Allgemeinen Geschäftsbedingungen, sowie den unten stehenden Zahlungsbedingungen geschlossen.
        Diese werden Ihnen auf Wunsch kostenlos übersandt und sind im Internet unter www.tpo-gross.de einzusehen. 
        Konzessionspflichtige Anschlüsse sowie Maurer- und Stemmarbeiten sind nicht im Preis enthalten und müssen bauseits erstellt werden. 
        Zu evtl. weiteren Entgeltminderungen verweisen wir auf die getroffenen Vereinbarungen.
    </p>

    <p style="margin-top: 4mm;"><strong>Zahlungsbedingungen:</strong><br>
    {{ payment_details or "Vorkasse"}}
    </p>

    <div class="unterschrift">
    <div class="line-with-label">
        <div class="line"></div>
        <div class="label">Datum, Unterschrift</div>
    </div>
    </div>
    <div class="AGB" style="page-break-before: always;">
    <p><strong>Durch die nachfolgenden Allgemeinen Geschäftsbedingungen (AGB) werden die vertraglichen Beziehungen
    zwischen der TPO (nachfolgend TPO) und dem Kunden geregelt. TPO verkauft Gastronomiebedarf an gewerbliche Kunden.</strong></p>
        <p><strong>1. Allgemeines</strong></p>
        <p>1.1 Alle Lieferungen und Leistungen erfolgen ausschließlich auf Grundlage dieser AGB. Diese sind Bestandteil aller
        Verträge, die TPO mit den Kunden schließt. Sie gelten auch für alle zukünftigen Verträge mit den Kunden, auch
        wenn sie nicht nochmals gesondert vereinbart wurden.</p>
        <p>1.2 Geschäftsbedingungen der Kunden oder Dritter finden keine Anwendung, auch wenn TPO ihrer Geltung im
        Einzelfall nicht gesondert widerspricht.</p>
        <p>1.3 Der Kunde versichert durch seine Anmeldung dass er Unternehmer i.S. d. § 14 BGB und der europarechtlichen
        Vorschriften ist und die Waren ausschließlich zu unternehmerischen Zwecken nutzt.</p>
        <p>1.4 TPO prüft regelmäßig bei Vertragsabschlüssen und in bestimmten Fällen, in denen ein berechtigtes Interesse
        vorliegt, Ihre Bonität. Dazu arbeiten wir mit der Creditreform Herford & Minden Dorff GmbH & Co. KG, Krellstraße
        68, 32584 Löhne zusammen, von der wir die dazu benötigten Daten erhalten. Zu diesem Zweck übermitteln wir
        Ihren Namen und Ihre Kontaktdaten an die Creditreform. Weitere Informationen zur Datenverarbeitung bei
        Creditreform erhalten Sie in dem ausführlichen Merkblatt „Creditreform-Informationen gem. Art. 14 EU-DSGVO
        oder unter <a href="www.creditreform-ORT.de/EU-DSGVO" target="_blank".>www.creditreform-ORT.de/EU-DSGVO</a>.</p>
        <p>1.5 TPO behält sich vor, bei unvorhersehbaren Änderungen, die TPO nicht veranlasst hat und auf die TPO auch
        keinen Einfluss hat und durch die das bei Vertragsschluss vorhandene Äquivalenzverhältnis in nicht
        unbedeutendem Maße gestört wurde, diese AGB zu ändern, soweit dies dem Kunden zumutbar ist. Die Kunden
        werden über die Änderungen umgehend informiert. Hierbei werden dem Kunden die geänderten AGB unter
        Hervorhebung der abgeänderten Passagen übersandt. Dies kann auch per Email erfolgen. Sollte der Kunde nicht
        innerhalb von sechs Wochen seit der Mitteilung den geänderten AGB widersprechen, so gelten diese als genehmigt
        und finden auch auf bereits bestehende Verträge Anwendung. Hierauf wird der Kunde bei der Mitteilung über die
        Änderung besonders hingewiesen.</p>
        <p><strong>2. Angebot und Vertragsschluss</strong></p>
        <p>2.1 Alle Angebote von TPO sind freibleibend und unverbindlich, es sei denn sie sind ausdrücklich als verbindlich
        gekennzeichnet. Sie verstehen sich lediglich als Aufforderung an den Kunden, ein Angebot gegenüber TPO
        abzugeben. Angaben von TPO über Maße, Gewichte, technische Daten usw. sowie Darstellungen und Abbildungen
        insbesondere auf den Internetseiten von TPO oder in Katalogen sind ebenfalls unverbindlich, soweit nicht die
        Verwendbarkeit zum vertraglichen vereinbarten Zweck eine genaue Übereinstimmung voraussetzt. Sie stellen
        keine Beschaffenheitsgarantie dar, sondern dienen lediglich der Beschreibung oder Kennzeichnung.
        Handelsübliche Abweichungen und solche, die auf grundrechtlicher Vorschriften erfolgen oder technische
        Verbesserungen darstellen sind zulässig soweit sie die Verwendbarkeit zum vertraglich vereinbarten Zweck nicht
        beeinträchtigen und dem Kunden zumutbar sind. Gleiches gilt für die Ersetzung von Bauteilen durch technisch
        mindestens Gleichwertige.</p>
        <p>2.2 Der Vertrag kommt folgendermaßen zu Stande: Der auf der Website dargestellte Warenkatalog stellt kein
        Angebot im juristischen Sinne dar. Mit der Bestellung erklärt der Kunde verbindlich sein Vertragsangebot.
        Eingabefehler können vor Absenden der Bestellung mittels der üblichen Tastatur- und Mausfunktionen berichtigt
        werden. Mit Mausklick auf den Bestellbutton unterbreitet der Kunde ein verbindliches Kaufangebot. Nach Eingang
        des Angebots des Kunden bei TPO erhält der Kunde eine automatisch generierte E-Mail, die den Eingang der
        Bestellung deren Einzelheiten aufführt. Diese Bestätigung stellt keine Annahme des Angebots durch den Verkäufer
        dar. Eine Bestellung des Kunden wird ausdrücklich durch Übersendung einer entsprechenden Auftragsbestätigung
        oder konkludent durch Ausführung der Lieferung oder Leistung angenommen.</p>
        <p>2.3 TPO behält sich das Eigentum oder Urheberrecht an allen abgegebenen Angeboten und Kostenvoranschlägen
        sowie sonstigen Unterlagen vor, die dem Kunden zur Verfügung gestellt wurden, sofern keine
        Eigentumsübertragung oder Übertragung von entsprechenden Rechten vereinbart wurde. Der Kunde darf diese
        Unterlagen nicht ohne Zustimmung von TPO Dritten zugänglich machen, vervielfältigen, bekanntgeben, selbst oder
        durch Dritte nutzen. Der Kunde ist verpflichtet diese Unterlagen auf Aufforderung an TPO herauszugeben und
        angefertigte Kopien zu vernichten, wenn diese im Rahmen der Geschäftsbeziehung nicht mehr benötigt werden.</p>
        <p>2.4 Der Vertragstext wird von uns nicht gespeichert.</p>
        <p><strong>3. Preise und Zahlung</strong></p>
        <p>3.1 Alle Preise verstehen sich in EUR ab Werk zuzüglich Verpackung, der gesetzlichen Umsatzsteuer, bei
        Exportlieferungen zuzüglich Zoll sowie Gebühren und anderer öffentlicher Abgaben. Für Lieferungen innerhalb
        Deutschlands fallen keine zusätzlichen Versandkosten an (bei Inseln und Bergstationen frei Station
        Festland/Talstation). Die Versandkosten für andere europäische Länder können Sie der Versandkostentabelle in
        den Lieferbedingungen entnehmen.</p>
        <p>3.2 Liegt der Liefertermin mehr als vier Monate nach dem Vertragsschluss, ist TPO berechtigt die Preise
        angemessen zu erhöhen und die Preise an veränderte Preisgrundlagen (Material, Löhne usw.) anzupassen. Es
        gelten dann die am Liefertag gültigen Preise.</p>
        <p>3.3 Die Zahlung erfolgt wahlweise per Kreditkarte, Sofortüberweisung, Leasing, Rechnung oder Vorkasse.</p>
        <p>3.4 Bei Auswahl der Zahlungsart Vorkasse nennen wir Ihnen unsere Bankverbindung in der Auftragsbestätigung
        bzw. im Anschluss. Der Rechnungsbetrag ist binnen 5 Tagen auf unser Konto zu überweisen. Die Belastung Ihres
        Kreditkartenkontos sowie der Bankeinzug erfolgen mit Abschluss der Bestellung.</p>
        <p>3.5 Kommen Sie in Zahlungsverzug, so ist der Kaufpreis während des Verzuges in Höhe von 5% über dem
        Basiszinssatz zu verzinsen. Wir behalten uns vor, einen höheren Verzugsschaden nachzuweisen und geltend zu
        machen. Mit Erhalt der 2. Mahnung wird eine zusätzliche Gebühr von 7,50 EUR berechnet.</p>
        <p>3.6 Eine Aufrechnung mit Zahlungsansprüchen des Kunden oder die Zurückbehaltung von Zahlungen wegen
        solcher Ansprüche ist nur mit unbestrittenen oder rechtskräftig festgestellten Forderungen zulässig.</p>
        <p>3.7 Werden nach Vertragsschluss Umstände bekannt, die geeignet sind die Kreditwürdigkeit des Kunden
        wesentlich herabzusetzen und durch die die Bezahlung der noch offenen Forderungen aus dem jeweiligen
        Vertragsverhältnis gefährdet wird so ist TPO berechtigt, die noch ausstehenden Lieferungen und Leistungen nur
        gegen Vorauszahlung oder Sicherheitsleistung zu erbringen.</p>
        <p><strong>4. Erfüllungsort, Versand</strong></p>
        <p>4.1 Soweit die Parteien nichts anderes bestimmen, ist der Erfüllungsort für alle Verpflichtungen aus dem
        Vertragsverhältnis der Sitz von TPO.</p>
        <p>4.2 Die Versandart und die Verpackung unterstehen dem pflichtgemäßen Ermessen von TPO .</p>
        <p>4.3 Mit Übergabe des Liefergegenstandes an den Spediteur, Frachtführer oder an eine sonstige zur Ausführung
        der Versendung bestimmten Dritten geht die Gefahr auf den Kunden über. Dies gilt auch, wenn Teillieferungen
        erfolgen oder der Verkäufer noch andere Leistungen (z. B. Installation) übernommen hat. Verzögert sich der
        Versand durch Umstände die der Kunde zu vertreten hat, so geht die Gefahr mit dem Zeitpunkt auf den Kunden
        über, mit dem TPO versandbereit ist und dies dem Kunden angezeigt hat.</p>
        <p>4.4 Lagerkosten nach Gefahrübergang trägt der Kunde. Erfolgt die Lagerung durch TPO so betragen die
        Lagerkosten 0,25% des Rechnungsbetrages der zu lagernden Liefergegenstände pro abgelaufener Woche. Die
        Geltendmachung und der Nachweis weiterer oder geringerer Lagerkosten bleiben vorbehalten.</p>
        <p><strong>5. Lieferung</strong></p>
        <p>5.1 Lieferungen erfolgen ab Werk (EXW) gemäß Incoterms 2010. Es wird ausdrücklich vereinbart, dass die
        Lieferung durch ein vom Verkäufer ausgesuchtes und beauftragtes Transportunternehmen vorgenommen wird. Es
        wird ausdrücklich vereinbart, dass das Transportunternehmen nur bis zur Bordsteinkante liefert.</p>
        <p>5.2 Unbeschadet ihrer Rechte aus Verzug des Kunden, kann TPO eine Verlängerung der Liefer- und
        Leistungsfristen um den Zeitraum verlangen, in dem der Kunden seinen vertraglichen Pflichten nicht nachkommt.
        Kann oder will der Kunde die Ware zum vereinbarten Zeitpunkt nicht abnehmen, kann TPO sämtliche durch den
        Annahmeverzug entstehenden Mehrkosten dem Kunden gesondert in Rechnung stellen. Bei Nichtdurchführung
        des Auftrags aus vom Kunden zu vertretenden Gründen gelten 30% der Auftragssumme als Schadensersatz
        vereinbart. Dem Kunden bleibt das Recht vorbehalten, nachzuweisen, dass uns durch die Nichtdurchführung kein
        oder ein wesentlich geringerer Schaden entstanden ist.</p>
        <p>5.3 TPO haftet nicht für die Unmöglichkeit der Lieferung oder Leistung oder für Lieferverzögerungen, soweit diese
        durch höhere Gewalt oder sonstige, zum Zeitpunkt des Vertragsschlusses nicht vorhersehbare Ereignisse die TPO
        nicht zu vertreten hat, verursacht worden sind. Erschweren solche Ereignisse TPO die Lieferung oder Leistung
        wesentlich oder machen sie unmöglich und ist die Behinderung nicht nur von vorübergehender Dauer, ist TPO zum
        Rücktritt vom Vertrag berechtigt.
        Bei Behinderungen von nur vorübergehender Dauer verlängern sich die Liefer- oder Leistungsfristen oder
        verschieben sich die Liefer- oder Leistungstermine um den Zeitraum der Behinderung zuzüglich einer
        angemessenen Anlauffrist.</p>
        <p>5.4 Soweit dem Kunden durch die Verzögerung die Abnahme der Lieferung oder Leistung nicht zuzumuten ist,
        kann er durch unverzügliche schriftliche Erklärung gegenüber TPO vom Vertrag zurück treten.</p>
        <p>5.5 TPO ist zu Teillieferungen berechtigt, soweit dem Kunden hierdurch kein erheblicher Mehraufwand und/oder
        zusätzliche Kosten entstehen, die Teillieferung für den Kunden im Rahmen des vertraglichen Bestimmungszweckes
        verwendbar ist und die Lieferung der restlichen bestellten Waren gesichert ist.</p>
        <p>5.6 Der Kunde ist verpflichtet, sich erkennbare Transportschäden sofort beim Empfang vom Transportunternehmer
        bescheinigen zu lassen um Ersatzforderungen an das Transportunternehmen geltend zu machen. TPO ist bemüht,
        dem Kunden bei der Abwicklung von Transportschäden behilflich zu sein. Äußerlich nicht erkennbare Schäden
        müssen nach Kenntnis telefonisch und schriftlich beim Transporteur angezeigt werden. Für die Einhaltung der Frist
        und Abwicklung des Transportschadens ist der Kunde alleinverantwortlich. Der Kunde ist als Empfänger zur
        Geltendmachung von Ansprüchen gegen das Transportunternehmen aus dem Frachtvertrag gemäß § 421 HGB im
        eigenen Namen berechtigt.</p>
        <p><strong>6. Gewährleistung</strong></p>
        <p>6.1 Die Gewährleistungsfrist beträgt ein Jahr ab Lieferung.</p>
        <p>6.2 Die gelieferten Gegenstände sind gem. § 377 HGB unverzüglich nach Ablieferung an den Kunden oder an den
        von ihm bestimmten Dritten sorgfältig zu untersuchen. Sie gelten als genehmigt, wenn TPO nicht eine Mängelrüge
        hinsichtlich offensichtlicher oder anderer Mängel, die bei einer unverzüglichen und sorgfältigen Untersuchung
        erkennbar waren, unverzüglich nach Ablieferung des Liefergegenstandes oder ansonsten unverzüglich nach der
        Entdeckung des Mangels oder dem Zeitpunkt in dem der Mangel für den Kunden bei normaler Verwendung des
        Liefergegenstandes ohne nähere Untersuchung erkennbar war, in Textform zugegangen ist.</p>
        <p>6.3 Auf Verlangen von TPO ist der beanstandete Gegenstand frachtfrei an diese zurück zu senden. Bei berechtigter
        Mängelrüge vergütet TPO die Kosten des günstigsten Versandweges. Dies gilt nicht, wenn die Kosten sich erhöhen,
        weil der Gegenstand sich an einem anderem Ort als dem Ort des bestimmungsgemäßen Gebrauchs befindet.</p>
        <p>6.4 Bei Sachmängeln ist TPO zur Nacherfüllung nach seiner Wahl zunächst zur Nachbesserung oder
        Ersatzlieferung verpflichtet und berechtigt. Eine Nacherfüllung gilt nach dem zweiten erfolglosen Versuch als
        fehlgeschlagen. Im Falle des Fehlschlagens, der Unmöglichkeit, Unzumutbarkeit, Verweigerung oder
        unangemessenen Verzögerung der Nachbesserung oder Ersatzlieferung, kann der Kunde vom Vertrag
        zurücktreten oder den Kaufpreis angemessen mindern. Ergibt sich bei einer im Rahmen der Mängelrüge
        durchgeführten Prüfung der Ware, dass die Mängelrüge zu Unrecht erfolgt ist, sind wir berechtigt, eine
        verkehrsübliche Vergütung für die Prüfung der Ware sowie die Kosten für den Versand zu berechnen.</p>
        <p>6.5 Der Gewährleistungsanspruch entfällt, wenn der Kunde den Kaufgegenstand ohne ausdrückliche Zustimmung
        von TPO ändert oder durch Dritte ändern lässt und die Mängelbeseitigung hierdurch unmöglich oder unzumutbar
        erschwert wird. In jedem Fall hat der Kunde die durch die Änderungen entstehenden Mehrkosten der
        Mängelbeseitigung zu tragen.</p>
        <p>6.6 Ein etwa erforderlicher Anschluss an die Versorgungsleitungen (Strom, Wasser, Dampf, Abwasser,
        Heißwasser, Gas, etc.) ist vom Käufer auf seine Kosten zu veranlassen, und darf nur von konzessionierten örtlichen
        Elektrofachleuten bzw. Installateuren vorgenommen werden. Ist ein Mangel auf eine nicht fachgerechte Installation
        zurückzuführen, entfällt der Gewährleistungsanspruch gegen TPO.</p>
        <p>6.7 Die Lieferung gebrauchter Gegenstände erfolgt unter Ausschluss jeglicher Gewährleistung.</p>
        <p>6.8 Sollte durch den Hersteller des Liefergegenstandes eine längere Gewährleistungsfrist oder eine Garantie
        eingeräumt werden, so treten wir unsere Rechte hieraus bereits mit dem Kauf an den Besteller/Käufer ab.</p>
        <p>6.9 Im Übrigen gilt Ziffer 7 dieses Vertrages.</p>
        <p><strong>7. Haftung</strong></p>
        <p>7.1 Für Schäden, die an anderen Rechtsgütern als dem Leben, Körper oder Gesundheit entstehen ist die Haftung
        ausgeschlossen, soweit die Schäden nicht auf vorsätzlichem oder grob fahrlässigem Verhalten der TPO, eines von
        deren gesetzlichen Vertretern oder eines von deren Erfüllungsgehilfen beruhen und das Verhalten auch keine
        Verletzung von vertragswesentlichen Pflichten ist. Wesentliche Vertragspflichten sind solche Pflichten, deren
        Erfüllung die ordnungsgemäße Durchführung des Vertrages überhaupt erst ermöglicht und auf deren Einhaltung
        der Nutzer regelmäßig vertrauen darf.</p>
        <p>7.2 In jedem Fall ist der Nutzer ebenfalls zur Schadensbegrenzung verpflichtet. Dies beinhaltet die rechtzeitige
        Anzeige von Schäden im Rahmen der weiteren Schadensminimierung.</p>
        <p>7.3 Haftet TPO für den Verlust von Daten, die der Kunde auf der Webseite hinterlegt hat, so gilt, dass TPO nur
        insoweit haftet, soweit der Kunde alle erforderlichen und zumutbaren Datensicherungsvorkehrungen getroffen und
        sichergestellt hat, dass die Daten aus Datenmaterial, das in maschinenlesbarer Form bereitgehalten wird, mit
        vertretbarem Aufwand rekonstruiert werden können.</p>
        <p>7.4 Die vorgenannten Haftungsausschlüsse und Beschränkungen gelten außerdem nicht im Fall der Übernahme
        ausdrücklicher Garantien durch TPO sowie bei Ansprüchen wegen fehlender zugesicherter Eigenschaften oder
        Ansprüchen aus dem Produkthaftungsgesetz.</p>
        <p><strong>8. Eigentumsvorbehalt</strong></p>
        <p>8.1 Die von TPO an den Kunden gelieferte Ware bleibt bis zur vollständigen Bezahlung aller gesicherten
        Forderungen Eigentum von TPO. Die Ware sowie die nach dieser Klausel an ihre Stelle tretende, vom
        Eigentumsvorbehalt erfasste Ware wird nachfolgend Vorbehaltsware genannt.</p>
        <p>8.2 Der Kunde verwahrt die Vorbehaltsware unentgeltlich für TPO.</p>
        <p>8.3 Der Kunde ist berechtigt, die Vorbehaltsware bis zum Eintritt des Verwertungsfalls im ordnungsgemäßen
        Geschäftsverkehr zu verarbeiten und zu veräußern. Verpfändungen und Sicherungsübereignungen sind
        unzulässig.</p>
        <p>8.4 Wird die Vorbehaltsware vom Kunde verarbeitet, so erfolgt die Verarbeitung im Namen und für Rechnung von
        TPO und TPO erwirbt unmittelbar das Eigentum oder – wenn die Verarbeitung aus Stoffen mehrerer Eigentümer
        erfolgt oder der Wert der verarbeiteten Sache höher ist als der Wert der Vorbehaltsware – das Miteigentum
        (Bruchteilseigentum) an der neu geschaffenen Sache im Verhältnis des Werts der Vorbehaltsware zum Wert der
        neu geschaffenen Sache erwirbt. Für den Fall, dass kein solcher Eigentumserwerb bei TPO eintreten sollte,
        überträgt der Kunde bereits jetzt sein künftiges Eigentum oder – im o.g. Verhältnis – Miteigentum an der neu
        geschaffenen Sache zur Sicherheit an TPO. Wird die Vorbehaltsware mit anderen Sachen zu einer einheitlichen
        Sache verbunden oder untrennbar vermischt und ist eine der anderen Sachen als Hauptsache anzusehen, so
        überträgt TPO, soweit die Hauptsache ihr gehört, dem Kunde anteilig das Miteigentum an der einheitlichen Sache
        in dem in Satz 1 genannten Verhältnis.</p>
        <p>8.5 Im Fall der Weiterveräußerung der Vorbehaltsware tritt der Kunde bereits jetzt sicherungshalber die hieraus
        entstehende Forderung gegen den Erwerber – bei Miteigentum von TPO an der Vorbehaltsware anteilig
        entsprechend dem Miteigentumsanteil – an TPO ab. Gleiches gilt für sonstige Forderungen, die an die Stelle der
        Vorbehaltsware treten oder sonst hinsichtlich der Vorbehaltsware entstehen, wie z.B. Versicherungsansprüche
        oder Ansprüche aus unerlaubter Handlung bei Verlust oder Zerstörung. TPO ermächtigt den Kunde widerruflich,
        die an TPO abgetretenen Forderungen in eigenem Namen für Rechnung von TPO einzuziehen. TPO darf diese
        Einzugsermächtigung nur im Verwertungsfall widerrufen.</p>
        <p>8.6 Greifen Dritte auf die Vorbehaltsware zu, insbesondere durch Pfändung, wird der Kunde sie unv erzüglich auf
        das Eigentum von TPO hinweisen und TPO hierüber informieren, um ihr die Durchsetzung ihrer Eigentumsrechte
        zu ermöglichen. Sofern der Dritte nicht in der Lage ist, TPO die in diesem Zusammenhang entstehenden
        gerichtlichen oder außergerichtlichen Kosten zu erstatten, haftet hierfür der Kunde gegenüber TPO.</p>
        <p>8.7 TPO wird die Vorbehaltsware sowie die an ihre Stelle tretenden Sachen oder Forderungen auf Verlangen nach
        ihrer Wahl freigeben, soweit ihr Wert die Höhe der gesicherten Forderungen um mehr als 10 % übersteigt.</p>
        <p>8.8 Tritt TPO bei vertragswidrigem Verhalten des Kunden– insbesondere Zahlungsverzug – vom Vertrag zurück
        (Verwertungsfall), ist TPO berechtigt, die Vorbehaltsware heraus zu verlangen.</p>
        <p><strong>9. Schadensersatzansprüche</strong></p>
        <p>9.1 Falls TPO ausdrücklich in die Aufhebung eines verbindlich erteilten Auftrages einwilligt, hat der Kunde 30 %
        der Auftragssumme zu zahlen, auch wenn wir dies bei der Aufhebung nicht ausdrücklich wiederholen. Dasselbe
        gilt, wenn der Kunde den Vertrag nicht erfüllt und bei Rücktritt. Ist der Lieferungsgegenstand bereits geliefert, erhöht
        sich der Pauschalbetrag um die Kosten Transportes sowie die Kosten der Aufarbeitung. Die Geltendmachung eines
        höheren Schadens ist nicht ausgeschlossen. Der Kunde ist berechtigt nachzuweisen, dass uns ein geringerer
        Schaden entstanden ist.</p>
        <p><strong>10. Schlussbestimmungen</strong></p>
        <p>10.1 Die rechtlichen Beziehungen zwischen dem Kunden und TPO unterliegen ausschließlich dem Recht der
        Bundesrepublik Deutschland unter Ausschluss der Bestimmungen des UN-Kaufrechts. Daneben gelten die
        Incoterms 2024 der internationalen Handelskammer Paris.</p>
        <p>10.2 Die TPO darf den Kunden nach Vertragsabschluss als Referenzkunden benennen. TPO hat das Recht, den
        Kundennamen als Referenz zu Werbezwecken zu nutzen. Dies gilt auch für die Werbung im Internet.
        Pressemitteilungen bedürfen darüber hinaus der einverständlichen Abstimmung des Texts.</p>
        <p>10.3 Erfüllungsort und ausschließlicher Gerichtsstand für alle Streitigkeiten aus der Geschäftsbeziehung zwischen
        TPO und dem Kunden ist Dortmund.</p>
        <p>10.4 Sollten einzelne Regelungen dieser AGB unwirksam sein oder werden, wird die Wirksamkeit der übrigen AGB
        davon nicht berührt.</p>
        <p>Die Allgemeinen Geschäftsbedingungen gelten für unseren gesamten Geschäftsverkehr mit unseren Kunden.
        Der Anwendung sämtlicher anders lautender Einkaufs- und Lieferbedingungen des Kunden wird hiermit ausdrücklich
        widersprochen, es sei denn, dass wir sie im Einzelfall explizit anerkannt haben. Die AGB werden von den Kunden mit
        Auftragserteilung anerkannt und gelten für die gesamte Dauer der Geschäftsverbindung, auch wenn wir auf die AGB bei
        der Annahme einzelner Aufträge nicht mehr Bezug nehmen. Sie gelten auch für künftige Geschäfte. Kunden sind sowohl
        juristische als auch natürliche Personen.</p>

        </div>
    </div>
    </body>
    </html>"""

    return template

def get_short_angebot_template():
    
    template = """<!DOCTYPE html>
    <html lang="de">
    <head>
    <meta charset="UTF-8">
    <style>
    @page {
    size: A4;
    margin: 30mm 20mm 30mm 20mm;
    font-size: 8px;
    font-family: Helvetica, sans-serif; 

    @bottom {
        content: "";
        border-top: 1px solid #ccc;
        height: 1px;
        margin-top: 2mm;
    }

    @bottom-left {
        content: "────────────────────────────────────────────" "\A"
                "Bankverbindung" "\A"
                "Volksbank Schnathorst" "\A"
                "IBAN: DE96 4926 2364 0070 4710 00" "\A"
                "BIC: GENODEM1SNA";
        white-space: pre;
    }

    @bottom-center {
        content: "──────────────────────────────────────────────" "\A" 
                "T.P.O." "\A"
                "Inh. Daniela Gross" "\A"
                "In den Fichten 34" "\A"
                "32584 Löhne";
        white-space: pre;
    }

    @bottom-right {
        content: "────────────────────────────────────────────" "\A"
                "Tel: 05731 755 13 11" "\A"
                "Fax: 05731 755 13 12" "\A"
                "Mail: tpo-gross@outlook.com" "\A"
                "UST-IdNr.: DE31 8295 117";
        white-space: pre;
    }
    }
    html {
    font-size: 8px;
    line-height: 1.5;
    }

    body {
        font-family: Helvetica, sans-serif;
        margin: 0;
        padding: 0;
        color: #222;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin: 30px 0px 0 0px;
    }

    .customer-info {
        max-width: 65%;
    }

    .logo {
        width: 170px;
        height: auto;
    }
    .logo img {
        width: 100%;
        height: auto;
    }

    /* Struktur */
    h2 {
        margin: 30px 30px 5px 30px;
        font-size: 11px;
    }
    p, th {
        font-size: 9px;
        margin: 0 30px;
    }

    table.content-table td {
        margin: 0 30px;
    }

    td {
        font-size: 9px;
        margin: 0; /* Kein globales margin mehr auf <td>! */
    }
    table {
        border-collapse: separate;
        border-spacing: 0 5px;
        margin: 18px 0px 0 0px;
        width: 100%;
    }
    th {
        background-color: #f0f0f0;
        text-align: left;
        padding: 4px;
        border-bottom: 1px solid #ccc;
    }
    td {
        background-color: #ffffff;
        padding: 4px;
        vertical-align: top;
        border: 1px solid #e0e0e0;
        border-top: none;
    }
    tr.no-split {
        page-break-inside: avoid;
    }
    .product-img {
        display: block;              /* Makes margin auto work */
        margin: 0 auto;              /* Center horizontally */
        max-width: 100%;
        max-height: 3.5cm;             /* or another fixed value */
        height: auto;
        object-fit: contain;
    }
    .totals-box {
        margin: 35px 30px 0 auto;
        width: 40%;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 8px 10px;
        font-size: 9px;
        background-color: #f9f9f9;
        page-break-inside: avoid;
    }
    .totals-box .row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
    }
    .totals-box .row.total {
        font-weight: bold;
        border-top: 1px solid #ccc;
        padding-top: 4px;
        margin-top: 6px;
    }

    td.product-description {
    padding: 2px 4px;
    line-height: 1.3;
    }

    .product-title {
    font-weight: bold;
    font-size: 9px;
    margin: 0;
    padding: 0;
    line-height: 1.2;
    }
    .product-alternative {
    font-weight: bold;
    font-size: 10px;
    line-height: 1.2;
    color: #B22222;
    }

    .product-text {
    font-size: 9px;
    margin: 0;
    padding: 0;
    line-height: 1.3;
    white-space: pre-wrap;
    }


    /* Customer block */
    .customer-block {
        font-size: 9px;            /* Make it bigger */
        line-height: 1.2;           /* Improve readability */
        margin-left: 0px;          /* Align exactly with table */
        margin-right: 30px;
        margin-bottom: 15px;
    }

    .customer-block p {
        font-size: 9px;
        line-height: 1.3;
        margin: 0;
    }

    .anschreiben {
        margin: 0;
        line-height: 1.6;
    }

    .anschreiben p {
        font-size: 9px;
        line-height: 1.6;
        margin: 0;
        padding: 0;
        text-indent: 0;
    }

    .angebot-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0;
        padding: 0;
        text-indent: 0;
    }

    .angebot-title {
        font-size: 16px;
        font-weight: bold;
    }

    .angebot-datum {
        font-size: 11px;
        color: #444;
    }

    /* Restlicher Text */
    .hinweise-block {
        font-size: 10px;
        margin-left: 0;
        line-height: 1.6;
    }

    .hinweise-block ol {
        font-size: 9px;
        padding-left: 2;
    }

    .hinweise-block li {
        font-size: 9px;
        margin-bottom: 4px;
        padding-left: 14px;
    }
    .AGB {
        font-size: 9px;
        margin-right: 0px;
        margin-bottom: 10px;
    }

    .AGB p {
        font-size: 9px;
        margin: 0 30px;
        margin-bottom: 10px;
        text-align: justify;
    }

    .agb-text {
        margin-top: 4px;
    }

    .unterschrift {
        margin-top: 15mm;
        text-align: right;
        font-size: 9px;
    }

    .unterschrift .line {
        border-top: 1px solid #000;
        width: 200px;
        margin-bottom: 2mm;
        float: right;
    }

    .unterschrift {
        margin-top: 15mm;
        font-size: 9px;
        text-align: right;
    }

    .line-with-label {
        display: inline-block;
        text-align: center;
    }

    .line {
        border-top: 1px solid #000;
        width: 200px;
        margin: 0 auto 2mm auto;
    }

    .label {
        width: 200px;
        text-align: center;
    }

    /* Footer wird durch diese Box "nach unten gedrückt" */
    .footer-push {
        height: 100px;
    }
    </style>
    </head>
    <body>

    <div class="header">
    <div class="customer-block">
        <p style="font-size: 13px;"><strong>{{ kunde['Firma'] }}</strong></p>
        <p>{{ kunde['Anrede'] }} {{ kunde['Vorname'] }} {{ kunde['Nachname'] }}</p>
        <p>{{ kunde['Adresse'] }}</p>
        <p>{{ kunde['PLZ'] }} {{ kunde['Ort'] }}</p>
        <p>Tel.: {{ kunde['Telefonnummer'] }}</p>
        <p>E-Mail: {{ kunde['E_Mail'] }}</p>
    </div>
    <div class="logo">
        <img src="{{ logo_base64 }}" alt="Logo">
    </div>
    </div>

    <div class="angebot-row">
    <div class="angebot-title" style="font-size: 13px;">Kurzes Angebot: {{ angebot_id }}</div>
    <div class="angebot-datum">{{ aktuelles_datum }}</div>
    </div>

    <div class="anschreiben">
    {% if kunde['Anrede'] == 'Herr' %}
    <p>Sehr geehrter Herr {{ kunde['Nachname'] }},</p>
    {% elif kunde['Anrede'] == 'Frau' %}
    <p>Sehr geehrte Frau {{ kunde['Nachname'] }},</p>
    {% else %}
    <p>Sehr geehrte Damen und Herren,</p>
    {% endif %}
    <p>für Ihren Auftrag und Ihr Interesse an unseren Produkten und Dienstleistungen dürfen wir uns bedanken.</p> 
    <p>Gerne bieten wir Ihnen wie folgt an.</p>
    <p>Bei Fragen stehen wir Ihnen gerne jeder Zeit zur Verfügung.</p>
    </div>
    <table>
    <colgroup>
        <col style="width: 5%;">
        <col style="width: 25%;">
        <col style="width: 43%;">
        <col style="width: 5%;">
        <col style="width: 12%;">
        <col style="width: 10%;">
    </colgroup>
    <thead>
    <tr>
    <th>Pos.</th>
    <th>Abbildungen ähnlich</th>
    <th>Bezeichnung</th>
    <th>Menge</th>
    <th>Preis/st netto</th>
    <th>Gesamtpreis</th>
    </tr>
    </thead>
    <tbody>
    {% for row in products %}
    <tr class="product-row{% if loop.index > 1 %} no-split{% endif %}">
    <td><strong>{{ row['Positionsbezeichnung'] }}</strong></td>
    <td>
    {% if row['image'] %}
    <img src="{{ row['image'] }}" class="product-img">
    {% endif %}
    </td>
    <td class="product-description">
    {% if row['Alternative'] == True %}
    <div class="product-alternative">Alternativ-Option</div>
    {% endif %}
    {% if row['Titel'] %}
    <div class="product-title">
    {{ row['Titel'] }}
    </div>
    {% endif %}
    <div class="product-text">{{ row['Abmessungen'] or '' }}</div>
    </td>
    <td>
    {% if not row.Alternative and row.Menge is not none %}
        {% if row.Menge == row.Menge|int %}
            {{ row.Menge|int }}
        {% else %}
            {% set formatted = "%.2f"|format(row.Menge) %}
            {{ formatted.replace('.', ',') }}
        {% endif %}
    {% endif %}
    </td>
    <td>{{ row.Preis | german_currency }} €</td>
    <td>
    {% if not row.Alternative %}
        {% if row.Menge is not none %}
        {{ row.Gesamtpreis | german_currency }} €
        {% else %}
        {{ row.Preis | german_currency }} €
        {% endif %}
    {% endif %}
    {% endfor %}

    </tbody>
    </table>

    <div class="totals-box">
    <div class="row">
        <div>Netto Gesamt:</div>
        <div>{{ netto | german_currency }} €</div>
    </div>

    {% if rabatt != 0 %}
    <div class="row">
        <div>{{ rabatt|replace('.', ',') }}% Rabatt:</div>
        <div>-{{ rabatt_num | german_currency }} €</div>
    </div>
    {% endif %}

    {% if if_mwst == True %}
    <div class="row">
        <div>19% MwSt:</div>
        <div>{{ mwst | german_currency }} €</div>
    </div>
    {% endif %}
    
    {% if if_mwst == False %}
    <div class="row">
        <div>ATU-Nummer:</div>
        <div>{{atu}}</div>
    </div>
    {% endif %}

    <div class="row total">
        <div>Brutto Gesamt:</div>
        <div>{{ brutto | german_currency }} €</div>
    </div>
    </div>
    </body>
    </html>"""

    return template

def get_angebot_wo_price_template():
    """
    Retrieves the html structure for formatting the offer.
    """

    template = """<!DOCTYPE html>
    <html lang="de">
    <head>
    <meta charset="UTF-8">
    <style>
    @page {
    size: A4;
    margin: 30mm 20mm 30mm 20mm;
    font-size: 8px;
    font-family: Helvetica, sans-serif; 

    @bottom {
        content: "";
        border-top: 1px solid #ccc;
        height: 1px;
        margin-top: 2mm;
    }

    @bottom-left {
        content: "────────────────────────────────────────────" "\A"
                "Bankverbindung" "\A"
                "Volksbank Schnathorst" "\A"
                "IBAN: DE96 4926 2364 0070 4710 00" "\A"
                "BIC: GENODEM1SNA";
        white-space: pre;
    }

    @bottom-center {
        content: "──────────────────────────────────────────────" "\A" 
                "T.P.O." "\A"
                "Inh. Daniela Gross" "\A"
                "In den Fichten 34" "\A"
                "32584 Löhne";
        white-space: pre;
    }

    @bottom-right {
        content: "────────────────────────────────────────────" "\A"
                "Tel: 05731 755 13 11" "\A"
                "Fax: 05731 755 13 12" "\A"
                "Mail: tpo-gross@outlook.com" "\A"
                "UST-IdNr.: DE31 8295 117";
        white-space: pre;
    }
    }
    html {
    font-size: 8px;
    line-height: 1.5;
    }

    body {
        font-family: Helvetica, sans-serif;
        margin: 0;
        padding: 0;
        color: #222;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin: 30px 0px 0 0px;
    }

    .customer-info {
        max-width: 65%;
    }

    .logo {
        width: 170px;
        height: auto;
    }
    .logo img {
        width: 100%;
        height: auto;
    }

    /* Struktur */
    h2 {
        margin: 30px 30px 5px 30px;
        font-size: 11px;
    }
    p, th {
        font-size: 9px;
        margin: 0 30px;
    }

    table.content-table td {
        margin: 0 30px;
    }

    td {
        font-size: 9px;
        margin: 0; /* Kein globales margin mehr auf <td>! */
    }
    table {
        border-collapse: separate;
        border-spacing: 0 5px;
        margin: 18px 0px 0 0px;
        width: 100%;
    }
    th {
        background-color: #f0f0f0;
        text-align: left;
        padding: 4px;
        border-bottom: 1px solid #ccc;
    }
    td {
        background-color: #ffffff;
        padding: 4px;
        vertical-align: top;
        border: 1px solid #e0e0e0;
        border-top: none;
    }
    tr.no-split {
        page-break-inside: avoid;
    }
    .product-img {
        display: block;              /* Makes margin auto work */
        margin: 0 auto;              /* Center horizontally */
        max-width: 100%;
        max-height: 3.5cm;             /* or another fixed value */
        height: auto;
        object-fit: contain;
    }
    .totals-box {
        margin: 35px 30px 0 auto;
        width: 40%;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 8px 10px;
        font-size: 9px;
        background-color: #f9f9f9;
        page-break-inside: avoid;
    }
    .totals-box .row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
    }
    .totals-box .row.total {
        font-weight: bold;
        border-top: 1px solid #ccc;
        padding-top: 4px;
        margin-top: 6px;
    }

    td.product-description {
    padding: 2px 4px;
    line-height: 1.3;
    }

    .product-title {
    font-weight: bold;
    font-size: 9px;
    margin: 0;
    padding: 0;
    line-height: 1.2;
    }
    .product-alternative {
    font-weight: bold;
    font-size: 10px;
    line-height: 1.2;
    color: #B22222;
    }

    .product-text {
    font-size: 9px;
    margin: 0;
    padding: 0;
    line-height: 1.3;
    white-space: pre-wrap;
    }


    /* Customer block */
    .customer-block {
        font-size: 9px;            /* Make it bigger */
        line-height: 1.2;           /* Improve readability */
        margin-left: 0px;          /* Align exactly with table */
        margin-right: 30px;
        margin-bottom: 15px;
    }

    .customer-block p {
        font-size: 9px;
        line-height: 1.3;
        margin: 0;
    }

    .anschreiben {
        line-height: 1.6;
    }

    .anschreiben p {
        font-size: 9px;
        line-height: 1.6;
        margin: 0;
        padding: 0;
        text-indent: 0;
    }

    .angebot-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0;
        padding: 0;
        text-indent: 0;
    }

    .angebot-title {
        font-size: 16px;
        font-weight: bold;
    }

    .angebot-datum {
        font-size: 11px;
        color: #444;
    }

    /* Restlicher Text */
    .hinweise-block {
        font-size: 10px;
        margin-left: 0;
        line-height: 1.6;
    }

    .hinweise-block ol {
        font-size: 9px;
        padding-left: 2;
    }

    .hinweise-block li {
        font-size: 9px;
        margin-bottom: 4px;
        padding-left: 14px;
    }
    .AGB {
        font-size: 9px;
        margin-right: 0px;
        margin-bottom: 10px;
    }

    .AGB p {
        font-size: 9px;
        margin: 0 30px;
        margin-bottom: 10px;
        text-align: justify;
    }

    .agb-text {
        margin-top: 4px;
    }

    .unterschrift {
        margin-top: 15mm;
        text-align: right;
        font-size: 9px;
    }

    .unterschrift .line {
        border-top: 1px solid #000;
        width: 200px;
        margin-bottom: 2mm;
        float: right;
    }

    .unterschrift {
        margin-top: 15mm;
        font-size: 9px;
        text-align: right;
    }

    .line-with-label {
        display: inline-block;
        text-align: center;
    }

    .line {
        border-top: 1px solid #000;
        width: 200px;
        margin: 0 auto 2mm auto;
    }

    .label {
        width: 200px;
        text-align: center;
    }

    /* Footer wird durch diese Box "nach unten gedrückt" */
    .footer-push {
        height: 100px;
    }
    </style>
    </head>
    <body>

    <div class="header">
    <div class="customer-block">
        <p style="font-size: 13px;"><strong>{{ kunde['Firma'] }}</strong></p>
        <p>{{ kunde['Anrede'] }} {{ kunde['Vorname'] }} {{ kunde['Nachname'] }}</p>
        <p>{{ kunde['Adresse'] }}</p>
        <p>{{ kunde['PLZ'] }} {{ kunde['Ort'] }}</p>
        <p>Tel.: {{ kunde['Telefonnummer'] }}</p>
        <p>E-Mail: {{ kunde['E_Mail'] }}</p>
    </div>
    <div class="logo">
        <img src="{{ logo_base64 }}" alt="Logo">
    </div>
    </div>

    <div class="angebot-row">
    <div class="angebot-title" style="font-size: 13px;">Angebot: {{ angebot_id }}</div>
    <div class="angebot-datum">{{ aktuelles_datum }}</div>
    </div>

    <div class="anschreiben">
    {% if kunde['Anrede'] == 'Herr' %}
    <p>Sehr geehrter Herr {{ kunde['Nachname'] }},</p>
    {% elif kunde['Anrede'] == 'Frau' %}
    <p>Sehr geehrte Frau {{ kunde['Nachname'] }},</p>
    {% else %}
    <p>Sehr geehrte Damen und Herren,</p>
    {% endif %}
    <p>für Ihre Anfrage und Ihr Interesse an unseren Produkten und Dienstleistungen dürfen wir uns bedanken.</p> 
    <p>Gerne bieten wir Ihnen wie folgt an.</p>
    <p>Unser Angebot hat eine Gültigkeit von 4 Wochen.</p>
    <p>Bei Fragen stehen wir Ihnen gerne jeder Zeit zur Verfügung.</p>
    </div>
    <table>
    <colgroup>
        <col style="width: 5%;">
        <col style="width: 30%;">
        <col style="width: 60%;">
        <col style="width: 5%;">
    </colgroup>
    <thead>
    <tr>
    <th>Pos.</th>
    <th>Abbildungen ähnlich</th>
    <th>Bezeichnung</th>
    <th>Menge</th>
    </tr>
    </thead>
    <tbody>
    {% for row in products %}
    <tr class="product-row{% if loop.index > 1 %} no-split{% endif %}">
    <td><strong>{{ row['Positionsbezeichnung'] }}</strong></td>
    <td>{% if row['image'] %}<img src="{{ row['image'] }}" class="product-img">{% endif %}</td>
    <td class="product-description">
    {% if row['Alternative'] == True %}
        <div class="product-alternative">Alternativ-Option</div>
    {% endif %}
    {% if row['Titel'] %}
        <div class="product-title">{{ row['Titel'] }}</div>
    {% endif %}
    <div class="product-text">{{ row['Beschreibung'] or ''}}</div>
    </td>
    <td>
    {% if not row.Alternative and row.Menge is not none %}
        {% if row.Menge == row.Menge|int %}
            {{ row.Menge|int }}
        {% else %}
            {% set formatted = "%.2f"|format(row.Menge) %}
            {{ formatted.replace('.', ',') }}
        {% endif %}
    {% endif %}
    </td>
    <td>
    {% endfor %}
    </tbody>
    </table>

    </body>
    </html>"""
    return template