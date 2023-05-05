import dash_mantine_components as dmc
from dash import html

def abstract():
    paper_title='The proteomic landscape of synaptic diversity across brain regions and cell types'
    paper_authors='Marc van Oostrum, Thomas Blok, Stefano L. Giandomenico, Susanne tom Dieck, Georgi Tushev, Nicole Fürst, Julian Langer, Erin M. Schuman'
    paper_doi='bioRxiv 2023.01.27.525780'
    paper_href='https://doi.org/10.1101/2023.01.27.525780'
    paper_abstract = 'Brain function relies on communication via neuronal synapses. Neurons build and diversify synaptic contacts using different protein combinations that define the specificity, function and plasticity potential of synapses. More than a thousand proteins have been globally identified in both pre- and postsynaptic compartments, providing substantial potential for synaptic diversity. While there is ample evidence of diverse synaptic structures, states or functional properties, the diversity of the underlying individual synaptic proteomes remains largely unexplored. Here we used 7 different Cre-driver mouse lines crossed with a floxed mouse line in which the presynaptic terminals were fluorescently labeled (SypTOM) to identify the proteomes that underlie synaptic diversity. We combined microdissection of 5 different brain regions with fluorescent-activated synaptosome sorting to isolate and analyze using quantitative mass spectrometry 18 types of synapses and their underlying synaptic proteomes. We discovered ~1’800 unique synapse type-enriched proteins and allocated thousands of proteins to different types of synapses. We identify commonly shared synaptic protein modules and highlight the hotspots for proteome specialization. A protein-protein correlation network classifies proteins into modules and their association with synaptic traits reveals synaptic protein communities that correlate with either neurotransmitter glutamate or GABA. Finally, we reveal specializations and commonalities of the striatal dopaminergic proteome and outline the proteome diversity of synapses formed by parvalbumin, somatostatin and vasoactive intestinal peptide-expressing cortical interneuron subtypes, highlighting proteome signatures that relate to their functional properties. This study opens the door for molecular systems-biology analysis of synapses and provides a framework to integrate proteomic information for synapse subtypes of interest with cellular or circuit-level experiments.'
    return dmc.Stack([dmc.Text(paper_title, size='sm'),
            dmc.Text(paper_authors, size='xs', color='dimmed'),
            dmc.Anchor(paper_doi, href=paper_href, size='xs'),
            dmc.Spoiler(
                showLabel="show",
                hideLabel="hide",
                maxHeight= 80,
                children=dmc.Text(paper_abstract, size='xs', style={"text-align": "justify"}))],
            style={"marginLeft": 40, "marginRight": 40, "marginTop": 40,"marginBottom": 40})