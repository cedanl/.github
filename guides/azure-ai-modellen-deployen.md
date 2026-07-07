# Azure AI – Modellen deployen

Handleiding voor het activeren van Azure-toegang via PIM en het deployen van een model via Azure AI Studio.

## Vereisten

- Een `adm-...@surf.nl` account (wordt verzorgd door intern IT)

## Stap 1 – Azure-toegang activeren via PIM

1. Log in op [portal.azure.com](https://portal.azure.com) met je `adm-...@surf.nl` account
2. Navigeer naar de CEDA-subscriptie
3. Ga naar **Access Control (IAM)**
4. Klik op de **Activate**-link naast de rol **Contributor** onder _Privileged Identity Management | Azure resources_
5. Er opent een paneel aan de rechterkant:
   - Stel de **Duration** in op **1 uur** (standaard is 8 uur — houd het kort)
   - Vul een korte toelichting in bij **Reason**
6. Klik op **Activate**
7. Wacht even — de pagina ververst automatisch zodra de toegang actief is

## Stap 2 – Model deployen via Azure AI Studio

1. Ga naar [ai.azure.com](https://ai.azure.com) en open het juiste project
2. Ga in het linkermenu naar **My assets > Models + endpoints**
3. Klik op **Deploy model**
4. Kies het gewenste model en klik op **Deploy**
