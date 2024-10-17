class FocusCategory():
    def __init__(self, name = ''):
        self.name = name
        self.description = []
        self.connections = []
        self.samples = []
        self.tiers = [None]*6
    
    def get_anchor(self):
        return self.name.lower().replace(' ','-')

    def __str__(self):
        categ_anchor = self.get_anchor()
        html = '    <h5 id="focus-category-'+categ_anchor+'">' + self.name + '<a class="og-h-anchor" href="#focus-'+categ_anchor+'" title="Permalink" aria-hidden="true"></a></h5>\n'
        html += '    <p class="og-cite"><span class="og-ref">(Cypher System Rulebook, page 82)</span></p>\n'
        for i in range(len(self.description)):
            if i==0:
                html += '    <p>'+self.description[i]+'</p>\n'
            else:
                html += '    <p class="og-ind">'+self.description[i]+'</p>\n'
        html += '    <ul class="list-unstyled og-ind">\n'
        html += '		<li><p><strong>Connexion:</strong> Choisissez quatre connexions pertinentes dans la liste des <a href="#focus-focus-connections">Connexions de foci</a>.</p></li>\n'
        for connection in self.connections:
            html += '		<li><p><strong>'+connection['name']+'</strong> '+connection['detail']+'</p></li>\n'
        html += '    </ul>\n'
        html += '    <div class="alert ps-4 pb-0">\n'
        html += '		<p>La liste ci-après ne sont que des exemples et n\'est pas une liste complète de toutes les foci possibles pour cette catégorie.</p>\n'
        html += '		<ul class="list-unstyled og-qr">\n'
        for sample in self.samples:
            html += '			<li><a href="#focus-'+sample.lower().replace(' ','-')+'">'+sample+'</a></li>\n'
        html += '		</ul>\n'
        html += '	</div>\n'
        html += '	<h6 id="focus-category-'+categ_anchor+'-ability-selection-guidelines">Indications pour la Sélection de Capacités<a class="og-h-anchor" href="#focus-category-'+categ_anchor+'-ability-selection-guidelines" title="Permalink" aria-hidden="true"></a></h6>\n'
        html += '		<p class="og-cite"><span class="og-ref">(Cypher System Rulebook, page 82)</span></p>\n'
        html += '		<ul class="list-unstyled">\n'
        for i in range(len(self.tiers)):
            tier = self.tiers[i]
            html += '         <li>\n'
            if None==tier:
                continue
            for j in range(len(tier)):
                detail = tier[j]
                if j == 0:
                    html += '			<p><strong>Rang '+format(i+1)+':</strong> ' + detail + '</p>\n'
                else:
                    html += '			<p class="og-ind">' + detail + '</p>\n'
            html += '         </li>\n'
        html += '     </ul>\n'
        return html


with open('focuscateg-2.md','r', encoding='utf8') as focuscategfile, open('focuscateg-2.html','w', encoding='utf8') as outputfile:
    current_category = None
    start_description = False
    start_connection = False
    start_samples = False
    start_tiers = False
    for line in focuscategfile:
        line = line.strip()
        if line.startswith('### '):
            categ_name = line[4:]
            if current_category != None:
                print(current_category, file=outputfile)
            current_category = FocusCategory(name=categ_name)
            start_description = True
            start_connection = False
            start_samples = False
            start_tiers = False
        elif line.startswith('**Connexion:**'):
            start_description = False
            start_connection = True
        elif line.startswith('La liste ci-après ne sont que des exemples'):
            start_connection = False
            start_samples = True
        elif line.startswith('**Indications pour la Sélection de Capacités**'):
            start_samples = False
            start_tiers = True
        elif line.startswith('-----'):
            start_tiers = False
        elif start_description:
            if len(line) > 0:
                current_category.description.append(line)
        elif start_connection:
            if line.startswith('**'):
                line = line.lstrip('*')
                name = line[0:line.find(':*')]
                detail = line[line.find('**')+2:].strip()
                current_category.connections.append({'name':name,'detail':detail})
        elif start_samples:
            if line.startswith('* '):
                current_category.samples.append(line.lstrip('* '))
        elif start_tiers:
            if line.startswith('**Rang 1:**'):
                current_tier = 1
            if line.startswith('**Rang 2:**'):
                current_tier = 2
            if line.startswith('**Rang 3:**'):
                current_tier = 3
            if line.startswith('**Rang 4:**'):
                current_tier = 4
            if line.startswith('**Rang 5:**'):
                current_tier = 5
            if line.startswith('**Rang 6:**'):
                current_tier = 6
            if line.startswith('**Rang'):
                current_category.tiers[current_tier-1] = [line[12:].strip()]
            elif len(line)>0 :
                current_category.tiers[current_tier-1].append(line)

    if current_category != None:
        print(current_category, file=outputfile)

        