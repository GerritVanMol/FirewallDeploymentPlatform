 Onderzoeksvragen: 
 1. VPN tunnel 
     Hoe en met welke toestellen/vendoren kan een vpn configuratie automatisch worden opgesteld? Welke soorten vpn tunnels zijn er, hoe kunnen ze worden opgebouwd worden, welke tunnels zijn best voor automatische opbouw. Kan dit met fortinet naar andere vendor toestellen/modellen?

2. Netwerk configuratie 
     Hoe kan een IP (public/private) adres/range van IP's automatisch worden toegewezen aan nieuw geplaatste toestellen. 

 3. Provisioning 
      Wat is de meest efficiënte manier om toestellen na configuratie te beheren (van op afstand). Met welk protocol wordt het configuratiebestand overgezet... 

 4. Configuratie bestanden
      Hoe worden configuratie bestanden verwerkt, zijn ze compatibel met verschillende toestel modellen en andere vendoren? Hoe kunne ze eventueel universeel worden gemaakt... 

 5. Platform availability
      Is het mogelijk om meerder configuratie tegelijk uit te voeren, zijn meerdere connecties tegelijk mogelijk?
 

6. Automatisatie
     Is het mogelijk de configuraties te automatiseren met Ansible? Kan Ansible samen werken met Fortimanager?

 Concreet: 
Onderzoek naar een nieuw framework voor deployment automatisatie van Fortigate firewalls. Het schrijven van een framework, dat toelaat om 50 Fortigate firewalls per week uit te rollen met behulp van Fortimanager. Ervan uitgaande dat de persoon die de uitrol doet (field services) geen enkele intelligentie heeft. Het gaat over een webapplicatie waar de fieldservices engineer enkel een QR-code of serienummer moet ingeven, en wanneer deze persoon deze input geeft, de instant provisioning van de router gebeurt. Denk aan de use case van de Telenet of Proximus engineer die bij je thuis een router met services komt installeren. Deze persoon is niet langer dan 30 minuten bij jou ter plaatse, en als hij vertrekt zijn alle services up and running. Aan de hand van Ansible, Python en andere technologien wordt het platform opgebouwd en toestel deployment geautomatiseerd. 
 Het einddoel is een werkend framework dat de workflow van service engineers versnelt bij plaatsen van netwerk firewalls. 